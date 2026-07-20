#!/usr/bin/env python3
"""Preflight generated web and SVG artifacts against Design DNA guardrails.

The checker is intentionally heuristic: structural and accessibility failures are
errors, while subjective design smells are warnings. Exit status is 1 only when a
strong error exists; warnings remain visible without blocking delivery.
"""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import unquote, urlparse


HTML_SUFFIXES = {".html", ".htm"}
SCRIPT_SUFFIXES = {".js", ".mjs", ".jsx", ".ts", ".tsx"}
SVG_SUFFIXES = {".svg"}
SOURCE_SUFFIXES = {".css"} | HTML_SUFFIXES | SCRIPT_SUFFIXES | SVG_SUFFIXES
SKIP_DIRECTORIES = {".git", ".pytest_cache", "__pycache__", "dist", "node_modules"}
BADGE_MARKERS = ("badge", "eyebrow", "kicker", "overline", "pill", "pretitle", "pre-title")
REMOTE_SCHEMES = ("http://", "https://", "//")


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
class PreflightReport:
    target: str
    findings: list[Finding]
    files_checked: list[str]
    color_families: dict[str, dict[str, object]]

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
            "target": self.target,
            "files_checked": self.files_checked,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "color_families": self.color_families,
            "findings": [item.to_dict() for item in self.findings],
        }


class PageParser(HTMLParser):
    """Collect only the HTML facts needed by the preflight checks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.has_viewport = False
        self.title_chunks: list[str] = []
        self._in_title = False
        self._capture_style = 0
        self._capture_script = 0
        self._ignored_visible_depth = 0
        self.style_chunks: list[str] = []
        self.script_chunks: list[str] = []
        self.style_attributes: list[str] = []
        self.visible_chunks: list[str] = []
        self.images_without_alt: list[int] = []
        self.badges_before_h1: list[tuple[int, str]] = []
        self.h1_lines: list[int] = []
        self.interactive_count = 0
        self.remote_assets: list[tuple[int, str, str]] = []
        self.local_code_assets: list[str] = []
        self.empty_hash_links: list[int] = []

    @staticmethod
    def _attrs(attributes: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): value or "" for key, value in attributes}

    @staticmethod
    def _is_remote(value: str) -> bool:
        value = value.strip().lower()
        return value.startswith(REMOTE_SCHEMES)

    def _record_asset(self, tag: str, attribute: str, value: str, line: int) -> None:
        if not value:
            return
        values = [part.strip().split()[0] for part in value.split(",")] if attribute == "srcset" else [value]
        for candidate in values:
            if self._is_remote(candidate):
                self.remote_assets.append((line, tag, candidate))

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs = self._attrs(attributes)
        line = self.getpos()[0]

        if tag == "html" and self.lang is None:
            self.lang = attrs.get("lang", "").strip()
        elif tag == "meta" and attrs.get("name", "").lower() == "viewport" and attrs.get("content", "").strip():
            self.has_viewport = True
        elif tag == "title":
            self._in_title = True
        elif tag == "style":
            self._capture_style += 1
            self._ignored_visible_depth += 1
        elif tag == "script":
            self._capture_script += 1
            self._ignored_visible_depth += 1
        elif tag == "template":
            self._ignored_visible_depth += 1

        if tag == "h1":
            self.h1_lines.append(line)
        elif not self.h1_lines:
            marker_source = " ".join((attrs.get("class", ""), attrs.get("id", ""))).lower()
            marker = next((item for item in BADGE_MARKERS if re.search(rf"(?:^|[-_\s]){re.escape(item)}(?:$|[-_\s])", marker_source)), None)
            if marker:
                self.badges_before_h1.append((line, marker))

        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(line)
        if tag == "input" and attrs.get("type", "").lower() == "image" and "alt" not in attrs:
            self.images_without_alt.append(line)

        if tag in {"button", "select", "textarea"}:
            self.interactive_count += 1
        elif tag == "a" and attrs.get("href"):
            self.interactive_count += 1
            if attrs["href"].strip() == "#":
                self.empty_hash_links.append(line)
        elif tag == "input" and attrs.get("type", "text").lower() != "hidden":
            self.interactive_count += 1
        elif "tabindex" in attrs and attrs["tabindex"].strip() != "-1":
            self.interactive_count += 1

        if attrs.get("style"):
            self.style_attributes.append(attrs["style"])

        if tag in {"img", "script", "source", "video", "audio", "iframe"}:
            self._record_asset(tag, "src", attrs.get("src", ""), line)
        if tag == "source":
            self._record_asset(tag, "srcset", attrs.get("srcset", ""), line)
        if tag == "video":
            self._record_asset(tag, "poster", attrs.get("poster", ""), line)
        if tag == "link":
            rel = {part.lower() for part in attrs.get("rel", "").split()}
            if rel.intersection({"stylesheet", "icon", "preload", "modulepreload"}):
                self._record_asset(tag, "href", attrs.get("href", ""), line)

        if tag == "script" and attrs.get("src") and not self._is_remote(attrs["src"]):
            self.local_code_assets.append(attrs["src"])
        if tag == "link" and "stylesheet" in attrs.get("rel", "").lower().split():
            href = attrs.get("href", "")
            if href and not self._is_remote(href):
                self.local_code_assets.append(href)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "style" and self._capture_style:
            self._capture_style -= 1
            self._ignored_visible_depth = max(0, self._ignored_visible_depth - 1)
        elif tag == "script" and self._capture_script:
            self._capture_script -= 1
            self._ignored_visible_depth = max(0, self._ignored_visible_depth - 1)
        elif tag == "template" and self._ignored_visible_depth:
            self._ignored_visible_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_chunks.append(data)
        if self._capture_style:
            self.style_chunks.append(data)
        elif self._capture_script:
            self.script_chunks.append(data)
        elif not self._ignored_visible_depth and data.strip():
            self.visible_chunks.append(data)

    @property
    def title(self) -> str:
        return " ".join(part.strip() for part in self.title_chunks if part.strip())

    @property
    def visible_text(self) -> str:
        return " ".join(part.strip() for part in self.visible_chunks if part.strip())


def _display_path(path: Path, target: Path) -> str:
    base = target if target.is_dir() else target.parent
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _iter_source_files(target: Path) -> Iterator[Path]:
    if target.is_file():
        if target.suffix.lower() in SOURCE_SUFFIXES:
            yield target
        return
    for path in sorted(target.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        if any(part in SKIP_DIRECTORIES for part in path.relative_to(target).parts):
            continue
        yield path


def _read_source(path: Path, report: PreflightReport, target: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        report.add("error", "source.encoding", "Arquivo não está em UTF-8.", _display_path(path, target))
    except OSError as exc:
        report.add("error", "source.read", f"Não foi possível ler o arquivo: {exc}.", _display_path(path, target))
    return None


def _local_asset_path(html_path: Path, raw: str) -> Path | None:
    clean = unquote(raw.strip()).split("#", 1)[0].split("?", 1)[0]
    if not clean or clean.startswith(("/", "\\", "data:", "javascript:")):
        return None
    parsed = urlparse(clean)
    if parsed.scheme or parsed.netloc:
        return None
    candidate = (html_path.parent / clean).resolve()
    return candidate if candidate.suffix.lower() in ({".css"} | SCRIPT_SUFFIXES) else None


def _extract_remote_css_assets(css: str) -> Iterator[tuple[str, int]]:
    pattern = re.compile(r"(?:url\(\s*|@import\s+(?:url\(\s*)?)(['\"]?)(https?://|//)([^)'\"\s;]+)", re.I)
    for match in pattern.finditer(css):
        yield match.group(2) + match.group(3), _line_number(css, match.start())


PLACEHOLDER_PATTERNS = (
    ("placeholder.lorem", re.compile(r"\blorem\s+ipsum\b", re.I), "Texto Lorem Ipsum ainda está presente."),
    ("placeholder.todo", re.compile(r"\b(?:TODO|FIXME|TBD)\b"), "Marcador de trabalho incompleto ainda está presente."),
    (
        "placeholder.copy",
        re.compile(r"\b(?:replace\s+me|your\s+(?:company|logo|brand|name)\s+here)\b", re.I),
        "Copy provisória ainda está presente.",
    ),
    ("placeholder.template", re.compile(r"\{\{\s*[^{}\n]+\s*\}\}"), "Token de template não resolvido."),
    (
        "placeholder.instruction",
        re.compile(r"\[\s*(?:inserir|preencher|colocar|placeholder)\b[^\]\n]*\]", re.I),
        "Instrução provisória ainda está presente.",
    ),
    (
        "placeholder.asset",
        re.compile(r"(?:https?://)?(?:www\.)?(?:placehold\.co|via\.placeholder\.com|picsum\.photos)\b", re.I),
        "Asset provisório está sendo usado.",
    ),
    ("placeholder.example", re.compile(r"https?://(?:www\.)?example\.com\b", re.I), "URL example.com ainda está presente."),
)


def _check_placeholders(path: Path, text: str, report: PreflightReport, target: Path) -> None:
    relative = _display_path(path, target)
    for code, pattern, message in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            report.add("error", code, message, relative, _line_number(text, match.start()))


def _has_motion(css: str, javascript: str) -> bool:
    if re.search(r"@keyframes\b", css, re.I):
        return True
    declarations = re.finditer(r"(?:^|[;{])\s*(animation(?:-[\w-]+)?|transition(?:-[\w-]+)?|scroll-behavior)\s*:\s*([^;}]+)", css, re.I)
    for match in declarations:
        value = match.group(2).strip().lower()
        if value not in {"none", "initial", "inherit", "unset", "auto"} and not value.startswith("none "):
            return True
    return bool(re.search(r"requestAnimationFrame|\.animate\s*\(|\b(?:gsap|anime)\s*\.|scrollTo\s*\(", javascript))


def _has_reduced_motion(css: str, javascript: str) -> bool:
    return bool(re.search(r"prefers-reduced-motion\s*:\s*reduce", css + "\n" + javascript, re.I))


def _has_responsive_css(css: str) -> bool:
    return bool(
        re.search(r"@media\s*[^{}]*(?:min|max)-width|@container\b", css, re.I)
        or re.search(r"(?:auto-fit|auto-fill|minmax\s*\(|clamp\s*\(|(?:min|max)\s*\()", css, re.I)
    )


def _has_decorative_grid(css: str, html: str) -> bool:
    if re.search(r"repeating-(?:linear|radial)-gradient\s*\(", css, re.I):
        return True
    dot_grid = re.search(
        r"radial-gradient\s*\([^)]*(?:\b1px\b|\b2px\b)[^)]*transparent[^)]*\)[^{};]*(?:;|})[^{}]*background-size",
        css,
        re.I | re.S,
    )
    if dot_grid:
        return True
    for block in re.finditer(r"[^{}]+\{([^{}]+)\}", css, re.S):
        body = block.group(1)
        if len(re.findall(r"linear-gradient\s*\(", body, re.I)) >= 2 and re.search(
            r"background-size\s*:", body, re.I
        ):
            return True
    marker = r"(?:dot[-_]?grid|grid[-_]?(?:background|bg|pattern)|(?:background|decorative)[-_]?grid)"
    return bool(re.search(marker, css + "\n" + html, re.I))


def _has_multicolor_gradient_text(css: str) -> bool:
    for match in re.finditer(r"([^{}]+)\{([^{}]+)\}", css, re.S):
        body = match.group(2)
        if not re.search(r"(?:-webkit-)?background-clip\s*:\s*text", body, re.I):
            continue
        gradient = re.search(r"(?:linear|radial|conic)-gradient\s*\(([^)]*)\)", body, re.I | re.S)
        if gradient and gradient.group(1).count(",") >= 1:
            return True
    return False


def _rgb_from_hex(token: str) -> tuple[float, float, float] | None:
    value = token.lstrip("#")
    if len(value) in {3, 4}:
        value = "".join(character * 2 for character in value[:3])
    elif len(value) in {6, 8}:
        value = value[:6]
    else:
        return None
    try:
        return tuple(int(value[index : index + 2], 16) / 255 for index in (0, 2, 4))  # type: ignore[return-value]
    except ValueError:
        return None


def _rgb_from_function(token: str) -> tuple[float, float, float] | None:
    inner = token[token.find("(") + 1 : token.rfind(")")]
    channels = re.split(r"\s*[,/]\s*|\s+", inner.strip())
    channels = [part for part in channels if part][:3]
    if len(channels) != 3:
        return None
    values: list[float] = []
    try:
        for part in channels:
            values.append(max(0.0, min(1.0, float(part[:-1]) / 100 if part.endswith("%") else float(part) / 255)))
    except ValueError:
        return None
    return values[0], values[1], values[2]


def _rgb_from_hsl(token: str) -> tuple[float, float, float] | None:
    inner = token[token.find("(") + 1 : token.rfind(")")]
    parts = [part for part in re.split(r"\s*[,/]\s*|\s+", inner.strip()) if part]
    if len(parts) < 3:
        return None
    try:
        hue = float(re.sub(r"(?:deg|turn|rad)$", "", parts[0])) % 360
        saturation = float(parts[1].rstrip("%")) / 100
        lightness = float(parts[2].rstrip("%")) / 100
    except ValueError:
        return None
    return colorsys.hls_to_rgb(hue / 360, lightness, saturation)


def _color_family(red: float, green: float, blue: float) -> str:
    hue, lightness, saturation = colorsys.rgb_to_hls(red, green, blue)
    if saturation < 0.18 or lightness < 0.08 or lightness > 0.94:
        return "neutral"
    degrees = hue * 360
    if degrees < 15 or degrees >= 345:
        return "red"
    if degrees < 45:
        return "orange"
    if degrees < 70:
        return "yellow"
    if degrees < 155:
        return "green"
    if degrees < 190:
        return "teal"
    if degrees < 210:
        return "cyan"
    if degrees < 255:
        return "blue"
    if degrees < 285:
        return "violet"
    if degrees < 330:
        return "magenta"
    return "pink"


def _color_report(css: str) -> dict[str, dict[str, object]]:
    token_pattern = re.compile(
        r"(?<![\w-])#[0-9a-fA-F]{3,8}\b|\b(?:rgb|rgba|hsl|hsla)\([^)]*\)",
        re.I,
    )
    counts: Counter[str] = Counter()
    samples: defaultdict[str, list[str]] = defaultdict(list)
    for match in token_pattern.finditer(css):
        token = match.group(0)
        lowered = token.lower()
        if lowered.startswith("#"):
            rgb = _rgb_from_hex(token)
        elif lowered.startswith("rgb"):
            rgb = _rgb_from_function(token)
        else:
            rgb = _rgb_from_hsl(token)
        if rgb is None:
            continue
        family = _color_family(*rgb)
        counts[family] += 1
        if token not in samples[family] and len(samples[family]) < 5:
            samples[family].append(token)
    return {
        family: {"count": counts[family], "samples": samples[family]}
        for family in sorted(counts, key=lambda item: (-counts[item], item))
    }


def audit_target(raw_target: str | Path) -> PreflightReport:
    target = Path(raw_target).expanduser().resolve()
    report = PreflightReport(target=str(target), findings=[], files_checked=[], color_families={})
    if not target.exists():
        report.add("error", "target.missing", "Arquivo ou diretório alvo não existe.")
        return report
    if target.is_file() and target.suffix.lower() not in SOURCE_SUFFIXES:
        report.add(
            "error",
            "target.unsupported",
            "Use HTML, CSS, JS/TS/React, SVG ou uma pasta que contenha esses arquivos.",
        )
        return report

    sources: dict[Path, str] = {}
    for path in _iter_source_files(target):
        text = _read_source(path, report, target)
        if text is not None:
            sources[path.resolve()] = text
    if not sources:
        report.add("error", "target.no_sources", "Nenhum arquivo web ou SVG suportado foi encontrado.")
        return report

    parsers: dict[Path, PageParser] = {}
    html_paths = [path for path in sources if path.suffix.lower() in HTML_SUFFIXES]
    svg_paths = [path for path in sources if path.suffix.lower() in SVG_SUFFIXES]
    markup_paths = html_paths + svg_paths
    for path in markup_paths:
        parser = PageParser()
        try:
            parser.feed(sources[path])
            parser.close()
        except Exception as exc:  # HTMLParser can surface malformed entity edge cases.
            report.add("error", "html.parse", f"Falha ao analisar HTML: {exc}.", _display_path(path, target))
        parsers[path] = parser
        for asset in parser.local_code_assets:
            asset_path = _local_asset_path(path, asset)
            if asset_path is not None and asset_path.exists() and asset_path not in sources:
                asset_text = _read_source(asset_path, report, target)
                if asset_text is not None:
                    sources[asset_path] = asset_text

    report.files_checked = sorted(_display_path(path, target) for path in sources)

    css_chunks = [text for path, text in sources.items() if path.suffix.lower() == ".css"]
    js_chunks = [text for path, text in sources.items() if path.suffix.lower() in SCRIPT_SUFFIXES]
    html_chunks = [sources[path] for path in markup_paths]
    for parser in parsers.values():
        css_chunks.extend(parser.style_chunks)
        css_chunks.extend(parser.style_attributes)
        js_chunks.extend(parser.script_chunks)
    css = "\n".join(css_chunks)
    javascript = "\n".join(js_chunks)
    html = "\n".join(html_chunks)

    for path, text in sources.items():
        relative = _display_path(path, target)
        em_dash = text.find("—")
        if em_dash >= 0:
            count = text.count("—")
            report.add(
                "error",
                "copy.em_dash",
                f"Foram encontrados {count} travessão(ões); reescreva com pontuação simples.",
                relative,
                _line_number(text, em_dash),
            )
        _check_placeholders(path, text, report, target)

    for path in html_paths:
        parser = parsers[path]
        relative = _display_path(path, target)
        if not parser.lang:
            report.add("error", "html.lang", "Elemento <html> precisa de atributo lang não vazio.", relative)
        if not parser.has_viewport:
            report.add("error", "html.viewport", "Meta viewport está ausente ou sem content.", relative)
        if not parser.title:
            report.add("error", "html.title", "Elemento <title> está ausente ou vazio.", relative)
        for line in parser.images_without_alt:
            report.add("error", "a11y.image_alt", "Imagem sem atributo alt.", relative, line)
        if not parser.h1_lines:
            report.add("warning", "html.h1", "Nenhum <h1> foi encontrado.", relative)
        for line, marker in parser.badges_before_h1:
            report.add(
                "warning",
                "design.badge_before_h1",
                f"Elemento '{marker}' aparece antes do H1; remova o rótulo decorativo do hero.",
                relative,
                line,
            )
        for line in parser.empty_hash_links:
            report.add("warning", "placeholder.link", "Link href='#' parece provisório.", relative, line)
        for line, tag, url in parser.remote_assets:
            report.add("warning", "asset.hotlink", f"Asset remoto em <{tag}>: {url}.", relative, line)

    for path in svg_paths:
        text = sources[path]
        relative = _display_path(path, target)
        root_match = re.search(r"<svg\b([^>]*)>", text, re.I | re.S)
        if not root_match:
            report.add("error", "svg.root", "Arquivo não contém elemento raiz <svg>.", relative)
            continue
        attributes = root_match.group(1)
        missing = [
            name
            for name in ("width", "height", "viewBox")
            if not re.search(rf"\b{name}\s*=\s*['\"][^'\"]+['\"]", attributes, re.I)
        ]
        if missing:
            report.add(
                "error",
                "svg.dimensions",
                "SVG precisa declarar " + ", ".join(missing) + ".",
                relative,
            )
        if not re.search(r"<title\b[^>]*>\s*[^<]+\s*</title>", text, re.I | re.S) and not re.search(
            r"\baria-label\s*=\s*['\"][^'\"]+['\"]", attributes, re.I
        ):
            report.add("warning", "svg.title", "SVG não possui <title> nem aria-label descritivo.", relative)
        for match in re.finditer(r"(?:href|xlink:href)\s*=\s*['\"](https?://|//)([^'\"]+)", text, re.I):
            report.add(
                "warning",
                "asset.hotlink",
                "Asset remoto no SVG: " + match.group(1) + match.group(2) + ".",
                relative,
                _line_number(text, match.start()),
            )

    for path, text in sources.items():
        if path.suffix.lower() != ".css":
            continue
        for url, line in _extract_remote_css_assets(text):
            report.add("warning", "asset.hotlink", f"Asset remoto no CSS: {url}.", _display_path(path, target), line)
    for path, parser in parsers.items():
        inline_css = "\n".join(parser.style_chunks)
        for url, line in _extract_remote_css_assets(inline_css):
            report.add("warning", "asset.hotlink", f"Asset remoto no CSS inline: {url}.", _display_path(path, target), line)

    if any(path.suffix.lower() not in SVG_SUFFIXES for path in sources) and not _has_responsive_css(css):
        report.add(
            "warning",
            "responsive.css",
            "Nenhuma estratégia responsiva clara foi encontrada (@media, @container, clamp ou grid fluido).",
        )

    interactive_count = sum(parser.interactive_count for parser in parsers.values())
    if interactive_count and not re.search(r":focus-visible\b", css, re.I):
        report.add(
            "warning",
            "a11y.focus_visible",
            f"Há {interactive_count} elemento(s) interativo(s), mas nenhum estilo :focus-visible.",
        )

    if _has_motion(css, javascript) and not _has_reduced_motion(css, javascript):
        report.add(
            "warning",
            "a11y.reduced_motion",
            "Há motion/transições sem fallback prefers-reduced-motion: reduce.",
        )

    if _has_decorative_grid(css, html):
        report.add("warning", "design.decorative_grid", "Possível grid/dot-grid decorativo detectado no fundo.")
    if _has_multicolor_gradient_text(css):
        report.add(
            "warning",
            "design.gradient_text",
            "Texto com gradiente multicolorido detectado; prefira ênfase por uma única cor de acento.",
        )

    svg_color_source = "\n".join(sources[path] for path in svg_paths)
    report.color_families = _color_report(css + "\n" + svg_color_source)
    rank = {"error": 0, "warning": 1, "info": 2}
    report.findings.sort(key=lambda item: (rank.get(item.severity, 9), item.path or "", item.line or 0, item.code))
    return report


def format_text(report: PreflightReport) -> str:
    status = "APROVADO" if report.ok else "REPROVADO"
    lines = [
        f"Design DNA Preflight: {status}",
        f"Alvo: {report.target}",
        f"Arquivos verificados: {len(report.files_checked)}",
        f"Erros fortes: {report.error_count} | Avisos: {report.warning_count}",
    ]
    if report.files_checked:
        lines.append("Fontes: " + ", ".join(report.files_checked))
    if report.color_families:
        families = []
        for name, details in report.color_families.items():
            samples = ", ".join(str(sample) for sample in details.get("samples", []))
            families.append(f"{name}={details.get('count', 0)} [{samples}]")
        lines.append("Famílias de cor: " + "; ".join(families))
    else:
        lines.append("Famílias de cor: nenhuma cor CSS reconhecida")
    if not report.findings:
        lines.append("Nenhum problema encontrado.")
    for finding in report.findings:
        location = finding.path or "."
        if finding.line is not None:
            location += f":{finding.line}"
        lines.append(f"[{finding.severity.upper()}] {finding.code} | {location} | {finding.message}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audita HTML/CSS/JS/TS/React/SVG com os guardrails do Design DNA.")
    parser.add_argument("target", nargs="?", default=".", help="Arquivo web/SVG ou diretório do projeto.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emite relatório JSON.")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    report = audit_target(args.target)
    if args.as_json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(format_text(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
