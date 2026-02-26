import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import pdfkit
import PyPDF2
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()

# ==============================
# GEMINI CONFIG
# ==============================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_ai_content(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

# ==============================
# PDF CONFIG (Cloud Safe)
# ==============================

try:
    config = pdfkit.configuration()
except:
    config = None

# ==============================
# APP CONFIG
# ==============================

st.set_page_config(page_title="AI Resume Builder", layout="wide")
st.title("AI Resume Builder & ATS Checker")

if "profile_data" not in st.session_state:
    st.session_state.profile_data = {}

if "generated_resume" not in st.session_state:
    st.session_state.generated_resume = None

if "projects" not in st.session_state:
    st.session_state.projects = []

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:
    st.header("Profile Information")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    location = st.text_input("Location")
    linkedin = st.text_input("LinkedIn")
    github = st.text_input("GitHub")

    st.subheader("Professional Summary")
    summary = st.text_area("Summary")

    st.subheader("Education")
    degree = st.text_input("Degree")
    institution = st.text_input("Institution")
    cgpa = st.text_input("CGPA")
    edu_duration = st.text_input("Education Duration")

    st.subheader("Technical Skills")
    languages = st.text_input("Programming Languages")
    frameworks = st.text_input("Frameworks")
    databases = st.text_input("Databases")
    tools = st.text_input("Tools")

    st.subheader("Add Projects (Unlimited)")
    project_title = st.text_input("Project Title")
    project_desc = st.text_area("Project Description")

    if st.button("Add Project"):
        if project_title and project_desc:
            st.session_state.projects.append({
                "title": project_title,
                "desc": project_desc
            })
            st.success("Project Added!")

    st.subheader("Experience")
    company = st.text_input("Company")
    role = st.text_input("Role")
    exp_duration = st.text_input("Experience Duration")

    st.subheader("Certifications")
    certifications = st.text_area("Certifications")

    st.subheader("Achievements")
    achievements = st.text_area("Achievements")

if st.button("Update Profile"):
    st.session_state.profile_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "linkedin": linkedin,
        "github": github,
        "summary": summary,
        "degree": degree,
        "institution": institution,
        "cgpa": cgpa,
        "edu_duration": edu_duration,
        "languages": languages,
        "frameworks": frameworks,
        "databases": databases,
        "tools": tools,
        "company": company,
        "role": role,
        "exp_duration": exp_duration,
        "certifications": certifications,
        "achievements": achievements,
    }
    st.success("Profile Updated!")

st.divider()

# ==============================
# HELPER FUNCTION
# ==============================

def improve_section(title, content):
    if not content:
        return ""
    prompt = f"""
Rewrite the following {title} professionally.
Return only final improved content.
Use strong action verbs.
Keep it ATS-friendly.
No explanations.
Content:
{content}
"""
    return generate_ai_content(prompt)

# ==============================
# BEGINNER RESUME
# ==============================

def generate_beginner_resume():
    data = st.session_state.profile_data

    projects_html = ""
    for project in st.session_state.projects:
        projects_html += f"<p><strong>{project['title']}</strong><br>{project['desc']}</p>"

    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; padding: 40px; }}
            h3 {{ border-bottom: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>{data.get('name')}</h1>
        <p>{data.get('email')} | {data.get('phone')}<br>
        {data.get('location')}<br>
        LinkedIn: {data.get('linkedin')} | GitHub: {data.get('github')}</p>

        <h3>Professional Summary</h3>
        <p>{data.get('summary')}</p>

        <h3>Education</h3>
        <p><strong>{data.get('degree')}</strong><br>
        {data.get('institution')}<br>
        CGPA: {data.get('cgpa')} | {data.get('edu_duration')}</p>

        <h3>Technical Skills</h3>
        <p>{data.get('languages')}<br>
        {data.get('frameworks')}<br>
        {data.get('databases')}<br>
        {data.get('tools')}</p>

        <h3>Projects</h3>
        {projects_html}

        <h3>Experience</h3>
        <p>{data.get('company')} - {data.get('role')}<br>
        {data.get('exp_duration')}</p>

        <h3>Certifications</h3>
        <p>{data.get('certifications')}</p>

        <h3>Achievements</h3>
        <p>{data.get('achievements')}</p>
    </body>
    </html>
    """

# ==============================
# PROFESSIONAL RESUME (AI)
# ==============================

def generate_professional_resume():
    data = st.session_state.profile_data

    improved_summary = improve_section("Professional Summary", data.get("summary"))
    improved_certifications = improve_section("Certifications", data.get("certifications"))
    improved_achievements = improve_section("Achievements", data.get("achievements"))

    projects_html = ""
    for project in st.session_state.projects:
        improved_project = improve_section("Project Description", project["desc"])
        projects_html += f"<p><strong>{project['title']}</strong><br>{improved_project}</p>"

    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; padding: 40px; }}
            h3 {{ border-bottom: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <h1>{data.get('name')}</h1>
        <p>{data.get('email')} | {data.get('phone')}<br>
        {data.get('location')}<br>
        LinkedIn: {data.get('linkedin')} | GitHub: {data.get('github')}</p>

        <h3>Professional Summary</h3>
        <p>{improved_summary}</p>

        <h3>Education</h3>
        <p><strong>{data.get('degree')}</strong><br>
        {data.get('institution')}<br>
        CGPA: {data.get('cgpa')} | {data.get('edu_duration')}</p>

        <h3>Technical Skills</h3>
        <p>{data.get('languages')}<br>
        {data.get('frameworks')}<br>
        {data.get('databases')}<br>
        {data.get('tools')}</p>

        <h3>Projects</h3>
        {projects_html}

        <h3>Experience</h3>
        <p>{data.get('company')} - {data.get('role')}<br>
        {data.get('exp_duration')}</p>

        <h3>Certifications</h3>
        <p>{improved_certifications}</p>

        <h3>Achievements</h3>
        <p>{improved_achievements}</p>
    </body>
    </html>
    """

# ==============================
# TABS
# ==============================

tab1, tab2 = st.tabs(["Resume Builder", "ATS Score Checker"])

with tab1:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Beginner Resume"):
            st.session_state.generated_resume = generate_beginner_resume()

    with col2:
        if st.button("Generate Professional Resume"):
            st.session_state.generated_resume = generate_professional_resume()

    if st.session_state.generated_resume:
        components.html(st.session_state.generated_resume, height=900)

        # ✅ SAFE PDF BLOCK
        if st.button("Download as PDF"):

            if config is None:
                st.error("PDF generation not supported on cloud deployment.")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    pdfkit.from_string(
                        st.session_state.generated_resume,
                        tmp.name,
                        configuration=config
                    )
                    pdf_data = open(tmp.name, "rb").read()

                st.download_button(
                    label="Click to Download PDF",
                    data=pdf_data,
                    file_name="resume.pdf",
                    mime="application/pdf"
                )

with tab2:

    st.subheader("Upload Resume (PDF only)")

    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ""

        # ✅ SAFE PDF TEXT EXTRACTION
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        job_description = st.text_area("Paste Job Description")

        if st.button("Analyze ATS Score"):
            prompt = f"""
You are an ATS system.
Give ATS Score out of 100.
List Missing Keywords.
Provide Improvements.
Resume:
{resume_text}
Job Description:
{job_description}
"""
            result = generate_ai_content(prompt)
            st.write(result)