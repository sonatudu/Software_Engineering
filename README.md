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

## ⚡ Live AI Mode vs. Demo Mode (Zero-Risk Presentation)

* **Live AI Mode:** Enter any free Gemini API key in the sidebar. The app will communicate dynamically with Google Gemini (`gemini-2.5-flash`).
* **Deterministic Demo Mode (Fail-Safe):** If no API key is provided or internet connectivity drops, the system automatically uses smart heuristic reasoning and pre-loaded domain data. **Your demo will never crash in front of the professor.**

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
│   └── sample_cases.py        # Pre-loaded financial case studies (Loan, KYC, Fraud)
├── requirements.txt           # Python package dependencies
├── Problem Statement.docx     # Course project problem statement
└── README.md                  # System documentation & quickstart guide
```

---

## 🎤 How to Demo to Your Professor (3-Minute Script)

1. **Open the App:** Run `streamlit run app.py` and show the clean web dashboard.
2. **Select a Case Study:** Pick *"Digital Loan Origination & Instant Credit Assessment"* from the sidebar.
3. **Tab 1 (Interview):** Show the 6-dimension requirement coverage meter and chat with the AI agent asking follow-up questions about transaction limits and compliance.
4. **Tab 2 (Requirements):** Show the structured requirements table with categories, priorities, and Gherkin acceptance criteria. Point out the **Quality & Defect Analysis** section catching ambiguous terms.
5. **Tab 3 (Compliance):** Show the automated mapping to **RBI Digital Lending Guidelines** and **PCI-DSS**, and the **Human Approval Gates** for high-risk transfers.
6. **Tab 4 (SDLC Engine):** Adjust the **Regulatory Criticality** and **Continuous Delivery** sliders to show live recalculation of the SDLC chart (**Agile-DevSecOps Hybrid** ranked top). Show the tailored phase workflow.
7. **Tab 5 (Export):** Click **"Download Full SRS Document (.md)"** to show the complete IEEE 830 document ready for delivery.
