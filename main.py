from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
from fastapi.middleware.cors import CORSMiddleware
import re
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from fastapi.responses import StreamingResponse

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {"message": "AI Career Assistant Running"}

# =========================
# RESUME ANALYSIS
# =========================
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    resume_text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"

    # simple NLP logic
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    job_words = set(re.findall(r'\w+', job_description.lower()))

    stopwords = {"the","is","and","to","a","of","in","for","with","on","an","by","as","at","or"}
    resume_words -= stopwords
    job_words -= stopwords

    matched = resume_words.intersection(job_words)
    missing = job_words - resume_words

    score = int((len(matched) / (len(job_words) + 1)) * 100)

    result = f"""
========================
📊 AI CAREER REPORT
========================

🎯 ATS SCORE: {score}/100

✔ MATCHED SKILLS:
{', '.join(list(matched)[:20]) if matched else 'None'}

❌ MISSING SKILLS:
{', '.join(list(missing)[:20]) if missing else 'None'}

✍ IMPROVEMENTS:
- Add missing job keywords
- Improve project descriptions
- Use action verbs

🎯 INTERVIEW QUESTIONS:
1. Tell me about yourself
2. Explain your projects
3. Technical questions
4. Problem solving
5. Why this role?

========================
"""

    return {"result": result, "score": score}


# =========================
# CHAT API
# =========================
@app.post("/chat")
async def chat(message: str = Form(...)):

    msg = message.lower()

    if "resume" in msg:
        response = "Improve resume by adding keywords, achievements, and action verbs."
    elif "job" in msg:
        response = "Match your skills with job description and identify gaps."
    elif "interview" in msg:
        response = "Prepare projects, DSA basics, HR questions, and role topics."
    else:
        response = "Ask about resume, job matching, or interview preparation."

    return {"response": response}


# =========================
# PDF DOWNLOAD
# =========================
@app.post("/download-pdf")
async def download_pdf(result: str = Form(...)):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("AI Career Assistant Report", styles["Title"]))
    content.append(Spacer(1, 12))

    for line in result.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 6))

    doc.build(content)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"}
    )