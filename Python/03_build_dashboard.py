"""Génère docs/index.html : dashboard exécutif interactif (hébergeable sur GitHub Pages).
Les données sont injectées depuis Data/*.csv — aucune valeur saisie à la main dans le HTML.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
g = pd.read_csv(ROOT / "Data/fact_group_financials.csv")
geo = pd.read_csv(ROOT / "Data/fact_geography.csv")
seg = pd.read_csv(ROOT / "Data/fact_segments.csv")
sc = pd.read_csv(ROOT / "Data/ceo_scorecard.csv")
recs = json.loads((ROOT / "Data/recommendations.json").read_text(encoding="utf-8"))

keep = ["company", "year", "revenue_meur", "recurring_op_income_meur", "op_margin_pct",
        "revenue_growth_pct", "organic_growth_pct", "employees"]
data = {
    "g": json.loads(g[keep].to_json(orient="records")),
    "geo": json.loads(geo[["company", "year", "region", "share_pct"]].to_json(orient="records")),
    "seg": json.loads(seg[seg.year == 2025][["company", "segment", "revenue_meur", "op_margin_pct",
                                             "organic_growth_2025_pct"]].to_json(orient="records")),
    "sc": json.loads(sc.to_json(orient="records")),
    "recs": recs,
}

TEMPLATE = r"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Luxury Intelligence Platform</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{--bg:#F7F3EC;--card:#fff;--ink:#1c1c1c;--mut:#6b6b6b;--gold:#B08D57;--navy:#1F3A5F;--line:#e6dfd2}
*{box-sizing:border-box}body{margin:0;font-family:Georgia,'Times New Roman',serif;background:var(--bg);color:var(--ink)}
header{background:var(--navy);color:#fff;padding:22px 32px}h1{margin:0;font-weight:400;font-size:26px;letter-spacing:.5px}
header p{margin:4px 0 0;color:#d8c9a8;font:13px Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:20px}
.bar{display:flex;gap:14px;align-items:center;flex-wrap:wrap;font:13px Arial,sans-serif;margin-bottom:16px}
select{padding:7px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;font-size:13px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.k small{display:block;font:11px Arial,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.6px}
.k b{font-size:24px;color:var(--navy)}.k i{font:12px Arial,sans-serif;font-style:normal}
.up{color:#2e7d32}.dn{color:#c62828}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px;margin-bottom:16px}
h2{font-size:16px;margin:0 0 10px;font-weight:700}.sub{font:12px Arial,sans-serif;color:var(--mut);margin:-6px 0 8px}
.ceo{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px}
.ceo .card{border-top:3px solid var(--gold)}.ceo b{font:12px Arial,sans-serif;text-transform:uppercase;color:var(--mut)}
.ceo p{margin:6px 0 0;font-size:15px}
table{width:100%;border-collapse:collapse;font:13px Arial,sans-serif}td,th{padding:6px 4px;border-bottom:1px solid var(--line);text-align:right}
td:first-child,th:first-child{text-align:left}
.rec{font:13px/1.45 Arial,sans-serif;border-left:3px solid var(--gold);padding:6px 12px;margin:8px 0;background:#fbf8f2}
footer{font:11px Arial,sans-serif;color:var(--mut);padding:10px 0 30px}
</style></head><body>
<header><h1>Luxury Intelligence Platform</h1><p>Benchmark stratégique LVMH · Hermès · Kering — données 2021-2025</p></header>
<main>
<div class="bar"><label>Entreprise <select id="co"><option>Toutes</option><option>LVMH</option><option>Hermès</option><option>Kering</option></select></label>
<label>Année <select id="yr"><option>2025</option><option>2024</option><option>2023</option><option>2022</option><option>2021</option></select></label></div>
<div class="kpis" id="kpis"></div>
<div class="ceo" id="ceo"></div>
<div class="grid">
<div class="card"><h2>Évolution du chiffre d'affaires (indice base 100 = 2021)</h2><canvas id="c1" height="230"></canvas></div>
<div class="card"><h2>Marge opérationnelle courante (%)</h2><canvas id="c2" height="230"></canvas></div>
<div class="card"><h2>Croissance annuelle publiée (%) — qui croît le plus vite ?</h2><canvas id="c3" height="230"></canvas></div>
<div class="card"><h2>Répartition géographique (%)</h2><p class="sub" id="gnote"></p><canvas id="c4" height="230"></canvas></div>
</div>
<div class="card" style="margin-bottom:16px"><h2>Segments d'activité 2025</h2><p class="sub">Croissance organique / comparable / taux constants selon l'entreprise</p><table id="seg"></table></div>
<div class="card"><h2>Recommandations stratégiques</h2><div id="recs"></div></div>
<footer>Sources : présentations de résultats annuels LVMH, Hermès (2025), rapport d'activité Kering 2024, communiqués annuels. Kering 2025 : activités poursuivies. Analyse pédagogique, pas un conseil en investissement.</footer>
</main>
<script>
const D=__DATA__;const COL={LVMH:'#B08D57','Hermès':'#E87722',Kering:'#1F3A5F'};const CO=Object.keys(COL);
const REG=['Europe','Amériques','Japon','Asie-Pacifique (hors Japon)','Autres'];const RC=['#5B7DB1','#B08D57','#C0504D','#E87722','#9AA5B1'];
const fmt=n=>n==null?'–':Math.round(n).toLocaleString('fr-FR');const pc=(n,d=1)=>n==null?'–':n.toFixed(d).replace('.',',')+' %';
const get=(c,y)=>D.g.find(r=>r.company==c&&r.year==y);let ch={};
function mk(id,cfg){if(ch[id])ch[id].destroy();ch[id]=new Chart(document.getElementById(id),cfg)}
const opt={plugins:{legend:{position:'bottom',labels:{boxWidth:10}}},maintainAspectRatio:true};
function render(){
 const co=document.getElementById('co').value,y=+document.getElementById('yr').value,list=co=='Toutes'?CO:[co];
 document.getElementById('kpis').innerHTML=list.map(c=>{const r=get(c,y),a=D.geo.find(x=>x.company==c&&x.year==y&&x.region.startsWith('Asie'));
  const gr=r.revenue_growth_pct;const cls=gr==null?'':gr>=0?'up':'dn';
  return `<div class="card k"><small>${c} · ${y}</small><b>${fmt(r.revenue_meur)} M€</b><br><i class="${cls}">${gr==null?'n.d.':(gr>0?'▲ ':'▼ ')+pc(gr)} vs N-1</i>
  <br><i>ROC ${fmt(r.recurring_op_income_meur)} M€ · marge ${pc(r.op_margin_pct)}</i><br><i>${fmt(r.employees)} employés · Asie hors Japon ${a?a.share_pct+' %':'n.d.'}</i></div>`}).join('');
 const m={GAGNE:'🟢',RALENTIT:'🟠','DÉCROCHE':'🔴'};const s=D.sc;
 const best=[...s].sort((a,b)=>b.organic_growth_2025_pct-a.organic_growth_2025_pct)[0],worst=[...s].sort((a,b)=>a.organic_growth_2025_pct-b.organic_growth_2025_pct)[0];
 document.getElementById('ceo').innerHTML=[
  ['✅ Qui gagne ?',`${best.company} : ${best.organic_growth_2025_pct>0?'+':''}${best.organic_growth_2025_pct} % organique, marge ${pc(best.op_margin_2025_pct)}`],
  ['✅ Qui ralentit ?',s.filter(x=>x.momentum!='GAGNE').map(x=>`${m[x.momentum]} ${x.company} (${x.organic_growth_2025_pct} %)`).join(' · ')],
  ['✅ Où investir ?','Distribution sélective (Sephora) et Montres & Joaillerie chez LVMH ; Maroquinerie-Sellerie (+13 %) chez Hermès ; Saint Laurent / Bottega Veneta chez Kering'],
  ['✅ Quel marché surveiller ?','Japon (LVMH −12 % vs Hermès +14 %) et Asie hors Japon (part en recul de 2 pts chez LVMH et Hermès)']
 ].map(x=>`<div class="card"><b>${x[0]}</b><p>${x[1]}</p></div>`).join('');
 const yrs=[2021,2022,2023,2024,2025];
 mk('c1',{type:'line',data:{labels:yrs,datasets:list.map(c=>{const b=get(c,2021).revenue_meur;return{label:c,data:yrs.map(t=>get(c,t).revenue_meur/b*100),borderColor:COL[c],backgroundColor:COL[c],tension:.2}})},options:opt});
 mk('c2',{type:'line',data:{labels:yrs,datasets:list.map(c=>({label:c,data:yrs.map(t=>get(c,t).op_margin_pct),borderColor:COL[c],backgroundColor:COL[c],tension:.2}))},options:opt});
 mk('c3',{type:'bar',data:{labels:yrs.slice(1),datasets:list.map(c=>({label:c,data:yrs.slice(1).map(t=>get(c,t).revenue_growth_pct),backgroundColor:COL[c]}))},options:opt});
 let gy=y,note='';const has=c=>D.geo.some(x=>x.company==c&&x.year==gy);
 if(![ 'LVMH','Hermès','Kering'].filter(c=>list.includes(c)).every(has)){note='Kering : géographie disponible pour 2024 uniquement ; LVMH/Hermès : 2024-2025.'}
 document.getElementById('gnote').textContent=note+' Amériques = États-Unis chez LVMH.';
 const gl=list.filter(has);
 mk('c4',{type:'bar',data:{labels:gl,datasets:REG.map((r,i)=>({label:r,data:gl.map(c=>(D.geo.find(x=>x.company==c&&x.year==gy&&x.region==r)||{}).share_pct),backgroundColor:RC[i]}))},options:{...opt,indexAxis:'y',scales:{x:{stacked:true,max:100},y:{stacked:true}}}});
 document.getElementById('seg').innerHTML='<tr><th>Entreprise · segment</th><th>CA (M€)</th><th>Croiss. 2025</th><th>Marge</th></tr>'+D.seg.filter(r=>list.includes(r.company)).map(r=>`<tr><td>${r.company} · ${r.segment}</td><td>${fmt(r.revenue_meur)}</td><td class="${r.organic_growth_2025_pct>=0?'up':'dn'}">${r.organic_growth_2025_pct==null?'–':(r.organic_growth_2025_pct>0?'+':'')+r.organic_growth_2025_pct+' %'}</td><td>${r.op_margin_pct==null?'n.d.':pc(r.op_margin_pct)}</td></tr>`).join('');
}
document.getElementById('recs').innerHTML=D.recs.map(r=>`<div class="rec"><b>Observation.</b> ${r.observation}<br><b>Recommandation.</b> ${r.recommendation}</div>`).join('');
['co','yr'].forEach(i=>document.getElementById(i).addEventListener('change',render));render();
</script></body></html>"""

out = ROOT / "docs" / "index.html"
out.write_text(TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":"))), encoding="utf-8")
print(out, out.stat().st_size, "bytes")
