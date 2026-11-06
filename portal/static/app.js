"use strict";
const el = id => document.getElementById(id);
const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({
  "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
}[c]));
const fmt = (value, unit = "") => value == null ? "N/D" :
  Number(value).toLocaleString("pt-BR",{maximumFractionDigits:2}) + unit;

let currentId = null, currentAnalysis = null, allEvents = [];

// Preferência local, sem armazenamento no servidor; "system" acompanha o SO.
const THEME_KEY = "monitor-theme";
const themeQuery = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
let themePreference = "system";
try {
  const saved = localStorage.getItem(THEME_KEY);
  if (["light","dark","system"].includes(saved)) themePreference = saved;
} catch (_) { /* Navegação privada pode bloquear armazenamento. */ }
function effectiveTheme() {
  return themePreference === "system" ? (themeQuery?.matches ? "dark" : "light") : themePreference;
}
function chartPalette() {
  const css = getComputedStyle(document.documentElement);
  const get = name => css.getPropertyValue(name).trim();
  return {bg:get("--plot-bg"),grid:get("--plot-grid"),text:get("--plot-text"),
          voltage:get("--plot-voltage"),low:get("--plot-low"),high:get("--plot-high")};
}
function applyTheme(persist = false) {
  const selected = effectiveTheme();
  document.documentElement.dataset.theme = selected;
  document.querySelector('meta[name="theme-color"]')?.setAttribute("content",
    getComputedStyle(document.documentElement).getPropertyValue("--page").trim());
  document.querySelectorAll("[data-theme-choice]").forEach(button => {
    button.setAttribute("aria-pressed",String(button.dataset.themeChoice === themePreference));
  });
  if (persist) {
    try { localStorage.setItem(THEME_KEY, themePreference); } catch (_) { /* Continue sem persistência. */ }
  }
  if (currentAnalysis?.samples?.some(row => row.v !== null) && typeof Plotly !== "undefined") {
    const p=chartPalette();
    Plotly.relayout("voltage-chart",{
      paper_bgcolor:p.bg,plot_bgcolor:p.bg,"font.color":p.text,
      "xaxis.gridcolor":p.grid,"xaxis.linecolor":p.grid,
      "xaxis.zerolinecolor":p.grid,"yaxis.gridcolor":p.grid,
      "yaxis.linecolor":p.grid,"yaxis.zerolinecolor":p.grid,
      "legend.bgcolor":p.bg
    }).catch(()=>{});
    Plotly.restyle("voltage-chart",{"line.color":[p.voltage,p.low,p.high]},[0,1,2]).catch(()=>{});
  }
}
document.querySelectorAll("[data-theme-choice]").forEach(button => {
  button.addEventListener("click",() => {
    themePreference=button.dataset.themeChoice;
    applyTheme(true);
  });
});
if (themeQuery) {
  const systemChange = () => { if (themePreference === "system") applyTheme(false); };
  if (typeof themeQuery.addEventListener === "function") themeQuery.addEventListener("change",systemChange);
  else if (typeof themeQuery.addListener === "function") themeQuery.addListener(systemChange);
}
applyTheme(false);


function card(title, value) {
  return '<article class="card"><small>'+esc(title)+'</small><strong>'+esc(value)+'</strong></article>';
}
function showError(error) {
  el("message").textContent="Não foi possível concluir: "+String(error.message || error);
  el("message").classList.add("error");
}
function renderEvents() {
  const filter=el("event-filter").value;
  const filtered=allEvents.map((event,index)=>({event,index})).filter(({event})=>filter==="all"||event.kind===filter);
  el("event-total").textContent=filtered.length+" de "+allEvents.length+" ocorrências";
  el("events").innerHTML=filtered.length? filtered.map(({event,index}) =>
    '<tr><td><button type="button" class="event-link" data-event="'+index+'">'+esc(event.kind)+'</button></td><td>'+
    esc(event.start)+'</td><td>'+esc(event.end || "Indeterminado")+'</td><td>'+
    esc(event.line)+'</td><td>'+esc(event.detail || "")+'</td></tr>'
  ).join(""):'<tr><td colspan="5">Nenhuma ocorrência com o filtro selecionado.</td></tr>';
}
function inspectEvent(index) {
  const event=allEvents[index];
  if(!event)return;
  const box=el("event-detail"); box.hidden=false;
  const stamp=event.start;
  const near=(currentAnalysis?.samples||[]).filter(s=>Math.abs(Date.parse(s.timestamp)-Date.parse(stamp))<=30000).slice(0,16);
  box.innerHTML='<h3>Detalhe da ocorrência: '+esc(event.kind)+'</h3>'+
    '<p><strong>Início:</strong> '+esc(event.start)+' | <strong>Fim:</strong> '+esc(event.end||"Não determinado")+
    ' | <strong>Linha de origem:</strong> '+esc(event.line)+
    ' | <strong>Sessão:</strong> '+esc(event.session)+'</p>'+
    '<p>'+esc(event.detail||"")+'</p>'+
    '<p><strong>Amostras próximas (janela de 30 segundos):</strong></p>'+
    '<div class="tablewrap"><table><thead><tr><th>UTC</th><th>Tensão (V)</th><th>Arquivo/linha</th></tr></thead><tbody>'+
    near.map(s=>'<tr><td>'+esc(s.timestamp)+'</td><td>'+esc(fmt(s.v))+'</td><td>'+esc(s.line)+'</td></tr>').join("")+
    '</tbody></table></div><p class="note">A presença de um evento não determina sua causa. Consulte integridade e limites de aquisição.</p>';
  const start = Date.parse(stamp);
  const end = event.end ? Date.parse(event.end) : start;
  if(Number.isFinite(start) && typeof Plotly !== "undefined")
    Plotly.relayout("voltage-chart",{"xaxis.range":[new Date(start-30000).toISOString(),new Date(end+30000).toISOString()]})
      .catch(()=>{});
  box.scrollIntoView({behavior:"smooth",block:"nearest"});
}
function drawGraph(analysis){
  const data=analysis.samples || [];
  if(!data.some(row=>row.v!==null)){
    el("voltage-chart").textContent="Sem dados de tensão válidos para este período.";
    return;
  }
  const first=data[0].timestamp,last=data[data.length-1].timestamp;
  // Inserir ponto nulo entre amostras afastadas para NÃO desenhar através de lacunas.
  const timePoints=[],voltagePoints=[];
  for(let i=0;i<data.length;i++){
    if(i>0 && (data[i].session!==data[i-1].session ||
        Date.parse(data[i].timestamp)-Date.parse(data[i-1].timestamp)>2500)){
      timePoints.push(new Date((Date.parse(data[i].timestamp)+Date.parse(data[i-1].timestamp))/2).toISOString());
      voltagePoints.push(null);
    }
    timePoints.push(data[i].timestamp);voltagePoints.push(data[i].v);
  }
  const palette = chartPalette();
  const traces=[{
    x:timePoints,y:voltagePoints,name:"Tensão RMS",
    type:"scatter",mode:"lines",connectgaps:false,
    line:{color:palette.voltage,width:2}
  },{
    x:[first,last],y:[analysis.lower_v,analysis.lower_v],name:"Limiar inferior",
    type:"scatter",mode:"lines",line:{color:palette.low,dash:"dash"}
  },{
    x:[first,last],y:[analysis.upper_v,analysis.upper_v],name:"Limiar superior",
    type:"scatter",mode:"lines",line:{color:palette.high,dash:"dash"}
  }];
  Plotly.react("voltage-chart",traces,{
    paper_bgcolor:palette.bg,plot_bgcolor:palette.bg,font:{color:palette.text},
    margin:{l:55,r:22,t:20,b:55},
    xaxis:{title:"Data/hora UTC",showgrid:true,gridcolor:palette.grid},
    yaxis:{title:"Volts (V)",showgrid:true,gridcolor:"#edf3f6"},
    legend:{orientation:"h",y:-0.25,bgcolor:palette.bg},hovermode:"x unified"
  },{responsive:true,displaylogo:false,scrollZoom:true});
}
function render(payload){
  const analysis=payload.analysis, imported=payload.import;
  currentId=payload.id;currentAnalysis=analysis;allEvents=analysis.events||[];
  el("source").textContent=imported.name;
  el("demo-warning").hidden=!payload.demo;
  el("integrity").textContent=imported.valid_lines+" válidas | "+
    imported.invalid_lines+" inválidas | "+(imported.issues||[]).length+" alertas";
  el("cards").innerHTML=[
    card("Tensão mínima",fmt(analysis.voltage?.min," V")),
    card("Tensão máxima",fmt(analysis.voltage?.max," V")),
    card("Tensão média",fmt(analysis.voltage?.mean," V")),
    card("Ocorrências",analysis.event_count),
    card("Amostras válidas",analysis.valid_voltage_count),
    card("Linhas importadas",imported.total_lines),
    card("Linhas inválidas",imported.invalid_lines),
    card("Frequência média",fmt(analysis.frequency?.mean," Hz"))
  ].join("");
  const kinds=[...new Set(allEvents.map(e=>e.kind))].sort();
  el("event-filter").innerHTML='<option value="all">Todos os tipos</option>'+
    kinds.map(kind=>'<option value="'+esc(kind)+'">'+esc(kind)+'</option>').join("");
  el("event-detail").hidden=true;renderEvents();drawGraph(analysis);
  el("issues").innerHTML=(imported.issues||[]).slice(0,100).map(i=>
    '<div class="issue">Linha '+esc(i.line)+': '+esc(i.reason)+'</div>'
  ).join("") || '<p>Não foram identificados avisos estruturais nesta importação.</p>';
  for(const [id,url] of [
    ["pdf-tecnico",'/api/report/'+currentId+'/tecnico.pdf'],
    ["pdf-cliente",'/api/report/'+currentId+'/cliente.pdf'],
    ["csv",'/api/export/'+currentId+'/csv']
  ]){el(id).href=url;el(id).classList.remove("disabled");}
  fetch('/api/records/'+currentId+'?limit=100')
    .then(r=>{if(!r.ok)throw Error("Falha na leitura de registros");return r.json();})
    .then(r=>{el("records").innerHTML=r.rows.map(row=>
      '<tr><td>'+esc(row.line)+'</td><td>'+esc(row.type)+'</td><td>'+esc(row.seq)+'</td><td>'+
      esc(row.timestamp)+'</td><td><code>'+esc(JSON.stringify(row.data))+'</code></td></tr>'
    ).join("");})
    .catch(error=>{el("records").textContent=error.message;});
}
el("upload-form").addEventListener("submit",async e=>{
  e.preventDefault();const button=el("import-btn");
  button.disabled=true;el("message").classList.remove("error");
  el("message").textContent="Importando registros, validando integridade e calculando indicadores...";
  try{
    const response=await fetch("/api/import",{method:"POST",body:new FormData(e.currentTarget)});
    const result=await response.json();
    if(!response.ok)throw Error(typeof result.detail==="string"?result.detail:JSON.stringify(result.detail));
    render(result);
    el("message").textContent="Importação concluída. Arquivos originais preservados.";
  }catch(error){showError(error);}
  finally{button.disabled=false;}
});
el("load-demo").addEventListener("click",async ()=>{
  const button=el("load-demo");button.disabled=true;el("message").classList.remove("error");
  el("message").textContent="Carregando cenário fictício...";
  try{
    const scenario=encodeURIComponent(el("demo-scenario").value);
    const response=await fetch("/api/demo?scenario="+scenario,{method:"POST"});
    const result=await response.json();
    if(!response.ok)throw Error(result.detail||"Falha na demonstração");
    render(result);
    el("message").textContent="Demonstração carregada. Todos os dados são sintéticos.";
    el("indicadores").scrollIntoView({behavior:"smooth"});
  }catch(error){showError(error);}
  finally{button.disabled=false;}
});
el("event-filter").addEventListener("change",renderEvents);
el("events").addEventListener("click",event=>{
  const target=event.target.closest("[data-event]");
  if(target)inspectEvent(Number(target.dataset.event));
});
el("reset-zoom").addEventListener("click",()=>{
  if(currentAnalysis && typeof Plotly!=="undefined")
    Plotly.relayout("voltage-chart",{"xaxis.autorange":true}).catch(()=>{});
});
