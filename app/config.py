import os
from dotenv import load_dotenv

load_dotenv()

ZILLIZ_API_KEY = os.getenv("ZILLIZ_API_KEY")
ZILLIZ_URL = os.getenv("ZILLIZ_URL")
# ZILLIZ_URI = os.getenv("ZILLIZ_URI")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
