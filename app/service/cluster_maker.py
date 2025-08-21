import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

def cluster_make(data: dict, num_clusters: int = 5) -> dict:
    query = data.get("query", "")
    patents = data.get("similar_patents", [])
    research = data.get("similar_research", [])

    all_records = patents + research
    if not all_records:
        return {"query": query, "clusters": {}}

    # Use TF-IDF on titles for clustering
    titles = [rec.get("title", "") for rec in all_records]
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(titles)

    # Run KMeans
    n_clusters = min(num_clusters, len(all_records))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)

    # Assign cluster_id
    for rec, cid in zip(all_records, clusters):
        rec["cluster_id"] = int(cid)

    # Create cluster names
    terms = vectorizer.get_feature_names_out()
    cluster_names = {}
    for cluster_id in range(n_clusters):
        cluster_indices = [i for i, cid in enumerate(clusters) if cid == cluster_id]
        cluster_texts = [titles[i] for i in cluster_indices]

        if not cluster_texts:
            cluster_names[cluster_id] = f"Cluster_{cluster_id}"
            continue

        tfidf_cluster = vectorizer.fit_transform(cluster_texts)
        avg_scores = np.asarray(tfidf_cluster.mean(axis=0)).flatten()
        top_indices = avg_scores.argsort()[-3:][::-1]
        top_words = [terms[i] for i in top_indices]
        cluster_names[cluster_id] = " / ".join(top_words)

    # Build output
    clustered_output = {"query": query}
    for cluster_id, cname in cluster_names.items():
        clustered_output[cname] = {
            "similar_patents": [],
            "similar_research": []
        }

    for rec in patents:
        cname = cluster_names[rec["cluster_id"]]
        clustered_output[cname]["similar_patents"].append(rec)

    for rec in research:
        cname = cluster_names[rec["cluster_id"]]
        clustered_output[cname]["similar_research"].append(rec)

    return clustered_output
