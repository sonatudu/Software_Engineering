"""
Compliance and Security Analysis Agent
Maps requirements to financial frameworks, detects regulatory gaps, and sets human approval gates.
Supports RBI PPI, RBI Digital Lending, PCI-DSS v4.0, GDPR/DPDP, and RBI Harmonization of TAT.
"""
from typing import List, Dict, Any, Optional
from agents.llm_client import LLMClient
from knowledge_base.regulations import FINANCIAL_REGULATIONS


class ComplianceAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def analyze_compliance(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Maps requirements to regulatory controls and identifies compliance gaps.
        """
        if not requirements:
            return {
                "compliance_mappings": [],
                "compliance_gaps": [],
                "mandatory_checkpoints": []
            }

        mappings = []
        gaps = []
        approval_checkpoints = []

        for req in requirements:
            stmt = req.get("statement", "").lower()
            cat = req.get("category", "")
            req_id = req.get("id", "")
            
            # Match against RBI PPI & UPI Interoperability
            if any(k in stmt for k in ["wallet", "ppi", "qr", "upi", "npci", "tiered kyc"]):
                mappings.append({
                    "req_id": req_id,
                    "regulation": "RBI PPI Master Directions & NPCI Directives",
                    "control_code": "RBI-PPI-MD-01 / NPCI-QR",
                    "control_desc": "Mandatory Tiered KYC balance limits & Interoperable QR code standards.",
                    "status": "COMPLIANT",
                    "confidence": 0.98
                })

            # Match against RBI Turnaround Time (TAT) for failed transactions
            if any(k in stmt for k in ["tat", "reversal", "reconciliation", "failed upi", "grievance"]):
                mappings.append({
                    "req_id": req_id,
                    "regulation": "RBI Harmonization of TAT (Failed Transactions)",
                    "control_code": "RBI-TAT-CIRC-629",
                    "control_desc": "Automated T+1 reconciliation & compensation reversal for failed digital transactions.",
                    "status": "COMPLIANT",
                    "confidence": 0.99
                })

            # Match against RBI Data Localization
            if any(k in stmt for k in ["domestic", "localization", "7 years", "worm"]):
                mappings.append({
                    "req_id": req_id,
                    "regulation": "RBI Data Localization Directive",
                    "control_code": "RBI-DATA-LOC-2018",
                    "control_desc": "End-to-end payment data & transaction logs stored strictly within domestic servers.",
                    "status": "COMPLIANT",
                    "confidence": 0.97
                })

            # Match against RBI Digital Lending
            if any(k in stmt for k in ["disburs", "kfs", "apr", "key fact", "loan", "borrower"]):
                mappings.append({
                    "req_id": req_id,
                    "regulation": "RBI Digital Lending Guidelines",
                    "control_code": "RBI-DL-01 / RBI-DL-03",
                    "control_desc": "Direct borrower bank account disbursal & Mandatory KFS disclosure.",
                    "status": "COMPLIANT",
                    "confidence": 0.98
                })
            
            # Match against PCI-DSS
            if any(k in stmt for k in ["mfa", "otp", "authentication", "tokeniz", "card", "payment", "mpin", "fingerprint", "biometric"]):
                mappings.append({
                    "req_id": req_id,
                    "regulation": "PCI-DSS v4.0 & Central Bank 2FA",
                    "control_code": "PCI-REQ-8 / 2FA-MANDATE",
                    "control_desc": "Mandatory Multi-Factor Authentication (biometric/MPIN) for high-value financial actions.",
                    "status": "COMPLIANT",
                    "confidence": 0.96
                })
            
            # Match against Audit & Basel
            if any(k in stmt for k in ["audit", "log", "retain", "score", "credit", "approval"]):
                mappings.append({
                    "req_id": req_id,
                    "regulation": "Basel III & Statutory Audit Norms",
                    "control_code": "BASEL-RISK-01 / AUD-04",
                    "control_desc": "Audit trail immutability and decision explainability.",
                    "status": "COMPLIANT",
                    "confidence": 0.94
                })

            # Check if high risk -> Human sign-off required
            if req.get("priority") == "Critical" or req.get("risk_level") == "Critical" or req.get("risk_level") == "High":
                approval_checkpoints.append({
                    "req_id": req_id,
                    "checkpoint": f"Mandatory sign-off on: {req.get('statement')[:70]}...",
                    "responsible_role": "Chief Information Security Officer (CISO) & Legal Counsel",
                    "gate_type": "Pre-Implementation Approval"
                })

        # Deduplicate mappings by (req_id, control_code)
        seen_map = set()
        unique_mappings = []
        for m in mappings:
            k = (m["req_id"], m["control_code"])
            if k not in seen_map:
                seen_map.add(k)
                unique_mappings.append(m)

        # Check for potential gaps in the requirements set
        all_stmts = " ".join([r.get("statement", "").lower() for r in requirements])
        
        if "erasure" not in all_stmts and "delete" not in all_stmts and "withdraw" not in all_stmts:
            gaps.append({
                "regulation": "GDPR / DPDP Privacy Act",
                "missing_control": "Right to Erasure / Consent Revocation (PRIV-01)",
                "risk": "Regulatory penalty for non-compliance with statutory privacy laws.",
                "recommendation": "Add a functional requirement allowing users to revoke data consent and request profile deletion."
            })
        
        if "disaster" not in all_stmts and "failover" not in all_stmts and "rpo" not in all_stmts:
            gaps.append({
                "regulation": "ISO 27001 / High Availability",
                "missing_control": "Business Continuity & Disaster Recovery (RPO/RTO)",
                "risk": "Prolonged financial service outage during cloud region disruption.",
                "recommendation": "Define Recovery Point Objective (RPO < 15 min) and automated multi-zone failover."
            })

        return {
            "compliance_mappings": unique_mappings,
            "compliance_gaps": gaps,
            "mandatory_checkpoints": approval_checkpoints
        }
