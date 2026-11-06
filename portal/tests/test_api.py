"""Smoke tests HTTP: portal técnico, demonstração e ambos os relatórios."""
import unittest
from fastapi.testclient import TestClient
from portal.app import app

class PortalAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_home_and_status(self):
        home = self.client.get("/")
        self.assertEqual(home.status_code, 200)
        self.assertIn("Modo técnico", home.text)
        status = self.client.get("/api/status").json()
        self.assertEqual(status["mode"], "technical")

    def test_demo_and_reports(self):
        response = self.client.post("/api/demo?scenario=oscilacoes")
        self.assertEqual(response.status_code, 200, response.text)
        info = response.json()
        self.assertTrue(info["demo"])
        self.assertGreater(info["analysis"]["valid_voltage_count"], 500)
        batch = info["id"]
        for audience in ("cliente", "tecnico"):
            pdf = self.client.get(f"/api/report/{batch}/{audience}.pdf")
            self.assertEqual(pdf.status_code, 200)
            self.assertTrue(pdf.content.startswith(b"%PDF"))
        csv = self.client.get(f"/api/export/{batch}/csv")
        self.assertEqual(csv.status_code, 200)
        self.assertIn("timestamp_utc",csv.text)
        records = self.client.get(f"/api/records/{batch}?limit=5")
        self.assertEqual(records.status_code,200)
        self.assertEqual(len(records.json()["rows"]),5)

    def test_invalid_scenario_and_unavailable_batch(self):
        self.assertEqual(self.client.post("/api/demo?scenario=x").status_code,422)
        self.assertEqual(self.client.get("/api/analysis/unknown").status_code,404)
