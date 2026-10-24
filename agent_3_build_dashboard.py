"""Agent 3: build the standalone dashboard. Reads data/analysis/*.csv and data/limits.csv only.
Embeds just the columns the page needs (no email links, no free-text descriptions) and writes output/spend_dashboard.html."""
import csv, json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(root, 'data', 'analysis')
def rd(p, cols=None):
    with open(p, newline='', encoding='utf-8') as f: rows = list(csv.DictReader(f))
    return [{c: r.get(c, '') for c in cols} for r in rows] if cols else rows
D = {
 'kpis': rd(os.path.join(A, 'summary_kpis.csv')),
 'merch': rd(os.path.join(A, 'by_merchant.csv')),
 'subs': rd(os.path.join(A, 'subscriptions.csv')),
 'top': [dict(r, view_url=str(i)) for i, r in enumerate(rd(os.path.join(A, 'top_purchases.csv'), ['date', 'merchant', 'currency', 'amount', 'view_url']))],
 'txns': rd(os.path.join(A, 'transactions_clean.csv'), ['date', 'month', 'merchant', 'currency', 'type', 'amount', 'signed_amount', 'category', 'budget_category']),
 'runinfo': rd(os.path.join(A, 'run_info.csv')),
 'income': rd(os.path.join(A, 'income_clean.csv'), ['date', 'source', 'source_type', 'amount', 'confidence']),
 'limits': rd(os.path.join(root, 'data', 'limits.csv'), ['budget_category', 'monthly_limit_inr']),
}
CD = {k: {'c': (list(v[0].keys()) if v else []), 'r': [list(r.values()) for r in v]} for k, v in D.items()}
data = json.dumps(CD, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent_3_page.html'), encoding='utf-8').read()
shell = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Spend Dashboard</title>
<style>
:root{--font-anthropic-sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--font-anthropic-serif:Georgia,"Times New Roman",serif;
--color-bg:#f7f6f2;--color-panel:#ffffff;--color-fg:#1f1e1b;--color-fg-muted:#6a675f;--color-border-line:#e3e0d6;--color-ok:#1b7f5c;--color-warn:#a15c07;--color-bad:#b42318;
--cds-font-size-caption:12px;--cds-font-size-body:14px;--cds-font-size-heading:16px;--cds-font-size-title:28px;--cds-font-weight-medium:600;
--cds-gap-sm:8px;--cds-gap-md:16px;--cds-pad-xs:4px;--cds-pad-sm:8px;--cds-pad-md:12px;--cds-pad-lg:16px;--cds-radius:10px;
--cds-chart-grid:#e9e6dc;--cds-chart-axis:#1f6f6b;--cds-chart-muted:#a9bdbb;--cds-chart-status-critical:#b42318;--cds-surface-popover:#ffffff;--cds-border:#d8d4c8;--cds-shadow-popover:0 4px 14px rgba(0,0,0,.12);color-scheme:light}
@media (prefers-color-scheme:dark){:root{--color-bg:#141413;--color-panel:#1e1d1b;--color-fg:#f1efe9;--color-fg-muted:#a5a199;--color-border-line:#34322c;--color-ok:#5fc49b;--color-warn:#f0b35a;--color-bad:#f97066;
--cds-chart-grid:#2d2b26;--cds-chart-axis:#5fc4bd;--cds-chart-muted:#3d5d5b;--cds-chart-status-critical:#f97066;--cds-surface-popover:#262520;--cds-border:#3d3a33;--cds-shadow-popover:0 4px 14px rgba(0,0,0,.5);color-scheme:dark}}
body{margin:0;background:var(--color-bg);color:var(--color-fg);font:14px/1.5 var(--font-anthropic-sans);padding:24px max(16px,env(safe-area-inset-left,0px)) 64px}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
</head><body>
<script>
(function(){const RAW=__DATA__;const DATA={};for(const k in RAW){const c=RAW[k].c;DATA[k]=RAW[k].r.map(r=>{const o={};c.forEach((n,i)=>o[n]=r[i]);return o})}const store={};const subs=[];
 for(const k in DATA)store[k]={status:'ok',data:DATA[k],columns:DATA[k][0]?Object.keys(DATA[k][0]):[],message:'',refreshing:false,meta:[]};
 window.dash={data:id=>store[id]||{status:'missing',data:[],columns:[],message:'',refreshing:false,meta:[]},
  calc(id,o){store[id]={status:'ok',data:o.fn(...o.inputs.map(i=>store[i].data)),columns:[],message:'',refreshing:false,meta:[]}},
  onData(fn){subs.push(fn);fn();let t;addEventListener('resize',()=>{clearTimeout(t);t=setTimeout(fn,120)})},
  params:()=>({}),setParams(){},resetParams(){},setLink(){},refresh(){},loader(){},colors:[]};})();
</script>
__PAGE__
</body></html>'''
html = shell.replace('__DATA__', data).replace('__PAGE__', page)
os.makedirs(os.path.join(root, 'output'), exist_ok=True)
out = os.path.join(root, 'output', 'spend_dashboard.html')
open(out, 'w', encoding='utf-8').write(html)
print('wrote', out, len(html), 'bytes')
