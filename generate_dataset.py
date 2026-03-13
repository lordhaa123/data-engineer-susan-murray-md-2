import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

def generate_invoice_dataset(n=1200):
    # --- 1. Define missing variables first ---
    np.random.seed(42)
    random.seed(42)
    
    # Generate the raw data used in the DataFrame
    c_ids = [f'CUST{str(i).zfill(4)}' for i in np.random.choice(range(1, 400), n)]
    sectors = ['Manufacturing', 'Retail', 'Technology', 'Healthcare', 'Logistics']
    start_date = datetime(2022, 1, 1)
    dates = [start_date + timedelta(days=int(np.random.normal(365, 120))) for _ in range(n)]
    amounts = np.clip(np.round(np.random.normal(12000, 4000, n), 2), 1500, 35000)
    
    days_to_pay = np.random.randint(5, 45, n)
    is_default = np.random.binomial(1, 0.13, n)
    sector_col = [random.choice(sectors) for _ in range(n)]
    created_hours = [random.randint(8, 20) for _ in range(n)]
    tenure = [np.random.randint(3, 80) for _ in range(n)]
    open_inv = [np.random.poisson(2) for _ in range(n)]
    avg_days_leak = [np.random.randint(15, 40) for _ in range(n)]

    # --- 2. Initialize DataFrame (Corrected Indentation) ---
    df = pd.DataFrame({
        'invoice_id': [f'INV{str(i).zfill(6)}' for i in range(n)],
        'customer_id': c_ids,
        'invoice_date': [d.strftime('%Y-%m-%d') for d in dates],
        'sector': sector_col,
        'invoice_amount': amounts,
        'invoice_created_hour': created_hours,
        'customer_tenure_months': tenure,
        'num_open_invoices': open_inv,
        'customer_avg_days_to_pay': avg_days_leak,
        'days_to_pay': days_to_pay,
        'is_default': is_default
    })

    # Add Categorical Buckets
    df['invoice_amount_bucket'] = pd.cut(
        df['invoice_amount'], 
        bins=[0, 7000, 15000, 25000, 40000], 
        labels=['low', 'med', 'high', 'very_high']
    )

    # 3. Inject Missing Values (NaNs)
    null_map = {
        'sector': 0.08, 
        'invoice_created_hour': 0.06, 
        'customer_tenure_months': 0.09, 
        'num_open_invoices': 0.05
    }
    for col, pct in null_map.items():
        idx = df.sample(frac=pct).index
        df.loc[idx, col] = np.nan

    # 4. Add Late Payment Outliers
    outlier_idx = df.sample(frac=0.04).index
    df.loc[outlier_idx, 'days_to_pay'] += np.random.randint(40, 90)

    # 5. Add Duplicates
    df = pd.concat([df, df.sample(frac=0.03)], ignore_index=True)

    # Final Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    print(f"Dataset generated. Shape: {df.shape}")
    print(f"Defaults: {df['is_default'].sum()} cases.")
    return df

# --- Execution ---
# Set the path to your Documents folder automatically
docs_path = os.path.join(os.path.expanduser('~'), 'Documents', 'invoices.csv')

# Run the function
df_invoices = generate_invoice_dataset(1200)

# Save the file
df_invoices.to_csv(docs_path, index=False)
print(f"Success! File saved to: {docs_path}")
