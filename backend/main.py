"""
main.py

This is the actual API server, the "waiter" that takes requests from the
website (frontend) and passes them to graph_engine.py (the "kitchen") to
get the real work done, then sends the answer back.

Once this is running, a website can:
  - upload a call records file
  - ask for the graph + clusters
  - ask for the shortest path between two numbers
  - ask for the most important numbers

Run this from the PROJECT ROOT folder (not inside backend/) with:
                uvicorn backend.main:app --reload
Then open:      http://127.0.0.1:8000/docs
                 (FastAPI gives you a free interactive test page here)
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.graph_engine import (
    build_graph_from_csv_text,
    get_clusters,
    get_centrality_scores,
    get_shortest_path,
    graph_to_json,
)

app = FastAPI(title="NexusTrace API")

# CORS: without this, a website running on a different address (like our
# future React app on localhost:3000) would be blocked by the browser
# from talking to this API on localhost:8000. This opens that door.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for development, we'll tighten this later
    allow_methods=["*"],
    allow_headers=["*"],
)

# We keep the most recently uploaded graph in memory, simplest possible
# approach for an MVP, no database needed yet. Every new upload replaces it.
current_graph = {"graph": None}


@app.get("/")
def health_check():
    """Just confirms the server is alive, visiting the root URL shows this."""
    return {"status": "NexusTrace API is running"}


@app.post("/upload")
async def upload_call_records(file: UploadFile = File(...)):
    """
    Accepts an uploaded CSV file, builds the graph from it, runs cluster
    detection, and returns the full graph + cluster data ready for the
    frontend to draw.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file")

    contents = await file.read()
    csv_text = contents.decode("utf-8")

    G = build_graph_from_csv_text(csv_text)
    if G.number_of_nodes() == 0:
        raise HTTPException(status_code=400, detail="No valid call records found in file")

    partition = get_clusters(G)

    # save this graph in memory so other endpoints (shortest-path, centrality)
    # can use it without re-uploading the file every time
    current_graph["graph"] = G
    current_graph["partition"] = partition

    result = graph_to_json(G, partition)
    result["summary"] = {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "total_clusters": len(set(partition.values())),
    }
    return result


@app.get("/central-numbers")
def central_numbers():
    """Returns the top 'hub' and 'bridge' phone numbers from the last uploaded graph."""
    G = current_graph["graph"]
    if G is None:
        raise HTTPException(status_code=400, detail="No data uploaded yet, call /upload first")

    scores = get_centrality_scores(G)
    top_hub = sorted(scores["degree"].items(), key=lambda x: x[1], reverse=True)[:5]
    top_bridge = sorted(scores["betweenness"].items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "top_hub_numbers": [{"number": n, "score": round(s, 3)} for n, s in top_hub],
        "top_bridge_numbers": [{"number": n, "score": round(s, 3)} for n, s in top_bridge],
    }


@app.get("/shortest-path")
def shortest_path(number_a: str, number_b: str):
    """Returns how two phone numbers are connected, from the last uploaded graph."""
    G = current_graph["graph"]
    if G is None:
        raise HTTPException(status_code=400, detail="No data uploaded yet, call /upload first")

    path = get_shortest_path(G, number_a, number_b)
    if path is None:
        return {"connected": False, "path": []}
    return {"connected": True, "path": path}
