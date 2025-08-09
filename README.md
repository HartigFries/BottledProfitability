# Dataset

The dataset (given as CSV files) represents **simulated operations** of an alcohol distribution company that sources beverages from multiple vendors and sells them to various businesses.

Although the figures are synthetic, they are structured to closely resemble **real-world business records**, including Vendor information, Purchase costs, Sales revenues, among other key operational metrics  

> **Note:** This dataset was provided by [*Ayushi Mishra*](https://www.linkedin.com/in/ayushi-mishra-30813b174/).

# Business Problem
In this analysis, we examine **profitable vendors** to help the distributor:

- **Prioritize** high-performing vendors and brands  
- **Reduce reliance** on low-turnover suppliers  
- **Manage inventory** more efficiently  
- **Focus marketing and sales efforts** on profitable but underperforming brands

## Structure
![Flow Chart showing the steps behind the project as well as the programming languages and applications used.](BottledProfitability.svg)

The [data](data), given in CSV files, was put into the database `inventory.db`  
(Not in the repository as the database is 2GB) via [`ingestion_db.py`](ingestion_db.py)  
in order to simulate working with databases provided by a company.

The data from this database was then loaded into a pandas dataframe in [`ECM.ipynb`](ECM.ipynb)  
then analysed to create a **summary table** containing all the information to conduct a vendor analysis,  
which was saved back into `inventory.db`.  
It was saved using an optimized multi-CTE SQL Query.

This summarized table was then used for **Vendor Performance Analysis** and **Hypothesis Testing**  
in [`VPA.ipynb`](VPA.ipynb), the key results of which were put into a **PowerBI Dashboard**  
for clients and stakeholders.

![BI Report](BI_Report.pdf)![Flow Chart showing the steps behind the project as well as the programming languages and applications used.](BottledProfitability.svg)

The [data](data), given in CSV files, was put into the database `inventory.db`  
(Not in the repository as the database is 2GB) via [`ingestion_db.py`](ingestion_db.py)  
in order to simulate working with databases provided by a company.

The data from this database was then loaded into a pandas dataframe in [`ECM.ipynb`](ECM.ipynb)  
then analysed to create a **summary table** containing all the information to conduct a vendor analysis,  
which was saved back into `inventory.db`.  
It was saved using an optimized multi-CTE SQL Query.

This summarized table was then used for **Vendor Performance Analysis** and **Hypothesis Testing**  
in [`VPA.ipynb`](VPA.ipynb), the key results of which were put into a **PowerBI Dashboard**  
for clients and stakeholders.

![BI Report](BI_Report.pdf)

