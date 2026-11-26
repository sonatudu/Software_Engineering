"""
Financial Knowledge Base: Regulatory Frameworks and Compliance Rules
Covers key standards: RBI Digital Lending, GDPR/DPDP, PCI-DSS v4.0, Basel III, ISO 27001.
"""

FINANCIAL_REGULATIONS = {
    "RBI_DIGITAL_LENDING": {
        "title": "RBI Digital Lending Guidelines (2022/2023)",
        "jurisdiction": "India / Banking Sector",
        "key_controls": [
            {
                "code": "RBI-DL-01",
                "clause": "Disbursals must be made directly to the borrower's bank account without pass-through accounts of third parties/LSPs.",
                "category": "Disbursement & Fund Flow"
            },
            {
                "code": "RBI-DL-02",
                "clause": "Prior explicit consent required for data collection; access to mobile phone resources (contacts, media, call logs) is strictly prohibited except one-time mic/camera for KYC.",
                "category": "Data Privacy & Consent"
            },
            {
                "code": "RBI-DL-03",
                "clause": "Key Fact Statement (KFS) including Annual Percentage Rate (APR) must be provided in standardized format before loan agreement execution.",
                "category": "Transparency & Consumer Protection"
            },
            {
                "code": "RBI-DL-04",
                "clause": "All financial transactions and data must be logged with tamper-proof audit trails stored within authorized domestic servers.",
                "category": "Audit & Data Localization"
            }
        ]
    },
    "PCI_DSS_V4": {
        "title": "PCI-DSS v4.0 (Payment Card Industry Data Security Standard)",
        "jurisdiction": "Global / Payment Systems",
        "key_controls": [
            {
                "code": "PCI-REQ-3",
                "clause": "Protect stored account data: Primary Account Numbers (PAN) must be masked, hashed, or tokenized; CVV/CVC must never be stored post-authorization.",
                "category": "Data Protection"
            },
            {
                "code": "PCI-REQ-8",
                "clause": "Multi-Factor Authentication (MFA) is mandatory for all administrative access and access into cardholder data environments.",
                "category": "Authentication"
            },
            {
                "code": "PCI-REQ-10",
                "clause": "Log and monitor all access to system components and cardholder data; retain audit logs for at least one year.",
                "category": "Audit & Monitoring"
            }
        ]
    },
    "GDPR_DPDP": {
        "title": "GDPR / DPDP Act (Data Protection & Privacy)",
        "jurisdiction": "Global / Digital Data Privacy",
        "key_controls": [
            {
                "code": "PRIV-01",
                "clause": "Right to erasure / data deletion and right to withdraw consent must be available through self-service or verified request.",
                "category": "Data Subject Rights"
            },
            {
                "code": "PRIV-02",
                "clause": "Principle of data minimization: only retain customer financial data for the duration legally mandated by anti-money laundering (AML) laws.",
                "category": "Data Retention"
            },
            {
                "code": "PRIV-03",
                "clause": "Mandatory breach notification within 72 hours of becoming aware of unauthorized personal data exposure.",
                "category": "Incident Response"
            }
        ]
    },
    "BASEL_III": {
        "title": "Basel III Operational Risk & Capital Adequacy Framework",
        "jurisdiction": "International Banking",
        "key_controls": [
            {
                "code": "RISK-01",
                "clause": "Automated credit risk assessment models must provide explainable score outputs with human override authority above risk threshold.",
                "category": "Credit Risk & Governance"
            },
            {
                "code": "RISK-02",
                "clause": "Real-time automated transaction limits and anomaly screening before clearing high-value settlements.",
                "category": "Operational Risk"
            }
        ]
    }
}

QUALITY_DEFECT_PATTERNS = [
    {
        "pattern_name": "Ambiguous Latency / Performance",
        "keywords": ["fast", "quick", "as soon as possible", "instant", "reasonable"],
        "issue": "Vague performance adjective. Lacks measurable test criteria (e.g. '< 200ms latency at 99th percentile')."
    },
    {
        "pattern_name": "Undefined User Role",
        "keywords": ["someone", "user can", "anyone", "the party"],
        "issue": "Undefined stakeholder role. Requires specific RBAC role (e.g., 'Borrower', 'Underwriter', 'Compliance Auditor')."
    },
    {
        "pattern_name": "Missing Security & Audit",
        "keywords": ["save", "store loan", "submit payment", "delete record"],
        "negative_check": ["audit", "log", "encrypt", "authorize"],
        "issue": "Financial action without explicit audit logging, authentication gate, or encryption control."
    },
    {
        "pattern_name": "Subjective Reliability",
        "keywords": ["bug free", "100% secure", "never fails", "always available"],
        "issue": "Infeasible / non-testable absolute claim. Needs formal SLA (e.g., '99.99% uptime with RPO < 15m, RTO < 1h')."
    }
]
