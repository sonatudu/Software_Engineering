"""
Agentic AI Requirements Engineering & SDLC Advisory Workbench
Built for Financial Sector Software Engineering Projects.
"""
import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

from agents.llm_client import LLMClient
from agents.interaction_agent import InteractionAgent
from agents.extraction_agent import ExtractionAgent
from agents.compliance_agent import ComplianceAgent
from agents.sdlc_engine import SDLCEngine
from agents.documentation_agent import DocumentationAgent
from data.sample_cases import SAMPLE_CASES
from knowledge_base.sdlc_rules import DECISION_FACTORS

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Agentic AI: Requirements & SDLC Workbench",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished financial engineering UI
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
    .card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
    .badge-critical { background-color: #FEE2E2; color: #991B1B; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-high { background-color: #FEF3C7; color: #92400E; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-medium { background-color: #E0E7FF; color: #3730A3; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .metric-box { background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px; text-align: center; }
</style>
""", unsafe_allow_html=True)


# ----------------- SESSION STATE SETUP -----------------
if "case_key" not in st.session_state:
    st.session_state.case_key = "loan_origination"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Load initial case study text if conversation is empty
current_case = SAMPLE_CASES[st.session_state.case_key]
if not st.session_state.messages:
    if current_case["raw_stakeholder_input"].strip():
        st.session_state.messages = [
            {"role": "user", "content": current_case["raw_stakeholder_input"].strip()},
            {"role": "assistant", "content": f"Hello! I am the Financial Requirements Engineering Agent. I have ingested the initial stakeholder inputs for '{current_case['title']}'. Would you like me to clarify any compliance thresholds, authentication rules, or audit log details before we generate the formal specifications?"}
        ]
    else:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your Financial Requirements Engineering Agent. Tell me about the banking system you want to build, and I will analyze it!"}
        ]

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=64)
    st.markdown("### 🏦 Financial Project Hub")
    
    selected_case = st.selectbox(
        "Choose Financial Case Study:",
        options=list(SAMPLE_CASES.keys()),
        format_func=lambda k: SAMPLE_CASES[k]["title"],
        index=list(SAMPLE_CASES.keys()).index(st.session_state.case_key)
    )

    # Handle project change
    if selected_case != st.session_state.case_key:
        st.session_state.case_key = selected_case
        case_data = SAMPLE_CASES[selected_case]
        if case_data["raw_stakeholder_input"].strip():
            st.session_state.messages = [
                {"role": "user", "content": case_data["raw_stakeholder_input"].strip()},
                {"role": "assistant", "content": f"Switched to '{case_data['title']}'. Requirements pipeline ready."}
            ]
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! Tell me about the financial system you want to build (e.g. loan limits, roles, rules) to begin the interview."}
            ]
        st.rerun()

    if st.button("🗑️ Clear / Start Fresh Chat", use_container_width=True):
        st.session_state.case_key = "custom_blank"
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared! Tell me about the banking system you want to build (e.g. mobile wallet, UPI payments, loan origination)."}
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 Agent Configuration")
    env_key = os.getenv("GEMINI_API_KEY", "").strip()
    api_key_input = st.text_input(
        "Gemini API Key (Optional):",
        value=env_key,
        type="password",
        help="Leave blank to run in robust Offline / Deterministic Demo Mode. Saved in .env so you don't have to re-enter."
    )
    
    # Auto-save key to .env if user enters a new one
    if api_key_input.strip() and api_key_input.strip() != env_key:
        if st.checkbox("💾 Remember key permanently in .env", value=True, help="Saves key locally to .env so it auto-loads every time you open the app."):
            try:
                with open(".env", "w") as f:
                    f.write(f"GEMINI_API_KEY={api_key_input.strip()}\n")
                os.environ["GEMINI_API_KEY"] = api_key_input.strip()
                st.toast("✅ Key saved to .env! You won't need to re-enter it.", icon="💾")
            except Exception as e:
                st.warning(f"Could not save .env: {e}")
    
    # Initialize agents
    llm = LLMClient(api_key=api_key_input)
    interaction_agent = InteractionAgent(llm)
    extraction_agent = ExtractionAgent(llm)
    compliance_agent = ComplianceAgent(llm)
    sdlc_engine = SDLCEngine(llm)
    doc_agent = DocumentationAgent()

    if llm.is_active():
        model_name = getattr(llm, "active_model", "gemini-2.0-flash")
        st.success(f"🟢 Live Gemini AI ({model_name}) Connected")
    elif api_key_input.strip() and getattr(llm, "last_error", ""):
        err = getattr(llm, "last_error", "")[:90]
        st.error(f"❌ Invalid API Key: Google returned '{err}...'")
        st.info("🔵 Running in Deterministic Demo Mode")
    else:
        st.info("🔵 Deterministic Demo Mode (Fail-Safe)")

    st.markdown("---")
    st.markdown("**Active Specialized Agents:**")
    st.markdown("✅ Coordinator Agent")
    st.markdown("✅ Interaction & Clarification Agent")
    st.markdown("✅ Extraction & Quality Agent")
    st.markdown("✅ Compliance & Security Agent")
    st.markdown("✅ SDLC Decision Engine")
    st.markdown("✅ Documentation (SRS) Agent")


# ----------------- MAIN TITLE -----------------
# Concatenate user inputs for complete analysis
full_conversation_text = "\n".join([m["content"] for m in st.session_state.messages if m["role"] == "user"])

# Dynamically infer active project title & domain from the conversation
if hasattr(extraction_agent, "infer_project_metadata"):
    proj_meta = extraction_agent.infer_project_metadata(full_conversation_text, current_case=current_case)
    active_title = proj_meta.get("title", current_case["title"])
    active_domain = proj_meta.get("domain", current_case["domain"])
else:
    active_title = current_case["title"]
    active_domain = current_case["domain"]

st.markdown('<div class="main-title">Agentic AI Requirements Engineering & SDLC Advisory</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Active Project: <b>{active_title}</b> ({active_domain})</div>', unsafe_allow_html=True)

# ----------------- RUN ANALYSIS PIPELINE -----------------
# Agent Extractions
extraction_result = extraction_agent.extract_and_analyze(full_conversation_text, case_key=st.session_state.case_key)
requirements = extraction_result["requirements"]
quality_issues = extraction_result["quality_issues"]

# Compliance Mapping
compliance_result = compliance_agent.analyze_compliance(requirements)

# Coverage & Dialogue Maturity Analysis
coverage = interaction_agent.evaluate_coverage(full_conversation_text)
user_message_count = len([m for m in st.session_state.messages if m["role"] == "user"])

# Dynamically derive live SDLC decision factors from ongoing dialogue
dynamic_sdlc = sdlc_engine.derive_factors_from_dialogue(
    full_conversation_text,
    requirements,
    coverage.get("score", 0),
    user_message_count=user_message_count
)
auto_factors = dynamic_sdlc["factors"]
auto_explanations = dynamic_sdlc["explanations"]

# Metrics bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Structured Requirements", len(requirements))
with col2:
    st.metric("Quality Checks Flagged", len(quality_issues))
with col3:
    st.metric("Compliance Mappings", len(compliance_result["compliance_mappings"]))
with col4:
    st.metric("Human Approval Gates", len(compliance_result["mandatory_checkpoints"]))

st.markdown("---")

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Stakeholder Interview",
    "📋 Requirements & Quality",
    "🛡️ Compliance & Security",
    "⚙️ SDLC Decision Engine",
    "📄 SRS Document & Export"
])


# ================= TAB 1: STAKEHOLDER INTERVIEW =================
with tab1:
    t_head_col1, t_head_col2 = st.columns([3, 1])
    with t_head_col1:
        st.markdown("#### Adaptive Stakeholder Requirement Gathering")
        st.caption("The Interaction Agent interviews stakeholders, checks coverage across 6 financial dimensions, and asks context-aware clarification questions.")
    with t_head_col2:
        if st.button("🗑️ Start Blank Chat", key="btn_clear_tab1", use_container_width=True):
            st.session_state.case_key = "custom_blank"
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I am your Financial Requirements Engineering Agent. Tell me about the banking software you want to build (roles, limits, rules) to start fresh!"}
            ]
            st.rerun()
    
    # Coverage Analysis
    coverage = interaction_agent.evaluate_coverage(full_conversation_text)
    cov_col1, cov_col2 = st.columns([1, 3])
    with cov_col1:
        st.metric("Dimension Coverage", f"{coverage['score']}%")
    with cov_col2:
        st.progress(coverage['score'] / 100)
        st.write(f"**Covered:** {', '.join(coverage['covered']) if coverage['covered'] else 'None'}")
        if coverage['missing']:
            st.write(f"**Missing / Needs Clarification:** :orange[{', '.join(coverage['missing'])}]")

    st.markdown("---")

    # Chat interface
    chat_container = st.container(height=380)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # User chat input
    user_input = st.chat_input("Add a requirement, answer a question, or clarify financial constraints...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            with st.chat_message("assistant"):
                with st.spinner("Clarification Agent analyzing requirement coverage..."):
                    agent_reply = interaction_agent.generate_next_question(st.session_state.messages)
                    st.markdown(agent_reply)
                    st.session_state.messages.append({"role": "assistant", "content": agent_reply})
        st.rerun()


# ================= TAB 2: REQUIREMENTS & QUALITY =================
with tab2:
    st.markdown("#### Structured System Requirements (IEEE 830)")
    
    if not requirements:
        st.info("💡 **No requirements extracted yet.** Start by describing your financial software project in **Tab 1 (Stakeholder Interview)** (e.g., P2P wallet, UPI payments, loan origination, or Video-KYC). Once you share requirements, the Extraction Agent will automatically generate IEEE 830 functional/non-functional cards, Gherkin acceptance criteria, and quality defect analyses here.")
    else:
        # Filters
        categories = list(set([r.get("category", "General") for r in requirements]))
        selected_cat = st.multiselect("Filter by Category:", options=categories, default=categories)
        
        filtered_reqs = [r for r in requirements if r.get("category") in selected_cat]
        
        for r in filtered_reqs:
            priority = r.get("priority", "Medium")
            badge_class = "badge-critical" if priority == "Critical" else ("badge-high" if priority == "High" else "badge-medium")
            
            with st.expander(f"**{r.get('id')}**: {r.get('statement')}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"**Category:** `{r.get('category')}`")
                    st.markdown(f"**Priority:** <span class='{badge_class}'>{priority}</span>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**Stakeholder Source:** {r.get('stakeholder')}")
                    st.markdown(f"**Risk Level:** `{r.get('risk_level', 'Medium')}`")
                with c3:
                    st.markdown(f"**Applicable Regulation:** `{r.get('applicable_regulation', 'General')}`")
                    st.markdown(f"**Confidence Score:** `{r.get('confidence_score', 0.95):.0%}`")
                
                st.markdown(f"**Acceptance Criteria (Gherkin):**")
                st.code(r.get("acceptance_criteria"), language="gherkin")

        st.markdown("---")
        st.markdown("#### 🔍 Quality & Defect Analysis (Ambiguity, Testability & Omissions)")
        if quality_issues:
            for q in quality_issues:
                st.warning(f"**[{q.get('req_id')}] {q.get('defect_type')}** (Flagged phrase: *\"{q.get('flagged_phrase')}\"*)\n\n"
                           f"**Issue & Refactoring:** {q.get('explanation')}")
        else:
            st.success("✅ All extracted requirements passed ambiguity and testability checks with measurable metrics!")


# ================= TAB 3: COMPLIANCE & SECURITY =================
with tab3:
    st.markdown("#### Financial Regulatory Mappings (RAG-Grounded)")
    st.caption("Requirements mapped against statutory guidelines: RBI PPI / Digital Lending, PCI-DSS v4.0, GDPR/DPDP, and Basel III.")
    
    if compliance_result["compliance_mappings"]:
        comp_df = pd.DataFrame(compliance_result["compliance_mappings"])
        st.dataframe(
            comp_df[["req_id", "regulation", "control_code", "control_desc", "status", "confidence"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("💡 **Awaiting requirements for regulatory mapping.** Once requirements are captured in Tab 1, the Compliance Agent will automatically map them against RBI, PCI-DSS, and DPDP mandates.")

    if compliance_result["compliance_gaps"]:
        st.markdown("#### 🚨 Regulatory Gaps & Unaddressed Obligations")
        for gap in compliance_result["compliance_gaps"]:
            st.error(f"**Missing Control:** {gap['missing_control']} ({gap['regulation']})\n\n"
                     f"**Regulatory Risk:** {gap['risk']}\n\n"
                     f"**Remediation Recommendation:** {gap['recommendation']}")

    if compliance_result["mandatory_checkpoints"]:
        st.markdown("#### 👤 Mandatory Human-in-the-Loop Approval Checkpoints")
        for cp in compliance_result["mandatory_checkpoints"]:
            st.info(f"**Gate:** {cp['checkpoint']}\n\n"
                    f"**Mandatory Approver:** {cp['responsible_role']} | **Stage:** `{cp['gate_type']}`")


# ================= TAB 4: SDLC DECISION ENGINE =================
with tab4:
    st.markdown("#### Hybrid SDLC Selection Engine (MCDA + Rule-Based)")
    st.caption("Dynamically analyzes dialogue maturity, regulatory mandates, and system complexity to recalculate SDLC rankings in real-time.")

    # Check if any requirements or conversation exist
    has_content = len(requirements) > 0 or user_message_count > 0

    if not has_content:
        st.info("💡 **Awaiting Requirements to Calculate SDLC Recommendation:** The SDLC Selection Engine evaluates project characteristics (regulatory criticality, security risk, throughput complexity, and requirement stability) to recommend and customize the optimal SDLC model. Start the interview in **Tab 1 (Stakeholder Interview)** to generate your project's customized SDLC roadmap.")
        sdlc_eval = sdlc_engine.evaluate_sdlc(auto_factors)
    else:
        st.success(f"🔄 **Live Conversation-Synced (Turn {user_message_count}):** The draggable factor lines below are auto-configured by AI from your conversation! You can drag any slider to test what-if scenarios.")
        
        st.markdown("##### 🎛️ Project Decision Factor Sliders (Scale 1 to 10)")
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
        with f_col1:
            f_reg = st.slider("Regulatory Criticality", 1, 10, auto_factors.get("reg_criticality", 8), key=f"sld_reg_{user_message_count}", help=f"AI Derived: {auto_factors.get('reg_criticality')}/10 ({auto_explanations.get('reg_criticality')})")
            f_sec = st.slider("Security & Financial Risk", 1, 10, auto_factors.get("security_risk", 8), key=f"sld_sec_{user_message_count}", help=f"AI Derived: {auto_factors.get('security_risk')}/10 ({auto_explanations.get('security_risk')})")
        
        with f_col2:
            f_stab = st.slider("Requirement Stability", 1, 10, auto_factors.get("req_stability", 6), key=f"sld_stab_{user_message_count}", help=f"AI Derived: {auto_factors.get('req_stability')}/10 ({coverage.get('score', 0)}% coverage)")
            f_freq = st.slider("Frequency of Expected Changes", 1, 10, auto_factors.get("change_freq", 6), key=f"sld_freq_{user_message_count}", help="Rate of new business features")
        
        with f_col3:
            f_cd = st.slider("Need for Continuous Delivery (CI/CD)", 1, 10, auto_factors.get("cd_need", 7), key=f"sld_cd_{user_message_count}", help="Automated testing and continuous release cadence")
            f_comp = st.slider("Technical Complexity", 1, 10, auto_factors.get("complexity", 7), key=f"sld_comp_{user_message_count}", help=f"AI Derived: {auto_factors.get('complexity')}/10 ({auto_explanations.get('complexity')})")

        with f_col4:
            f_avail = st.slider("Stakeholder Availability", 1, 10, auto_factors.get("stakeholder_avail", 7), key=f"sld_avail_{user_message_count}", help="Availability of Product Owners and Risk Officers")
            f_fail = st.slider("Consequences of System Failure", 1, 10, auto_factors.get("failure_consequence", 8), key=f"sld_fail_{user_message_count}", help=f"AI Derived: {auto_factors.get('failure_consequence')}/10 ({auto_explanations.get('failure_consequence')})")

        user_factors = {
            "reg_criticality": f_reg,
            "security_risk": f_sec,
            "req_stability": f_stab,
            "change_freq": f_freq,
            "cd_need": f_cd,
            "complexity": f_comp,
            "stakeholder_avail": f_avail,
            "failure_consequence": f_fail
        }

        # Evaluate SDLC
        sdlc_eval = sdlc_engine.evaluate_sdlc(user_factors)
        
        st.markdown("---")
        
        # Visual Chart of SDLC Rankings
        chart_col, exp_col = st.columns([1, 1])
        
        with chart_col:
            st.markdown("##### 📊 SDLC Model Suitability Rankings")
            scores_df = pd.DataFrame([{"Model": r["model"], "Suitability (%)": r["score"]} for r in sdlc_eval["rankings"]])
            
            fig = px.bar(
                scores_df,
                x="Suitability (%)",
                y="Model",
                orientation='h',
                text="Suitability (%)",
                color="Suitability (%)",
                color_continuous_scale="Blues",
                range_x=[0, 100]
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=320, margin=dict(l=0, r=0, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with exp_col:
            st.markdown(f"##### 🏆 Recommended Model: :blue[{sdlc_eval['recommended_model']}]")
            st.markdown(f"**Compatibility Score:** `{sdlc_eval['recommended_score']}%`")
            st.markdown(f"**Engineering Justification:**")
            st.info(sdlc_eval["justification"])

        st.markdown("---")
        st.markdown("##### 🛠️ Generated Project-Specific SDLC Workflow & Gates")
        w_col1, w_col2 = st.columns(2)
        with w_col1:
            st.markdown("**Customized Phase Sequence:**")
            for ph in sdlc_eval["customized_workflow"]:
                st.markdown(f"- 📌 **{ph}**")
        with w_col2:
            st.markdown("**Mandatory Verification & Security Gates:**")
            for gate in sdlc_eval["mandatory_gates"]:
                st.markdown(f"- 🔒 {gate}")


# ================= TAB 5: SRS EXPORT =================
with tab5:
    st.markdown("#### Software Requirements Specification (SRS) Generator")
    st.caption("IEEE Std 830-1998 compliant document synthesized from the multi-agent analysis.")
    
    if not has_content:
        st.info("💡 **No SRS Generated Yet:** The IEEE Std 830-1998 document generator synthesizes functional requirements, compliance mappings, and SDLC decisions into formal specifications. Conduct the interview in **Tab 1** to compile, preview, and download your publication-grade SRS document.")
    else:
        srs_text = doc_agent.generate_srs_markdown(
            project_title=active_title,
            domain=active_domain,
            requirements=requirements,
            compliance_data=compliance_result,
            sdlc_data=sdlc_eval,
            quality_issues=quality_issues
        )

        d_col1, d_col2 = st.columns([3, 1])
        with d_col1:
            st.write("Ready to export formal documentation for submission or sprint backlog:")
        with d_col2:
            st.download_button(
                label="📥 Download Full SRS Document (.md)",
                data=srs_text,
                file_name=f"SRS_{st.session_state.case_key}.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.markdown("---")
        with st.expander("📄 Click to Preview Generated IEEE 830 SRS Document", expanded=True):
            st.markdown(srs_text)
