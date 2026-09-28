import streamlit as st
from backend.parser import extract_text
from backend.matcher import analyze

st.set_page_config(page_title="Resume Matcher", page_icon="📄", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1F1F1B; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #F6F3EC; }
.block-container { max-width: 720px; padding-top: 4rem; padding-bottom: 4rem; }

.eyebrow { font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: #8A8574; margin-bottom: 10px; }
.hero { font-family: 'Instrument Serif', serif; font-size: 52px; line-height: 1.05; margin: 0 0 12px 0; font-weight: 400; }
.sub { color: #6B6759; font-size: 16px; line-height: 1.6; margin-bottom: 36px; }

.stTextArea textarea {
  background: #FBFAF6; border: 1px solid #E2DCCB; border-radius: 14px;
  padding: 16px; font-size: 15px; box-shadow: 0 1px 2px rgba(60,50,20,0.04);
}
.stTextArea textarea:focus { border-color: #1F1F1B; box-shadow: none; }
[data-testid="stFileUploaderDropzone"] {
  background: #FBFAF6; border: 1px dashed #CFC8B4; border-radius: 14px;
}
label, .stTextArea label p, .stFileUploader label p { font-size: 13px !important; font-weight: 500; color: #6B6759; }

.stButton > button {
  background: #1F1F1B; color: #F6F3EC; border: none; border-radius: 999px;
  padding: 12px 32px; font-weight: 500; font-size: 15px; transition: all .2s;
}
.stButton > button:hover { background: #3A3A33; color: #fff; transform: translateY(-1px); }

.card {
  background: #FBFAF6; border: 1px solid #E8E2D2; border-radius: 18px;
  padding: 28px; margin-top: 20px;
  box-shadow: 0 1px 2px rgba(60,50,20,0.04), 0 8px 24px rgba(60,50,20,0.05);
}
.card h4 { font-family: 'Instrument Serif', serif; font-weight: 400; font-size: 24px; margin: 0 0 14px 0; }
.score-wrap { display: flex; align-items: center; gap: 28px; }
.score-label { font-size: 13px; letter-spacing: 0.1em; text-transform: uppercase; color: #8A8574; }
.score-verdict { font-family: 'Instrument Serif', serif; font-size: 30px; margin-top: 4px; }

.chip { display: inline-block; padding: 6px 14px; margin: 0 6px 8px 0; border-radius: 999px; font-size: 13px; font-weight: 500; }
.chip.ok { background: #E4EBDD; color: #3B5A2A; border: 1px solid #CFDCC3; }
.chip.miss { background: #F3E1DA; color: #8A3B22; border: 1px solid #E8C9BD; }
.tip { padding: 12px 0; border-bottom: 1px solid #EDE7D7; font-size: 15px; color: #3A3A33; }
.tip:last-child { border-bottom: none; }
.empty { color: #8A8574; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="eyebrow">Resume Matcher</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero">Does your resume fit the role?</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Upload your resume, paste a job description, and see your match score and the skills you\'re missing.</p>', unsafe_allow_html=True)

resume = st.file_uploader("Resume (PDF)", type="pdf")
jd = st.text_area("Job description", height=200, placeholder="Paste the full job description, including requirements...")

def ring(score: float) -> str:
    c = 2 * 3.14159 * 54
    offset = c * (1 - min(score, 100) / 100)
    return f"""<svg width="130" height="130" viewBox="0 0 130 130">
<circle cx="65" cy="65" r="54" fill="none" stroke="#E8E2D2" stroke-width="8"/>
<circle cx="65" cy="65" r="54" fill="none" stroke="#1F1F1B" stroke-width="8" stroke-linecap="round"
stroke-dasharray="{c:.1f}" stroke-dashoffset="{offset:.1f}" transform="rotate(-90 65 65)"/>
<text x="65" y="74" text-anchor="middle" font-family="Instrument Serif, serif" font-size="32" fill="#1F1F1B">{score:.0f}</text>
</svg>"""

def chips(items, kind):
    if not items:
        return '<span class="empty">None</span>'
    return "".join(f'<span class="chip {kind}">{i}</span>' for i in items)

if st.button("Analyze") and resume and jd:
    with st.spinner("Reading your resume..."):
        res = analyze(extract_text(resume), jd)

    score = res["score"]
    verdict = "Strong match" if score >= 60 else "Decent match" if score >= 40 else "Needs work"

    st.markdown(
        f'<div class="card"><div class="score-wrap">{ring(score)}'
        f'<div><div class="score-label">Match score</div>'
        f'<div class="score-verdict">{verdict}</div></div></div></div>',
        unsafe_allow_html=True,
    )

    if not res["matched"] and not res["missing"]:
        st.warning("No known skills found in this job description. Paste the full JD, including the requirements section.")
    else:
        st.markdown(f'<div class="card"><h4>Matched skills</h4>{chips(res["matched"], "ok")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><h4>Missing skills</h4>{chips(res["missing"], "miss")}</div>', unsafe_allow_html=True)
        if res["suggestions"]:
            tips = "".join(f'<div class="tip">{s}</div>' for s in res["suggestions"])
            st.markdown(f'<div class="card"><h4>Suggestions</h4>{tips}</div>', unsafe_allow_html=True)