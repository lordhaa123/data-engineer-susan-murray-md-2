import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


# 1. SETUP & DATA QUALITY LOGGING
def log_data_quality(df):
    print("=== Data Quality Report ===")
    print(f"Total Records: {len(df)}")
    print(f"Duplicate Invoices: {df.duplicated('invoice_id').sum()}")
    
    missing_pct = df.isnull().sum() / len(df) * 100
    print("\nMissing Values (%):")
    print(missing_pct[missing_pct > 0])
    
    # Outlier detection for days_to_pay
    q_high = df['days_to_pay'].quantile(0.99)
    print(f"\nOutlier Threshold (99th percentile): {q_high:.2f} days")
    print("-" * 30)

# Load data
file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'invoices.csv')
df = pd.read_csv(r"C:\Users\Pratik\Documents\invoices.csv")

# Drop duplicates immediately
df = df.drop_duplicates(subset=['invoice_id'])
log_data_quality(df)


# Drop duplicates immediately
df = df.drop_duplicates(subset=['invoice_id'])
log_data_quality(df)


# 2. CHRONOLOGICAL SPLIT
# Ensuring we train on older invoices and test on the newest ones
df['invoice_date'] = pd.to_datetime(df['invoice_date'])
df = df.sort_values('invoice_date')

split_point = int(len(df) * 0.8)
train_df = df.iloc[:split_point]
test_df = df.iloc[split_point:]


# 3. FEATURE ENGINEERING & LEAKAGE FIX
# We remove 'customer_avg_days_to_pay' to prevent leakage
features = [
    'invoice_amount', 'invoice_created_hour', 'customer_tenure_months',
    'num_open_invoices', 'sector', 'invoice_amount_bucket'
]

numeric_features = ['invoice_amount', 'invoice_created_hour', 'customer_tenure_months', 'num_open_invoices']
categorical_features = ['sector', 'invoice_amount_bucket']

# Create Preprocessing Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('ohe', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features)
    ]
)


# 4. MODEL TRAINING (Regression & Classification)
reg_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

clf_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced'))
])

# Fit Models
reg_pipeline.fit(train_df[features], train_df['days_to_pay'])
clf_pipeline.fit(train_df[features], train_df['is_default'])


# 5. BATCH INFERENCE PIPELINE
def run_inference(model_reg, model_clf, input_df):
    preds = input_df[['invoice_id', 'customer_id']].copy()
    preds['predicted_days_to_pay'] = model_reg.predict(input_df[features])
    # Probability of default (class 1)
    preds['default_probability'] = model_clf.predict_proba(input_df[features])[:, 1]
    return preds


# Generate Results
results = run_inference(reg_pipeline, clf_pipeline, test_df)


# 6. EVALUATION
mae = mean_absolute_error(test_df['days_to_pay'], results['predicted_days_to_pay'])
acc = accuracy_score(test_df['is_default'], clf_pipeline.predict(test_df[features]))

print(f"\n=== Performance Metrics (Chronological) ===")
print(f"Regression MAE: {mae:.2f} days")
print(f"Classification Accuracy: {acc:.3f}")
print(f"Top 5 High-Risk Invoices:")
print(results.sort_values('default_probability', ascending=False).head())

