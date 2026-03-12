import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, avg, count, when
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')


spark = SparkSession.builder.appName('PaymentPredictionEngine').getOrCreate()

pdf = pd.read_csv('invoices.csv')
df = spark.createDataFrame(pdf)

df = df.dropDuplicates(['invoice_id'])

feature_cols = [
    'invoice_amount', 'invoice_created_hour', 'customer_tenure_months',
    'num_open_invoices', 'customer_avg_days_to_pay', 'sector', 'invoice_amount_bucket'
]

for colname in ['sector', 'invoice_amount_bucket']:
    mode = pdf[colname].mode()[0]
    pdf[colname] = pdf[colname].fillna(mode)
    le = LabelEncoder()
    pdf[colname] = le.fit_transform(pdf[colname])

pdf = pdf.fillna(-1)

X_reg = pdf[feature_cols]
y_reg = pdf['days_to_pay']

X_clf = pdf[feature_cols]
y_clf = pdf['is_default']

from sklearn.model_selection import train_test_split
Xr_train, Xr_test, yr_train, yr_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
Xc_train, Xc_test, yc_train, yc_test = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

reg = LinearRegression()
reg.fit(Xr_train, yr_train)
pred_reg = reg.predict(Xr_test)

clf = LogisticRegression(max_iter=200)
clf.fit(Xc_train, yc_train)
pred_clf = clf.predict(Xc_test)

mae = mean_absolute_error(yr_test, pred_reg)
clf_acc = accuracy_score(yc_test, pred_clf)
print(f"\n=== Payment Days Regression ===\nMAE: {mae:.2f}")
print(f"\n=== Default Risk Classification ===\nAccuracy: {clf_acc:.3f}")

# TODO: Implement batch inference pipeline that outputs per-invoice predictions (days_to_pay_pred, is_default_prob)

# TODO: Log data quality stats (missing %, duplicate count, outliers found)

# TODO: Replace random split with invoice_date-based chronological split for production realism

