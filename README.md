<div align="center">

# 🕸️ NexusTrace

### Turning raw call records into investigation-ready intelligence

**From messy spreadsheets to instant suspect networks — automatically.**

![Version](https://img.shields.io/badge/version-v1.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active--development-brightgreen?style=for-the-badge)
![Stage](https://img.shields.io/badge/stage-MVP-orange?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge)

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![NetworkX](https://img.shields.io/badge/NetworkX-graph--engine-black?style=flat-square)

</div>

---

## 📖 What is NexusTrace?

Investigators receive **Call Detail Records (CDR)** and **Internet Protocol Detail Records (IPDR)** as raw spreadsheets — thousands of rows of who-called-whom data — and today, finding suspect networks inside that noise is a slow, manual, error-prone process.

**NexusTrace turns that spreadsheet into a picture.** Upload the data, and it automatically:

- 🔵 Draws every phone number as a node, every call as a connection
- 🧩 Detects tightly-connected groups (potential suspect clusters) — without being told where to look
- ⭐ Highlights the most "important" numbers in the network (likely coordinators/hubs)
- 🔍 Finds hidden links between any two numbers, even if they never called each other directly

> This is v1 — the foundation. See the [Roadmap](#-roadmap--future-episodes) below for where this is headed.

---

## 🎬 Demo

<div align="center">

*(Demo GIF/video coming soon)*

</div>

---

## ⚙️ How It Works

```
   raw CSV/XLSX               graph construction         analysis engine            visual output
  ┌───────────────┐        ┌───────────────────┐        ┌──────────────────┐       ┌─────────────────┐
  │ call_records.  │──────▶│  build nodes +     │─────▶│ community        │─────▶│ interactive     │
  │ csv (uploaded) │       │  weighted edges    │       │ detection +      │       │ force-graph in  │
  │                │       │  (NetworkX)        │       │ centrality       │       │ the browser     │
  └───────────────┘        └───────────────────┘        └──────────────────┘       └─────────────────┘
```

1. **Ingest** — parse the uploaded call record file into a clean, normalized format
2. **Build the graph** — every phone number becomes a node, every call becomes a connection between two nodes
3. **Analyze** — run graph algorithms (community detection, centrality scoring) to surface patterns a human would take hours to spot
4. **Visualize** — render it as an interactive, clickable network diagram in the browser

All four steps are fully working now, upload a file and see live results end to end.

---

## 🧱 Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Core analysis engine | **Python + NetworkX + python-louvain** | Industry-standard graph algorithms, fast to prototype |
| Backend API | **FastAPI** | Lightweight, connects the Python engine to the web app |
| Frontend | **React (Vite)** | Builds the interactive webpage/dashboard |
| Graph rendering | **react-force-graph-2d** | Draws the interactive dot-and-line network |
| Data storage | CSV (v1) → **PostgreSQL** (planned) | Starting simple, upgrading as the project matures |

---

## 📂 Project Structure

```
nexustrace/
├── README.md
├── ROADMAP.md              → full project checklist, current + future versions
├── requirements.txt         → Python dependencies
├── .gitignore
├── generate_data.py         → synthetic CDR data generator (for testing without real data)
├── data/
│   ├── call_records.csv     → sample generated call records
│   └── graph_output.json    → sample analysis output (nodes, edges, clusters)
├── analyze_graph.py          → standalone script: run the full analysis from the command line
├── backend/
│   ├── __init__.py
│   ├── graph_engine.py       → reusable graph analysis functions
│   └── main.py                → FastAPI server exposing the engine as an API
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx, App.jsx, api.js, index.css
        └── components/         → UploadPanel, GraphView, SearchBar, PathFinder
```

---

## 🚀 Getting Started

### 1. Backend setup
```bash
pip install -r requirements.txt
python3 generate_data.py        # creates sample test data
uvicorn backend.main:app --reload
```
This starts the API server at `http://127.0.0.1:8000`. Visit `http://127.0.0.1:8000/docs` for an interactive test page of every endpoint.

### 2. Frontend setup
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
This starts the app at `http://localhost:5173`. Make sure the backend (step 1) is running at the same time.

### 3. Try it out
Open `http://localhost:5173`, upload `data/call_records.csv`, and you'll see the network graph with clusters colored, key numbers sized larger, and search/path-finding available in the sidebar.

---

## ✅ v1.0 — What's Included (Current Version)

| Feature | Status |
|---|---|
| Synthetic call-record data generator | ✅ Done |
| Data ingestion & normalization | ✅ Done |
| Graph construction (NetworkX) | ✅ Done |
| Community/cluster detection | ✅ Done |
| Centrality scoring (find key numbers) | ✅ Done |
| Shortest-path search between two numbers | ✅ Done |
| Backend API (FastAPI) | ✅ Done |
| Interactive graph visualization (frontend) | ✅ Done |
| Full end-to-end testing | 🔄 In progress |
| Demo video/GIF | 🔜 Planned |

Full detailed checklist (including every future version) is tracked in [`ROADMAP.md`](./ROADMAP.md).

---

## 🗺️ Roadmap — Future Episodes

This project is being built version by version — each one adding real, meaningful capability, not just polish.

| Version | Codename | What it adds |
|---|---|---|
| **v1.0** *(current)* | *Foundation* | Core graph engine — upload data, see connections, spot clusters, find key players |
| **v2.0** | *Timeline* | Time-based analysis — see how a network's calling pattern changes around key event dates; date-range filtering on the graph |
| **v3.0** | *Geo* | Tower-location based geo-clustering — visualize movement patterns and physical proximity between suspects |
| **v4.0** | *Fusion* | Combine CDR with IPDR (internet/app usage data) for a multi-source correlated view, not just calls |
| **v5.0** | *Signal* | Lightweight anomaly detection — flag numbers whose calling behavior suddenly changes (possible early warning indicator) |

> 💡 The vision: not just a call-graph viewer, but a full **investigation correlation platform** — this repo will grow into that, one solid version at a time.

---

## 🤝 Contributing

This is a student-built project, growing with the team. If you're a teammate:

1. Pull the latest code
2. Check [`ROADMAP.md`](./ROADMAP.md) for the current task list, pick something unchecked
3. Build it, test it against `data/call_records.csv`
4. Share your update — we'll merge progress together

---

## 👥 Team

*Jatin Solanki* (till now)

---

<div align="center">

**NexusTrace** — built for SIH, built to actually be useful.

</div>
