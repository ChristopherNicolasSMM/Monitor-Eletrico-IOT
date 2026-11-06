const q = s => document.querySelector(s);
const escapeHtml = x => String(x??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
let currentId = null;
const fmt = (v,unit="") => v===null||v===undefined?"N/D":Number(v).toLocaleString("pt-BR",{maximumFractionDigits:2})+unit;
function card(name,val){return '<div class="card"><small>'+escapeHtml(name)+'</small><strong>'+escapeHtml(val)+'</strong></div>'}
function render(data){
 const x=data.analysis, imp=data.import;currentId=data.id;
 q("#source").textContent=imp.name;
 q("#integrity").textContent=imp.valid_lines+" válidas · "+imp.invalid_lines+" inválidas · "+imp.issues.length+" avisos";
 q("#cards").innerHTML=[
 card("Tensão mínima",fmt(x.voltage?.min," V")),
 card("Tensão máxima",fmt(x.voltage?.max," V")),
 card("Tensão média",fmt(x.voltage?.mean," V")),
 card("Eventos identificados",x.event_count),
 card("Amostras de tensão",x.valid_voltage_count),
 card("Linhas válidas",imp.valid_lines),
 card("Linhas inválidas",imp.invalid_lines),
 card("Frequência média",fmt(x.frequency?.mean," Hz"))
 ].join("");
 q("#event-total").textContent=x.event_count+" eventos";
 q("#events").innerHTML=x.events.length?x.events.map(e=>'<tr><td>'+escapeHtml(e.kind)+'</td><td>'+escapeHtml(e.start)+'</td><td>'+escapeHtml(e.end??"Indeterminado")+'</td><td>'+escapeHtml(e.line)+'</td><td>'+escapeHtml(e.detail)+'</td></tr>').join(""):'<tr><td colspan="5">Nenhum evento detectado nos dados disponíveis.</td></tr>';
 q("#issues").innerHTML=imp.issues.slice(0,100).map(i=>'<div class="issue">Linha '+escapeHtml(i.line)+': '+escapeHtml(i.reason)+'</div>').join("") || '<p>Nenhum aviso no parser.</p>';
 const plotted = x.samples.filter(s=>s.v!==null);
 if(plotted.length){
   Plotly.newPlot("voltage-chart",[
     {x:plotted.map(s=>s.timestamp),y:plotted.map(s=>s.v),mode:"lines+markers",name:"Tensão RMS",line:{color:"#3b9c9d"},connectgaps:false},
     {x:[plotted[0].timestamp,plotted[plotted.length-1].timestamp],y:[x.lower_v,x.lower_v],mode:"lines",name:"Limiar inferior",line:{color:"#e9a844",dash:"dash"}},
     {x:[plotted[0].timestamp,plotted[plotted.length-1].timestamp],y:[x.upper_v,x.upper_v],mode:"lines",name:"Limiar superior",line:{color:"#c26a55",dash:"dash"}}
   ],{paper_bgcolor:"#fff",plot_bgcolor:"#fff",margin:{l:48,r:20,b:65,t:20},xaxis:{title:"UTC"},yaxis:{title:"Volts"},legend:{orientation:"h"}},{responsive:true,displaylogo:false});
 }else{q("#voltage-chart").textContent="Nenhuma medição de tensão válida disponível."}
 for (const [id,href] of [["pdf-tecnico",`/api/report/${currentId}/tecnico.pdf`],["pdf-cliente",`/api/report/${currentId}/cliente.pdf`],["csv",`/api/export/${currentId}/csv`]]){
   q("#"+id).href=href;q("#"+id).classList.remove("disabled");
 }
 fetch("/api/records/"+currentId+"?limit=100").then(r=>r.json()).then(v=>{
   q("#records").innerHTML=v.rows.map(r=>'<tr><td>'+r.line+'</td><td>'+escapeHtml(r.type)+'</td><td>'+r.seq+'</td><td>'+escapeHtml(r.timestamp)+'</td><td><code>'+escapeHtml(JSON.stringify(r.data))+'</code></td></tr>').join("");
 });
}
q("#upload-form").addEventListener("submit",async e=>{
 e.preventDefault();const button=q("#import-btn");button.disabled=true;q("#message").textContent="Importando e validando...";
 try{
 const fd=new FormData(e.target);const resp=await fetch("/api/import",{method:"POST",body:fd});
 const payload=await resp.json();if(!resp.ok)throw new Error(JSON.stringify(payload.detail??payload));
 render(payload);q("#message").textContent="Importação concluída. Arquivos originais preservados e resultados disponíveis.";
 }catch(err){q("#message").textContent="Falha: "+err.message}
 finally{button.disabled=false}
});
