"""Parser e análise dos arquivos de medição. Sem dependências web."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from statistics import mean, median
from typing import Any
import math
import zlib

SCHEMA = "1"
MAX_SAMPLE_AGE_MS = 3500
MEASUREMENT_KEYS = {"v_rms", "i_rms", "p_w", "e_kwh", "freq_hz", "pf"}
TYPES = {"000","100","110","111","120","130","140","200","210","900","999"}


def encode_record(kind: str, device: str, session: str, seq: int, stamp: str,
                  uptime: int, values: dict[str, object]) -> str:
    """Formato v1 experimental: CRC32 sobre campos UTF-8 unidos por pipe, sem pipes exteriores."""
    for v in [kind, device, session, stamp, *map(str, values.values())]:
        if any(c in str(v) for c in "|;\r\n"):
            raise ValueError("Caractere reservado no campo")
    payload = ";".join(f"{key}={val}" for key, val in values.items())
    body = "|".join([kind, SCHEMA, device, session, str(seq), stamp, str(uptime), payload])
    crc = zlib.crc32(body.encode("utf-8")) & 0xFFFFFFFF
    return f"|{body}|{crc:08X}|\n"


def parse_time(value: str) -> datetime:
    d = datetime.fromisoformat(value.replace("Z","+00:00"))
    if not d.tzinfo:
        raise ValueError("Timestamp sem timezone")
    return d.astimezone(timezone.utc)


def parse_bytes(data: bytes, name: str = "medicao.log") -> dict:
    digest = sha256(data).hexdigest()
    lines = data.splitlines()
    records, issues = [], []
    for n, raw in enumerate(lines, 1):
        try:
            s = raw.decode("utf-8")
            if not (s.startswith("|") and s.endswith("|")):
                raise ValueError("Envelope incompleto")
            parts = s[1:-1].split("|")
            if len(parts) != 9:
                raise ValueError(f"Esperados 9 campos, encontrados {len(parts)}")
            kind, schema, device, session, seq, stamp, uptime, payload, crc = parts
            if schema != SCHEMA:
                raise ValueError(f"Versão do esquema não suportada: {schema}")
            if kind not in TYPES:
                raise ValueError(f"Bloco não reconhecido: {kind}")
            body = "|".join(parts[:8])
            expected = f"{zlib.crc32(body.encode('utf-8')) & 0xFFFFFFFF:08X}"
            if crc.upper() != expected:
                raise ValueError("CRC32 divergente")
            seq_i, uptime_i = int(seq), int(uptime)
            if seq_i < 0 or uptime_i < 0:
                raise ValueError("Contador negativo")
            timestamp = parse_time(stamp)
            fields = {}
            if payload:
                for pair in payload.split(";"):
                    if pair.count("=") != 1:
                        raise ValueError("Payload malformado")
                    k, v = pair.split("=", 1)
                    if not k or k in fields:
                        raise ValueError("Chave vazia ou duplicada")
                    fields[k] = v
            records.append({"line": n, "type": kind, "device": device, "session": session,
                            "seq": seq_i, "timestamp": timestamp.isoformat(),
                            "uptime_ms": uptime_i, "data": fields})
        except (UnicodeError, ValueError, OverflowError) as exc:
            issues.append({"line": n, "reason": str(exc)})
    groups: dict[tuple, list] = {}
    for r in records:
        groups.setdefault((r["device"],r["session"]), []).append(r)
    for group in groups.values():
        ordered = sorted(group, key=lambda r: r["line"])
        last_seq = None
        for r in ordered:
            if last_seq is not None and r["seq"] != last_seq + 1:
                issues.append({"line": r["line"], "reason": "Sequência descontínua/duplicada"})
            last_seq = r["seq"]
        if not any(r["type"] == "000" for r in ordered):
            issues.append({"line": ordered[0]["line"],"reason":"Sessão sem bloco 000"})
        if not any(r["type"] == "999" for r in ordered):
            issues.append({"line": ordered[-1]["line"],"reason":"Sessão sem encerramento formal 999"})
    return {"name": name, "sha256": digest, "total_lines":len(lines),
            "valid_lines":len(records), "invalid_lines":len(lines)-len(records),
            "records": records, "issues": sorted(issues,key=lambda x:x["line"]),
            "sessions":[{"device":k[0],"session":k[1],"records":len(v)} for k,v in groups.items()]}


def numeric(row: dict, field: str) -> float | None:
    value = row["data"].get(field)
    if value in (None, "", "NA", "null"):
        return None
    try:
        v = float(value)
        return v if math.isfinite(v) else None
    except (TypeError,ValueError):
        return None


def analyze(parsed: dict, nominal: float = 127.0, lower_pct: float = 0.9,
            upper_pct: float = 1.1, min_duration_s: float = 1.0) -> dict:
    """Sem interpolar lacunas e sem inferir falta de rede por timeout."""
    if not (80 <= nominal <= 260 and 0 < lower_pct < 1 < upper_pct and min_duration_s >= 0):
        raise ValueError("Parâmetros analíticos inválidos")
    rows = sorted((r for r in parsed["records"] if r["type"] == "100"),
                  key=lambda r:(r["device"],r["session"],r["timestamp"],r["seq"]))
    samples = []
    for r in rows:
        d = r["data"]
        age = numeric(r, "sample_age_ms")
        sensor_ok = d.get("pzem_valid","true").lower() == "true"
        fresh = age is None or (0 <= age <= MAX_SAMPLE_AGE_MS)
        volts = numeric(r,"v_rms") if sensor_ok and fresh else None
        if volts is not None and not 80 <= volts <= 260:
            volts = None
        sample = {"timestamp":r["timestamp"],"session":r["session"],"device":r["device"],
                  "line":r["line"],"seq":r["seq"],"v":volts,
                  "freq":numeric(r,"freq_hz") if sensor_ok and fresh else None,
                  "i":numeric(r,"i_rms") if d.get("ct_present") == "true" and sensor_ok and fresh else None,
                  "p":numeric(r,"p_w") if d.get("ct_present") == "true" and sensor_ok and fresh else None,
                  "pf":numeric(r,"pf") if d.get("ct_present") == "true" and sensor_ok and fresh else None}
        samples.append(sample)
    vals = [s["v"] for s in samples if s["v"] is not None]
    events = []
    # Confirmar apenas estados declarados por detector isolado.
    for r in parsed["records"]:
        if r["type"] == "120" and r["data"].get("source") == "isolated_detector":
            status = r["data"].get("ac_state")
            if status in ("absent","present"):
                events.append({"kind":"REDE_AUSENTE" if status=="absent" else "REDE_RETORNOU",
                               "start":r["timestamp"],"end":None,"line":r["line"],
                               "session":r["session"],"detail":"Estado informado por detector AC isolado"})
    lo, hi = nominal * lower_pct, nominal * upper_pct
    # Taxonomia conservadora: eventos sustentados exigem duração demonstrada por leituras consecutivas.
    for key, test in [("SUBTENSAO",lambda x:x<lo),("SOBRETENSAO",lambda x:x>hi)]:
        active = []
        def flush():
            if not active: return
            start, end = active[0], active[-1]
            duration = (parse_time(end["timestamp"])-parse_time(start["timestamp"])).total_seconds()
            if duration >= min_duration_s and len(active) >= 2:
                events.append({"kind":key,"start":start["timestamp"],"end":end["timestamp"],
                               "duration_s":duration,"line":start["line"],"session":start["session"],
                               "min_v":min(v["v"] for v in active),"max_v":max(v["v"] for v in active),
                               "detail":f"Limiar {lo:.1f} a {hi:.1f} V; período observado"})
            active.clear()
        for r in samples:
            gap = (parse_time(r["timestamp"])-parse_time(active[-1]["timestamp"])).total_seconds() if active else 0
            if active and (r["session"] != active[-1]["session"] or gap < 0 or gap > 2.5):
                flush()
            if r["v"] is not None and test(r["v"]):
                active.append(r)
            else:
                flush()
        flush()
    events.sort(key=lambda x:x["start"])
    def stats(seq):
        return {"min":min(seq),"max":max(seq),"mean":round(mean(seq),3),
                "median":round(median(seq),3)} if seq else None
    return {"nominal_v":nominal,"lower_v":round(lo,2),"upper_v":round(hi,2),
            "samples":samples,"sample_count":len(samples),"valid_voltage_count":len(vals),
            "voltage":stats(vals),
            "frequency":stats([s["freq"] for s in samples if s["freq"] is not None]),
            "current":stats([s["i"] for s in samples if s["i"] is not None]),
            "power":stats([s["p"] for s in samples if s["p"] is not None]),
            "events":events,"event_count":len(events),
            "quality":{"records_valid":parsed["valid_lines"],"records_invalid":parsed["invalid_lines"],
                       "warnings":len(parsed["issues"]),"unknown_intervals":True},
            "limitations":["Medições fora de 80 a 260 V não são quantificadas pelo PZEM.",
                           "Distúrbios de milissegundos e surtos rápidos podem não ser detectados.",
                           "Ausência de eventos detectados não comprova rede sem perturbações.",
                           "Intervalos sem leituras não foram interpolados."],
            "source_sha256":parsed["sha256"]}
