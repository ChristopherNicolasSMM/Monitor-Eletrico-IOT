"""Testes estruturais dos temas; não substituem screenshots e testes de acessibilidade no navegador."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "static"


def relative_luminance(value):
    rgb = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    aa, bb = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (aa + 0.05) / (bb + 0.05)


def token(css, theme, name):
    if theme == "dark":
        section = css.split('html[data-theme="dark"]{', 1)[1].split("}", 1)[0]
    else:
        section = css.split(':root,html[data-theme="light"]{', 1)[1].split("}", 1)[0]
    match = re.search(r"--" + re.escape(name) + r":(#[0-9a-fA-F]{6})", section)
    assert match is not None, f"Token {name} ausente em {theme}"
    return match.group(1)


class ThemeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = (ROOT / "style.css").read_text(encoding="utf-8")
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.js = (ROOT / "app.js").read_text(encoding="utf-8")

    def test_all_three_theme_controls(self):
        for choice in ("light", "dark", "system"):
            self.assertIn(f'data-theme-choice="{choice}"', self.html)
        self.assertIn('aria-pressed="false"', self.html)

    def test_system_theme_and_persistence(self):
        self.assertIn("prefers-color-scheme: dark", self.js)
        self.assertIn("monitor-theme", self.js)
        self.assertIn('localStorage.setItem(', self.js)
        self.assertIn('themeQuery.addEventListener("change"', self.js)

    def test_plotly_retheming(self):
        self.assertIn('Plotly.relayout("voltage-chart"', self.js)
        self.assertIn('Plotly.restyle("voltage-chart"', self.js)
        self.assertIn('const palette = chartPalette()', self.js)

    def test_light_and_dark_text_contrast(self):
        for name in ("light", "dark"):
            with self.subTest(theme=name):
                bg = token(self.css, name, "surface")
                for text_token in ("text", "muted", "subtle"):
                    self.assertGreaterEqual(contrast(bg, token(self.css, name, text_token)), 4.5)

    def test_dark_never_uses_black_background(self):
        self.assertNotIn("--page:#000000", self.css)
        self.assertNotIn("--surface:#000000", self.css)
        self.assertNotEqual(token(self.css, "dark", "page"), token(self.css, "dark", "surface"))

    def test_warning_contrast(self):
        for name in ("light", "dark"):
            self.assertGreaterEqual(contrast(token(self.css, name, "warning-text"), token(self.css, name, "warning-bg")), 4.5)

if __name__ == "__main__":
    unittest.main()
