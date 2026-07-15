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

*(Demo GIF/video will go here once the UI is ready — coming in v1 finalization)*

``

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
4. **Visualize** — render it as an interactive, clickable network diagram

---

## 🧱 Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Core analysis engine | **Python + NetworkX** | Industry-standard graph algorithms, fast to prototype |
| Backend API | **FastAPI** | Lightweight, connects the Python engine to the web app |
| Frontend | **React** | Builds the interactive webpage/dashboard |
| Graph rendering | **react-force-graph / D3.js** | Draws the interactive dot-and-line network |
| Data storage | CSV (v1) → **PostgreSQL** (planned) | Starting simple, upgrading as the project matures |

---

## 📂 Project Structure

```
nexustrace/
├── data/                  → sample/synthetic datasets
├── generate_data.py       → synthetic CDR data generator (for testing without real data)
├── backend/                → API + graph analysis logic (coming next)
├── frontend/               → dashboard + visualization (coming next)
└── docs/                   → notes, architecture, demo media
```

---

## 🚀 Getting Started

> ⚠️ v1 is under active development. Setup instructions will be filled in as each piece is built.

```bash
# clone the repo
git clone <repo-url>
cd nexustrace

# generate sample test data
python3 generate_data.py
```

---

## ✅ v1.0 — What's Included (Current Version)

| Feature | Status |
|---|---|
| Synthetic call-record data generator | ✅ Done |
| Data ingestion & normalization | 🔄 In progress |
| Graph construction (NetworkX) | 🔜 Planned |
| Community/cluster detection | 🔜 Planned |
| Centrality scoring (find key numbers) | 🔜 Planned |
| Interactive graph visualization | 🔜 Planned |
| Shortest-path search between two numbers | 🔜 Planned |

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
2. Pick a piece from the current version's task list (ask in the group if unsure where to start)
3. Build it, test it against `data/call_records.csv`
4. Share your update — we'll merge progress together

---

## 👥 Team

*Jatin Solanki* (till now)

---

<div align="center">

**NexusTrace** — built for SIH, built to actually be useful.

</div>
