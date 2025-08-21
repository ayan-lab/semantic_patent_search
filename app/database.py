import json
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, list_collections
from config import ZILLIZ_API_KEY, ZILLIZ_URL, COLLECTION_NAME

connections.connect(alias="default", uri=ZILLIZ_URL, token=ZILLIZ_API_KEY)

fields = [
    FieldSchema(name="doc_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="citation_count", dtype=DataType.INT64),
    FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="type", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="publication_date", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]

schema = CollectionSchema(fields, description="Patent titles as vector embeddings")

if COLLECTION_NAME not in list_collections():
    collection = Collection(name=COLLECTION_NAME, schema=schema)
else:
    collection = Collection(name=COLLECTION_NAME)

if not collection.indexes:
    print("⚙️ Creating index on embedding field...")
    collection.create_index(
        field_name="embedding",
        index_params={
            "index_type": "HNSW",
            "metric_type": "COSINE",
            "params": {"M": 16, "efConstruction": 200}
        }
    )

collection.load()

