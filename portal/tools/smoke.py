"""Smoke do gerador de 10 minutos e do parser, portável no Windows/Linux."""
from pathlib import Path
from portal.core import parse_bytes, analyze

def main():
    path = Path("portal/sample_data/demo_127v.log")
    dataset = parse_bytes(path.read_bytes(),path.name)
    assert dataset["invalid_lines"] == 0, dataset["issues"]
    calculated = analyze(dataset)
    assert calculated["valid_voltage_count"] > 500
    assert any(e["kind"] == "SUBTENSAO" for e in calculated["events"])
    assert any(e["kind"] == "SOBRETENSAO" for e in calculated["events"])
    assert any(e["kind"] == "REDE_AUSENTE" for e in calculated["events"])
    print("Smoke OK:", len(calculated["events"]), "ocorrências")

if __name__ == "__main__":
    main()
