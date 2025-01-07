from flask import jsonify
from google.cloud import bigquery
import asyncio

# custom imports
from logger import logger
from db_connector import DBSession


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
    
    async def fetch_data(self):
        # Module will generate a query and fetch data aysnchronously
        try:
             # Create query job configuration
            job_config = bigquery.QueryJobConfig(labels={
            "query_preview_enabled": "true"  # Corrected label
            })
            job_config.use_query_cache = True
            job_config.maximum_bytes_billed = 10**10  # 10 GB limit
            job_config.dry_run = False

            # Query DB
            query_job = self.client.query()
            # Using asyncio.to_thread for offloading to another thread
            self.df = await asyncio.to_thread(query_job.to_dataframe)

        except Exception as err:
            logger.error()

        return