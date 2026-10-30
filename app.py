import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

from paranormal_engine import TabPFNParanormalDetector
from dossier_generator import DossierGenerator

# Page Configuration
st.set_page_config(
    page_title="TabPFN Paranormal | IoT Poltergeist Investigator",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Atmospheric Paranormal CSS
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

/* Main Background */
.stApp {
    background: radial-gradient(circle at 50% 10%, #151124 0%, #090710 60%, #040307 100%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    letter-spacing: 0.05em;
}

h1 {
    color: #ff9f43 !important;
    text-shadow: 0 0 20px rgba(255, 159, 67, 0.4);
}

/* Radar & Metric Cards */
.paranormal-card {
    background: rgba(22, 17, 38, 0.7);
    border: 1px solid rgba(255, 159, 67, 0.25);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(8px);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.paranormal-card:hover {
    border-color: rgba(255, 159, 67, 0.6);
    box-shadow: 0 8px 32px 0 rgba(255, 159, 67, 0.15);
}

.classified-stamp {
    display: inline-block;
    padding: 6px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 800;
    font-size: 0.85rem;
    border: 2px solid #e74c3c;
    color: #e74c3c;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    transform: rotate(-2deg);
}

.metric-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ff9f43;
}

/* Custom Alert / Callout */
.ghost-alert {
    background: rgba(231, 76, 60, 0.1);
    border-left: 4px solid #e74c3c;
    padding: 14px 18px;
    border-radius: 0 8px 8px 0;
    margin: 15px 0;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 48px;
    border-radius: 8px 8px 0 0;
    padding: 0 24px;
    background-color: rgba(255, 255, 255, 0.04);
    color: #a0aec0;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(255, 159, 67, 0.15) !important;
    color: #ff9f43 !important;
    border-bottom: 2px solid #ff9f43 !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Initialize Engines
@st.cache_resource
def load_detector():
    return TabPFNParanormalDetector()

@st.cache_resource
def load_generator():
    return DossierGenerator()

detector = load_detector()
generator = load_generator()


# Top Banner / Header
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 10px; border-bottom: 1px solid rgba(255,159,67,0.2);">
        <div>
            <h1 style="margin: 0; font-size: 2.2rem;">👻 TabPFN Paranormal</h1>
            <p style="margin: 4px 0 0; color: #a0aec0; font-size: 0.95rem;">
                IoT Poltergeist Investigator & Edge Telemetry Forensic Analyzer • <i>Prior Labs TabPFN-3.5 + Gemma 2</i>
            </p>
        </div>
        <div style="text-align: right;">
            <span class="classified-stamp">TOP SECRET // S.P.E.C.T.R.E.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🎛️ Telemetry Source")
    
    data_source = st.radio(
        "Choose Sensor Feed",
        [
            "Blackwood Manor (3:17 AM Poltergeist)",
            "Server Room Vault (Ghost in the Machine)",
            "Suburban Basement (HVAC Control Baseline)",
            "Upload Custom IoT CSV",
        ],
        index=0,
    )

    df = None
    if data_source == "Blackwood Manor (3:17 AM Poltergeist)":
        df = pd.read_csv("demo_datasets/blackwood_manor_3am.csv")
    elif data_source == "Server Room Vault (Ghost in the Machine)":
        df = pd.read_csv("demo_datasets/server_room_specter.csv")
    elif data_source == "Suburban Basement (HVAC Control Baseline)":
        df = pd.read_csv("demo_datasets/suburban_hvac_glitch.csv")
    else:
        uploaded_file = st.file_uploader("Upload Smart-Home CSV", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            st.info("Awaiting sensor telemetry CSV upload...")

    st.markdown("---")
    st.markdown("### 🧠 AI Engine Status")
    
    tabpfn_status = "⚡ TabPFN Native Weights" if detector.is_tabpfn_native else "🔬 Prior Labs Bayesian Prior Engine"
    st.success(f"**Analytics:** {tabpfn_status}")

    ollama_online = generator.check_ollama_available()
    llm_status = "🟢 Local Ollama (Gemma 2 Online)" if ollama_online else "🟡 Autonomous Synthetic Engine (Offline)"
    st.info(f"**LLM:** {llm_status}")

    st.markdown("---")
    st.markdown("### 🛡️ Edge Privacy Guarantee")
    st.caption(
        "Smart-home sensor telemetry exposes intimate occupancy and sleep schedules. "
        "By computing TabPFN and Gemma 2 on local edge hardware, data **never** leaves your home."
    )


# Main Content Area
if df is not None:
    # Run TabPFN Anomaly Detection
    analysis = detector.analyze(df)
    proc_df = analysis["processed_df"]
    peak_score = analysis["peak_score"]
    threat_level = analysis["threat_level"]
    threat_color = analysis["threat_color"]
    probs = analysis["classification_probs"]

    # 4 Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Telemetry & TabPFN Analytics",
        "🕵️ Classified Field Dossier",
        "🔒 Why Open Innovation Matters",
        "📝 DEV.to Submission Drafter"
    ])

    # TAB 1: Visual Telemetry Dashboard
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        # 4 Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""
                <div class="paranormal-card">
                    <span style="color: #a0aec0; font-size: 0.85rem; font-weight: 600;">TABPFN ANOMALY SCORE</span>
                    <div class="metric-number" style="color: {threat_color};">{peak_score}%</div>
                    <span style="color: #cbd5e0; font-size: 0.8rem;">Multivariate Prior Deviation</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="paranormal-card">
                    <span style="color: #a0aec0; font-size: 0.85rem; font-weight: 600;">THREAT LEVEL</span>
                    <div style="font-size: 1.15rem; font-weight: 800; color: {threat_color}; margin: 8px 0;">{threat_level.split('(')[0]}</div>
                    <span style="color: #cbd5e0; font-size: 0.8rem;">Sector: {analysis['peak_room']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="paranormal-card">
                    <span style="color: #a0aec0; font-size: 0.85rem; font-weight: 600;">COLD SPOT MINIMUM</span>
                    <div class="metric-number" style="color: #54a0ff;">{analysis['peak_temp']}°C</div>
                    <span style="color: #cbd5e0; font-size: 0.8rem;">At {analysis['peak_timestamp'].split(' ')[-1]}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
                <div class="paranormal-card">
                    <span style="color: #a0aec0; font-size: 0.85rem; font-weight: 600;">ELECTROMAGNETIC PEAK</span>
                    <div class="metric-number" style="color: #ff9f43;">{analysis['peak_emf']} mG</div>
                    <span style="color: #cbd5e0; font-size: 0.8rem;">Baseline: 0.3 - 0.5 mG</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Charts Section
        st.markdown("### 📈 Synchronized Sensor Telemetry Timeline")
        
        # Plotly Time-Series Chart
        fig = go.Figure()

        if "ambient_temp_c" in proc_df.columns:
            fig.add_trace(go.Scatter(
                x=proc_df["timestamp"],
                y=proc_df["ambient_temp_c"],
                name="Ambient Temp (°C)",
                line=dict(color="#54a0ff", width=2.5),
                yaxis="y1"
            ))

        if "emf_milligauss" in proc_df.columns:
            fig.add_trace(go.Scatter(
                x=proc_df["timestamp"],
                y=proc_df["emf_milligauss"],
                name="EMF Magnitude (mG)",
                line=dict(color="#ff9f43", width=2, dash="dot"),
                yaxis="y2"
            ))

        if "anomaly_score" in proc_df.columns:
            fig.add_trace(go.Bar(
                x=proc_df["timestamp"],
                y=proc_df["anomaly_score"],
                name="TabPFN Anomaly Score (%)",
                marker_color="rgba(231, 76, 60, 0.4)",
                yaxis="y3"
            ))

        fig.update_layout(
            paper_bgcolor="rgba(10, 8, 18, 0.8)",
            plot_bgcolor="rgba(18, 14, 30, 0.6)",
            font=dict(color="#e2e8f0"),
            height=460,
            margin=dict(l=40, r=40, t=30, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Temperature (°C)", titlefont=dict(color="#54a0ff"), tickfont=dict(color="#54a0ff")),
            yaxis2=dict(title="EMF (mG)", titlefont=dict(color="#ff9f43"), tickfont=dict(color="#ff9f43"), overlaying="y", side="right"),
            yaxis3=dict(title="Anomaly Score", showgrid=False, overlaying="y", visible=False, range=[0, 200]),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Forensic Diagnosis Radar & Probabilities
        col_prob1, col_prob2 = st.columns([1.2, 1])

        with col_prob1:
            st.markdown("### 🕸️ TabPFN Diagnostic Classification Breakdown")
            prob_df = pd.DataFrame(list(probs.items()), columns=["Diagnosis", "Probability (%)"])
            
            fig_bar = px.bar(
                prob_df,
                x="Probability (%)",
                y="Diagnosis",
                orientation="h",
                color="Probability (%)",
                color_continuous_scale=["#2ed573", "#ffa502", "#ff4757"],
                text="Probability (%)"
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(10, 8, 18, 0.8)",
                plot_bgcolor="rgba(18, 14, 30, 0.6)",
                font=dict(color="#e2e8f0"),
                height=320,
                margin=dict(l=20, r=20, t=10, b=10),
            )
            fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_prob2:
            st.markdown("### 🎚️ Diagnostic Probability Radar")
            radar_categories = list(probs.keys())
            radar_values = list(probs.values())
            # close polygon
            radar_categories.append(radar_categories[0])
            radar_values.append(radar_values[0])

            fig_radar = go.Figure(data=go.Scatterpolar(
                r=radar_values,
                theta=radar_categories,
                fill="toself",
                fillcolor="rgba(255, 159, 67, 0.35)",
                line=dict(color="#ff9f43", width=2)
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9, color="#a0aec0")),
                    bgcolor="rgba(18, 14, 30, 0.6)"
                ),
                paper_bgcolor="rgba(10, 8, 18, 0.8)",
                font=dict(color="#e2e8f0"),
                height=320,
                margin=dict(l=40, r=40, t=20, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    # TAB 2: S.P.E.C.T.R.E. Dossier
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🗂️ S.P.E.C.T.R.E. Paranormal Investigation Dossier")
        st.write("Synthesize an intelligence dossier by coupling TabPFN's tabular likelihoods with local LLM forensic reasoning (Gemma 2 via Ollama).")

        investigator_notes = st.text_area(
            "Investigator Field Notes (Optional context, e.g. 'Dog barked at empty corner', 'Cold draft near chandelier'):",
            placeholder="Log subjective observations here...",
            height=85
        )

        if st.button("🔮 Generate Classified Dossier (Local Gemma 2 / TabPFN)", type="primary"):
            with st.spinner("Synthesizing telemetry across TabPFN Bayesian priors and Gemma 2..."):
                dossier_text = generator.generate_dossier(analysis, investigator_notes)
                st.session_state["cached_dossier"] = dossier_text

        if "cached_dossier" in st.session_state:
            st.markdown(
                f"""
                <div style="background: rgba(18, 14, 30, 0.85); border: 1px solid rgba(255, 159, 67, 0.3); border-radius: 12px; padding: 30px; margin-top: 20px;">
                """,
                unsafe_allow_html=True
            )
            st.markdown(st.session_state["cached_dossier"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Dossier (.md)",
                data=st.session_state["cached_dossier"],
                file_name=f"spectre_dossier_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

    # TAB 3: Why Open Innovation Matters
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## 🔒 Why Open Innovation Matters: The Edge Privacy Mandate")
        
        st.markdown("""
        ### The Threat of Cloud-Tethered Telemetry
        Modern smart homes are outfitted with an invisible mesh of sensors: **acoustic decibel meters, passive infrared motion sensors, circuit wattage monitors, and thermal gauges**.

        When these sensors are hooked up to cloud-based proprietary AI APIs (such as OpenAI, Anthropic, or cloud brokers):
        1. **Intimate Lifestyle Surveillance:** Cloud companies receive precise mathematical timestamps of when you sleep, which room you are in, when you shower, and when you are away from home.
        2. **Breach Vulnerability:** If a central cloud broker is breached, bad actors obtain real-time physical occupancy maps of your residence.
        3. **Monthly Rent & Deprecation:** Cloud APIs charge per-token, rate-limit queries, and can deprecate endpoints without warning.

        ---

        ### The Open-Source Solution: TabPFN-3.5 + Gemma 2 at the Edge
        By building **TabPFN Paranormal** on 100% open-source foundation models:
        * **Prior Labs' TabPFN:** Runs directly on edge hardware. It evaluates complex tabular prior distributions in a **single forward pass** without needing massive cloud training clusters.
        * **Google Gemma 2 (via Ollama):** Synthesizes forensic intelligence dossiers locally, entirely offline.
        * **Zero Telemetry Leakage:** Your sensor logs never cross your local Wi-Fi gateway. The investigator functions seamlessly even during a total internet or storm outage on Halloween night.
        """)

    # TAB 4: DEV.to Submission Generator
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## 📝 DEV.to Hacktoberfest Submission Generator")
        st.write("Copy and paste this pre-formatted Markdown article directly into DEV.to to enter Week 4 of the Hacktoberfest Challenge!")

        submission_template = f"""---
title: TabPFN Paranormal: Investigating the Ghost in the Smart-Home Machine
published: true
tags: devchallenge, hf26challenge, tabpfn, opensource
canonical_url: https://github.com/vidishagupta/tabpfn-paranormal
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)*

## What I Built
**TabPFN Paranormal** is an open-source, edge-native IoT paranormal investigation system. It monitors smart-home environmental telemetry (temperature drops, electromagnetic field surges, infrasound frequency resonances, and circuit wattage spikes) to catch the "ghost in the machine."

Using **Prior Labs' TabPFN-3.5 tabular foundation model**, the system evaluates multivariate Bayesian prior distributions to distinguish between mundane mechanical failures (like an HVAC compressor defrost cycle or an electrical ground loop) and genuine Class-IV spectral anomalies. It then pairs with **Google Gemma 2 (running locally via Ollama)** to generate classified S.P.E.C.T.R.E. forensic field dossiers.

## Demo
- **Source Code & GitHub Repository:** [https://github.com/vidishagupta/tabpfn-paranormal](https://github.com/vidishagupta/tabpfn-paranormal)

![TabPFN Paranormal Dashboard](https://raw.githubusercontent.com/your-username/tabpfn-paranormal/main/assets/demo.png)

## How I Built It
1. **Prior Labs TabPFN-3.5:** Employs TabPFN's Bayesian prior-data fitted network for zero-shot tabular anomaly detection and multi-class diagnosis.
2. **Local Open LLM (Gemma 2 via Ollama):** Transforms raw numerical anomalies into a structured S.P.E.C.T.R.E. investigative dossier with containment protocols.
3. **Interactive Streamlit UI & Plotly:** Multi-channel time-series charts, radar probability distributions, and gothic dark-mode styling.

```mermaid
graph TD
    A[Smart Home Sensors: Temp, EMF, Audio, Power] --> B[Data Pipeline / CSV Telemetry]
    B --> C[Prior Labs TabPFN Foundation Model]
    C --> D[Anomaly Score & Probabilistic Diagnostic]
    D --> E[Local Open LLM: Gemma 2 via Ollama]
    E --> F[Classified S.P.E.C.T.R.E. Forensic Dossier]
    D --> G[Streamlit Visual Radar & Telemetry Charts]
```

## Why Does Open Innovation Matter?
Smart-home sensor feeds contain the most intimate telemetry of personal life: sleep schedules, room occupancy, and domestic routines. Uploading this telemetry to closed cloud APIs poses severe physical security and surveillance risks.

By running **Prior Labs' TabPFN** and **Gemma 2** entirely on local edge hardware:
- **100% Air-Gapped Privacy:** Sensor logs never leave the home network.
- **Zero Cloud Costs:** No token billing or rate limits.
- **Offline Resilience:** The ghost investigator operates during storms and internet blackouts.

## Prize Categories
- **Best Use of TabPFN** (Prior Labs tabular foundation model for anomaly detection & classification)
- **Hacktoberfest Open-Source AI Challenge Week 4 Top Prize**

---
*Built with open-source AI for Hacktoberfest 2026.*
"""
        st.text_area("Submission Markdown (Ready to copy):", submission_template, height=350)
        st.download_button(
            label="📋 Download Submission Post (submission.md)",
            data=submission_template,
            file_name="dev_hacktoberfest_week4_submission.md",
            mime="text/markdown"
        )
