import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(2)
random.seed(2)

N = 1200

customer_ids = [f'CUST{str(i).zfill(4)}' for i in np.random.choice(range(1, 400), N)]
sectors = ['Manufacturing', 'Retail', 'Technology', 'Healthcare', 'Logistics']

start_date = datetime(2022, 1, 1)
dates = [start_date + timedelta(days=int(np.random.normal(365, 120))) for _ in range(N)]

amounts = np.round(np.random.normal(12000, 4000, N), 2)
amounts = np.clip(amounts, 1500, 35000)

base_days_to_pay = np.random.randint(5, 45, N)
seasonal_adj = np.array([(date.month in [3, 6, 9, 12]) * np.random.randint(3, 8) for date in dates])
days_to_pay = base_days_to_pay + seasonal_adj

is_default = np.random.binomial(1, 0.13, N)
high_risk_sector = [1 if random.random()<0.25 else 0 for _ in range(N)]
for i in range(N):
    if amounts[i]>18000 and days_to_pay[i]>35:
        if random.random()<0.33:
            is_default[i] = 1
    if high_risk_sector[i] and sectors.index(sectors[random.randint(0,4)]) in [1, 4]:
        if random.random()<0.25:
            is_default[i] = 1

avg_days_map = {}
for cust in set(customer_ids):
    avg_days_map[cust] = np.random.randint(15, 40)
avg_days_leak = [avg_days_map[cid] + int(np.random.normal(0,2)) for cid in customer_ids]

created_hours = [random.choices(range(8, 20), weights=[7,8,12,12,15,15,10,8,8,5,5,3], k=1)[0] for _ in range(N)]

sector_col = [random.choice(sectors) for _ in range(N)]

tenure = [np.random.randint(3, 80) for _ in range(N)]

open_invoices = [np.random.poisson(2 + 0.015*tenure[i]) for i in range(N)]

amount_bucket = pd.cut(amounts, bins=[0, 7000, 15000, 25000, 40000], labels=['low','med','high','very_high'])

for col, pct in [('sector_col', 0.08), ('created_hours', 0.06), ('tenure', 0.09), ('open_invoices', 0.05)]:
    idx = np.random.choice(range(N), int(N*pct), replace=False)
    eval(f"{col}")[idx] = None

for i in np.random.choice(range(N), int(N*0.04), replace=False):
    days_to_pay[i] = days_to_pay[i] + np.random.randint(40, 90)

df = pd.DataFrame({
    'invoice_id': [f'INV{str(i).zfill(6)}' for i in range(N)],
    'customer_id': customer_ids,
    'invoice_date': [d.strftime('%Y-%m-%d') for d in dates],
    'sector': sector_col,
    'invoice_amount': amounts,
    'invoice_created_hour': created_hours,
    'customer_tenure_months': tenure,
    'num_open_invoices': open_invoices,
    'invoice_amount_bucket': amount_bucket,
    'customer_avg_days_to_pay': avg_days_leak,
    'days_to_pay': days_to_pay,
    'is_default': is_default
})

dup_idx = np.random.choice(range(N), int(0.03*N), replace=False)
df = pd.concat([df, df.iloc[dup_idx]], ignore_index=True)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"is_default distribution: {df['is_default'].value_counts().to_dict()}")

df.to_csv('invoices.csv', index=False)