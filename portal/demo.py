"""Dados de demonstração determinísticos, sem qualquer conexão com hardware."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from math import sin
from portal.core import encode_record

SCENARIOS = {
    "normal": "Rede estável (10 minutos)",
    "oscilacoes": "Subtensão e sobretensão (10 minutos)",
    "interrupcoes": "Quedas e retorno da rede (10 minutos)",
}

def demo_bytes(scenario: str = "oscilacoes") -> bytes:
    if scenario not in SCENARIOS:
        raise ValueError(f"Cenário desconhecido: {scenario}")
    begin = datetime(2026, 11, 6, 14, 0, tzinfo=timezone.utc)
    count = 0
    records: list[str] = []
    def append(kind: str, t: int, payload: dict[str, object]) -> None:
        nonlocal count
        count += 1
        time = (begin + timedelta(seconds=t)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        records.append(encode_record(kind, "DEMO-001", "DEMO-" + scenario.upper(), count, time, t*1000, payload))

    append("000", 0, {"reason": "demo_start", "firmware": "SIMULADO", "rtc_quality": "valid"})
    append("200", 0, {"v_nom": 127, "interval_s": 1, "ct_present": "false"})
    for second in range(1, 601):
        if scenario == "interrupcoes" and second in (150, 380):
            append("120", second, {"ac_state": "absent", "source": "isolated_detector"})
        if scenario == "interrupcoes" and second in (158, 386):
            append("120", second, {"ac_state": "present", "source": "isolated_detector"})
        if scenario == "interrupcoes" and (150 <= second < 158 or 380 <= second < 386):
            if second in (150, 380):
                append("130", second, {"pzem_valid": "false", "error_code": "timeout"})
            continue
        volts = round(127 + 1.25 * sin(second/33), 2)
        if scenario == "oscilacoes":
            if 105 <= second <= 120:
                volts = 105.3
            if 325 <= second <= 337:
                volts = 143.4
        append("100", second, {
            "v_rms": volts, "freq_hz": 60.0, "pzem_valid": "true",
            "sample_age_ms": 250, "ct_present": "false",
            "i_rms": "NA", "p_w": "NA", "pf": "NA", "e_kwh": "NA",
        })
    append("999", 602, {"reason": "demo_end"})
    return "".join(records).encode("utf-8")
