#!/usr/bin/env python3
"""Validate the structure and portability of a Codex skill package.

The validator deliberately uses only the Python standard library so it can travel
with the skill. Findings have two actionable severities: ``error`` (the package is
not safe to ship) and ``warning`` (quality issue that should be reviewed). The CLI
returns status 1 only when at least one error is present.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import unquote


TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mdx",
    ".py",
    ".sh",
    ".txt",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}
SKIP_DIRECTORIES = {".git", ".pytest_cache", "__pycache__", "node_modules"}
PATH_ROOTS = ("assets", "evals", "references", "scripts")
ABSOLUTE_USER_PREFIX = "/" + "Users/"


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass
class DoctorReport:
    root: str
    findings: list[Finding]
    files_checked: int = 0

    @property
    def error_count(self) -> int:
        return sum(item.severity == "error" for item in self.findings)

    @property
    def warning_count(self) -> int:
        return sum(item.severity == "warning" for item in self.findings)

    @property
    def ok(self) -> bool:
        return self.error_count == 0

    def add(
        self,
        severity: str,
        code: str,
        message: str,
        path: str | None = None,
        line: int | None = None,
    ) -> None:
        self.findings.append(Finding(severity, code, message, path, line))

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "root": self.root,
            "files_checked": self.files_checked,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "findings": [item.to_dict() for item in self.findings],
        }


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _iter_text_files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRECTORIES for part in path.relative_to(root).parts):
            continue
        yield path


def _read_text(path: Path, report: DoctorReport, root: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        report.add(
            "error",
            "text.encoding",
            "Arquivo textual não está em UTF-8.",
            _relative(path, root),
        )
    except OSError as exc:
        report.add(
            "error",
            "file.read",
            f"Não foi possível ler o arquivo: {exc}.",
            _relative(path, root),
        )
    return None


def _parse_frontmatter(text: str) -> tuple[dict[str, str], int | None]:
    """Parse the simple top-level scalar fields used by SKILL.md frontmatter."""

    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, None

    closing = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if closing is None:
        return {}, -1

    fields: dict[str, str] = {}
    index = 1
    while index < closing:
        match = re.match(r"^([A-Za-z_][\w-]*):(?:\s*(.*))?$", lines[index])
        if not match:
            index += 1
            continue
        key, raw_value = match.group(1), (match.group(2) or "").strip()
        if raw_value in {"|", ">"}:
            chunks: list[str] = []
            index += 1
            while index < closing and (lines[index].startswith((" ", "\t")) or not lines[index].strip()):
                chunks.append(lines[index].strip())
                index += 1
            fields[key] = " ".join(part for part in chunks if part)
            continue
        if len(raw_value) >= 2 and raw_value[0] == raw_value[-1] and raw_value[0] in {"'", '"'}:
            raw_value = raw_value[1:-1]
        fields[key] = raw_value.strip()
        index += 1
    return fields, closing + 1


def _check_skill(skill_path: Path, text: str, report: DoctorReport, root: Path) -> None:
    relative = _relative(skill_path, root)
    fields, closing_line = _parse_frontmatter(text)
    if closing_line is None:
        report.add("error", "frontmatter.missing", "SKILL.md deve começar com frontmatter YAML.", relative, 1)
        return
    if closing_line == -1:
        report.add("error", "frontmatter.unclosed", "Frontmatter YAML não foi fechado com ---. ", relative, 1)
        return

    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()
    allowed_fields = {"name", "description", "license", "allowed-tools", "metadata"}
    unexpected_fields = sorted(set(fields) - allowed_fields)
    if unexpected_fields:
        report.add(
            "error",
            "frontmatter.unexpected_keys",
            "Chave(s) de frontmatter não suportada(s): " + ", ".join(unexpected_fields) + ".",
            relative,
            2,
        )
    if not name:
        report.add("error", "frontmatter.name", "Campo obrigatório 'name' está ausente ou vazio.", relative, 2)
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        report.add(
            "error",
            "frontmatter.name_format",
            "'name' deve ter até 64 caracteres e usar somente minúsculas, números e hífens.",
            relative,
            2,
        )
    if not description:
        report.add(
            "error",
            "frontmatter.description",
            "Campo obrigatório 'description' está ausente ou vazio.",
            relative,
            3,
        )

    line_count = len(text.splitlines())
    if line_count >= 500:
        report.add(
            "error",
            "skill.too_long",
            f"SKILL.md tem {line_count} linhas; mantenha-o abaixo de 500.",
            relative,
        )


def _check_fences(path: Path, text: str, report: DoctorReport, root: Path) -> None:
    opening: tuple[str, int, int] | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if not match:
            continue
        marker = match.group(1)
        if opening is None:
            opening = (marker[0], len(marker), line_number)
        elif marker[0] == opening[0] and len(marker) >= opening[1]:
            opening = None
    if opening is not None:
        report.add(
            "error",
            "markdown.fence_unclosed",
            "Bloco de código Markdown não foi fechado.",
            _relative(path, root),
            opening[2],
        )


def _target_from_markdown(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        title = re.search(r"\s+(?:['\"(]).*$", target)
        if title:
            target = target[: title.start()].strip()
    return unquote(target).split("#", 1)[0].split("?", 1)[0].strip()


def _relative_targets(text: str) -> Iterator[tuple[str, int]]:
    found: set[tuple[str, int]] = set()
    for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text):
        target = _target_from_markdown(match.group(1))
        item = (target, match.start(1))
        if item not in found:
            found.add(item)
            yield item

    roots = "|".join(re.escape(part) for part in PATH_ROOTS)
    pattern = re.compile(rf"(?<![\w:/])((?:\.\.?/)?(?:{roots})/[A-Za-z0-9_@%+.,()\-/]+)")
    for match in pattern.finditer(text):
        target = match.group(1).rstrip(".,;:")
        while target.endswith(")") and target.count(")") > target.count("("):
            target = target[:-1]
        item = (target, match.start(1))
        if item not in found:
            found.add(item)
            yield item

    inline_path = re.compile(
        r"`((?:\.\.?/)?[A-Za-z0-9_@%+.,()\-/]+\.(?:md|ya?ml|json|py|html?))`",
        re.I,
    )
    for match in inline_path.finditer(text):
        item = (match.group(1), match.start(1))
        if item not in found:
            found.add(item)
            yield item


def _is_local_target(target: str) -> bool:
    if not target or target.startswith(("#", "/", "\\")):
        return False
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
        return False
    if any(symbol in target for symbol in ("*", "{", "}", "[", "]", "$")):
        return False
    return True


def _target_exists(source: Path, root: Path, target: str) -> bool:
    candidate = Path(target)
    options = (source.parent / candidate, root / candidate)
    return any(option.exists() for option in options)


def _check_paths(path: Path, text: str, report: DoctorReport, root: Path) -> None:
    relative = _relative(path, root)
    for target, offset in _relative_targets(text):
        if not _is_local_target(target):
            continue
        if not _target_exists(path, root, target):
            report.add(
                "error",
                "path.missing",
                f"Caminho relativo não existe: {target}.",
                relative,
                _line_number(text, offset),
            )


def _check_absolute_paths(path: Path, text: str, report: DoctorReport, root: Path) -> None:
    start = 0
    while True:
        offset = text.find(ABSOLUTE_USER_PREFIX, start)
        if offset < 0:
            return
        report.add(
            "error",
            "path.absolute_users",
            "Caminho absoluto sob o diretório de usuário torna a skill não portátil.",
            _relative(path, root),
            _line_number(text, offset),
        )
        start = offset + len(ABSOLUTE_USER_PREFIX)


TOC_PATTERN = re.compile(
    r"(?im)^#{1,4}\s+(?:table of contents|contents|sum[aá]rio|[ií]ndice|navega[cç][aã]o)\s*$|<!--\s*TOC\s*-->",
)


def _check_long_doc_toc(path: Path, text: str, report: DoctorReport, root: Path) -> None:
    line_count = len(text.splitlines())
    if line_count > 300 and not TOC_PATTERN.search(text):
        report.add(
            "warning",
            "markdown.toc_missing",
            f"Documento longo ({line_count} linhas) não possui sumário identificável.",
            _relative(path, root),
        )


def _check_evals(evals_path: Path, text: str, report: DoctorReport, root: Path) -> None:
    relative = _relative(evals_path, root)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        report.add("error", "evals.invalid_json", f"JSON inválido: {exc.msg}.", relative, exc.lineno)
        return

    if isinstance(payload, dict):
        cases = payload.get("evals")
    elif isinstance(payload, list):
        cases = payload
    else:
        cases = None
    if not isinstance(cases, list) or not cases:
        report.add("error", "evals.missing_cases", "O arquivo de evals deve conter uma lista não vazia.", relative)
        return

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            report.add("error", "evals.case_type", f"Eval #{index + 1} deve ser um objeto JSON.", relative)
            continue
        assertions = case.get("assertions")
        expectations = case.get("expectations")
        if not assertions and not expectations:
            label = case.get("eval_name") or case.get("name") or case.get("id") or f"#{index + 1}"
            report.add(
                "error",
                "evals.expectations_missing",
                f"Eval '{label}' precisa de 'assertions' ou 'expectations' não vazio.",
                relative,
            )
        files = case.get("files", [])
        if isinstance(files, str):
            files = [files]
        if files is None:
            files = []
        if not isinstance(files, list):
            report.add(
                "error",
                "evals.files_type",
                f"Campo 'files' do eval #{index + 1} deve ser uma lista.",
                relative,
            )
            continue
        for file_index, raw_target in enumerate(files):
            if not isinstance(raw_target, str):
                report.add(
                    "error",
                    "evals.file_type",
                    f"Entrada #{file_index + 1} de 'files' no eval #{index + 1} deve ser texto.",
                    relative,
                )
                continue
            target = _target_from_markdown(raw_target)
            if _is_local_target(target) and not _target_exists(evals_path, root, target):
                report.add(
                    "error",
                    "path.missing",
                    f"Arquivo de eval não existe: {target}.",
                    relative,
                )


def audit_package(package: str | Path) -> DoctorReport:
    root = Path(package).expanduser().resolve()
    report = DoctorReport(root=str(root), findings=[])
    if not root.exists() or not root.is_dir():
        report.add("error", "package.missing", "Diretório da skill não existe ou não é uma pasta.")
        return report

    texts: dict[Path, str] = {}
    for path in _iter_text_files(root):
        text = _read_text(path, report, root)
        if text is not None:
            texts[path] = text
    report.files_checked = len(texts)

    skill_path = root / "SKILL.md"
    skill_text = texts.get(skill_path)
    if skill_text is None:
        if not skill_path.exists():
            report.add("error", "skill.missing", "SKILL.md não foi encontrado.", "SKILL.md")
    else:
        _check_skill(skill_path, skill_text, report, root)

    for path, text in texts.items():
        _check_absolute_paths(path, text, report, root)
        if path.suffix.lower() in {".md", ".mdx"}:
            _check_fences(path, text, report, root)
            _check_paths(path, text, report, root)
            _check_long_doc_toc(path, text, report, root)

    evals_path = root / "evals" / "evals.json"
    evals_text = texts.get(evals_path)
    if evals_text is None:
        if not evals_path.exists():
            report.add("error", "evals.missing", "evals/evals.json não foi encontrado.", "evals/evals.json")
    else:
        _check_evals(evals_path, evals_text, report, root)

    rank = {"error": 0, "warning": 1, "info": 2}
    report.findings.sort(key=lambda item: (rank.get(item.severity, 9), item.path or "", item.line or 0, item.code))
    return report


def format_text(report: DoctorReport) -> str:
    status = "APROVADO" if report.ok else "REPROVADO"
    lines = [
        f"Design DNA Doctor: {status}",
        f"Raiz: {report.root}",
        f"Arquivos verificados: {report.files_checked}",
        f"Erros: {report.error_count} | Avisos: {report.warning_count}",
    ]
    if not report.findings:
        lines.append("Nenhum problema encontrado.")
    for finding in report.findings:
        location = finding.path or "."
        if finding.line is not None:
            location += f":{finding.line}"
        lines.append(f"[{finding.severity.upper()}] {finding.code} | {location} | {finding.message}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Valida estrutura, portabilidade e evals de uma skill.")
    default_root = Path(__file__).resolve().parents[1]
    parser.add_argument("path", nargs="?", default=str(default_root), help="Pasta raiz da skill.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emite relatório JSON.")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    report = audit_package(args.path)
    if args.as_json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(format_text(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
