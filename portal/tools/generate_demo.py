"""Gerar uma sessão sintética de ~10 minutos para exercitar o portal; nunca usar como evidência real."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import math
from portal.core import encode_record

def main():
    output = Path("portal/sample_data/demo_127v.log")
    output.parent.mkdir(parents=True,exist_ok=True)
    t0 = datetime(2026,11,6,14,0,0,tzinfo=timezone.utc)
    device, session = "DEMO-001", "DEMO-SESSION-001"
    seq, lines = 0, []
    def add(kind,sec,data):
        nonlocal seq
        seq += 1
        stamp = (t0+timedelta(seconds=sec)).isoformat(timespec="milliseconds").replace("+00:00","Z")
        lines.append(encode_record(kind,device,session,seq,stamp,round(sec*1000),data))
    add("000",0,{"reason":"demo_start","firmware":"simulated","rtc_quality":"valid"})
    add("200",0.01,{"v_nom":"127","interval_s":"1","ct_present":"false"})
    for sec in range(1,601):
        v = round(127 + 1.5 * math.sin(sec/37),2)
        if 100 <= sec <= 112: v = 105.5
        if 310 <= sec <= 320: v = 144.2
        if sec == 405:
            add("120",sec-0.1,{"ac_state":"absent","source":"isolated_detector"})
        if sec == 411:
            add("120",sec-0.1,{"ac_state":"present","source":"isolated_detector"})
        if not 405 <= sec <= 411:
            add("100",sec,{"v_rms":v,"i_rms":"NA","p_w":"NA","e_kwh":"NA",
                           "freq_hz":60,"pf":"NA","ct_present":"false",
                           "pzem_valid":"true","sample_age_ms":500})
        elif sec == 405:
            add("130",sec,{"pzem_valid":"false","error_code":"timeout"})
    add("999",602,{"reason":"demo_end"})
    output.write_text("".join(lines),encoding="utf-8")
    print(f"Arquivo sintético: {output} ({len(lines)} registros)")

if __name__ == "__main__":
    main()
