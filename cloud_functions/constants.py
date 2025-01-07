import os

GCP_PROJECT_ID = os.getenv("PROJECT_ID", "fleet-rhino-340408")
DATASET_ID = os.getenv("DATASET_ID", "Self_id_data")
RESPONDENT_TABLE = os.getenv("RESPONDENT_TABLE", "DEV_Respondent_data_from_client")

LOW_COUNT_GENDER = 5
