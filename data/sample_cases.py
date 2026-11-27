"""
Pre-loaded Financial Sector Case Studies
Provides rich sample inputs for instant, robust demo presentations.
"""

SAMPLE_CASES = {
    "custom_blank": {
        "title": "🆕 Blank Custom Project (Live Interactive Interview)",
        "domain": "Custom Financial Banking",
        "description": "Start a fresh, interactive requirement gathering session from scratch with no pre-loaded text.",
        "raw_stakeholder_input": "",
        "default_factors": {
            "req_stability": 6,
            "reg_criticality": 8,
            "security_risk": 8,
            "complexity": 7,
            "change_freq": 6,
            "cd_need": 7,
            "stakeholder_avail": 7,
            "failure_consequence": 8
        }
    },
    "p2p_wallet": {
        "title": "Peer-to-Peer Mobile Wallet & UPI Payment Platform",
        "domain": "Digital Payments / PPI (Prepaid Instruments)",
        "description": "High-throughput mobile wallet platform with tiered KYC limits up to $5,000, NPCI/UPI QR code interoperability, biometric MFA, and RBI TAT compliance.",
        "raw_stakeholder_input": """
Product Owner: We want to build a peer-to-peer mobile wallet where users can store up to $5,000, send money via QR codes, and withdraw to their bank account.
Compliance Officer: The system must operate under RBI Prepaid Payment Instrument (PPI) regulations with tiered KYC: Basic KYC allows up to $1,000 balance, and Full Video-KYC unlocks $5,000. All transaction logs and audit trails must be retained for 7 years on domestic Indian servers.
Security Architect: Low-value payments under $50 can use 4-digit MPIN or fingerprint. High-value transfers up to $5,000 require Multi-Factor Authentication (biometric + MPIN). Withdrawals over $2,500 enforce a 30-minute cooling period.
Operations Lead: The platform must support interoperable NPCI/UPI QR codes, 1,000 TPS peak load with 99.99% uptime, and automated T+1 reconciliation with RBI TAT compensation for failed transactions.
        """,
        "default_factors": {
            "req_stability": 5,
            "reg_criticality": 10,
            "security_risk": 10,
            "complexity": 8,
            "change_freq": 8,
            "cd_need": 9,
            "stakeholder_avail": 7,
            "failure_consequence": 10
        }
    },
    "loan_origination": {
        "title": "Digital Loan Origination & Instant Credit Assessment",
        "domain": "Retail Banking / Lending",
        "description": "An end-to-end mobile and web platform where retail borrowers apply for personal loans up to $25,000, undergo instant automated credit scoring, and receive loan disbursements within 15 minutes.",
        "raw_stakeholder_input": """
Business Analyst: We need an instant loan processing portal where retail customers can apply for unsecured loans up to $25,000. The customer uploads their government ID, salary slips, and bank statements.
Loan Officer: The system must pull credit bureau scores (e.g. CIBIL/Experian) and run an automated scoring algorithm. If score > 750 and debt-to-income < 40%, auto-approve immediately.
Borrower: I want the application process to be fast and intuitive. Once approved, money should be in my bank account in 10 minutes.
Compliance Officer: We must strictly follow Central Bank / RBI digital lending norms. Disbursals must go directly into the verified borrower's bank account, never through any third-party intermediary. All interest calculations, processing fees, and Annual Percentage Rate (APR) must be displayed in a Key Fact Statement (KFS) before the customer signs.
Infosec Specialist: All customer PII and financial docs must be encrypted at rest using AES-256 and in transit via TLS 1.3. For loan disbursements over $10,000, step-up two-factor authentication is required. All admin actions and loan decisions must have an immutable audit log retained for 7 years.
        """,
        "default_factors": {
            "req_stability": 6,       # Fairly stable business rules
            "reg_criticality": 9,     # Strict RBI / Financial Lending guidelines
            "security_risk": 9,       # Direct fund disbursement & PII data
            "complexity": 7,          # Credit bureau APIs, document OCR, risk engine
            "change_freq": 6,         # Moderate update cycle
            "cd_need": 8,             # Automated pipelines needed for rapid security patches
            "stakeholder_avail": 7,   # Good availability of BA and Risk officers
            "failure_consequence": 9  # High: illegal disbursement or regulatory penalties
        }
    },
    "kyc_onboarding": {
        "title": "Digital Customer Onboarding & Video KYC System",
        "domain": "Digital Banking / Identity Verification",
        "description": "Self-service customer onboarding system enabling new users to open zero-balance savings accounts using automated biometric verification and live Video-KYC with bank agents.",
        "raw_stakeholder_input": """
Product Manager: Customers should be able to open a verified bank account in under 8 minutes using their smartphone camera.
Customer: I want a quick video call with an agent without downloading any external software or waiting in long queues.
KYC Officer: During the live video session, the system must perform geo-tagging to ensure the customer is physically located within the national jurisdiction. Face match between live capture and ID photo must score at least 85% confidence.
Legal & Compliance: Under DPDP / GDPR regulations, customer biometric data cannot be permanently stored on cloud servers without explicit informed consent. Video recordings must be stored in encrypted domestic storage for 5 years for audit.
Security Architect: Session must prevent Deepfake attacks and replay attacks using active liveness challenges (e.g. random blink or head turn). All transmission must be end-to-end encrypted.
        """,
        "default_factors": {
            "req_stability": 7,
            "reg_criticality": 10,
            "security_risk": 8,
            "complexity": 8,
            "change_freq": 5,
            "cd_need": 7,
            "stakeholder_avail": 8,
            "failure_consequence": 9
        }
    },
    "fraud_detection": {
        "title": "Real-Time Payment Gateway & Fraud Detection Engine",
        "domain": "Payment Processing / Card Networks",
        "description": "High-throughput payment gateway processing 10,000+ transactions per second with real-time ML-based anomaly detection and PCI-DSS compliance.",
        "raw_stakeholder_input": """
Merchant: We need checkout processing with latency under 150ms so shoppers don't abandon their carts.
Fraud Analyst: Transactions with risk score > 80 based on geolocation anomalies or velocity spikes must trigger immediate OTP challenge or decline.
Risk Officer: Chargeback fraud must be kept below 0.05% of total transaction volume.
Security Officer: Strict PCI-DSS v4.0 compliance is mandatory. Primary Account Numbers (PAN) must be tokenized; CVV numbers must never be written to persistent disks or memory logs.
Architect: The system must achieve 99.999% availability with automated multi-region failover.
        """,
        "default_factors": {
            "req_stability": 5,
            "reg_criticality": 9,
            "security_risk": 10,
            "complexity": 9,
            "change_freq": 8,
            "cd_need": 9,
            "stakeholder_avail": 6,
            "failure_consequence": 10
        }
    },
    "student_microlending": {
        "title": "Student Micro-Lending & Instant Credit (₹1,000 - ₹10,000)",
        "domain": "Digital Lending / Micro-Credit (RBI Regulated)",
        "description": "Instant digital micro-lending platform for university students offering credit from ₹1,000 to ₹10,000 within 5 minutes, compliant with RBI Digital Lending Directions, KFS mandates, and DPDP PII encryption.",
        "raw_stakeholder_input": """
Stakeholder: We want to build a Student Micro-Lending App that gives instant loans from ₹1,000 to ₹10,000 within 5 minutes using Aadhaar/PAN KYC and UPI auto-debit for repayment.
Compliance Officer: The loan tenure is 1 to 6 months. For missed repayments, we charge a flat penal charge of ₹50 without any compounding interest, strictly capped as per RBI Digital Lending Guidelines and Fair Practices Code.
Credit Risk Analyst: Credit scoring uses real-time bureau API (CIBIL score > 650) plus college ID verification and 3-month bank statement analysis. Before disbursement, an in-app Key Fact Statement (KFS) is presented with explicit digital consent, an email copy is dispatched, and a mandatory 3-day cooling-off period is provided for exit.
Security Architect: Audit trails are logged using append-only, tamper-evident hash chains stored for 7 years. All PII data is masked and encrypted using AES-256 at rest (Aadhaar Data Vault) and TLS 1.3 in transit. Third-party bureau APIs have a strict 3-second timeout SLA.
        """,
        "default_factors": {
            "req_stability": 7,
            "reg_criticality": 10,
            "security_risk": 9,
            "complexity": 8,
            "change_freq": 7,
            "cd_need": 8,
            "stakeholder_avail": 7,
            "failure_consequence": 9
        }
    }
}
