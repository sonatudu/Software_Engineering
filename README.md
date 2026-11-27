# 🏦 Agentic AI Requirements Engineering & SDLC Advisory Workbench

An autonomous multi-agent platform for automated requirement gathering, analysis, regulatory compliance verification, and SDLC model selection in the financial sector. Built directly according to the course problem statement specifications.

---

## 🚀 Quick Start (Running the App)

The virtual environment and dependencies are already installed in `venv`. To launch the web application:

```bash
# Activate virtual environment
source venv/bin/activate

# Launch the Streamlit application
streamlit run app.py
```

The application will start immediately and open in your browser at:
**`http://localhost:8501`**

---

## 🎯 What This System Solves

Gathering software requirements for financial institutions (banks, lending platforms, payment gateways) is traditionally slow, ambiguous, and carries severe regulatory risks. 

This platform uses a **Collaborative Multi-Agent Architecture** to:
1. **Conduct Adaptive Stakeholder Interviews:** Discovers hidden requirements and asks context-aware follow-up questions across 6 core financial dimensions.
2. **Extract & Structure Requirements:** Formats unstructured stakeholder dialogue into standard IEEE 830 functional and non-functional requirements with Gherkin acceptance criteria.
3. **Inspect Requirement Quality:** Automatically detects ambiguities (e.g. "fast response"), untestable assertions, and missing security controls.
4. **Enforce Financial Compliance (RAG-Grounded):** Maps requirements directly against **RBI Digital Lending Guidelines**, **PCI-DSS v4.0**, **GDPR/DPDP**, and **Basel III**. Detects compliance gaps and sets mandatory human approval gates.
5. **Recommend Optimal SDLC Models:** Evaluates 13 project decision factors using Multi-Criteria Decision Analysis (MCDA) to rank models (Agile-DevSecOps, V-Model, Spiral, Agile, Waterfall) with customized workflows.
6. **Export Formal Documentation:** Generates complete, downloadable IEEE 830 **Software Requirements Specification (SRS)** and **Requirements Traceability Matrix (RTM)**.

---

## 🤖 Multi-Agent Architecture

| Agent | Responsibility |
| :--- | :--- |
| **Coordinator Agent** | Manages session flow, orchestrates agent execution order and shared context. |
| **Interaction & Clarification Agent** | Evaluates requirement coverage and conducts dynamic follow-up questioning. |
| **Extraction & Quality Agent** | Parses requirements into structured cards and flags defects (ambiguities, testability). |
| **Compliance & Security Agent** | Maps statements to RBI, PCI-DSS, and GDPR regulations; flags regulatory gaps. |
| **SDLC Selection Engine** | Computes MCDA suitability scores, generates engineering justifications and workflows. |
| **Documentation Agent** | Generates exportable IEEE 830 SRS markdown and Requirements Traceability Matrices. |

---

## ⚡ Execution Modes & 100% Free AI Engine Support

The system supports multiple **100% free AI engines** (requiring zero payment or credit card) with automatic fallback resiliency:

1. **Google Gemini (Free Cloud Tier):** High-speed interactive elicitation via `gemini-2.0-flash` and `gemini-1.5-flash` with dynamic model discovery.
2. **Groq Cloud (Free Open-Source Powerhouse):** Ultra-high-speed inference hosting Meta's flagship **Llama 3.3 70B**, **DeepSeek-R1 Distill 70B** (for deep regulatory reasoning), and **Llama 3.1 8B**.
3. **Local Ollama (100% Free & Air-Gapped):** Connects to on-premise Ollama instances (`http://localhost:11434`) running `llama3.2`, `mistral`, or `deepseek-r1`. Zero API keys needed, ensuring 100% data sovereignty compliant with **RBI Data Localization** and GDPR mandates.
4. **Free Multi-Model Ensemble (Hybrid Collaborative AI):** Dynamically assigns specialized free models across agents:
   * *Interview Agent:* Llama 3.1 8B / Gemini Flash (Low latency conversational flow)
   * *Compliance Agent:* DeepSeek-R1 Distill 70B (Chain-of-thought regulatory parsing)
   * *Extraction Agent:* Llama 3.3 70B (High-precision structured IEEE 830 JSON)
5. **Deterministic Rule Engine (Offline Fail-Safe):** In offline or disconnected environments, rule-based heuristic parsing and domain expert knowledge bases run seamlessly with zero crashes.

---

## 📁 Project Structure

```
Software_Engineering/
├── app.py                     # Main Streamlit web dashboard
├── agents/                    # Multi-agent system implementations
│   ├── llm_client.py          # Google GenAI SDK wrapper & fallback handler
│   ├── interaction_agent.py   # Adaptive interview & clarification agent
│   ├── extraction_agent.py    # Structured extraction & quality defect analyzer
│   ├── compliance_agent.py    # Financial compliance & human approval gates
│   ├── sdlc_engine.py         # MCDA SDLC decision engine & workflow generator
│   └── documentation_agent.py # IEEE 830 SRS and RTM generator
├── knowledge_base/            # Domain knowledge & rule bases
│   ├── regulations.py         # RBI, PCI-DSS, GDPR, Basel III controls
│   └── sdlc_rules.py          # 13 decision factors & SDLC model profiles
├── data/
│   └── sample_cases.py        # Pre-loaded financial case studies (Wallet, Loan, KYC, Fraud)
├── requirements.txt           # Python package dependencies
├── Problem Statement.docx     # Course project problem statement
└── README.md                  # System documentation & quickstart guide
```

---

## 🖥️ System Walkthrough & Operational Workflow

1. **Launch the Workbench:** Execute `streamlit run app.py` to start the interactive web application.
2. **Domain Case Initialization:** Select a pre-configured financial case study from the sidebar (e.g., *Peer-to-Peer Mobile Wallet*, *Digital Loan Origination*, or *Video-KYC*) or begin a fresh session via *Blank Custom Project*.
3. **Module 1 (Adaptive Elicitation):** Engage in dynamic stakeholder dialogue while tracking the real-time 6-dimension requirement coverage meter.
4. **Module 2 (Structured Requirements):** Inspect structured IEEE 830 requirement cards, Gherkin acceptance criteria (*Given... When... Then...*), and automated ambiguity defect inspections.
5. **Module 3 (Regulatory Grounding):** Review automated compliance mappings against RBI PPI Directions, RBI Data Localization, PCI-DSS v4.0, and DPDP mandates.
6. **Module 4 (SDLC Decision Engine):** Examine dialogue-derived MCDA suitability rankings, interact with decision factor sliders, and review customized SDLC workflows.
7. **Module 5 (SRS & RTM Export):** Preview and export publication-grade IEEE 830 Software Requirements Specifications and Traceability Matrices.
