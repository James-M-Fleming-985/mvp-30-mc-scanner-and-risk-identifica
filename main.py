"""Auto-generated FastAPI wrapper for layer_mvp_0030 with HTML dashboard."""
import re
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from src.layer_mvp_0030 import RegulatoryEvent, DataSource, APIDataSource, RSSDataSource, HTMLScrapingDataSource

app = FastAPI(
    title="Regulatory Intelligence Risk Scanner",
    description="Auto-generated MVP API with dashboard",
    version="1.0.0",
)

DASHBOARD_HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Regulatory Intelligence Risk Scanner</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}header{background:linear-gradient(135deg,#1e293b,#334155);padding:2rem;border-bottom:2px solid #3b82f6}header h1{font-size:1.8rem;color:#fff}header p{color:#94a3b8;margin-top:0.3rem}.status-bar{display:flex;gap:1rem;margin-top:1rem;flex-wrap:wrap}.badge{padding:0.3rem 0.8rem;border-radius:9999px;font-size:0.75rem;font-weight:600}.badge.live{background:#065f46;color:#6ee7b7}.badge.api{background:#1e3a5f;color:#7dd3fc}.badge.score{background:#4c1d95;color:#c4b5fd}.badge.market{background:#78350f;color:#fde68a}.badge.trend{background:#064e3b;color:#6ee7b7}.badge.searches{background:#1e3a5f;color:#7dd3fc}.badge.competition{background:#7f1d1d;color:#fca5a5}.badge.viability{background:#14532d;color:#86efac}.hero{background:#1e293b;border-bottom:1px solid #334155;padding:2rem}.hero-subtitle{color:#f1f5f9;font-size:1.15rem;font-weight:500;margin-bottom:0.5rem}.hero-desc{color:#94a3b8;line-height:1.6;max-width:800px;margin-bottom:1rem}.stats-row{display:flex;gap:0.75rem;flex-wrap:wrap;margin-bottom:1rem}.features{margin-top:0.5rem}.features h3{color:#f1f5f9;font-size:1rem;margin-bottom:0.5rem}.features ul{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:0.4rem}.features li{color:#cbd5e1;font-size:0.9rem;padding-left:1.2rem;position:relative}.features li::before{content:"\2713";position:absolute;left:0;color:#6ee7b7}.container{max-width:1200px;margin:0 auto;padding:2rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:1.5rem}.card{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.5rem;transition:border-color 0.2s}.card:hover{border-color:#3b82f6}.card h3{color:#f1f5f9;margin-bottom:0.5rem;font-size:1.1rem}.endpoint{margin-bottom:1rem}.endpoint code{background:#0f172a;padding:0.3rem 0.6rem;border-radius:6px;font-size:0.8rem;color:#7dd3fc}.result{background:#0f172a;border-radius:8px;padding:1rem;font-size:0.85rem;max-height:300px;overflow-y:auto;line-height:1.5}.result pre{white-space:pre-wrap;word-break:break-word}.loading{color:#94a3b8}.error{color:#fca5a5}.ok{color:#6ee7b7}.key{color:#7dd3fc}.str{color:#fde68a}.num{color:#c4b5fd}footer{text-align:center;padding:2rem;color:#475569;font-size:0.8rem}</style></head><body><header><h1>Regulatory Intelligence Risk Scanner</h1><p>Auto-generated MVP — layer_mvp_0030</p><div class="status-bar"><span class="badge live">LIVE</span><span class="badge api">3 endpoints</span></div></header><section class="hero"><p class="hero-subtitle">Platform for detecting, classifying, and prioritizing materials compliance regulatory changes</p><p class="hero-desc">An application that takes data from various material compliance data sources to identify changes in material compliance policy and regulation and classifies associated risks</p><div class="stats-row"><span class="badge score">Opportunity: 50/100</span><span class="badge market">Manufacture</span><span class="badge viability">Viability: 50/100</span></div><div class="features"><h3>Features</h3><ul><li>System must ingest regulatory data from multiple sources including APIs, RSS feeds, and HTML scraping</li><li>System must convert raw regulatory signals into structured events with risk scoring</li><li>Dashboard must display regulatory event feed with filtering and risk visualization</li><li>System must provide modular framework supporting UK REACH with expansion capability</li></ul></div></section><div class="container"><div class="grid"><div class="card" id="card-regulatoryevent"><h3>\1egulatory \1vent</h3><div class="endpoint"><code>GET /api/regulatoryevent</code></div><div class="result" id="result-regulatoryevent"><span class="loading">Loading...</span></div></div>\n<div class="card" id="card-datasource"><h3>\1ata \1ource</h3><div class="endpoint"><code>GET /api/datasource</code></div><div class="result" id="result-datasource"><span class="loading">Loading...</span></div></div>\n<div class="card" id="card-apidatasource"><h3>\1 \1 \1 \1ata \1ource</h3><div class="endpoint"><code>GET /api/apidatasource</code></div><div class="result" id="result-apidatasource"><span class="loading">Loading...</span></div></div>\n</div></div><footer>Built by Causal Affect MVP Pipeline</footer><script>function renderResult(d){if(d.status==="error")return"<span class=error>Error: "+d.error+"</span>";return"<pre>"+syntaxHL(JSON.stringify(d,null,2))+"</pre>"}function syntaxHL(j){return j.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"([^"]+)":/g,"<span class=key>$1</span>:").replace(/: "([^"]*)"/g,": <span class=str>$1</span>").replace(/: (\\d+\\.?\\d*)/g,": <span class=num>$1</span>")}if(!sessionStorage.getItem("_ca_b")){fetch("https://businessventures-production.up.railway.app/api/dashboard/mvp-beacon/30",{method:"POST",mode:"no-cors",headers:{"Content-Type":"application/json"},body:JSON.stringify({r:document.referrer})}).catch(function(){});sessionStorage.setItem("_ca_b","1")}fetch("/api/regulatoryevent").then(r=>r.json()).then(d=>{document.getElementById("result-regulatoryevent").innerHTML=renderResult(d)}).catch(e=>{document.getElementById("result-regulatoryevent").innerHTML="<span class=error>"+e+"</span>"});\nfetch("/api/datasource").then(r=>r.json()).then(d=>{document.getElementById("result-datasource").innerHTML=renderResult(d)}).catch(e=>{document.getElementById("result-datasource").innerHTML="<span class=error>"+e+"</span>"});\nfetch("/api/apidatasource").then(r=>r.json()).then(d=>{document.getElementById("result-apidatasource").innerHTML=renderResult(d)}).catch(e=>{document.getElementById("result-apidatasource").innerHTML="<span class=error>"+e+"</span>"});\n</script></body></html>"""

@app.get("/", response_class=HTMLResponse)
def dashboard():
    """Interactive HTML dashboard."""
    return DASHBOARD_HTML

@app.get("/api/status")
def api_status():
    return {"service": "layer_mvp_0030", "status": "running", "version": "1.0.0", "endpoints": ['/api/regulatoryevent', '/api/datasource', '/api/apidatasource']}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/regulatoryevent")
def get_regulatoryevent():
    """Auto-generated endpoint for RegulatoryEvent."""
    try:
        instance = RegulatoryEvent()
        # Try common method names
        for method in ["analyze", "run", "execute", "get_data", "process", "calculate", "evaluate"]:
            if hasattr(instance, method):
                result = getattr(instance, method)()
                return {"status": "ok", "class": "RegulatoryEvent", "method": method, "result": str(result)[:1000]}
        return {"status": "ok", "class": "RegulatoryEvent", "message": "Instance created successfully"}
    except Exception as e:
        return {"status": "error", "class": "RegulatoryEvent", "error": str(e)}


@app.get("/api/datasource")
def get_datasource():
    """Auto-generated endpoint for DataSource."""
    try:
        instance = DataSource()
        # Try common method names
        for method in ["analyze", "run", "execute", "get_data", "process", "calculate", "evaluate"]:
            if hasattr(instance, method):
                result = getattr(instance, method)()
                return {"status": "ok", "class": "DataSource", "method": method, "result": str(result)[:1000]}
        return {"status": "ok", "class": "DataSource", "message": "Instance created successfully"}
    except Exception as e:
        return {"status": "error", "class": "DataSource", "error": str(e)}


@app.get("/api/apidatasource")
def get_apidatasource():
    """Auto-generated endpoint for APIDataSource."""
    try:
        instance = APIDataSource()
        # Try common method names
        for method in ["analyze", "run", "execute", "get_data", "process", "calculate", "evaluate"]:
            if hasattr(instance, method):
                result = getattr(instance, method)()
                return {"status": "ok", "class": "APIDataSource", "method": method, "result": str(result)[:1000]}
        return {"status": "ok", "class": "APIDataSource", "message": "Instance created successfully"}
    except Exception as e:
        return {"status": "error", "class": "APIDataSource", "error": str(e)}

