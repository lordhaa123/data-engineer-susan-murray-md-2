Please document your findings and improvements here.

## Issues Found
We an observe critical flaw that would make the model appear perfect in testing while failing miserably in the production environment: Data Leakage.
I have updated the the correct code 

## The Problem Analysis
1. The Bug: The feature customer_avg_days_to_pay includes the current invoice's duration in its calculation. The model is essentially looking at the past data to predict the answer. I noticed the Accuracy looks worse than the existing baseline. This is actually a success. The existing baseline had nearly 100% accuracy because of the customer_avg_days_to_pay leak. The new metrics reflect how the model will actually perform when a brand-new invoice arrives and the outcome isn't known yet.

2. Chronological Risk: Considering predictive modeling for Finance domain, you cannot use a random split. If we train on an invoice from December to predict one from January, we are predicting the past using the future.

3. Encoding Issues: Label Encoder assigns arbitrary numbers (1, 2, 3) to sectors. A Linear Regression model will interpret "Sector 3" as being "three times more sector-y" than "Sector 1," which is nonsensical.

## Improvements Made
1. Ensured we train on older invoices and test on the newest ones and avoid the random split considering predictive modeling for finance domain.

2. In the original code, is_default was only ~13% of the data. I added class_weight='balanced' to the Logistic Regression. This forces the model to pay more attention to the "Default" cases, which are the most expensive for the business to miss.

3. Architectural Design for Scale
i. In the baseline, the SparkSession has been initialized but then converted everything to a Pandas pdf. For small data (1,200 rows), Spark actually slows things down due to overhead.

ii. To scale to millions of rows, the ColumnTransformer and Pipeline logic should be ported to PySpark MLlib. This allows the preprocessing (One-Hot Encoding, Scaling) to happen across a distributed cluster rather than in a single machine's memory.

iii. By using sklearn.pipeline, we ensure that the exact same scaling and transformation parameters used during training are applied during inference, preventing "training-serving skew."


## Final Results

Regression MAE: 13.23 days
Classification Accuracy: 0.512
Top 5 High-Risk Invoices:
     invoice_id customer_id  predicted_days_to_pay  default_probability
1136  INV000323    CUST0169              26.416695             0.696850
42    INV001087    CUST0047              27.421813             0.680228
741   INV000996    CUST0119              26.177247             0.653405
751   INV000462    CUST0355              29.691839             0.623242
128   INV000183    CUST0286              28.436627             0.618165
