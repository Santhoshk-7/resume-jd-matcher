import streamlit as st
import requests

st.title("Resume vs Job Description Matcher")
resume = st.file_uploader("Upload your resume (PDF)", type="pdf")
jd = st.text_area("Paste the job description", height=200)

if st.button("Analyze") and resume and jd:
    res = requests.post(
        "http://localhost:8000/analyze",
        files={"resume": (resume.name, resume.getvalue(), "application/pdf")},
        data={"jd": jd},
    ).json()
    st.metric("Match score", f"{res['score']}%")
    st.subheader("Matched skills")
    st.write(", ".join(res["matched"]) or "None")
    st.subheader("Missing skills")
    st.write(", ".join(res["missing"]) or "None")
    st.subheader("Suggestions")
    for s in res["suggestions"]:
        st.write("-", s)