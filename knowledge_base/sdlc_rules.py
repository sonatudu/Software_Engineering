"""
SDLC Selection Engine Knowledge Base:
Defines the 13 Decision Factors from the Problem Statement and Multi-Criteria Decision Analysis (MCDA) weights.
"""

SDLC_MODELS = {
    "Agile-DevSecOps Hybrid": {
        "tagline": "Continuous delivery with automated security controls and iterative release cycles.",
        "best_for": "Fintech platforms requiring rapid feature updates, high security automation, and CI/CD audit trails.",
        "phases": [
            "1. Sprint Planning & Threat Modeling",
            "2. Iterative Secure Coding & SAST/DAST Automated Scans",
            "3. CI/CD Automated Testing (Unit, Integration, Security)",
            "4. Regulatory Automated Compliance Checkpoints",
            "5. Production Canary Deployment & Zero-Downtime Monitoring",
            "6. Sprint Retrospective & Continuous Audit Feedback"
        ],
        "mandatory_gates": [
            "Automated Static Analysis (SAST) zero critical vulnerability gate",
            "Peer code review + Architecture approval",
            "Automated compliance test suite pass",
            "Infosec sign-off on pipeline secrets management"
        ]
    },
    "V-Model (Verification & Validation)": {
        "tagline": "Rigorous bilateral testing mapping each specification phase directly to a validation phase.",
        "best_for": "Core banking engines, settlement networks, and mission-critical financial systems requiring zero-defect validation.",
        "phases": [
            "1. Requirements Analysis <---> Acceptance Testing",
            "2. System Specification <---> System & Security Testing",
            "3. High-Level Architecture <---> Integration Testing",
            "4. Detailed Module Design <---> Unit Testing",
            "5. Coding & Implementation Gate"
        ],
        "mandatory_gates": [
            "Traceability Matrix 100% test coverage sign-off",
            "Independent V&V (IV&V) compliance audit",
            "User Acceptance Testing (UAT) executive sign-off"
        ]
    },
    "Spiral Model": {
        "tagline": "Risk-driven iterative cycles with progressive prototyping and cost evaluation.",
        "best_for": "Novel financial products, experimental AI credit scoring algorithms, or high technical ambiguity.",
        "phases": [
            "Cycle 1: Objectives & Feasibility Analysis",
            "Cycle 2: Risk Assessment & Algorithm Prototype",
            "Cycle 3: Architectural Design & Security Benchmarking",
            "Cycle 4: Final Product Development, Testing, and Deployment"
        ],
        "mandatory_gates": [
            "Milestone risk review checkpoint at end of each spiral loop",
            "Go/No-Go investment committee evaluation"
        ]
    },
    "Agile (Scrum / Kanban)": {
        "tagline": "Adaptive, collaborative, customer-centric iterations delivering working software in sprints.",
        "best_for": "Customer-facing digital banking frontends with frequent UX improvements and active product owners.",
        "phases": [
            "1. Product Backlog Refinement",
            "2. Sprint Planning (1-2 weeks)",
            "3. Daily Standups & Feature Development",
            "4. Sprint Review & Stakeholder Demo",
            "5. Sprint Retrospective"
        ],
        "mandatory_gates": [
            "Definition of Done (DoD) verification",
            "Product Owner demo acceptance"
        ]
    },
    "Waterfall": {
        "tagline": "Sequential, document-heavy development with strict phase gates and upfront requirement freezing.",
        "best_for": "Fixed-scope compliance reporting tools with unalterable statutory requirements and rigid external deadlines.",
        "phases": [
            "1. Requirements Analysis & Formal SRS Freezing",
            "2. System Design & Architectural Specification",
            "3. Implementation & Unit Testing",
            "4. System Integration & Acceptance Testing",
            "5. Deployment & Maintenance"
        ],
        "mandatory_gates": [
            "Formal baseline sign-off by all Department Heads before design begins",
            "Formal change control board approval for any scope revision"
        ]
    }
}

DECISION_FACTORS = [
    {"id": "req_stability", "name": "Requirement Stability", "low": "Frequently Changing", "high": "Completely Fixed / Frozen"},
    {"id": "reg_criticality", "name": "Regulatory & Compliance Criticality", "low": "Internal / Low Regulation", "high": "Strict Central Bank / RBI / GDPR"},
    {"id": "security_risk", "name": "Security & Financial Risk", "low": "Low Impact", "high": "Severe / Direct Fund Flow Risk"},
    {"id": "complexity", "name": "Project & Technical Complexity", "low": "Simple CRUD", "high": "Distributed / Real-Time / AI"},
    {"id": "change_freq", "name": "Expected Frequency of Changes", "low": "Rare (Annual)", "high": "Frequent (Weekly / Bi-weekly)"},
    {"id": "cd_need", "name": "Need for Continuous Delivery (CI/CD)", "low": "Not required", "high": "Essential for business"},
    {"id": "stakeholder_avail", "name": "Stakeholder Availability for Sprints", "low": "Busy / Hands-off", "high": "Daily active collaboration"},
    {"id": "failure_consequence", "name": "Consequences of System Failure", "low": "Minor inconvenience", "high": "Catastrophic financial / legal penalty"}
]
