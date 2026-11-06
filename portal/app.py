"""FastAPI portal técnico local. Execute: python -m uvicorn portal.app:app --host 127.0.0.1 --port 8080"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from threading import RLock
from uuid import uuid4
import json
import os

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from plotly.offline import get_plotlyjs

from portal.core import parse_bytes, analyze
from portal.demo import demo_bytes, SCENARIOS
from xml.sax.saxutils import escape as xml_escape

HERE = Path(__file__).resolve().parent
DATA_ROOT = Path(os.environ.get("MONITOR_DATA_DIR", str(Path.home() / ".monitor-eletrico-iot"))).resolve()
RAW = DATA_ROOT / "raw"
RAW.mkdir(parents=True, exist_ok=True)
MAX_UPLOAD = 32 * 1024 * 1024
app = FastAPI(title="Monitor Elétrico IoT", version="0.1.1")
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
_lock = RLock()
_cache: dict[str, dict] = {}


def get_batch(batch_id: str) -> dict:
    with _lock:
        batch = _cache.get(batch_id)
    if batch is None:
        raise HTTPException(404, "Importação não encontrada nesta execução")
    return batch


def validate_origin(request: Request) -> None:
    """Defesa adicional de origem; binding em loopback é requisito de execução."""
    origin = request.headers.get("origin")
    if origin:
        from urllib.parse import urlsplit
        target = urlsplit(origin)
        if target.hostname not in {"127.0.0.1","localhost"} or target.port not in {8080, None}:
            raise HTTPException(403, "Origem não permitida")


@app.get("/", response_class=HTMLResponse)
def home():
    return (HERE / "static" / "index.html").read_text(encoding="utf-8")


@app.get("/api/status")
def status():
    return {"version":"0.1.1","mode":"technical","offline":True,
            "import_count":len(_cache),"temporary_analysis_cache":True}


@app.get("/api/vendor/plotly.js")
def plotly_js():
    return Response(content=get_plotlyjs(), media_type="application/javascript")



@app.get("/api/demo/scenarios")
def demo_scenarios():
    return {"scenarios": SCENARIOS, "notice": "Dados inteiramente sintéticos."}

@app.post("/api/demo")
def load_demo(request: Request, scenario: str = "oscilacoes"):
    validate_origin(request)
    try:
        data = demo_bytes(scenario)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    parsed = parse_bytes(data, "DEMONSTRACAO_" + scenario + ".log")
    result = analyze(parsed, 127.0)
    batch_id = uuid4().hex
    with _lock:
        _cache[batch_id] = {"import": parsed, "analysis": result, "nominal": 127.0, "demo": True, "files": [{"name": parsed["name"], "sha256": parsed["sha256"]}]}
    return {"id": batch_id, "demo": True, "import": {k: v for k, v in parsed.items() if k != "records"}, "analysis": result}

@app.post("/api/import")
async def import_logs(request: Request, files: list[UploadFile] = File(...),
                      nominal: float = Form(127.0)):
    validate_origin(request)
    if len(files) > 30 or not 80 <= nominal <= 260:
        raise HTTPException(422,"Limite de arquivos ou tensão nominal inválidos")
    parsed_list = []
    for item in files:
        filename = Path(item.filename or "medicao.log").name
        if not filename.lower().endswith(".log"):
            raise HTTPException(415,"Por enquanto use arquivos .log")
        data = await item.read(MAX_UPLOAD + 1)
        if len(data) > MAX_UPLOAD:
            raise HTTPException(413,"Arquivo excede 32 MiB")
        if not data:
            raise HTTPException(422,"Arquivo vazio")
        parsed = parse_bytes(data,filename)
        digest = parsed["sha256"]
        target = RAW / (digest + ".log")
        if not target.exists():
            tmp = RAW / (digest + "." + uuid4().hex + ".tmp")
            tmp.write_bytes(data)
            tmp.replace(target)
        parsed_list.append(parsed)
    # Reimportações idênticas na mesma requisição não repetem registros.
    unique = {p["sha256"]:p for p in parsed_list}
    merged = {"name":", ".join(p["name"] for p in unique.values()),
              "sha256":sha256("".join(sorted(unique)).encode()).hexdigest(),
              "total_lines":sum(p["total_lines"] for p in unique.values()),
              "valid_lines":sum(p["valid_lines"] for p in unique.values()),
              "invalid_lines":sum(p["invalid_lines"] for p in unique.values()),
              "records":[r for p in unique.values() for r in p["records"]],
              "issues":[{"file":p["name"],**issue} for p in unique.values() for issue in p["issues"]],
              "sessions":[s for p in unique.values() for s in p["sessions"]]}
    result = analyze(merged,nominal)
    batch_id = uuid4().hex
    with _lock:
        _cache[batch_id] = {"import":merged,"analysis":result,"nominal":nominal,
                            "files":[{"name":p["name"],"sha256":p["sha256"]} for p in unique.values()]}
    return {"id":batch_id,"import":{k:v for k,v in merged.items() if k!="records"},"analysis":result,"demo":False}


@app.get("/api/analysis/{batch_id}")
def get_analysis(batch_id: str):
    batch = get_batch(batch_id)
    return {"id":batch_id,"import":{k:v for k,v in batch["import"].items() if k!="records"},
            "analysis":batch["analysis"],"demo":batch.get("demo",False)}


@app.get("/api/records/{batch_id}")
def records(batch_id: str, offset: int = 0, limit: int = 100):
    batch = get_batch(batch_id)
    if offset < 0 or not 1 <= limit <= 500:
        raise HTTPException(422,"Paginação inválida")
    entries = batch["import"]["records"]
    return {"total":len(entries),"rows":entries[offset:offset+limit]}


@app.get("/api/export/{batch_id}/csv")
def export_csv(batch_id: str):
    import csv
    from portal.core import numeric
    batch = get_batch(batch_id)
    output = BytesIO()
    from io import StringIO
    txt = StringIO()
    writer = csv.writer(txt)
    writer.writerow(["timestamp_utc","device","session","seq","line","type","voltage_v","current_a","power_w","frequency_hz","power_factor"])
    for r in batch["import"]["records"]:
        writer.writerow([r["timestamp"],r["device"],r["session"],r["seq"],r["line"],r["type"],
                         r["data"].get("v_rms",""),r["data"].get("i_rms",""),
                         r["data"].get("p_w",""),r["data"].get("freq_hz",""),r["data"].get("pf","")])
    return Response(txt.getvalue(),media_type="text/csv; charset=utf-8",
                    headers={"Content-Disposition":'attachment; filename="medicoes.csv"'})


def pdf_bytes(batch: dict, view: str) -> bytes:
    if view not in {"cliente","tecnico"}:
        raise HTTPException(404,"Modelo de relatório desconhecido")
    buf = BytesIO()
    doc = SimpleDocTemplate(buf,pagesize=A4,leftMargin=38,rightMargin=38,topMargin=40,bottomMargin=40)
    styles = getSampleStyleSheet()
    analysis, source = batch["analysis"], batch["import"]
    title = "Relatório Executivo de Monitoramento" if view == "cliente" else "Relatório Técnico de Monitoramento"
    elements = [Paragraph(title,styles["Title"]),Spacer(1,12),
                Paragraph("Monitor Elétrico IoT | Protótipo experimental | Dados não certificados",styles["Normal"]),Spacer(1,12),
                Paragraph(f"Emissão UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",styles["Normal"]),
                Paragraph(f"Arquivo(s): {xml_escape(source['name'])}",styles["Normal"]),
                Paragraph(f"Registros válidos: {source['valid_lines']} | Inválidos: {source['invalid_lines']} | Alertas: {len(source['issues'])}",styles["Normal"]),
                Spacer(1,12)]
    v = analysis["voltage"]
    summary = [["Indicador","Valor"],["Tensão nominal",f"{analysis['nominal_v']:.1f} V"],
               ["Amostras com tensão válida",str(analysis["valid_voltage_count"])],
               ["Tensão mínima",f"{v['min']:.2f} V" if v else "Indisponível"],
               ["Tensão máxima",f"{v['max']:.2f} V" if v else "Indisponível"],
               ["Média",f"{v['mean']:.2f} V" if v else "Indisponível"],
               ["Eventos identificados",str(analysis["event_count"])]]
    table = Table(summary,colWidths=[270,220])
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1C3445")),
                               ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                               ("GRID",(0,0),(-1,-1),0.4,colors.lightgrey),("PADDING",(0,0),(-1,-1),7)]))
    elements.extend([table,Spacer(1,14),Paragraph("Ocorrências observadas",styles["Heading2"])])
    if batch.get("demo"):
        elements.insert(1, Paragraph("<b>DEMONSTRAÇÃO: DADOS FICTÍCIOS</b>", styles["Heading2"]))
    for ev in analysis["events"][:35]:
        elements.append(Paragraph(xml_escape(f"{ev['kind']} | {ev['start']} | {ev.get('detail','')}"),styles["BodyText"]))
    if len(analysis["events"])>35:
        elements.append(Paragraph("Demais ocorrências disponíveis no portal e na exportação.",styles["Normal"]))
    elements.append(Spacer(1,14))
    if view == "tecnico":
        elements.extend([Paragraph("Rastreabilidade",styles["Heading2"]),
                         Paragraph("SHA-256 da importação: "+source["sha256"],styles["Normal"]),
                         Paragraph("Versão do algoritmo: portal 0.1.0 (experimental)",styles["Normal"]),
                         Paragraph(f"Limiares configurados: {analysis['lower_v']} a {analysis['upper_v']} V",styles["Normal"])])
        for issue in source["issues"][:30]:
            elements.append(Paragraph(xml_escape(f"Linha {issue['line']}: {issue['reason']}"),styles["BodyText"]))
    elements.append(Paragraph("Limitações e interpretação",styles["Heading2"]))
    for limitation in analysis["limitations"]:
        elements.append(Paragraph(xml_escape("- "+limitation),styles["BodyText"]))
    elements.append(Spacer(1,8))
    elements.append(Paragraph("Este protótipo auxilia investigações, mas não comprova origem de falhas, conformidade regulatória ou ausência de transientes.",styles["BodyText"]))
    doc.build(elements)
    return buf.getvalue()


@app.get("/api/report/{batch_id}/{view}.pdf")
def report(batch_id: str, view: str):
    data = pdf_bytes(get_batch(batch_id),view)
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition":f'attachment; filename="relatorio-{view}.pdf"'})
