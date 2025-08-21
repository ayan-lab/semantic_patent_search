# 🔍 Semantic Search Engine for Patents & Research Papers

This project implements a **semantic search** system that lets users retrieve relevant **patents** and **research papers** using natural language. Powered by **sentence embeddings**, **vector similarity search**, and a **FastAPI backend**, it offers an intelligent alternative to keyword-based search.

---

## 🚀 Live Demo

🌐 Try it here: [https://semantic-patent-search.onrender.com](https://semantic-patent-search.onrender.com) {currently link broken ## from Render}

---

## Screenshot
```json
{
  "query": "Patents related to logistics, security, and blockchain"
}
<img width="1776" height="722" alt="image" src="https://github.com/user-attachments/assets/7cdc7e06-45b1-4620-8e14-e020b1d3666a" />
```
```json
{
  "query": "Research papers on medical imaging, AI-based diagnostics"
}
<img width="1632" height="662" alt="image" src="https://github.com/user-attachments/assets/e648084d-4512-40e1-9503-4ccd2f3864a0" />

```
```json
{
  "query": "Patents & research on LIDAR, GPS, AI-driven pathfinding"
}
<img width="1667" height="676" alt="image" src="https://github.com/user-attachments/assets/9fbb2d61-9f41-4f6d-9403-2312d05ec597" />

```

## 🧠 Approach

### 🟢 1. Vectorization

- Each document's `desc` (description) is embedded using the `all-MiniLM-L6-v2` model from SentenceTransformers.
- This yields a **384-dimensional vector** per document.

### 🟢 2. Storage in Zilliz (Milvus)

- All vectors are stored in **Zilliz Serverless**, a managed vector database based on Milvus.
- Indexed using **HNSW** (Hierarchical Navigable Small World) with `COSINE` similarity for fast nearest-neighbor search.

### 🟢 3. FastAPI Backend

- Exposes a `/search` POST endpoint that:
  - Accepts user queries.
  - Converts them to vector embeddings.
  - Sends them to Zilliz to retrieve the top-K matches.
  - Returns results grouped by `type`: `patent` or `research`.

---

## 🔡 Sample Queries

| Query                                      | Expected Matches                                         |
|--------------------------------------------|---------------------------------------------------------|
| `AI techniques for cancer detection`       | Research papers on medical imaging, AI-based diagnostics |
| `Blockchain-based supply chain patents`    | Patents related to logistics, security, and blockchain   |
| `Machine learning for drug discovery`      | Research on predictive analytics in pharmaceuticals      |
| `Autonomous vehicle navigation systems`    | Patents & research on LIDAR, GPS, AI-driven pathfinding |

---

## 🧰 Tech Stack

| Layer         | Tech Used                            |
|---------------|---------------------------------------|
| Backend       | FastAPI                               |
| Embeddings    | SentenceTransformers (`MiniLM`)       |
| Vector DB     | Zilliz Serverless (Milvus)            |
| HTTP Client   | HTTPX (async)                         |
| Deployment    | *(e.g. Render, Railway, Vercel, etc.)* |

---

## 🗂️ Project Structure

```
greyb-assignment/
├── app/
│   ├── main.py                   # FastAPI entrypoint
│   ├── routes/search_routes.py    # API endpoint logic
│   ├── service/embeddings.py      # Embedding generation
│   ├── models/search.py           # Pydantic request models
│   └── config.py                  # Env vars & constants
├── vectorize_and_upload.py         # Script to embed & upload data
├── final.json                      # Original text data
├── result.json                     # Vectorized data
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## ⚙️ Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/greyb-assignment.git
cd greyb-assignment
```

### 2. Setup virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create .env file

```ini
ZILLIZ_API_KEY=your_zilliz_api_key
ZILLIZ_URL=https://your_zilliz_serverless_endpoint
COLLECTION_NAME=patent_research_data
```

### 4. Start the server

```bash
uvicorn app.main:app --reload
```
API will be available at: `http://localhost:8000`

### 📦 Uploading Data to Zilliz

Use this script to preprocess and upload the vectorized data:

```bash
python vectorize_and_upload.py
```
Ensure vectors have correct shape (384,).

### 📬 API Usage

▶️ **POST /search/**

**Request:**

```json
{
  "query": "AI techniques for cancer detection",
}
```

**Response:**

```json
{
  "query": "AI techniques for cancer detection",
  <cluster_topic1> :[
    "similar_patents": [
      {
        "doc_id": 123,
        "score": 0.91,
        "title": "Deep Learning for Tumor Detection",
        "source": "USPTO",
        "publication_date": "2021-03-22",
        "type": "patent"
      }
    ],
    "similar_research": [
      {
        "doc_id": 456,
        "score": 0.87,
        "title": "AI in Radiology: A Survey",
        "source": "IEEE Xplore",
        "publication_date": "2022-08-01",
        "type": "research"
      }
    ]],
 <cluster_topic2> :[
    "similar_patents": [
      {
        "doc_id": 123,
        "score": 0.91,
        "title": "Deep Learning for Tumor Detection",
        "source": "USPTO",
        "publication_date": "2021-03-22",
        "type": "patent"
      }
    ],
    "similar_research": [
      {
        "doc_id": 456,
        "score": 0.87,
        "title": "AI in Radiology: A Survey",
        "source": "IEEE Xplore",
        "publication_date": "2022-08-01",
        "type": "research"
      }
    ]],
}
```

---

## 🙏 Acknowledgements

- Sentence Transformers
- Zilliz / Milvus
- FastAPI
