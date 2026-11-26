# 🎓 Viva & Oral Defense Q&A Guide
### Project: Agentic AI Requirements Engineering & SDLC Advisory Workbench
**Course:** Software Engineering Mini-Project  
**Domain:** Financial Technology & Agentic AI  

---

### Q1: What is the core problem your project addresses?
**Answer:**  
In the financial sector, requirements gathering is traditionally manual, time-consuming, and prone to costly errors like ambiguous specifications, regulatory omissions (e.g., RBI guidelines, PCI-DSS), and mismatched SDLC processes. Our project develops an **Agentic AI Workbench** where autonomous, specialized AI agents collaborate to conduct adaptive stakeholder interviews, extract structured IEEE 830 requirements, detect ambiguities, enforce financial regulatory compliance, and mathematically recommend the optimal SDLC model using Multi-Criteria Decision Analysis (MCDA).

---

### Q2: Why did you use a Multi-Agent architecture instead of a single LLM prompt?
**Answer:**  
Single-prompt LLMs suffer from prompt crowding, hallucinations, and lack of specialized validation. A multi-agent system uses the **Separation of Concerns (SoC)** principle:
1. **Interaction Agent:** Focuses purely on conversational stakeholder interviewing and adaptive follow-up questioning.
2. **Extraction Agent:** Focuses strictly on syntactic structuring into IEEE 830 standards and Gherkin acceptance criteria.
3. **Compliance Agent:** Focuses on regulatory cross-referencing against banking laws (RBI, PCI-DSS, GDPR).
4. **SDLC Engine:** Uses mathematical multi-criteria decision rules rather than generic guesses.
5. **Coordinator Agent:** Orchestrates state and approval gates.
This modularity ensures explainability, citation accuracy, and independent verification.

---

### Q3: How do you prevent LLM hallucinations in a safety-critical banking domain?
**Answer:**  
We employ a four-tier defense:
1. **Retrieval-Augmented Grounding (RAG):** The model is constrained to an authoritative financial knowledge base containing verified regulatory clauses.
2. **Deterministic Quality Rules:** Algorithmic regex checks for non-testable claims (*"fast"*, *"100% bug-free"*) and undefined roles.
3. **Confidence Scoring:** Every extracted requirement and compliance mapping receives a confidence score (0.0–1.0).
4. **Mandatory Human-in-the-Loop (HITL) Gates:** High-risk actions (e.g., loan disbursals > $10,000, PII deletion) cannot proceed without explicit CISO/Compliance Officer sign-off.

---

### Q4: How does your SDLC Selection Engine work? What algorithm is used?
**Answer:**  
It uses **Multi-Criteria Decision Analysis (MCDA)** combined with deterministic heuristic weighting across **13 project factors** derived from the IEEE standards (e.g., Requirement Stability, Regulatory Criticality, Security Risk, Frequency of Changes, Continuous Delivery Need).  
The engine computes suitability percentages:
$$\text{Score}(M) = \sum_{i=1}^{n} w_{i, M} \cdot f_i$$
Where $f_i$ is the project factor score (1–10) and $w_{i, M}$ is the weight matrix for each SDLC model $M$.
For instance, when *Regulatory Criticality* is high (9/10) and *Continuous Delivery Need* is high (8/10), the engine recommends an **Agile-DevSecOps Hybrid** because it embeds automated security gates (SAST/DAST) into rapid sprint pipelines.

---

### Q5: What specific financial regulations does your system verify?
**Answer:**  
1. **RBI Digital Lending Guidelines (2022/2023):** Mandates direct disbursement to borrower bank accounts (no third-party pass-through) and Key Fact Statement (KFS) disclosure with Annual Percentage Rate (APR).
2. **PCI-DSS v4.0:** Requires Multi-Factor Authentication (MFA) for administrative actions, PAN tokenization, and strict prohibition on post-authorization CVV storage.
3. **GDPR / DPDP Act:** Enforces data minimization, consent revocation, and right to erasure (PRIV-01).
4. **Basel III Framework:** Mandates explainable automated credit decisions with human override capability for high-risk loans.

---

### Q6: What artifacts does the system generate?
**Answer:**  
1. **IEEE 830-1998 Compliant SRS Document:** Complete with Purpose, System Scope, Functional & Non-Functional specifications.
2. **User Stories & Acceptance Criteria:** Written in formal BDD Gherkin format (*Given... When... Then...*).
3. **Requirements Traceability Matrix (RTM):** Mapping each requirement ID to its source stakeholder, design module, test case reference, and sign-off gate.
4. **Customized SDLC Phase Workflow:** Detailed phase-by-phase activities and quality exit gates.

---

### Q7: What technology stack is used in the implementation?
**Answer:**  
* **Frontend UI:** Streamlit with Plotly for dynamic SDLC radar/bar analytics and responsive metrics.
* **Backend Multi-Agent Framework:** Python 3.12 with asynchronous orchestration.
* **LLM Engine:** Google GenAI SDK (`gemini-2.5-flash`) for live contextual reasoning, paired with a local deterministic rule-based fallback for 100% offline uptime.
* **Knowledge Base:** Structured regulatory vectors and rule dictionaries.

---

### Q8: What happens if there is no internet during the evaluation?
**Answer:**  
The architecture includes an automatic **Fail-Safe Deterministic Demo Mode**. If no API key or network is present, the Coordinator Agent switches to local heuristic extraction, maintaining full UI functionality, chart generation, and document export with zero downtime.
