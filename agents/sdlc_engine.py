"""
SDLC Selection Engine and Workflow Generator
Implements Multi-Criteria Decision Analysis (MCDA) + Rule-Based Ranking + Workflow Customization.
"""
from typing import Dict, Any, List
from agents.llm_client import LLMClient
from knowledge_base.sdlc_rules import SDLC_MODELS


class SDLCEngine:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def derive_factors_from_dialogue(
        self,
        conversation_text: str,
        requirements: List[Dict[str, Any]],
        coverage_score: int,
        user_message_count: int = 1
    ) -> Dict[str, Any]:
        """
        Dynamically derives the 8 MCDA decision factors based on the depth, maturity,
        and specific architectural/regulatory constraints in the ongoing conversation.
        """
        t = conversation_text.lower() if conversation_text else ""
        
        # 1. Requirement Stability (1 to 10)
        # Low/volatile early on, rises as dialogue and requirement coverage expand
        if user_message_count <= 1:
            req_stability = 4
        elif user_message_count == 2:
            req_stability = 6
        elif coverage_score >= 80 and len(requirements) >= 5:
            req_stability = 9
        elif coverage_score >= 50:
            req_stability = 7
        else:
            req_stability = 5

        # 2. Regulatory Criticality (1 to 10)
        reg_criticality = 4 if user_message_count <= 1 else 6
        if any(k in t for k in ["rbi", "central bank", "pci", "gdpr", "dpdp", "pmla"]):
            reg_criticality += 3
        if any(k in t for k in ["localization", "tat", "turnaround", "worm", "7 years", "v-cip"]):
            reg_criticality += 2
        reg_criticality = min(10, max(2, reg_criticality))

        # 3. Security & Financial Risk (1 to 10)
        security_risk = 5 if user_message_count <= 1 else 6
        if any(k in t for k in ["wallet", "disburs", "$5,000", "$25,000", "loan", "card", "fund", "money"]):
            security_risk += 2
        if any(k in t for k in ["mfa", "biometric", "cooling period", "tokeniz", "mpin", "otp", "fido"]):
            security_risk += 2
        if any(k in t for k in ["velocity", "fraud", "anomaly", "lock"]):
            security_risk += 1
        security_risk = min(10, max(3, security_risk))

        # 4. Technical Complexity (1 to 10)
        complexity = 5
        if any(k in t for k in ["tps", "throughput", "latency", "1,000", "10,000", "< 200ms", "200 ms"]):
            complexity += 2
        if any(k in t for k in ["distributed", "consensus", "state machine", "redis", "rto", "rpo"]):
            complexity += 2
        if any(k in t for k in ["interoperab", "qr", "upi", "npci", "face match"]):
            complexity += 1
        complexity = min(10, max(3, complexity))

        # 5. Frequency of Expected Changes (1 to 10)
        change_freq = 7
        if any(k in t for k in ["wallet", "consumer", "mobile", "p2p", "qr"]):
            change_freq = 8
        if any(k in t for k in ["core banking", "fixed"]):
            change_freq = 4

        # 6. Need for Continuous Delivery (CI/CD) (1 to 10)
        cd_need = 6 if user_message_count <= 1 else 7
        if any(k in t for k in ["99.99%", "uptime", "failover", "resilien", "cloud", "saas"]):
            cd_need += 2
        if any(k in t for k in ["ci/cd", "pipeline", "security gate", "sast", "automated test"]):
            cd_need += 2
        cd_need = min(10, max(4, cd_need))

        # 7. Stakeholder Availability (1 to 10)
        stakeholder_avail = min(9, 6 + user_message_count)

        # 8. Consequences of System Failure (1 to 10)
        failure_consequence = 5 if user_message_count <= 1 else 7
        if any(k in t for k in ["financial loss", "rbi", "penalty", "compensation", "pmla", "audit"]):
            failure_consequence += 2
        if any(k in t for k in ["rto", "disaster", "failover", "zero loss", "rpo", "consensus"]):
            failure_consequence += 2
        failure_consequence = min(10, max(3, failure_consequence))

        derived = {
            "req_stability": req_stability,
            "reg_criticality": reg_criticality,
            "security_risk": security_risk,
            "complexity": complexity,
            "change_freq": change_freq,
            "cd_need": cd_need,
            "stakeholder_avail": stakeholder_avail,
            "failure_consequence": failure_consequence
        }

        explanations = {
            "req_stability": f"Turn {user_message_count} maturity ({coverage_score}% coverage)",
            "reg_criticality": "Elevated by RBI/PMLA/DPDP statutory mandates" if reg_criticality >= 8 else "General financial regulation",
            "security_risk": "High-value fund transfers & Biometric MFA gates" if security_risk >= 8 else "Baseline financial risk",
            "complexity": "1,000+ TPS, distributed state & sub-200ms SLAs" if complexity >= 8 else "Standard modular services",
            "failure_consequence": "Direct balance liabilities & RBI TAT penalties" if failure_consequence >= 8 else "Standard operational impact"
        }

        return {
            "factors": derived,
            "explanations": explanations
        }

    def evaluate_sdlc(self, factors: Dict[str, int]) -> Dict[str, Any]:
        """
        Calculates ranked suitability percentages for SDLC models using MCDA scoring.
        factors: dict mapping factor_id -> rating (1 to 10 scale).
        """
        # Factor extraction with safe defaults
        req_stability = factors.get("req_stability", 5)
        reg_criticality = factors.get("reg_criticality", 8)
        security_risk = factors.get("security_risk", 8)
        complexity = factors.get("complexity", 7)
        change_freq = factors.get("change_freq", 6)
        cd_need = factors.get("cd_need", 7)
        stakeholder_avail = factors.get("stakeholder_avail", 7)
        failure_consequence = factors.get("failure_consequence", 8)

        # 1. Agile-DevSecOps Hybrid
        # Thrives on high change frequency, high security risk, high CD need, moderate/high regulation
        devsecops_score = (
            (change_freq * 2.0) +
            (security_risk * 2.5) +
            (cd_need * 2.5) +
            (stakeholder_avail * 1.5) +
            (reg_criticality * 1.5)
        ) # max ~ 100
        devsecops_pct = min(98, max(45, int(devsecops_score)))

        # 2. V-Model (Verification & Validation)
        # Thrives on high regulation, catastrophic failure consequences, stable specs, low change freq
        vmodel_score = (
            (reg_criticality * 2.5) +
            (failure_consequence * 2.5) +
            (req_stability * 2.0) +
            (security_risk * 1.5) +
            ((10 - change_freq) * 1.5)
        )
        vmodel_pct = min(96, max(38, int(vmodel_score)))

        # 3. Spiral Model
        # Thrives on high technical complexity, novel algorithms, high risk
        spiral_score = (
            (complexity * 3.0) +
            (failure_consequence * 2.5) +
            ((10 - req_stability) * 2.0) +
            (security_risk * 1.5) +
            (10)
        )
        spiral_pct = min(92, max(40, int(spiral_score)))

        # 4. Pure Agile (Scrum / Kanban)
        # Thrives on high change frequency, high stakeholder availability, low requirement freezing
        agile_score = (
            (change_freq * 2.8) +
            (stakeholder_avail * 2.5) +
            (cd_need * 2.2) +
            ((10 - req_stability) * 1.5) +
            ((10 - reg_criticality) * 1.0)
        )
        agile_pct = min(95, max(35, int(agile_score)))

        # 5. Waterfall
        # Thrives only on rigid stability, low change frequency, document-heavy environments
        waterfall_score = (
            (req_stability * 3.5) +
            ((10 - change_freq) * 3.0) +
            (reg_criticality * 1.5) +
            ((10 - cd_need) * 2.0)
        )
        waterfall_pct = min(90, max(20, int(waterfall_score)))

        raw_rankings = [
            {"model": "Agile-DevSecOps Hybrid", "score": devsecops_pct, "info": SDLC_MODELS["Agile-DevSecOps Hybrid"]},
            {"model": "V-Model (Verification & Validation)", "score": vmodel_pct, "info": SDLC_MODELS["V-Model (Verification & Validation)"]},
            {"model": "Spiral Model", "score": spiral_pct, "info": SDLC_MODELS["Spiral Model"]},
            {"model": "Agile (Scrum / Kanban)", "score": agile_pct, "info": SDLC_MODELS["Agile (Scrum / Kanban)"]},
            {"model": "Waterfall", "score": waterfall_pct, "info": SDLC_MODELS["Waterfall"]}
        ]

        # Sort descending by score
        ranked = sorted(raw_rankings, key=lambda x: x["score"], reverse=True)
        top_model = ranked[0]

        # Generate justification explanation
        explanation = self._generate_justification(top_model["model"], factors)

        return {
            "rankings": ranked,
            "recommended_model": top_model["model"],
            "recommended_score": top_model["score"],
            "justification": explanation,
            "customized_workflow": top_model["info"]["phases"],
            "mandatory_gates": top_model["info"]["mandatory_gates"]
        }

    def _generate_justification(self, model_name: str, factors: Dict[str, int]) -> str:
        if self.llm.is_active():
            prompt = f"""
Provide a concise, formal Software Engineering justification (3-4 sentences) explaining why '{model_name}' was selected as the optimal SDLC model for a financial project with:
- Regulatory Criticality: {factors.get('reg_criticality', 8)}/10
- Security & Financial Risk: {factors.get('security_risk', 8)}/10
- Frequency of Expected Changes: {factors.get('change_freq', 6)}/10
- Need for Continuous Delivery: {factors.get('cd_need', 7)}/10
Focus on risk mitigation, regulatory compliance gates, and iterative delivery agility.
"""
            res = self.llm.generate_text(prompt)
            if res:
                return res.strip()

        # Deterministic fallback justification
        if "DevSecOps" in model_name:
            return (
                f"The Agile–DevSecOps Hybrid model is selected because the financial project combines stringent security/compliance "
                f"criticality ({factors.get('reg_criticality', 8)}/10) with the operational necessity for continuous delivery ({factors.get('cd_need', 7)}/10). "
                f"By embedding automated SAST/DAST testing and compliance verification directly into iterative CI/CD pipelines, "
                f"the engineering team ensures continuous audit readiness without sacrificing agile sprint velocity."
            )
        elif "V-Model" in model_name:
            return (
                f"The V-Model is recommended due to exceptionally high regulatory criticality ({factors.get('reg_criticality', 9)}/10) "
                f"and strict verification requirements. Every specification phase is coupled with a rigorous bilateral testing phase, "
                f"minimizing defect slippage into production environments."
            )
        elif "Spiral" in model_name:
            return (
                f"The Spiral Model is chosen due to high technical complexity and novel algorithmic risk. Iterative prototype cycles "
                f"permit structured risk mitigation before capital allocation to full-scale development."
            )
        else:
            return f"The {model_name} provides the optimal balance of stakeholder collaboration and development velocity based on the assessed project characteristics."
