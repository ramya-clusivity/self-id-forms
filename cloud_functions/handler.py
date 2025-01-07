from flask import jsonify
from google.cloud import bigquery
import asyncio
from io import StringIO

# custom imports
from logger import logger
from db_connector import DBSession
from constants import *

def health(request):
    """Handles /health route."""
    name = request.args.get("name", "World")
    return jsonify(message=f"Hello, {name}!")

class CreateClientSession:
    def __init__(self):
        self.client = None
        self.df = None

    def client_session(self):
        # Initialize the client using DBSession singleton instance
        if self.client is None:
            self.client = DBSession.get_instance()
        return self.client
    
class Self_ID_FORMS(CreateClientSession):
    """
    This class will initiate a DB session singleton
    extracts the results and returns data
    """
    def __init__(self, request):
        super().__init__()  # Initialize the CreateClientSession class
        self.client_session = self.client_session()
        self.request = request
        
        # fetch company_id form_id from request and extract data from BigQuery
        self.company_id = request.args.get('company_id')
        self.form_id = request.args.get('form_id')
                    
        logger.info(f"company_id: {self.company_id}")
        logger.info(f"form_id: {self.form_id}")
    
    async def fetch_data(self):
        # Module will generate a query and fetch data aysnchronously
        try:
             # Create query job configuration
            job_config = bigquery.QueryJobConfig(labels={
            "query_preview_enabled": "true"  # Corrected label
            })
            job_config.use_query_cache = True
            job_config.maximum_bytes_billed = 1**10  # 1 GB limit
            job_config.dry_run = False

            query = f"""
            SELECT 
                *
            FROM `{DATASET_ID}.{TABLE_ID}`
            WHERE Company_id = '{self.company_id}'
            AND Form_id = '{self.form_id}'
            """
            # Query DB
            query_job = self.client.query(query, job_config=job_config)
            self.df = await asyncio.to_thread(query_job.to_dataframe)

            logger.info(f"DB data: {len(self.df)}")

            # Convert DataFrame to CSV
            csv_buffer = StringIO()
            self.df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            return csv_buffer.getvalue()

        except Exception as err:
            logger.error(f"Error: {err}")

        return