"""Testes do parser e do motor. Execute: python -m unittest discover -s portal/tests -v"""
import unittest
from portal.core import encode_record, parse_bytes, analyze

TS = "2026-11-06T14:00:00.000Z"

def make_line(kind, seq, values, sec=0):
    from datetime import datetime,timezone,timedelta
    t=(datetime(2026,11,6,14,tzinfo=timezone.utc)+timedelta(seconds=sec)).isoformat(timespec="milliseconds").replace("+00:00","Z")
    return encode_record(kind,"TEST-001","S001",seq,t,sec*1000,values)

class ProtocolTest(unittest.TestCase):
    def test_roundtrip(self):
        data=(make_line("000",1,{"reason":"start"})+
              make_line("100",2,{"v_rms":"127.20","freq_hz":"60","pzem_valid":"true"},1)+
              make_line("999",3,{"reason":"end"},2)).encode()
        result=parse_bytes(data)
        self.assertEqual(result["valid_lines"],3)
        self.assertEqual(result["invalid_lines"],0)
        self.assertEqual(analyze(result)["voltage"]["min"],127.2)

    def test_crc_rejected(self):
        raw=make_line("100",1,{"v_rms":"127"})
        corrupt=raw.replace("127","125")
        result=parse_bytes(corrupt.encode())
        self.assertEqual(result["invalid_lines"],1)
        self.assertTrue(any("CRC32" in issue["reason"] for issue in result["issues"]))

    def test_timeout_is_not_blackout(self):
        data=(make_line("000",1,{"reason":"start"})+
              make_line("130",2,{"pzem_valid":"false","error_code":"timeout"},1)).encode()
        a=analyze(parse_bytes(data))
        self.assertFalse(any(e["kind"]=="REDE_AUSENTE" for e in a["events"]))

    def test_confirmed_ac_missing(self):
        data=(make_line("000",1,{"reason":"start"})+
              make_line("120",2,{"ac_state":"absent","source":"isolated_detector"},1)).encode()
        self.assertIn("REDE_AUSENTE",[e["kind"] for e in analyze(parse_bytes(data))["events"]])

    def test_missing_ct_does_not_create_current(self):
        data=(make_line("000",1,{"reason":"start"})+
              make_line("100",2,{"v_rms":"127","i_rms":"12","ct_present":"false"},1)).encode()
        self.assertIsNone(analyze(parse_bytes(data))["current"])

    def test_no_formal_shutdown(self):
        r=parse_bytes(make_line("000",1,{"reason":"boot"}).encode())
        self.assertTrue(any("999" in i["reason"] for i in r["issues"]))

    def test_invalid_voltage_out_of_range(self):
        data=(make_line("000",1,{"reason":"start"})+
              make_line("100",2,{"v_rms":"20"},1)).encode()
        self.assertIsNone(analyze(parse_bytes(data))["voltage"])

    def test_subvoltage_requires_multiple_samples(self):
        text=make_line("000",1,{"reason":"start"})
        for s in range(1,5):
            text+=make_line("100",s+1,{"v_rms":"100","pzem_valid":"true"},s)
        a=analyze(parse_bytes(text.encode()))
        self.assertTrue(any(x["kind"]=="SUBTENSAO" for x in a["events"]))

if __name__=="__main__":
    unittest.main()
