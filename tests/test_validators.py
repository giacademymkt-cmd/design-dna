from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import doctor, preflight, reference_manifest  # noqa: E402


GOOD_EVALS = {
    "skill_name": "sample-skill",
    "evals": [
        {
            "id": 1,
            "prompt": "Crie uma página.",
            "assertions": ["Entrega HTML válido", "Inclui viewport"],
        }
    ],
}


def write_skill(root: Path, *, skill_body: str = "# Sample\n\nUse o material em `references/guide.md`.\n", evals=None) -> None:
    (root / "references").mkdir(parents=True, exist_ok=True)
    (root / "evals").mkdir(parents=True, exist_ok=True)
    (root / "references" / "guide.md").write_text("# Guide\n\nConteúdo.\n", encoding="utf-8")
    skill = "---\nname: sample-skill\ndescription: Use para criar páginas de amostra.\n---\n\n" + skill_body
    (root / "SKILL.md").write_text(skill, encoding="utf-8")
    (root / "evals" / "evals.json").write_text(
        json.dumps(GOOD_EVALS if evals is None else evals, ensure_ascii=False),
        encoding="utf-8",
    )


def write_html(root: Path, content: str, name: str = "index.html") -> Path:
    path = root / name
    path.write_text(content, encoding="utf-8")
    return path


GOOD_HTML = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Produto premium</title>
  <style>
    :root { --ink: #0a0c0f; --accent: #22c55e; }
    body { color: var(--ink); }
    button { animation: enter .2s ease; }
    button:focus-visible { outline: 3px solid var(--accent); }
    @keyframes enter { from { opacity: 0; } to { opacity: 1; } }
    @media (max-width: 720px) { main { padding: 1rem; } }
    @media (prefers-reduced-motion: reduce) { * { animation: none; transition: none; } }
  </style>
</head>
<body>
  <main><h1>Produto premium</h1><img src="product.png" alt="Tela do produto"><button>Começar</button></main>
</body>
</html>
"""


class DoctorTests(unittest.TestCase):
    def test_valid_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root)

            report = doctor.audit_package(root)

            self.assertTrue(report.ok, doctor.format_text(report))
            self.assertEqual(report.error_count, 0)
            self.assertGreaterEqual(report.files_checked, 3)

    def test_detects_absolute_missing_path_and_unclosed_fence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            absolute_user_path = "/" + "Users/demo/reference.png"
            body = (
                "# Sample\n\n"
                "Leia `references/does-not-exist.md`.\n\n"
                f"Não use {absolute_user_path}.\n\n"
                "```css\nbody { color: red; }\n"
            )
            write_skill(root, skill_body=body)

            report = doctor.audit_package(root)
            codes = {finding.code for finding in report.findings}

            self.assertFalse(report.ok)
            self.assertIn("path.absolute_users", codes)
            self.assertIn("path.missing", codes)
            self.assertIn("markdown.fence_unclosed", codes)

    def test_requires_frontmatter_fields_and_short_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root)
            oversized = "---\nname: Bad Name\ndescription:\n---\n" + "linha\n" * 500
            (root / "SKILL.md").write_text(oversized, encoding="utf-8")

            report = doctor.audit_package(root)
            codes = {finding.code for finding in report.findings}

            self.assertIn("frontmatter.name_format", codes)
            self.assertIn("frontmatter.description", codes)
            self.assertIn("skill.too_long", codes)

    def test_rejects_officially_unsupported_frontmatter_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root)
            skill_path = root / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8").replace(
                    "description: Use para criar páginas de amostra.\n",
                    "description: Use para criar páginas de amostra.\ncompatibility: browser\n",
                ),
                encoding="utf-8",
            )

            report = doctor.audit_package(root)

            self.assertIn("frontmatter.unexpected_keys", {item.code for item in report.findings})

    def test_inline_code_path_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root, skill_body="# Sample\n\nLeia `missing-guide.md`.\n")

            report = doctor.audit_package(root)

            self.assertIn("path.missing", {item.code for item in report.findings})

    def test_long_document_without_toc_is_non_blocking_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root)
            long_doc = "# Long reference\n" + "conteúdo\n" * 301
            (root / "references" / "guide.md").write_text(long_doc, encoding="utf-8")

            report = doctor.audit_package(root)

            self.assertTrue(report.ok, doctor.format_text(report))
            self.assertIn("markdown.toc_missing", {finding.code for finding in report.findings})

    def test_expectations_field_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evals = {"evals": [{"prompt": "Teste", "expectations": ["Resultado claro"]}]}
            write_skill(root, evals=evals)

            report = doctor.audit_package(root)

            self.assertNotIn("evals.expectations_missing", {finding.code for finding in report.findings})
            self.assertTrue(report.ok, doctor.format_text(report))

    def test_eval_without_assertions_or_expectations_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root, evals={"evals": [{"prompt": "Teste"}]})

            report = doctor.audit_package(root)

            self.assertIn("evals.expectations_missing", {finding.code for finding in report.findings})
            self.assertFalse(report.ok)

    def test_missing_eval_fixture_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evals = {"evals": [{"prompt": "Teste", "assertions": ["Ok"], "files": ["fixtures/missing.html"]}]}
            write_skill(root, evals=evals)

            report = doctor.audit_package(root)

            self.assertIn("path.missing", {finding.code for finding in report.findings})
            self.assertFalse(report.ok)

    def test_doctor_cli_json_and_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root)
            (root / "evals" / "evals.json").write_text("{broken", encoding="utf-8")

            process = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "doctor.py"), str(root), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(process.stdout)

            self.assertEqual(process.returncode, 1)
            self.assertFalse(payload["ok"])
            self.assertGreater(payload["error_count"], 0)


class PreflightTests(unittest.TestCase):
    def test_clean_page_passes_and_reports_color_families(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = write_html(Path(temporary), GOOD_HTML)

            report = preflight.audit_target(path)

            self.assertTrue(report.ok, preflight.format_text(report))
            self.assertIn("green", report.color_families)
            self.assertIn("neutral", report.color_families)
            self.assertNotIn("a11y.reduced_motion", {finding.code for finding in report.findings})

    def test_detects_strong_html_and_copy_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = write_html(
                Path(temporary),
                """<html><head></head><body><h1>Lorem ipsum — produto</h1>
                <img src="https://placehold.co/600x400"><button>Ir</button></body></html>""",
            )

            report = preflight.audit_target(path)
            codes = {finding.code for finding in report.findings}

            self.assertFalse(report.ok)
            self.assertIn("html.lang", codes)
            self.assertIn("html.viewport", codes)
            self.assertIn("html.title", codes)
            self.assertIn("a11y.image_alt", codes)
            self.assertIn("copy.em_dash", codes)
            self.assertIn("placeholder.lorem", codes)
            self.assertIn("placeholder.asset", codes)
            self.assertIn("asset.hotlink", codes)

    def test_design_smells_are_warnings_not_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = write_html(
                Path(temporary),
                """<!doctype html><html lang="pt-BR"><head>
                <meta name="viewport" content="width=device-width,initial-scale=1"><title>Teste</title>
                <style>
                body { background-image: linear-gradient(#ffffff22 1px,transparent 1px),
                       linear-gradient(90deg,#ffffff22 1px,transparent 1px); background-size:24px 24px; }
                .rainbow { background: linear-gradient(#f00,#0f0); background-clip:text; color:transparent; }
                button { transition: transform .2s; }
                </style></head><body><span class="eyebrow">Novo</span><h1 class="rainbow">Título</h1>
                <button>Comprar</button></body></html>""",
            )

            report = preflight.audit_target(path)
            codes = {finding.code for finding in report.findings}

            self.assertTrue(report.ok, preflight.format_text(report))
            self.assertIn("design.badge_before_h1", codes)
            self.assertIn("design.decorative_grid", codes)
            self.assertIn("design.gradient_text", codes)
            self.assertIn("a11y.focus_visible", codes)
            self.assertIn("a11y.reduced_motion", codes)
            self.assertIn("responsive.css", codes)

    def test_external_asset_is_reported_without_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            html = GOOD_HTML.replace(
                "<meta charset=\"utf-8\">",
                '<meta charset="utf-8"><link rel="stylesheet" href="https://cdn.test/styles.css">',
            )
            path = write_html(Path(temporary), html)

            report = preflight.audit_target(path)

            self.assertTrue(report.ok, preflight.format_text(report))
            self.assertIn("asset.hotlink", {finding.code for finding in report.findings})

    def test_local_linked_css_and_js_are_audited(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "style.css").write_text(
                "button:focus-visible{outline:2px solid #2563eb}@media(max-width:600px){body{padding:1rem}}",
                encoding="utf-8",
            )
            (root / "app.js").write_text("document.documentElement.dataset.ready = 'true';", encoding="utf-8")
            path = write_html(
                root,
                """<!doctype html><html lang="pt-BR"><head><meta name="viewport" content="width=device-width">
                <title>Linked</title><link rel="stylesheet" href="style.css"><script src="app.js"></script>
                </head><body><h1>Linked</h1><button>Ok</button></body></html>""",
            )

            report = preflight.audit_target(path)

            self.assertTrue(report.ok, preflight.format_text(report))
            self.assertIn("style.css", report.files_checked)
            self.assertIn("app.js", report.files_checked)
            self.assertNotIn("responsive.css", {finding.code for finding in report.findings})
            self.assertNotIn("a11y.focus_visible", {finding.code for finding in report.findings})

    def test_css_only_target_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "style.css"
            path.write_text(
                "body{color:#0f172a}@media(max-width:600px){body{padding:1rem}}:focus-visible{outline:2px solid #22c55e}",
                encoding="utf-8",
            )

            report = preflight.audit_target(path)

            self.assertTrue(report.ok, preflight.format_text(report))
            self.assertEqual(report.files_checked, ["style.css"])

    def test_tsx_target_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "Panel.tsx"
            path.write_text(
                "export function Panel(){ return <button aria-label='Salvar'>Salvar</button> }",
                encoding="utf-8",
            )

            report = preflight.audit_target(path)

            self.assertTrue(report.ok, preflight.format_text(report))
            self.assertEqual(report.files_checked, ["Panel.tsx"])

    def test_svg_target_is_supported_and_checks_portable_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "creative.svg"
            path.write_text(
                "<svg width='1080' height='1350' viewBox='0 0 1080 1350' "
                "xmlns='http://www.w3.org/2000/svg'><title>Criativo</title>"
                "<rect width='1080' height='1350' fill='#f5f5f0'/><text fill='#135dff'>Título</text></svg>",
                encoding="utf-8",
            )

            report = preflight.audit_target(path)

            self.assertTrue(report.ok, preflight.format_text(report))
            self.assertEqual(report.warning_count, 0)
            self.assertIn("blue", report.color_families)

    def test_preflight_cli_json_warnings_exit_zero(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = write_html(Path(temporary), GOOD_HTML.replace("button:focus-visible", "button:focus"))
            process = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "preflight.py"), str(path), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(process.stdout)

            self.assertEqual(process.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertGreaterEqual(payload["warning_count"], 1)

    def test_preflight_cli_errors_exit_one(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = write_html(Path(temporary), "<html><body><img src='x.png'></body></html>")
            process = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "preflight.py"), str(path), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(process.stdout)

            self.assertEqual(process.returncode, 1)
            self.assertFalse(payload["ok"])
            self.assertGreater(payload["error_count"], 0)


class ReferenceManifestTests(unittest.TestCase):
    def test_build_manifest_uses_relative_paths_and_style_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "dark-ui-lab" / "01__source"
            source.mkdir(parents=True)
            (source / "frame.jpg").write_bytes(b"reference-bytes")

            manifest = reference_manifest.build_manifest(root, include_hashes=True)

            self.assertEqual(manifest["total_files"], 1)
            self.assertEqual(manifest["styles"]["dark-ui-lab"]["files"], 1)
            self.assertEqual(manifest["files"][0]["path"], "dark-ui-lab/01__source/frame.jpg")
            self.assertNotIn(str(root), json.dumps(manifest))
            self.assertEqual(len(manifest["files"][0]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
