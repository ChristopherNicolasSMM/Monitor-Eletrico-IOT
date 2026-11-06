"""Testes de demonstração, usando somente gerador e análise em memória."""
import unittest
from portal.core import parse_bytes, analyze
from portal.demo import demo_bytes, SCENARIOS

class DemoTest(unittest.TestCase):
    def test_each_scenario_imports_without_invalid_lines(self):
        for key in SCENARIOS:
            with self.subTest(scenario=key):
                parsed = parse_bytes(demo_bytes(key), key + ".log")
                self.assertEqual(parsed["invalid_lines"], 0)
                self.assertEqual(parsed["valid_lines"], parsed["total_lines"])
                self.assertFalse(parsed["issues"])
                self.assertGreater(parsed["valid_lines"], 500)

    def test_scenario_distinctions(self):
        normal = analyze(parse_bytes(demo_bytes("normal")))
        variations = analyze(parse_bytes(demo_bytes("oscilacoes")))
        interruption = analyze(parse_bytes(demo_bytes("interrupcoes")))
        self.assertFalse(any(e["kind"] in ("SUBTENSAO", "SOBRETENSAO") for e in normal["events"]))
        self.assertTrue(any(e["kind"] == "SUBTENSAO" for e in variations["events"]))
        self.assertTrue(any(e["kind"] == "SOBRETENSAO" for e in variations["events"]))
        self.assertEqual(sum(e["kind"] == "REDE_AUSENTE" for e in interruption["events"]),2)

    def test_unknown_scenario_is_rejected(self):
        with self.assertRaises(ValueError):
            demo_bytes("inexistente")
