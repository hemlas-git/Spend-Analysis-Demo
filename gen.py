import csv, random, datetime as dt, collections
random.seed(7)
A='data/analysis/'
start=dt.date(2026,4,17); end=dt.date(2026,10,17)
days=[start+dt.timedelta(i) for i in range((end-start).days+1)]
tx=[]
def add(d,m,amt,cat,bc,typ='purchase'):
    tx.append(dict(date=d.isoformat(),month=d.isoformat()[:7],merchant=m,currency='INR',type=typ,amount=round(amt,2),signed_amount=round(-amt if typ=='refund' else amt,2),category=cat,budget_category=bc))
def rnd(a,b): return random.uniform(a,b)
for d in days:
    if random.random()<.55: add(d,'Uber',rnd(70,260),'Travel & Transport','Transportation')
    if random.random()<.22: add(d,'Zomato',rnd(350,1300),'Food & Dining','Restaurants & Dining')
    if random.random()<.11: add(d,'Blinkit',rnd(250,2400),'Groceries','Groceries')
    if d.weekday()==5 and random.random()<.8: add(d,'BigBasket',rnd(900,2600),'Groceries','Groceries')
    if random.random()<.17:
        a=rnd(300,4200); add(d,'Amazon',a,'Shopping','Shopping & Entertainment')
        if random.random()<.25: add(d+dt.timedelta(random.randint(2,9)) if d+dt.timedelta(9)<=end else d,'Amazon',a*rnd(.4,1),'Shopping','Shopping & Entertainment','refund')
    if random.random()<.05: add(d,random.choice(['Myntra','Nykaa']),rnd(900,3800),'Fashion','Personal & Family Care')
    if random.random()<.03: add(d,'Apollo Pharmacy',rnd(200,1500),'Health','Health')
    if random.random()<.015: add(d,'Cult Fit',rnd(1500,4500),'Fitness','Fitness & Learning')
    if random.random()<.02: add(d,'Cash withdrawal (ATM)',random.choice([2000,3000,5000]),'Other','Cash, Checks & Misc')
    if d.day==3: add(d,'Society maintenance',9500,'Bills & Utilities','Home & Utilities','bill')
    if d.day==12: add(d,'Airtel Broadband',799,'Bills & Utilities','Home & Utilities','bill'); add(d,'Electricity (BESCOM)',rnd(1400,2600),'Bills & Utilities','Home & Utilities','bill')
    if d.day==5: add(d,'Netflix',649,'Subscriptions','Shopping & Entertainment')
    if d.day==9: add(d,'Spotify',139,'Subscriptions','Shopping & Entertainment'); add(d,'Apple Media Services',219,'Subscriptions','Shopping & Entertainment')
    if d.day==15: add(d,'LIC Premium',9100,'Insurance','Finance','bill') if d.month in (6,9) else None
# a few big-ticket items and one trip
add(dt.date(2026,6,20),'Urban Ladder',48999,'Shopping','Home & Utilities')
add(dt.date(2026,8,2),'Urban Ladder',31998,'Shopping','Home & Utilities')
add(dt.date(2026,7,14),'Wooden Street',24999,'Shopping','Home & Utilities')
add(dt.date(2026,9,7),'Flipkart',21499,'Shopping','Home & Utilities')
add(dt.date(2026,8,21),'Havells India Limited',14200,'Shopping','Home & Utilities')
add(dt.date(2026,9,19),'MakeMyTrip',23400,'Travel','Travel')
add(dt.date(2026,9,20),'IndiGo',11800,'Travel','Travel')
add(dt.date(2026,9,12),'Amazon',12499,'Shopping','Shopping & Entertainment')
add(dt.date(2026,7,22),'Amazon',10999,'Shopping','Shopping & Entertainment')
add(dt.date(2026,9,25),'Uber',24.5,'Travel & Transport','Transportation')
tx[-1]['currency']='USD'
tx.sort(key=lambda r:r['date'])
for i,r in enumerate(tx): r['message_id']='demo%04d'%i
cols=['message_id','date','merchant','amount','currency','type','category','signed_amount','month','budget_category']
w=csv.DictWriter(open(A+'transactions_clean.csv','w',newline=''),fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(tx)
net=lambda r:r['signed_amount']
utx=[r for r in tx if r['currency']=='USD']; tx=[r for r in tx if r['currency']=='INR']; tot=sum(r['signed_amount'] for r in tx); gross=sum(r['amount'] for r in tx if r['type']!='refund'); ref=gross-tot
orders=sum(1 for r in tx if r['type']!='refund')
bym=collections.defaultdict(lambda:[0,0])
for r in tx:
    bym[r['merchant']][0]+=r['signed_amount']
    if r['type']!='refund': bym[r['merchant']][1]+=1
ms=sorted(bym.items(),key=lambda x:-x[1][0])
months=sorted({r['month'] for r in tx}); mt=collections.defaultdict(float)
for r in tx: mt[r['month']]+=r['signed_amount']
prev,last=months[-3],months[-2]
rows=[('total_spend',round(tot,2)),('gross_spend',round(gross,2)),('refunds_total',round(ref,2)),('monthly_avg',round(tot/len(months),2)),('order_count',orders),('avg_order_value',round(gross/orders,2)),('top_merchant',ms[0][0]),('mom_change_pct',round((mt[last]-mt[prev])/mt[prev]*100,1)),('mom_compared_months',prev+' -> '+last)]
w=csv.writer(open(A+'summary_kpis.csv','w',newline=''));w.writerow(['metric','currency','value']);[w.writerow([a,'INR',b]) for a,b in rows]
for a,b in [('total_spend',24.5),('gross_spend',24.5),('refunds_total',0.0),('monthly_avg',4.08),('order_count',1),('avg_order_value',24.5),('top_merchant','Uber')]: w.writerow([a,'USD',b])
w=csv.writer(open(A+'by_merchant.csv','w',newline=''));w.writerow(['merchant','currency','spend','orders','avg_order_value'])
for m,(s,n) in ms: w.writerow([m,'INR',round(s,2),n,round(s/max(n,1),2)])
w.writerow(['Uber','USD',24.5,1,24.5])
subs=[('Netflix',649,6,'2026-10-05'),('Spotify',139,6,'2026-10-09'),('Apple Media Services',219,6,'2026-10-09'),('Airtel Broadband',799,6,'2026-10-12')]
w=csv.writer(open(A+'subscriptions.csv','w',newline=''));w.writerow(['merchant','currency','amount','months_seen','last_charged']);[w.writerow([a,'INR',b,c,d]) for a,b,c,d in subs]
top=sorted([r for r in tx if r['type']!='refund'],key=lambda r:-r['amount'])[:10]
w=csv.writer(open(A+'top_purchases.csv','w',newline=''));w.writerow(['date','merchant','currency','amount','view_url']);[w.writerow([r['date'],r['merchant'],'INR',r['amount'],'']) for r in top]
w=csv.writer(open(A+'run_info.csv','w',newline=''));w.writerow(['period_from','period_to','generated_on','emails_scanned','transactions_found','fx_rate_used']);w.writerow(['2026-04-17','2026-10-17','2026-10-17','',len(tx),''])
inc=[]
for m in range(5,11):
    inc.append((dt.date(2026,m,1),'Salary - Acme Corp (sample)','Other credits',185000,'confirmed'))
    if m in (6,9): inc.append((dt.date(2026,m,30),'Savings account interest','Interest',random.randint(1200,3100),'confirmed'))
    if m in (7,9): inc.append((dt.date(2026,m,18),'Freelance project (sample)','Other credits',random.choice([22000,35000]),'confirmed'))
w=csv.writer(open(A+'income_clean.csv','w',newline=''));w.writerow(['date','source','source_type','amount','currency','confidence','class','description','message_id','view_url'])
for d,s,t,a,c in inc: w.writerow([d.isoformat(),s,t,a,'INR',c,'credit','','',''])
import shutil
lim=[('Home & Utilities',25000),('Transportation',8000),('Groceries',14000),('Personal & Family Care',6000),('Health',3000),('Restaurants & Dining',9000),('Shopping & Entertainment',20000),('Travel',15000),('Cash, Checks & Misc',8000),('Finance',10000),('Fitness & Learning',5000)]
w=csv.writer(open('data/limits.csv','w',newline=''));w.writerow(['budget_category','monthly_limit_inr','basis']);[w.writerow([a,b,'Sample limit']) for a,b in lim]
print(len(tx),round(tot),sum(a for _,_,_,a,_ in inc))
