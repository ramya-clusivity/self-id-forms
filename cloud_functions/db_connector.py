from google.cloud import bigquery
from constants import GCP_PROJECT_ID


class DBSession:
    _client_instance = None  # Initialize the class attribute to None

    @classmethod
    def get_instance(cls):
        try:
            if cls._client_instance is None:
                cls._client_instance = bigquery.Client(project=GCP_PROJECT_ID)
        except Exception as e:
            print(f"Error initializing BigQuery client: {e}")
            raise
        
        return cls._client_instance
    

# client = DBSession.get_instance()


