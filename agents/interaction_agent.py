"""
Stakeholder Interaction & Adaptive Clarification Agent
Conducts dynamic requirement-gathering conversations, asking targeted follow-ups.
"""
from typing import List, Dict, Any, Optional
from agents.llm_client import LLMClient

CHECKLIST_DIMENSIONS = [
    {"name": "User Roles & Permissions", "keywords": ["role", "admin", "customer", "officer", "borrower", "stakeholder", "manager", "user", "underwriter"]},
    {"name": "Transaction Limits & Rules", "keywords": ["limit", "amount", "threshold", "$", "usd", "inr", "maximum", "loan", "000", "over", "up to"]},
    {"name": "Authentication & MFA", "keywords": ["mfa", "2fa", "otp", "biometric", "password", "authentication"]},
    {"name": "Compliance & Regulations", "keywords": ["rbi", "gdpr", "pci", "dpdp", "regulation", "compliance", "law", "central bank"]},
    {"name": "Audit Logs & Retention", "keywords": ["audit", "log", "retain", "years", "storage", "tamper", "record"]},
    {"name": "Performance & SLA", "keywords": ["ms", "second", "minute", "latency", "throughput", "uptime", "99.", "fast", "instant"]}
]


class InteractionAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def evaluate_coverage(self, conversation_text: str) -> Dict[str, Any]:
        """Calculates which dimensions have been covered in stakeholder dialogue."""
        text_lower = conversation_text.lower()
        covered = []
        missing = []
        for dim in CHECKLIST_DIMENSIONS:
            if any(k in text_lower for k in dim["keywords"]):
                covered.append(dim["name"])
            else:
                missing.append(dim["name"])
        
        score = int((len(covered) / len(CHECKLIST_DIMENSIONS)) * 100)
        return {
            "score": score,
            "covered": covered,
            "missing": missing
        }

    def generate_next_question(self, conversation_history: List[Dict[str, str]], context: str = "") -> str:
        """Generates an adaptive clarification or follow-up question."""
        conversation_str = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_history])
        
        if self.llm.is_active():
            prompt = f"""
You are an expert Requirements Engineering Assistant for the Financial Sector.
Review the following stakeholder input and conversation:

--- CONVERSATION ---
{conversation_str}
--------------------

Identify any vague, incomplete, or missing financial specifications (e.g. transaction limits, authentication gates, compliance laws like RBI/PCI-DSS, audit trails, latency SLAs).
Ask exactly ONE precise, polite, and technically rigorous follow-up question to clarify the missing requirements. Keep it under 2 sentences.
"""
            res = self.llm.generate_text(prompt, system_instruction="You are a Financial Requirements Engineering Agent.")
            if res:
                return res.strip()

        # Check if the user just sent a greeting
        last_user_msg = ""
        for m in reversed(conversation_history):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "").strip().lower()
                break
        
        greetings = ["hi", "hii", "hello", "hey", "hola", "good morning", "good evening", "greetings"]
        if last_user_msg in greetings or (len(last_user_msg.split()) <= 2 and any(g in last_user_msg for g in greetings)):
            return "Hello! I am your Financial Requirements Engineering Agent. What financial software system are you planning to build? (For example: a Digital Loan Origination platform, a Video-KYC onboarding app, or a Payment Gateway?)"

        # Offline deterministic fallback
        coverage = self.evaluate_coverage(conversation_str)
        if coverage["missing"]:
            next_topic = coverage["missing"][0]
            if next_topic == "Authentication & MFA":
                return "Could you specify what multi-factor authentication (MFA) or biometric controls are required for high-risk actions?"
            elif next_topic == "Transaction Limits & Rules":
                return "What are the exact financial transaction thresholds (e.g., maximum daily limit or amount requiring manual manager approval)?"
            elif next_topic == "Compliance & Regulations":
                return "Which specific regulatory jurisdictions or guidelines (e.g. RBI Digital Lending, GDPR, or PCI-DSS) must this system comply with?"
            elif next_topic == "Audit Logs & Retention":
                return "What are the specific requirements for transaction audit trails and data retention duration (e.g., 5 or 7 years)?"
            elif next_topic == "Performance & SLA":
                return "What target response latency and availability SLA (e.g., 99.99% uptime) is expected during peak load?"
            elif next_topic == "User Roles & Permissions":
                return "What distinct user roles (e.g., Customer, Underwriter, Compliance Officer, Super Admin) need access, and what are their privileges?"
        
        conv_lower = conversation_str.lower()
        if "legacy" in conv_lower or "core-banking" in conv_lower or "api" in conv_lower or "integrate" in conv_lower:
            if not any(k in conv_lower for k in ["month", "week", "schedule", "deadline", "quarter", "timeline"]):
                return "What is the expected project schedule or target launch timeline (e.g., MVP in 3 months)?"
            return "✅ Excellent! All core functional, security, compliance, integration, and schedule requirements have been successfully gathered. Please proceed to Tab 2 to review the structured specifications and Tab 4 for your customized SDLC roadmap!"
        
        return "Are there any legacy core-banking systems or third-party APIs that this solution must integrate with?"
