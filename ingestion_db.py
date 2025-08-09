import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

engine = create_engine('sqlite:///inventory.db')

logger = logging.getLogger(__name__)

# Only configure handler if it's not already set
if not logger.handlers:
    handler = logging.FileHandler('logs/ingestion_db.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def ingest(df, table_name, engine):
    '''Ingests the DataFrame into the specified table in the SQLite database.'''
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    logger.info(f"Data ingested into table: {table_name}")

def load_raw_data():
    '''Will load the raw data from the data directory and ingest it into the database.'''
    start = time.time()
    if not os.path.exists('data'):
        os.makedirs('data')

    for file in os.listdir('data'):
        if file.endswith('.csv'):
            df = pd.read_csv('data/' + file)
            logging.info(f"ingesting file: {file} in inventory.db")
            ingest(df, file.split('.')[0], engine)

    end = time.time()

    logger.info("|====================Ingestion Complete====================|")
    logger.info(f"\nData ingestion completed in {(end - start)/60} minutes.")

if __name__ == "__main__":

    load_raw_data()
    logger.info("Data ingestion script completed successfully.")
    print("Data ingestion script completed successfully.")