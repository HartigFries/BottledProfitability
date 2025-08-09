import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest

# Module-specific logger for get_vendor_summary
logger = logging.getLogger(__name__)

# Only configure handler if not already set
if not logger.handlers:
    handler = logging.FileHandler("logs/get_vendor_summary.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def create_vendor_summary(conn):
    """
    Create a summary of vendor sales data.
    
    Args:
        conn (sqlite3.Connection): SQLite database connection.
    
    Returns:
        pd.DataFrame: Summary DataFrame with vendor sales data.
    """
    vendor_sales_summary = pd.read_sql(f"""WITH FreightSummary AS (
                        SELECT 
                            VendorNumber, 
                            SUM(Freight) as FreightCost
                        FROM vendor_invoice
                        GROUP BY VendorNumber
                        ),
                    PurchaseSummary AS (
                        SELECT
                            p.VendorNumber,
                            p.VendorName,
                            p.Brand,
                            p.Description,
                            p.PurchasePrice,
                            pp.Price AS ActualPrice,
                            pp.Volume,
                            SUM(p.Quantity) AS TotalPurchaseQuantity,
                            SUM(p.Dollars) AS TotalPurchaseDollars
                        FROM purchases as p
                        JOIN purchase_prices as pp
                            ON p.Brand = pp.Brand
                        WHERE p.PurchasePrice > 0
                        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
                    ),
                    SalesSummary AS (
                        SELECT
                            VendorNo as VendorNumber,
                            Brand,
                            SUM(SalesQuantity) as TotalSalesQuantity,
                            SUM(SalesDollars) as TotalSalesDollars,
                            SUM(SalesPrice) as TotalSalesPrice,
                            SUM(ExciseTax) as TotalExciseTax
                        FROM sales
                        GROUP BY VendorName, Brand
                    )
            
                SELECT
                    ps.VendorNumber,
                    ps.VendorName,
                    ps.Brand,
                    ps.Description,
                    ps.PurchasePrice,
                    ps.ActualPrice,
                    ps.Volume,
                    ps.TotalPurchaseQuantity,
                    ps.TotalPurchaseDollars,
                    ss.TotalSalesQuantity,
                    ss.TotalSalesDollars,
                    ss.TotalSalesPrice,
                    ss.TotalExciseTax,
                    fs.FreightCost
                FROM PurchaseSummary AS ps
                LEFT JOIN SalesSummary AS ss
                    ON ps.VendorNumber = ss.VendorNumber
                    AND ps.Brand = ss.Brand
                LEFT JOIN FreightSummary AS fs
                    ON ps.VendorNumber = fs.VendorNumber
                ORDER BY ps.TotalPurchaseDollars DESC""", conn)

    return vendor_sales_summary

    
def clean_data(df):
    """
    Clean the vendor sales summary DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to clean.
    
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df.fillna(0, inplace=True)
    df["VendorName"] = df["VendorName"].str.strip()
    df["Volume"] = df["Volume"].astype('float64')
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    
    return df

if __name__ == "__main__":
    conn = sqlite3.connect('inventory.db')

    try:
        logger.info("Creating vendor sales summary...")
        summary = create_vendor_summary(conn)
        logger.info("Cleaning vendor sales summary data...")
        logger.info(summary.head())

        clean_summary = clean_data(summary)
        logger.info(f"Ingesting Data...")
        logger.info(clean_summary.head())

        ingest(clean_summary, 'vendor_sales_summary', conn)
        logger.info("Vendor sales summary ingestion completed successfully.")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
    finally:
        conn.close()