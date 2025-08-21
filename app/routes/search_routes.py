from fastapi import APIRouter
import httpx
from typing import Dict, Any
from dotenv import load_dotenv

from models.search import SearchRequest
from service.embeddings import embed_query
from config import ZILLIZ_API_KEY, ZILLIZ_URL, COLLECTION_NAME
from service.cluster_maker import cluster_make

router = APIRouter()
load_dotenv()

@router.post("/", response_model=Dict[str, Any])
async def semantic_search(req: SearchRequest):
    vector = embed_query(req.query)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            ZILLIZ_URL,
            json={
                "collectionName": COLLECTION_NAME,
                "data": [vector], 
                "limit": req.top_k,
                "outputFields": ["doc_id", "title", "publication_date", "source", "type"]
            },
            headers={
                "Authorization": f"Bearer {ZILLIZ_API_KEY}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    if response.status_code != 200:
        return {
            "error": f"Zilliz API error: {response.status_code}",
            "message": response.text
        }

    results = response.json().get("data", [])


    similar_patents = []
    similar_research = []

    for item in results:
        item_data = {
            "doc_id": item.get("doc_id"),
            "score": float(item.get("score", 0)),
            "title": item.get("title"),
            "source": item.get("source"),
            "publication_date": item.get("publication_date"),
            "type": item.get("type"),
        }

        if item.get("type") == "patent":
            similar_patents.append(item_data)
        elif item.get("type") == "research":
            similar_research.append(item_data)

    final_result = {
        "query": req.query,
        "similar_patents": similar_patents,
        "similar_research": similar_research
    }
    clustered_output = cluster_make(final_result)
    return clustered_output
