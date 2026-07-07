# TRU: Sovereign, Edge-Capable Offline Intelligence
> **Truth is constant. Perspective is fluid.**
> *Public Architectural Snapshot · July 2026*

TRU is a secure, offline-first knowledge engine engineered for resilient cognitive processing in zero-connectivity environments. Built on a strict zero-trust model, TRU separates immutable grounding data from fluid UI layers, ensuring absolute information integrity without cloud dependencies.

TRU is not a generic chatbot or a cloud-dependent API wrapper. It is a highly portable, self-contained software stack designed for mission-critical continuity when networks fail.

---

## 🛠️ The Architectural Stack

### 1. The Edge-Executable Artifact (Offline Engine)
A completely self-contained, browser-openable HTML/JS payload containing localized cognitive reasoning logic, data structures, and execution rules. 
* **Zero Dependencies:** Operates entirely from `file://` protocols on local disk.
* **Air-Gapped Portability:** Can be distributed via secure physical media, localized local area networks (LANs), or direct peer-to-peer transmission.

### 2. The Operational Work Surface (Live Node)
An interactive runtime console executed via localized user nodes (`Zo Site`) providing real-time data exploration, memory archiving, and audit workflows.

---

## 🛡️ Core Defense & Enterprise Capabilities

### 📡 Disconnected & Contested Operations (Edge AI)
Traditional AI systems collapse during network denial or infrastructure failure. TRU executes multi-source data retrieval, translation, and localized inference entirely on host hardware with zero outbound network calls.

### 🔒 Cryptographic Supply-Chain Verification
The system enforces a **Canonical Primary-Data Lock**. 
* **Boot-Time Tripwires:** During initialization, the system computes checksum validations across all immutable knowledge layers.
* **Tamper Refusal:** If local data structures show drift or unauthorized modification, the boot path immediately executes a hardware-isolated refusal protocol rather than risking compromised output.

### 🗂️ Verifiable Provenance & Deterministic Grounding
TRU eliminates behavioral hallucinations by binding its reasoning to explicitly indexed data packs (including language corpora, cross-references, and specialized historical/scientific text layers). The system names technical gaps rather than guessing when data is missing.

### 💾 Portable, Non-Volatile Memory
System state, localized user updates, and behavioral logs are structured in versioned, signed, and highly exportable SQLite/file-backed formats. Device migration requires zero centralized cloud syncing.

---

## 📊 System Overview at a Glance

| Layer | Technology Mapping | Operational Role |
| :--- | :--- | :--- |
| **Runtime** | Bun + Hono | High-throughput, localized edge execution |
| **Frontend** | React + Vite + Tailwind 4 | Resource-efficient, semantic presentation |
| **UI Primitives** | shadcn/ui + Lucide | Monospace-ready, scannable system console |
| **Storage** | SQLite + Local File Assets | Decentralized, portable memory structures |
| **Integrations** | Local Mail Hooks + Node APIs | Automated local notification & backup paths |
| **Security** | Primary-Data Verification | Anti-drift, anti-tamper initialization guards |

---

## 🚫 What TRU Is Not

* **Not a cloud-first SaaS framework** vulnerable to remote outages or data interception.
* **Not an ungrounded LLM wrapper** that invents factual metrics or technical specifications.
* **Not a transient session environment** that treats user-generated knowledge as disposable state.

---

## 🚪 Repository Status & Contact

The underlying source code for TRU is intentionally restricted to maintain operational integrity and prevent unauthorized distribution. 

**Looking to collaborate or review a technical capability brief?**
To discuss defensive deployment, edge-computing pilot programs, or private codebase inspection, please file a GitHub Issue requesting an encrypted communication channel or reach out through your project coordinator.
