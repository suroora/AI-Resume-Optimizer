import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from preprocessing.resume_parser import parse_resume
from preprocessing.text_cleaning import clean_text
from preprocessing.skill_extractor import load_skill_dictionary
from core.matching_engine import ResumeMatcher
from core.skill_gap import skill_match_analysis
from core.scoring import calculate_final_score, generate_recommendation

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

/* ── Reset & Root ── */
:root {
    --bg:        #080c14;
    --surface:   #0d1320;
    --surface2:  #111827;
    --border:    #1e2d45;
    --accent:    #00d4ff;
    --accent2:   #7c3aed;
    --success:   #00ffa3;
    --danger:    #ff4d6d;
    --warn:      #fbbf24;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'Space Mono', monospace;
}

/* ── App background ── */
.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,212,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(124,58,237,0.08) 0%, transparent 60%),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 79px,
            rgba(30,45,69,0.25) 79px,
            rgba(30,45,69,0.25) 80px
        ),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 79px,
            rgba(30,45,69,0.25) 79px,
            rgba(30,45,69,0.25) 80px
        ) !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    padding: 6px 18px;
    border-radius: 2px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero-title {
    font-family: var(--font-head);
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.05;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent) 60%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: #e2e8f0;
    background-clip: text;
}
.hero-sub {
    font-family: var(--font-mono);
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 0.8rem;
    letter-spacing: 0.04em;
}

/* ── Divider ── */
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── Panel cards ── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    position: relative;
    overflow: hidden;
}
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0.6;
}
.panel-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(0,212,255,0.03) !important;
    border: 1px dashed rgba(0,212,255,0.25) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,212,255,0.6) !important;
}
[data-testid="stFileUploader"] label { color: var(--text) !important; }

/* ── Text area ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.08) !important;
}
.stTextArea label { color: var(--muted) !important; font-size: 0.75rem !important; letter-spacing: 0.1em !important; }

/* ── Analyze button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.75rem 2.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2) !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 0 32px rgba(0,212,255,0.35) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 1.2rem 1.4rem !important;
    text-align: center !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.14em !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-head) !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    color: var(--accent) !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 4px !important;
    height: 6px !important;
}
.stProgress > div {
    background: var(--surface2) !important;
    border-radius: 4px !important;
    height: 6px !important;
}

/* ── Skill chips ── */
.skill-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 0.6rem;
}
.chip {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    padding: 5px 14px;
    border-radius: 4px;
    letter-spacing: 0.06em;
    display: inline-block;
}
.chip-match {
    background: rgba(0,255,163,0.10);
    border: 1px solid rgba(0,255,163,0.35);
    color: var(--success);
}
.chip-miss {
    background: rgba(255,77,109,0.10);
    border: 1px solid rgba(255,77,109,0.35);
    color: var(--danger);
}

/* ── Recommendation box ── */
.rec-box {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.25);
    border-left: 3px solid var(--accent2);
    border-radius: 0 8px 8px 0;
    padding: 1.2rem 1.4rem;
    font-family: var(--font-mono);
    font-size: 0.84rem;
    line-height: 1.7;
    color: var(--text);
}

/* ── Section headers ── */
.section-head {
    font-family: var(--font-head);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.01em;
    margin: 0 0 0.6rem;
}

/* ── Spinner text ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Warning ── */
.stAlert { border-radius: 8px !important; font-family: var(--font-mono) !important; font-size: 0.82rem !important; }

/* ── Score ring wrapper ── */
.score-ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Powered by AI · NLP · Semantic Matching</div>
    <h1 class="hero-title">AI Resume Optimizer</h1>
    <p class="hero-sub">// Upload your resume → paste a job description → get instant gap analysis</p>
</div>
<hr class="divider"/>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT SECTION
# ─────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="panel"><div class="panel-label">01 · Resume File</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop your PDF or DOCX here",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.markdown(f"""
        <div style="margin-top:10px; padding:8px 14px; background:rgba(0,255,163,0.07);
             border:1px solid rgba(0,255,163,0.25); border-radius:6px;
             font-family:var(--font-mono); font-size:0.72rem; color:#00ffa3;">
            ✔ &nbsp; {uploaded_file.name} &nbsp;·&nbsp; {uploaded_file.size/1024:.1f} KB
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="panel"><div class="panel-label">02 · Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste the full job description here",
        height=180,
        placeholder="Paste the job description here — include required skills, responsibilities, and qualifications...",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 3, 2])
with btn_col:
    analyze = st.button("⚡  Analyze Resume Now", use_container_width=True)

st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  ANALYSIS ENGINE
# ─────────────────────────────────────────────
if analyze:
    if uploaded_file and job_description.strip():
        with st.spinner("Crunching semantic vectors and skill embeddings…"):
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            raw_text         = parse_resume(uploaded_file.name)
            resume_text      = clean_text(raw_text)
            jd_text          = clean_text(job_description)
            skill_list       = load_skill_dictionary()
            matcher          = ResumeMatcher()
            similarity_score = matcher.compute_similarity(resume_text, jd_text)
            matched, missing, skill_percent = skill_match_analysis(resume_text, jd_text, skill_list)
            final_score      = calculate_final_score(similarity_score, skill_percent)
            recommendation   = generate_recommendation(final_score)

        # ── Score level label ──
        if final_score >= 80:
            level, level_color = "EXCELLENT FIT", "#00ffa3"
        elif final_score >= 60:
            level, level_color = "GOOD MATCH", "#00d4ff"
        elif final_score >= 40:
            level, level_color = "PARTIAL MATCH", "#fbbf24"
        else:
            level, level_color = "NEEDS WORK", "#ff4d6d"

        # ── Section header ──
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:1.5rem;">
            <span style="font-family:var(--font-head); font-size:1.5rem; font-weight:800; color:#e2e8f0;">
                Analysis Results
            </span>
            <span style="font-family:var(--font-mono); font-size:0.68rem; letter-spacing:0.15em;
                  padding:4px 14px; border-radius:3px; border:1px solid {level_color};
                  color:{level_color}; background:rgba(0,0,0,0.3);">
                {level}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # ── Metric cards ──
        m1, m2, m3 = st.columns(3, gap="medium")
        with m1:
            st.metric("Job Fit Score", f"{similarity_score}%", help="Semantic similarity between resume and JD")
        with m2:
            st.metric("Skill Match", f"{skill_percent}%", help="% of required skills found in your resume")
        with m3:
            st.metric("Final Score", f"{final_score}%", help="Weighted composite of all signals")

        # ── Progress bar ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<p style="font-family:var(--font-mono); font-size:0.68rem; letter-spacing:0.12em; color:var(--muted); margin-bottom:4px;">SKILL COVERAGE — {skill_percent}%</p>', unsafe_allow_html=True)
        st.progress(int(skill_percent) / 100)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Skills columns ──
        sk1, sk2 = st.columns(2, gap="large")

        with sk1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-label">✔ Matched Skills</div>', unsafe_allow_html=True)
            if matched:
                chips = "".join([f'<span class="chip chip-match">{s}</span>' for s in matched])
                st.markdown(f'<div class="skill-grid">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:var(--muted); font-size:0.8rem; font-family:var(--font-mono);">No matched skills detected.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with sk2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-label">✗ Missing Skills</div>', unsafe_allow_html=True)
            if missing:
                chips = "".join([f'<span class="chip chip-miss">{s}</span>' for s in missing])
                st.markdown(f'<div class="skill-grid">{chips}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:var(--muted); font-size:0.8rem; font-family:var(--font-mono);">All key skills accounted for 🎉</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Recommendation ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-head">💡 Recommendation</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="rec-box">{recommendation}</div>', unsafe_allow_html=True)

        # ── Footer note ──
        st.markdown("""
        <br>
        <p style="font-family:var(--font-mono); font-size:0.65rem; color:var(--muted); text-align:center; letter-spacing:0.1em;">
            Analysis powered by semantic NLP · Results are indicative, not definitive
        </p>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.3);
             border-radius:8px; padding:1rem 1.4rem;
             font-family:var(--font-mono); font-size:0.82rem; color:#fbbf24; letter-spacing:0.04em;">
            ⚠ &nbsp; Please upload a resume file <strong>and</strong> paste a job description to proceed.
        </div>
        """, unsafe_allow_html=True)