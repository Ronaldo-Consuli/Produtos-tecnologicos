"""Streamlit: tempos e movimentos do laboratório. Execute: streamlit run app.py."""
import hashlib
import html
import io
import json
import math
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

BASE = [{'bench': 'Etanol', 'activity': 'Coleta etanol', 'minutes': 15.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': '°GL vinhaça', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': '°GL flegamaça', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': 'pH etanol', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': 'Condutividade etanol', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': '°Inpm, massa, °GL etanol', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': 'Acidez etanol', 'minutes': 3.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': 'Análises cromatógraficas em etanol', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': 'Análise sensorial etanol em etanol', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Etanol', 'activity': 'Análise de Barbet em etanol', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Cor açúcar NIR', 'minutes': 1.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Pol açúcar NIR', 'minutes': 1.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Cinzas açúcar NIR', 'minutes': 1.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Umidade do açúcar NIR', 'minutes': 1.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Insoluvel açúcar NIR', 'minutes': 1.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Cor açúcar Conv.', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Pol açúcar Conv.', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Cinzas açúcar Conv.', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Umidade do açúcar Conv.', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Açúcar', 'activity': 'Insoluvel açúcar Conv.', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'ART mosto Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'Coleta fermentação', 'minutes': 15.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'pH do mosto Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'Acidez do mosto Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'ART Mosto NIR', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'pH do mosto NIR', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'Acidez do mosto NIR', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'Proteína levedura Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'pH da levedura Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Fermentação', 'activity': 'Umidade da levedura Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Caldo', 'activity': 'Análise de umidade de bagaço Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Caldo', 'activity': 'Análise de Pol de bagaço Conv.', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Caldo', 'activity': 'Brix mel/caldo', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Caldo', 'activity': 'Brix de Pol mel/caldo', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Caldo', 'activity': 'pH caldo', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Caldo', 'activity': 'Insoluvel caldo', 'minutes': 2.0, 'q': [1, 0, 0]}, {'bench': 'Caldo', 'activity': 'coleta de bagaço', 'minutes': 15.0, 'q': [1, 0, 0]}, {'bench': 'Águas', 'activity': 'Coleta de águas do processo', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Águas', 'activity': 'Coleta de águas de caldeiras', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Águas', 'activity': 'Analise de carboidratos em águas', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Águas', 'activity': 'Analise de DQO', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Águas', 'activity': 'Análise de DBO', 'minutes': 5.0, 'q': [1, 0, 0]}, {'bench': 'Microbiologia', 'activity': 'Viabilidade celular', 'minutes': 2.0, 'q': [0, 1, 0]}, {'bench': 'Microbiologia', 'activity': 'Contaminação bactérias', 'minutes': 2.0, 'q': [0, 1, 0]}, {'bench': 'Microbiologia', 'activity': 'Plaqueamento', 'minutes': 2.0, 'q': [0, 1, 0]}, {'bench': 'Microbiologia', 'activity': 'Coleta na fermentação', 'minutes': 2.0, 'q': [0, 1, 0]}, {'bench': 'Microbiologia', 'activity': 'Coleta na fabrica de levedura', 'minutes': 2.0, 'q': [0, 1, 0]}]
REPORT_TEMPLATE = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gestão das atividades do Laboratório Industrial</title><style>\n:root { --verde:#00983A; --azul:#004881; --navy:#143257; --vermelho:#C0392B; --muted:#6B7785; --fundo:#E9EDF1; --borda:#E0E5EA; }\n* { box-sizing:border-box; }\nbody { margin:0; padding:24px; background:var(--fundo); color:#2B3542; font-family:Arial,Helvetica,sans-serif; }\n.wrap { max-width:1500px; margin:0 auto; }\n.header { background:linear-gradient(118deg,var(--verde) 0%,var(--azul) 64%,#083050 100%); color:#fff; border-radius:12px; padding:24px 30px; }\n.header h1 { margin:0 0 8px; font-size:30px; }\n.meta { font-size:12px; opacity:.92; line-height:1.6; }\n.card { background:#fff; border:1px solid var(--borda); border-radius:10px; box-shadow:0 1px 2px rgba(12,34,64,.06); padding:16px; margin-top:16px; overflow:auto; }\nh2 { margin:0 0 4px; color:var(--navy); font-size:18px; }\n.note { color:var(--muted); font-size:12px; margin-bottom:12px; }\n.filtros-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin-top:12px; }\n.filtro label { display:block; color:#4B5868; font-size:12px; font-weight:700; margin-bottom:6px; }\n.filtro select { width:100%; height:42px; border:1px solid var(--borda); border-radius:7px; background:#fff; color:#2B3542; padding:0 10px; font-size:13px; }\n.kpis { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; margin:16px 0 10px; }\n.kpis-secundarios { width:60%; margin:0 auto 16px; display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }\n.kpi { background:#fff; border:1px solid var(--borda); border-radius:10px; box-shadow:0 1px 2px rgba(12,34,64,.06); padding:14px; text-align:center; }\n.kpi.titulo { min-height:96px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; }\n.kpi .label { color:var(--muted); font-size:12px; min-height:30px; }\n.kpi .value { color:var(--navy); font-size:21px; font-weight:700; margin-top:6px; }\n.kpi.titulo .label { min-height:0; color:#3E3E3E; font-size:13px; font-weight:600; }\n.kpi.titulo .value { color:var(--navy); margin-top:0; }\n.kpi.ok .value { color:#009A44; }\n.kpi.alerta .value { color:var(--vermelho); }\n.kpi.neutro .value { color:var(--muted); }\n#grafico { width:100%; min-height:455px; }\ntable { width:100%; border-collapse:collapse; font-size:12px; table-layout:fixed; }\nth { background:var(--navy); color:#fff; text-align:center; padding:9px 8px; position:sticky; top:0; z-index:2; }\ntd { border-bottom:1px solid #E8ECF0; padding:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; text-align:center; }\ntd.status { font-weight:700; }\ntd.dentro { color:#00702C; background:#E9F5EE; }\ntd.fora { color:var(--vermelho); background:#FDECEA; }\n.table-wrap { max-height:520px; overflow:auto; border:1px solid var(--borda); border-radius:8px; }\n@media (max-width:900px) {\n  body { padding:10px; }\n  .filtros-grid { grid-template-columns:1fr; }\n  .kpis { grid-template-columns:1fr 1fr; }\n  .kpis-secundarios { width:100%; grid-template-columns:1fr; }\n}\n\nsection {background:#fff;border:1px solid #E0E5EA;border-radius:10px;box-shadow:0 1px 2px rgba(12,34,64,.06);padding:16px;margin:16px 0}\n.viz-controls{display:flex;flex-wrap:wrap;gap:16px;align-items:end;margin:12px 0}.form-label{display:grid;gap:6px;flex:1 1 220px}.form-control{width:100%;min-width:0;padding:10px;border:1px solid #CBD5E1;border-radius:7px;font:inherit;background:white;color:#2B3542}\n.btn{padding:10px 16px;border:0;border-radius:7px;background:#004881;color:white;cursor:pointer;font:inherit}\n.text-small{font-size:12px;color:#596778;margin:8px 0}.text-destructive{color:#C0392B}.text-end{text-align:right}.table-responsive{overflow:auto}.table{table-layout:auto}.table th{background:#143257}.table td{white-space:normal}.table th,.table td{padding:10px}summary{cursor:pointer;color:#143257;font-weight:600;padding:8px 0}\n:root{--muted:#E9EDF1;--viz-series-1:#00983A}\n</style><style>\n.quantity-stepper{display:flex;align-items:center;gap:6px;min-width:0;width:100%}\n.quantity-stepper .btn{display:grid;place-items:center;min-width:44px;height:44px;padding:0;flex:0 0 44px;background:#F3F4F6;color:#143257;border:1px solid #CBD5E1;font-size:20px;touch-action:manipulation}\n.quantity-stepper input{flex:1 1 0;min-width:54px;width:100%;height:44px;text-align:center;font-size:16px;color:#143257;-webkit-text-fill-color:#143257;opacity:1}\n.table th{background:transparent;color:#2B3542;font-weight:400;text-align:left;position:static}\n.table th,.table td{border-bottom:1px solid #E0E5EA;padding:8px;font-size:13px}\n#lab-three .lt-fill{background:#087E91}\n#lab-three .lt-row{grid-template-columns:minmax(0,1fr) 65px 190px}\n@media(max-width:700px){#lab-three .lt-row{grid-template-columns:minmax(0,1fr) minmax(156px,190px);gap:6px 10px;padding:8px 0}#lab-three .lt-row>span:first-child{grid-column:1/-1;font-size:14px;font-weight:600;overflow-wrap:anywhere}#lab-three .lt-row>span:nth-child(2){grid-column:1}#lab-three .lt-row>.quantity-stepper{grid-column:2}}\n</style></head><body><main class="wrap"><div id="lab-three">\n<div class="header"><h1>Gestão das atividades do Laboratório Industrial</h1></div>\n\n\n\n<div id="lt-error" role="alert" class="text-destructive"></div>\n<div id="lt-cards" class="shift-cards" aria-live="polite"></div>\n<div id="lt-turns"></div>\n<details><summary>Base de tempos por atividade</summary><div class="table-responsive"><table class="table table-sm"><thead><tr><th>Bancada</th><th>Atividade</th><th>Tempo efetivo (min)</th></tr></thead><tbody id="lt-data"></tbody></table></div></details>\n</div>\n<style>\n#lab-three section {margin:24px 0}\n#lab-three .lt-lanes {display:grid;gap:12px;margin:12px 0}\n#lab-three .lt-track {height:24px;display:flex;background:#DFE8F0;border-radius:8px;overflow:hidden}\n#lab-three .lt-fill {height:100%;background:#087E91;border-radius:8px}\n#lab-three .lt-label {display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}\n#lab-three .lt-row {display:grid;grid-template-columns:minmax(100px,1fr) 70px 150px;gap:8px;align-items:center;margin:8px 0}\n#lab-three details {margin:12px 0}\n#lab-three .shift-cards{width:100%;margin:16px 0 20px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}\n#lab-three .shift-card{min-height:116px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:#fff;border:1px solid #E0E5EA;border-radius:10px;box-shadow:0 1px 2px rgba(12,34,64,.06);padding:14px;text-align:center}\n#lab-three .shift-card .label{color:#3E3E3E;font-size:13px;font-weight:600}\n#lab-three .shift-card .value{color:#143257;font-size:34px;font-weight:700;line-height:1.2}\n#lab-three .shift-card.alerta .value{color:#C0392B}\n#lab-three .shift-card .note{color:#6B7785;font-size:12px;line-height:1.4;margin:0}\n@media(max-width:700px){#lab-three .shift-cards{grid-template-columns:1fr}}\n</style>\n\n<script>\n(()=>{\nconst root=document.getElementById(\'lab-three\'),get=id=>root.querySelector(\'#lt-\'+id);\nlet rows=__DATA_TOKEN__;\nconst turnNames=[\'A\',\'B\',\'C\'];\nconst shiftTimes=[[\'00:00\',\'03:00\',\'04:00\',\'07:00\'],[\'07:00\',\'12:00\',\'13:00\',\'16:48\'],[\'15:40\',\'19:00\',\'20:00\',\'23:50\']];\nconst benchNames=[\'Etanol\',\'Açúcar\',\'Fermentação\',\'Caldo\',\'Águas\',\'Microbiologia\'];\nconst benchKeys={etanol:0,acucar:1,fermentacao:2,caldo:3,caldos:3,agua:4,aguas:4,micro:5,microbiologia:5};\nfunction benchIndex(name){const key=String(name).trim().toLowerCase().normalize(\'NFD\').replace(/[\\u0300-\\u036f]/g,\'\');return benchKeys[key]??-1;}\n\nconst settings=__CONFIG_TOKEN__,views=[];\nconst number=v=>typeof v===\'number\'?v:Number(String(v).trim().replace(\',\',\'.\'));\nconst fmt=v=>new Intl.NumberFormat(\'pt-BR\',{maximumFractionDigits:2}).format(v);\nconst time=v=>fmt(v)+\' min\';\nfunction element(tag,text,cls){const d=document.createElement(tag);if(text!==undefined)d.textContent=text;if(cls)d.className=cls;return d;}\nfunction stepper(input){\n const wrap=element(\'div\',undefined,\'quantity-stepper\');\n const minus=element(\'button\',\'−\',\'btn\'),plus=element(\'button\',\'+\',\'btn\');\n minus.type=plus.type=\'button\';minus.setAttribute(\'aria-label\',\'Diminuir quantidade\');plus.setAttribute(\'aria-label\',\'Aumentar quantidade\');\n for(const [button,delta] of [[minus,-1],[plus,1]])button.addEventListener(\'click\',()=>{const current=Number(input.value),base=Number.isInteger(current)?current:0;input.value=Math.max(Number(input.min||0),Math.min(Number(input.max||10000),base+delta));input.dispatchEvent(new Event(\'input\',{bubbles:true}));});\n wrap.append(minus,input,plus);return wrap;\n}\nfunction field(parent,label,value,min,max,step,onchange){const l=element(\'label\',label,\'form-label\'),i=element(\'input\',undefined,\'form-control\');i.type=\'text\';i.inputMode=\'numeric\';i.pattern=\'[0-9]*\';i.autocomplete=\'off\';i.value=value;i.min=min;i.max=max;i.step=step;i.addEventListener(\'input\',()=>onchange(/^\\d+$/.test(i.value)?Number(i.value):NaN));l.append(label.startsWith(\'Quantidade\')?stepper(i):i);parent.append(l);return i;}\nfunction calculate(data,settings,k){const cap=Math.round((settings.hours*60-settings.other)*1e6)/1e6,total=data.reduce((s,r)=>s+r.minutes*r.q[k],0),count=data.reduce((s,r)=>s+r.q[k],0);const loads=Array(6).fill(0),counts=Array(6).fill(0),demands=Array(6).fill(0);let done=0,used=0,unknown=false;const pending=[];\n const ordered=data.map((r,index)=>({...r,index})).sort((a,b)=>b.minutes-a.minutes);\n for(const r of ordered){let remaining=r.q[k];const idx=benchIndex(r.bench);if(idx>=0)demands[idx]+=r.minutes*remaining;else if(remaining)unknown=true;\n const assigned=idx>=0;\n if(assigned){const fitting=Math.max(0,Math.floor((cap-loads[idx]+1e-8)/r.minutes));const completed=Math.min(remaining,fitting);loads[idx]+=completed*r.minutes;counts[idx]+=completed;used+=completed*r.minutes;done+=completed;remaining-=completed;}\n if(remaining)pending.push({name:r.activity,bench:r.bench,q:remaining,time:remaining*r.minutes,reason:idx<0?\'Bancada sem vínculo\':\'Capacidade da bancada esgotada\'});}\n return {cap,total,count,loads,counts,demands,done,used,pending,needed:unknown?\'Bancada sem vínculo\':demands.reduce((s,v)=>s+Math.ceil(v/cap-1e-10),0)};}\nfunction isValid(k){const s=settings[k];return Number.isInteger(s.people)&&s.people>=0&&s.people<=30&&Number.isFinite(s.hours)&&s.hours>0&&s.hours<=24&&Number.isFinite(s.other)&&s.other>=0&&s.other<s.hours*60&&rows.every(r=>Number.isInteger(r.q[k])&&r.q[k]>=0&&r.q[k]<=10000);}\nfunction update(){get(\'cards\').replaceChildren();settings.forEach((s,k)=>{const v=views[k];if(!isValid(k)){v.error.textContent=\'Revise equipe, jornada e quantidades. Outras atividades devem ocupar menos que o turno.\';v.result.textContent=\'Cálculo indisponível\';v.lanes.replaceChildren();v.pending.replaceChildren();return;}v.error.textContent=\'\';const r=calculate(rows,s,k);\n const capacity=r.cap*s.people,percent=100*r.total/capacity;\n const card=element(\'div\',undefined,\'shift-card\');if(percent>100)card.classList.add(\'alerta\');card.append(element(\'div\',\'Turno \'+turnNames[k]+\' · Carga / capacidade\',\'label\'),element(\'div\',fmt(percent)+\'%\',\'value\'),element(\'div\',\'Carga programada \'+time(r.total)+\' · Capacidade \'+time(capacity),\'note\'));get(\'cards\').append(card);\n v.result.replaceChildren();const t=element(\'table\',undefined,\'table table-sm\');const b=element(\'tbody\');[\n [\'Carga programada\',time(r.total)],[\'Capacidade da equipe\',time(r.cap*s.people)],[\'Carga / capacidade\',s.people?fmt(100*r.total/(r.cap*s.people))+\'%\':r.total?\'Sem equipe\':\'Sem demanda\']\n ].forEach(([label,val])=>{const tr=element(\'tr\');tr.append(element(\'th\',label),element(\'td\',val,\'text-end tabular-nums\'));b.append(tr);});t.append(b);v.result.append(t);\n v.lanes.replaceChildren();r.loads.forEach((load,i)=>{const line=element(\'div\');const head=element(\'div\',undefined,\'lt-label text-small\');head.append(element(\'span\',\'Bancada \'+benchNames[i]),element(\'span\',time(r.demands[i])+\' programados · Capacidade \'+time(r.cap)));const track=element(\'div\',undefined,\'lt-track\');track.setAttribute(\'role\',\'img\');track.setAttribute(\'aria-label\',\'Bancada \'+benchNames[i]+\': \'+time(r.demands[i])+\' programados; Capacidade \'+time(r.cap));const fill=element(\'div\',undefined,\'lt-fill\');fill.style.width=Math.min(100,100*r.demands[i]/r.cap)+\'%\';track.append(fill);line.append(head,track);v.lanes.append(line);});\n v.pending.replaceChildren();\n });}\nfunction build(){get(\'turns\').replaceChildren();views.length=0;settings.forEach((s,k)=>{const section=element(\'section\');section.append(element(\'h3\',\'Turno \'+turnNames[k]));const controls=element(\'div\',undefined,\'viz-controls\');\n const [start,breakStart,breakEnd,end]=shiftTimes[k],effective=Math.round(s.hours*60),duration=String(Math.floor(effective/60)).padStart(2,\'0\')+\':\'+String(effective%60).padStart(2,\'0\');\n section.append(element(\'div\',\'Trabalho: \'+start+\'–\'+breakStart+\' e \'+breakEnd+\'–\'+end+\' | Descanso: \'+breakStart+\'–\'+breakEnd+\' | Jornada efetiva: \'+duration+\' (\'+time(effective)+\')\',\'text-small\'));\n const teamLabel=element(\'label\',\'Quantidade de analistas\',\'form-label\'),teamSelect=element(\'select\',undefined,\'form-control\');\n for(let n=1;n<=(k===1?6:5);n++){const option=element(\'option\',String(n));option.value=n;option.selected=n===s.people;teamSelect.append(option);}\n teamSelect.addEventListener(\'change\',()=>{s.people=Number(teamSelect.value);update();});teamLabel.append(teamSelect);controls.append(teamLabel);section.append(controls);\n const error=element(\'div\',undefined,\'text-destructive\');error.setAttribute(\'role\',\'alert\');const result=element(\'div\');result.setAttribute(\'aria-live\',\'polite\');const lanes=element(\'div\',undefined,\'lt-lanes\'),pending=element(\'div\');section.append(error,result,lanes,pending);\n const editor=element(\'details\');editor.append(element(\'summary\',\'Quantidades por atividade — Turno \'+turnNames[k]));editor.append(element(\'div\',\'Toque no número para editar pelo teclado ou use os botões − e +. Se recebeu o arquivo por mensagem, abra-o no navegador para editar.\',\'text-small\'));\n const bulk=element(\'div\',undefined,\'viz-controls\');let qty=1;const quantity=field(bulk,\'Quantidade para todas as atividades\',1,0,10000,1,v=>qty=v);const button=element(\'button\',\'Aplicar a este turno\',\'btn\');button.type=\'button\';const inputs=[];button.addEventListener(\'click\',()=>{if(!Number.isInteger(qty)||qty<0||qty>10000){quantity.reportValidity();return;}rows.forEach((r,i)=>{r.q[k]=qty;inputs[i].value=qty;});update();});bulk.append(button);editor.append(bulk);\n let bench=\'\';rows.forEach((r,index)=>{if(r.bench!==bench){bench=r.bench;editor.append(element(\'h3\',bench));}const line=element(\'div\',undefined,\'lt-row\');line.append(element(\'span\',r.activity),element(\'span\',time(r.minutes),\'text-small\'));const input=element(\'input\',undefined,\'form-control\');input.type=\'text\';input.inputMode=\'numeric\';input.pattern=\'[0-9]*\';input.autocomplete=\'off\';input.value=r.q[k];input.min=0;input.max=10000;input.step=1;input.setAttribute(\'aria-label\',r.bench+\' \'+r.activity+\' quantidade no Turno \'+turnNames[k]);input.addEventListener(\'input\',()=>{r.q[k]=/^\\d+$/.test(input.value)?Number(input.value):NaN;update();});inputs.push(input);line.append(stepper(input));editor.append(line);});section.append(editor);get(\'turns\').append(section);views.push({error,result,lanes,pending});});\n get(\'data\').replaceChildren();rows.forEach(r=>{const tr=element(\'tr\');tr.append(element(\'td\',r.bench),element(\'td\',r.activity),element(\'td\',fmt(r.minutes),\'text-end\'));get(\'data\').append(tr);});update();}\nfunction parseWorkbook(book){const sheet=book.Sheets[book.SheetNames[0]],matrix=XLSX.utils.sheet_to_json(sheet,{header:1,defval:null,raw:true});const normalize=x=>String(x??\'\').trim().toLowerCase().normalize(\'NFD\').replace(/[\\u0300-\\u036f]/g,\'\');const h=matrix[0]?.map(normalize)||[];const a=h.indexOf(\'bancada\'),b=h.indexOf(\'atividade\'),c=h.findIndex(x=>x.startsWith(\'tempo efetivo\'));if([a,b,c].some(x=>x<0))throw Error(\'A primeira aba deve ter as colunas Bancada, Atividade e Tempo efetivo (min.).\');\n const data=[];matrix.slice(1).forEach((row,i)=>{if(row.every(x=>x===null||String(x).trim()===\'\'))return;const bench=String(row[a]??\'\').trim(),activity=String(row[b]??\'\').trim(),minutes=number(row[c]);if(!bench||!activity||row[c]===null||!Number.isFinite(minutes)||minutes<=0)throw Error(\'Linha \'+(i+2)+\': preencha bancada, atividade e tempo positivo em minutos.\');data.push({bench,activity,minutes,q:benchIndex(bench)===5?[0,1,0]:[1,0,0]});});if(!data.length)throw Error(\'A planilha não contém atividades.\');if(data.length>2000)throw Error(\'Use uma base com até 2.000 atividades.\');return data;}\nbuild();\n})();\n</script></main></body></html>'
CSS = '\n.stApp {background:#E9EDF1;color:#2B3542;font-family:Arial,Helvetica,sans-serif}\n.block-container {max-width:1500px;padding-top:2rem}\n.lab-header {background:linear-gradient(118deg,#00983A 0%,#004881 64%,#083050 100%);color:white;border-radius:12px;padding:24px 30px;margin-bottom:18px}\n.lab-header h1 {color:white;font-size:30px;margin:0 0 8px;padding:0}\nh2,h3 {color:#143257}\n[data-testid="stVerticalBlockBorderWrapper"] {background:white;border:1px solid #E0E5EA;border-radius:10px;box-shadow:0 1px 2px rgba(12,34,64,.06)}\n[data-testid="stMetric"] {background:white;border:1px solid #E0E5EA;border-radius:10px;padding:14px}\n[data-testid="stMetricLabel"] {color:#6B7785}\n[data-testid="stMetricValue"] {color:#143257}\n[data-testid="stFileUploader"] {background:white;border-radius:10px;padding:12px}\n.stDownloadButton button {background:#004881;color:white;border-radius:7px}\n'
BENCHES = ["Etanol", "Açúcar", "Fermentação", "Caldo", "Águas", "Microbiologia"]
TEAMS = {"A": 5, "B": 6, "C": 5}
SHIFT_TIMES = {
    "A": ("00:00", "03:00", "04:00", "07:00"),
    "B": ("07:00", "12:00", "13:00", "16:48"),
    "C": ("15:40", "19:00", "20:00", "23:50"),
}


def shift_minutes(start, end):
    start_hour, start_minute = map(int, start.split(":"))
    end_hour, end_minute = map(int, end.split(":"))
    return ((end_hour * 60 + end_minute) - (start_hour * 60 + start_minute)) % 1440


def effective_shift_minutes(schedule):
    start, break_start, break_end, end = schedule
    return shift_minutes(start, break_start) + shift_minutes(break_end, end)


def duration_label(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"



def normalize(value):
    return "".join(c for c in unicodedata.normalize("NFD", str(value).strip().lower())
                   if unicodedata.category(c) != "Mn")


def bench_index(value):
    return {"etanol": 0, "acucar": 1, "fermentacao": 2, "caldo": 3,
            "caldos": 3, "agua": 4, "aguas": 4, "micro": 5,
            "microbiologia": 5}.get(normalize(value), -1)


def import_excel(data, sheet):
    """Read only: retain supplied times and reject incomplete/invalid records."""
    frame = pd.read_excel(io.BytesIO(data), sheet_name=sheet, engine="openpyxl").dropna(how="all")
    names = {normalize(c): c for c in frame.columns}
    time_cols = [c for c in frame.columns if normalize(c).startswith("tempo efetivo")]
    if "bancada" not in names or "atividade" not in names or len(time_cols) != 1:
        raise ValueError("Use as colunas Bancada, Atividade e Tempo efetivo (min.).")
    if not 0 < len(frame) <= 2000:
        raise ValueError("A base deve conter entre 1 e 2.000 atividades.")
    result = []
    for offset, (_, row) in enumerate(frame.iterrows(), 2):
        bench, activity, raw = row[names["bancada"]], row[names["atividade"]], row[time_cols[0]]
        if pd.isna(bench) or pd.isna(activity) or not str(bench).strip() or not str(activity).strip():
            raise ValueError(f"Linha {offset}: bancada ou atividade em branco.")
        try:
            minutes = float(str(raw).strip().replace(",", "."))
        except (ValueError, TypeError):
            raise ValueError(f"Linha {offset}: tempo inválido em minutos.") from None
        if not math.isfinite(minutes) or minutes <= 0:
            raise ValueError(f"Linha {offset}: informe tempo positivo em minutos.")
        idx = bench_index(bench)
        result.append({"bench": str(bench).strip(), "activity": str(activity).strip(),
                       "minutes": minutes, "q": [0, 1, 0] if idx == 5 else [1, 0, 0]})
    return result


def simulate(rows, people, hours, other, shift):
    cap = round(hours * 60 - other, 6)
    if cap <= 0:
        raise ValueError("Outras atividades devem ocupar menos que a jornada.")
    loads, demands = [0.0] * len(BENCHES), [0.0] * len(BENCHES)
    count = done = 0
    total = 0.0
    pending = []
    unknown = False
    for row in sorted(rows, key=lambda r: -r["minutes"]):
        q = row["q"][shift]
        if not isinstance(q, (int, float)) or not math.isfinite(q) or q < 0 or q != int(q):
            raise ValueError("As quantidades devem ser inteiras e não negativas.")
        q = int(q)
        minutes = row["minutes"]
        idx = bench_index(row["bench"])
        count += q
        total += minutes * q
        if idx >= 0:
            demands[idx] += minutes * q
        elif q:
            unknown = True
        completed = 0
        if idx >= 0:
            completed = min(q, max(0, math.floor((cap - loads[idx] + 1e-8) / minutes)))
            loads[idx] += completed * minutes
        done += completed
        if completed < q:
            reason = "Bancada sem vínculo" if idx < 0 else "Capacidade da bancada esgotada"
            pending.append({"Bancada": row["bench"], "Atividade": row["activity"],
                            "Quantidade pendente": q - completed,
                            "Tempo pendente (min)": (q - completed) * minutes, "Motivo": reason})
    return dict(cap=cap, loads=loads, demands=demands, total=total, count=count, done=done,
                pending=pending, pending_minutes=max(0, total - sum(loads)),
                needed=None if unknown else sum(math.ceil(d / cap - 1e-10) for d in demands))


def json_safe(data):
    return json.dumps(data, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def make_report(rows, configs, source, stamp):
    # Replace the source last, so user-supplied labels cannot become template tokens.
    return REPORT_TEMPLATE.replace("__DATA_TOKEN__", json_safe(rows)).replace(
        "__CONFIG_TOKEN__", json_safe(configs)).replace("__STAMP_TOKEN__", html.escape(stamp)).replace(
        "__SOURCE_TOKEN__", html.escape(source))


def main():
    import streamlit as st
    st.set_page_config(page_title="Gestão das atividades do Laboratório Industrial", layout="wide", initial_sidebar_state="expanded")
    st.markdown("<style>" + CSS + """
        .turn-summary{width:100%;border-collapse:collapse;margin:12px 0}
        .turn-summary td{border-bottom:1px solid #E0E5EA;padding:8px;font-size:14px}
        .turn-summary td:last-child{text-align:right}
        .bench-track{height:24px;background:#DFE8F0;border-radius:8px;overflow:hidden;margin:4px 0 14px}
        .bench-fill{height:100%;background:#087E91;border-radius:8px}
        .shift-cards{width:100%;margin:16px 0 20px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
        .shift-card{min-height:116px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:#fff;border:1px solid #E0E5EA;border-radius:10px;box-shadow:0 1px 2px rgba(12,34,64,.06);padding:14px;text-align:center}
        .shift-card .label{color:#3E3E3E;font-size:13px;font-weight:600}
        .shift-card .value{color:#143257;font-size:34px;font-weight:700;line-height:1.2}
        .shift-card.alerta .value{color:#C0392B}
        .shift-card .note{color:#6B7785;font-size:12px;line-height:1.4}
        @media(max-width:700px){.shift-cards{grid-template-columns:1fr}}
        </style>""", unsafe_allow_html=True)
    st.markdown('<div class="lab-header"><h1>Gestão das atividades do Laboratório Industrial</h1></div>', unsafe_allow_html=True)
    upload = st.sidebar.file_uploader("Planilha Excel", type=["xlsx"])
    source = "Tempos e movimentos mestrado(1).xlsx — base incorporada"
    records = json.loads(json.dumps(BASE))
    digest = "base-47"
    if upload is not None:
        data = upload.getvalue()
        if len(data) > 10 * 1024 * 1024:
            st.error("Use um arquivo de até 10 MB.")
            st.stop()
        try:
            sheets = pd.ExcelFile(io.BytesIO(data), engine="openpyxl").sheet_names
            sheet = sheets[0]  # A primeira aba é utilizada automaticamente.
            records = import_excel(data, sheet)
            source = f"{upload.name} · {sheet}"
            digest = hashlib.sha256(data + sheet.encode()).hexdigest()
        except Exception as exc:
            st.error(f"Não foi possível importar a planilha: {exc}")
            st.stop()
    if st.session_state.get("base_digest") != digest:
        st.session_state.base_digest = digest
        st.session_state.loaded_at = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")
    unmatched = sorted({r["bench"] for r in records if bench_index(r["bench"]) < 0})
    if unmatched:
        st.warning("Bancadas sem analista vinculado: " + ", ".join(unmatched))
    cards_slot = st.empty()
    configs, summaries = [], []
    for k, (turn, default_people) in enumerate(TEAMS.items()):
        with st.container(border=True):
            st.subheader(f"Turno {turn}")
            start_time, break_start, break_end, end_time = SHIFT_TIMES[turn]
            minutes = effective_shift_minutes(SHIFT_TIMES[turn])
            hours = minutes / 60
            st.caption(
                f"Trabalho: {start_time}–{break_start} e {break_end}–{end_time} | "
                f"Descanso: {break_start}–{break_end} | "
                f"Jornada efetiva: {duration_label(minutes)} ({minutes} min)"
            )
            people = st.selectbox("Quantidade de analistas", options=list(range(1, 7 if turn == "B" else 6)),
                                  index=default_people - 1, key=f"people_{turn}")
            other = 0
            for i, row in enumerate(records):
                quantity_key = f"qty_{digest}_{turn}_{i}"
                if quantity_key not in st.session_state:
                    st.session_state[quantity_key] = row["q"][k]
                row["q"][k] = st.session_state[quantity_key]
            result = simulate(records, people, hours, other, k)
            configs.append({"people": people, "hours": hours, "other": other})
            summaries.append(result)
            capacity = people * result["cap"]
            st.markdown(
                '<table class="turn-summary">'
                f'<tr><td>Carga programada</td><td>{result["total"]:g} min</td></tr>'
                f'<tr><td>Capacidade da equipe</td><td>{capacity:g} min</td></tr>'
                f'<tr><td>Carga / capacidade</td><td>{100 * result["total"] / capacity:.2f}%</td></tr>'
                '</table>', unsafe_allow_html=True)
            for i, load in enumerate(result["loads"]):
                demand = result["demands"][i]
                st.caption(f'Bancada {BENCHES[i]}')
                ratio = min(100, 100 * demand / result["cap"])
                st.markdown(
                    f'<div>{demand:g} min programados · Capacidade {result["cap"]:g} min</div>'
                    f'<div class="bench-track" role="img" aria-label="Bancada {BENCHES[i]}: '
                    f'{demand:g} min programados; Capacidade {result["cap"]:g} min">'
                    f'<div class="bench-fill" style="width:{ratio:.2f}%"></div></div>',
                    unsafe_allow_html=True,
                )
            with st.expander(f"Quantidades por atividade — Turno {turn}"):
                st.caption("Use os botões − e + para escolher a quantidade sem digitar.")
                bulk_key = f"bulk_{digest}_{turn}"
                st.number_input("Quantidade para todas as atividades", min_value=0, max_value=10000,
                                value=1, step=1, key=bulk_key)
                def apply_all(current_turn=turn, current_digest=digest, size=len(records), key=bulk_key):
                    for row_index in range(size):
                        st.session_state[f"qty_{current_digest}_{current_turn}_{row_index}"] = st.session_state[key]
                st.button("Aplicar a este turno", key=f"apply_{turn}", on_click=apply_all)
                bench = None
                for i, row in enumerate(records):
                    if row["bench"] != bench:
                        bench = row["bench"]
                        st.markdown(f"**{html.escape(bench)}**")
                    label_col, time_col, qty_col = st.columns([5, 1, 2])
                    label_col.write(row["activity"])
                    time_col.write(f'{row["minutes"]:g} min')
                    qty_col.number_input(f'Quantidade — {row["activity"]} — Turno {turn}',
                                         min_value=0, max_value=10000, step=1,
                                         key=f"qty_{digest}_{turn}_{i}", label_visibility="collapsed")
    cards = ['<div class="shift-cards">']
    for turn, result, config in zip(TEAMS, summaries, configs):
        capacity = result["cap"] * config["people"]
        percentage = 100 * result["total"] / capacity
        cards.append(
            f'<div class="shift-card{" alerta" if percentage > 100 else ""}"><div class="label">Turno {turn} · Carga / capacidade</div>'
            f'<div class="value">{percentage:.1f}%</div>'
            f'<div class="note">Carga programada {result["total"]:g} min · Capacidade {capacity:g} min</div></div>'
        )
    cards_slot.markdown(''.join(cards) + '</div>', unsafe_allow_html=True)
    export = make_report(records, configs, source, datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S"))
    st.download_button("Gerar e baixar HTML interativo", data=export.encode("utf-8"),
                       file_name="tempos_movimentos_laboratorio.html", mime="text/html", type="primary")
    st.caption("O HTML inclui as quantidades e jornadas atuais e pode ser aberto sem internet. "
               "Para importar outra planilha, utilize este aplicativo.")
    with st.expander("Base de tempos importada"):
        st.dataframe(pd.DataFrame([{"Bancada": r["bench"], "Atividade": r["activity"], "Tempo efetivo (min)": r["minutes"]} for r in records]), hide_index=True, width="stretch")


if __name__ == "__main__":
    main()
