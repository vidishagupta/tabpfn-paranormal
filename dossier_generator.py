"""
Classified Paranormal Field Dossier Generator.
Pairs TabPFN sensor anomaly analytics with Local Open LLMs (Gemma 2 / Ollama)
to synthesize forensic investigation dossiers while keeping smart-home telemetry 100% private.
"""

import json
import requests
from typing import Dict, Any, Optional
import os


class DossierGenerator:
    """
    Generates structured forensic dossiers using local Ollama (Gemma 2)
    with autonomous offline fallback.
    """

    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "gemma2"):
        self.ollama_url = ollama_url
        self.model = model

    def check_ollama_available(self) -> bool:
        """Checks if local Ollama daemon is reachable."""
        try:
            res = requests.get(f"{self.ollama_url}/api/tags", timeout=1.5)
            return res.status_code == 200
        except Exception:
            return False

    def generate_dossier(self, analysis_result: Dict[str, Any], investigator_notes: str = "") -> str:
        """
        Synthesizes a classified S.P.E.C.T.R.E. paranormal dossier from TabPFN analytics.
        Uses Ollama Gemma 2 if available; otherwise uses high-fidelity local synthetic engine.
        """
        peak_score = analysis_result["peak_score"]
        threat_level = analysis_result["threat_level"]
        peak_time = analysis_result["peak_timestamp"]
        peak_room = analysis_result["peak_room"]
        peak_temp = analysis_result["peak_temp"]
        peak_emf = analysis_result["peak_emf"]
        peak_acoustic = analysis_result["peak_acoustic"]
        probs = analysis_result["classification_probs"]

        prompt = f"""
[CLASSIFIED S.P.E.C.T.R.E. PARANORMAL FORENSIC REPORT]
You are a Senior Paranormal Investigator & Edge Telemetry Forensic Specialist.
Analyze the following anomalous sensor metrics identified by Prior Labs' TabPFN model:

- Location: {peak_room}
- Peak Anomaly Timestamp: {peak_time}
- TabPFN Composite Anomaly Score: {peak_score} / 100
- Threat Classification: {threat_level}
- Minimum Temperature: {peak_temp} °C (Cold Spot Gradient)
- Peak Electromagnetic Field: {peak_emf} mG
- Peak Acoustic Disturbance: {peak_acoustic} dB
- Probabilistic Diagnostics:
  * Spectral Entity Manifestation: {probs.get('Spectral / Poltergeist Entity', 0)}%
  * HVAC Mechanical Cycling: {probs.get('HVAC / Thermal Cycling (Mundane)', 0)}%
  * Electrical Surge / Ground Loop: {probs.get('Electrical Ground Loop / Surge', 0)}%
  * Infrasound Acoustic Resonance: {probs.get('Infrasonic Vent Resonance', 0)}%

Investigator Field Notes: {investigator_notes or 'No manual notes logged.'}

Generate a classified, atmospheric forensic dossier in Markdown.
Structure your report with:
1. EXECUTIVE SUMMARY & THREAT ASSESSMENT
2. SENSOR ANOMALY FORENSIC BREAKDOWN (Why the metrics deviate from baseline)
3. ENTITY HYPOTHESIS VS. MECHANICAL HYPOTHESIS (Differentiating paranormal from HVAC)
4. RECOMMENDED CONTAINMENT PROTOCOL (Actionable mitigation)
5. PRIVACY STATEMENT (Why running TabPFN & Gemma 2 on local edge hardware is vital for domestic security)
"""

        # Try calling local Ollama first
        if self.check_ollama_available():
            try:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.65, "top_p": 0.9}
                }
                resp = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=25.0)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("response", "").strip()
            except Exception:
                pass

        # Offline High-Fidelity Synthetic Engine
        return self._generate_synthetic_dossier(analysis_result, investigator_notes)

    def _generate_synthetic_dossier(self, analysis_result: Dict[str, Any], notes: str) -> str:
        """High-fidelity fallback mimicking Gemma 2's classified S.P.E.C.T.R.E. dossier."""
        peak_score = analysis_result["peak_score"]
        threat = analysis_result["threat_level"]
        timestamp = analysis_result["peak_timestamp"]
        room = analysis_result["peak_room"]
        temp = analysis_result["peak_temp"]
        emf = analysis_result["peak_emf"]
        acoustic = analysis_result["peak_acoustic"]
        probs = analysis_result["classification_probs"]
        p_spectral = probs.get("Spectral / Poltergeist Entity", 0)
        p_hvac = probs.get("HVAC / Thermal Cycling (Mundane)", 0)

        is_haunted = p_spectral > 40.0

        if is_haunted:
            verdict = "CONFIRMED CLASS-IV ANOMALOUS INCIDENT"
            assessment = (
                f"TabPFN multivariate Bayesian inference detected severe non-linear divergence at {timestamp}. "
                f"Ambient temperature collapsed to {temp}°C while EMF spiked to {emf} mG without an inductive electrical "
                f"load on the local breaker circuit. Motion sensors registered continuous kinetic displacement in {room} "
                f"despite the absence of a thermal infrared human silhouette."
            )
            entity_analysis = (
                f"The probability of a spectral entity is evaluated at **{p_spectral}%**. The co-occurrence of 18.9 Hz "
                f"infrasonic resonance with severe localized thermal absorption strongly aligns with historic poltergeist "
                f"phenomenology. Mechanical HVAC failure is ruled improbable ({p_hvac}%) due to the asymmetric localized "
                f"magnetic gradient which standard ventilation compressors cannot generate."
            )
            protocol = (
                "- **Electromagnetic Dampening:** Deploy localized Mu-metal shielding around the central junction.\n"
                "- **Thermal Monitoring:** Mount dual-spectrum thermal cameras calibrated to 8-14 µm spectral range.\n"
                "- **Kinetic Anchoring:** Secure physical artifacts in the sensor zone prone to kinetic levitation.\n"
                "- **Salt & Iron Threshold Seal:** Place traditional iron filings along room perimeter as an analog heuristic."
            )
        else:
            verdict = "NOMINAL / MUNDANE MECHANICAL ANOMALY"
            assessment = (
                f"TabPFN analytics isolated environmental fluctuations at {timestamp} in {room}. "
                f"While temperature decreased to {temp}°C, the corresponding circuit draw and acoustic signature "
                f"({acoustic} dB) strongly match mechanical compressor cycling rather than an autonomous manifestation."
            )
            entity_analysis = (
                f"Spectral manifestation probability is negligible (**{p_spectral}%**). TabPFN's prior distribution "
                f"confirms a **{p_hvac}% confidence in HVAC / Thermal Cycling**. The acoustic frequency spikes "
                f"are harmonics of standard 60Hz mains induction and ventilation duct vibration."
            )
            protocol = (
                "- **HVAC Inspection:** Service compressor refrigerant and inspect duct dampers for mechanical rattle.\n"
                "- **Ground Loop Verification:** Check neutral-to-ground impedance on electrical panel sub-feeder.\n"
                "- **Continue Baseline Logging:** Maintain local sensor recording to verify nominal threshold stability."
            )

        dossier = f"""### S.P.E.C.T.R.E. DIVISION — INVESTIGATIVE DOSSIER #TABPFN-{timestamp.replace(' ', '-').replace(':', '')}
**CLEARANCE LEVEL:** RESTRICTED // PARANORMAL INCIDENT RESPONSE  
**MONITORING SECTOR:** `{room}` | **EVENT HORIZON:** `{timestamp}`  
**STATUS:** `{verdict}` | **THREAT METRIC:** `{threat}`

---

#### 1. EXECUTIVE SUMMARY & TABPFN INFERENCE
{assessment}

* **TabPFN Anomaly Score:** `{peak_score} / 100`
* **Peak EMF Magnitude:** `{emf} mG` (Baseline: <0.5 mG)
* **Localized Cold Spot:** `{temp} °C`
* **Investigator Notes:** *{notes or "Standard telemetry acquisition. No manual overrides logged."}*

---

#### 2. SPECTRAL VS. MECHANICAL PROBABILISTIC DIAGNOSTIC
Prior Labs' TabPFN foundation model evaluated multivariate prior likelihoods across all sensor channels:

| Diagnostic Channel | Evaluated Probability | Forensic Interpretation |
| :--- | :--- | :--- |
| **Spectral / Poltergeist Entity** | **{p_spectral}%** | {"Direct paranormal thermal-electromagnetic convergence." if is_haunted else "Low anomaly footprint; spectral hypothesis rejected."} |
| **HVAC Thermal Cycling** | **{p_hvac}%** | {"Incompatible with magnetic spike profile." if is_haunted else "Consistent with mechanical thermostat kick-in."} |
| **Electrical Ground Surge** | **{probs.get('Electrical Ground Loop / Surge', 0)}%** | {"Secondary induced magnetic field fluctuation." if is_haunted else "Standard electrical transient."} |
| **Infrasound Resonance** | **{probs.get('Infrasonic Vent Resonance', 0)}%** | {"18.9 Hz resonant harmonic detected." if is_haunted else "Acoustic baseline within safe limits."} |

{entity_analysis}

---

#### 3. CONTAINMENT & REMEDIATION PROTOCOLS
{protocol}

---

#### 4. WHY OPEN INNOVATION & EDGE AI MATTERS
> **DOMESTIC PRIVACY DIRECTIVE:**  
> Smart-home sensor feeds (occupancy, bedroom sleep patterns, power draws, micro-acoustics) contain the most intimate telemetry of personal life. Routing this telemetry to proprietary cloud APIs (e.g. OpenAI or cloud brokers) creates unacceptable surveillance and physical security risks.
>
> By utilizing **Prior Labs' TabPFN open-weight model** running directly on edge hardware paired with **local open-weight LLMs (Gemma 2 via Ollama)**:
> 1. Telemetry never crosses an internet gateway; your home remains an encrypted redoubt.
> 2. Zero operational cloud API costs, subscription paywalls, or token rate limits.
> 3. Autonomous offline resilience: the investigator works even during complete power/internet blackouts.
"""
        return dossier.strip()
