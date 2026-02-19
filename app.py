# ============================================
# STEP 1: IMPORTS
# ============================================
import re
import json
import streamlit as st
import pandas as pd
import pdfplumber as pdf
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
from huggingface_hub import InferenceClient

# ============================================
# STEP 2: PAGE CONFIGURATION
# ============================================
st.set_page_config(page_title='GenAI Resume Scanner', page_icon=':file_folder:', layout='wide')

# ============================================
# STEP 3: MAIN TITLE
# ============================================
st.title("GenAI Resume Scanner")




# ============================================
# STEP 4: SIDEBAR SETUP
# ============================================
with st.sidebar:
    st.header("Upload a resume")
    uploaded_file = st.file_uploader("Upload a resume ", type = ['pdf', 'docx'], accept_multiple_files=False)
    job_description = st.text_area("Enter the job description", height = 300)
    st.markdown("---")
    hf_token = st.text_input("Hugging Face API Token", type="password",
                             help="Get a free token at https://huggingface.co/settings/tokens")


#extract the text from the resume
def extract_resume_text(uploaded_file):
    """
    Extract all text content from an uploaded PDF or DOCX resume.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        str: Extracted text, or None if error
    """
    # Get file extension to determine file type
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    # Initialize empty string to store extracted text
    extracted_text = ""
    
    try:
        # Route to PDF or DOCX logic based on file extension
        if file_extension == "pdf":
            # PDF extraction using pdfplumber
            with pdf.open(uploaded_file) as pdf_document:
                # Iterate through all pages in the PDF
                for page in pdf_document.pages:
                    # Extract text from current page
                    page_text = page.extract_text()
                    # Append extracted text to extracted_text variable
                    if page_text:
                        extracted_text += page_text + "\n"
        
        elif file_extension == "docx":
            # DOCX extraction using python-docx
            # Reset file pointer to beginning (Streamlit files need this)
            uploaded_file.seek(0)
            # Load the document
            doc = Document(uploaded_file)
            # Iterate through all paragraphs in the document
            for paragraph in doc.paragraphs:
                # Extract text from current paragraph
                if paragraph.text:
                    extracted_text += paragraph.text + "\n"
        
        else:
            # Unsupported file type
            st.error(f"Unsupported file type: {file_extension}. Please upload a PDF or DOCX file.")
            return None
        
        # Return the extracted text (cleaned/trimmed)
        return extracted_text.strip() if extracted_text else None
        
    except Exception as e:
        # Handle errors gracefully
        st.error(f"Error extracting text from resume: {e}")
        return None


# --------------------------------------------------
# Parse resume into sections
# --------------------------------------------------
def parse_sections(extracted_text):
    """
    Parse the extracted text into sections.

    Args:
        extracted_text: str - Extracted text from the resume

    Returns:
        dict: Parsed sections, or None if error
    """
    def is_overlapping(new_start, existing_matches):
        if not existing_matches:
            return False
        for match in existing_matches:
            start_index = match["start_index"]
            end_index = match["end_index"]
            if new_start >= start_index and new_start < end_index:
                return True
        return False
    skills = ["skills", "technical skills", "core competencies", "technical skills and competencies", "technical skills and abilities", "technical skills and qualifications", "technical skills and experience", "technical skills and education", "technical skills and training", "technical skills and certification", "technical skills and licenses", "technical skills and awards", "technical skills and achievements", "technical skills and accomplishments", "technical skills and contributions", "technical skills and responsibilities", "technical skills and duties", "technical skills and tasks", "technical skills and projects", "technical skills and responsibilities", "technical skills and duties", "technical skills and tasks", "technical skills and projects"]
    experience = ["experience", "work experience", "professional experience", "professional experience and responsibilities", "professional experience and duties", "professional experience and tasks", "professional experience and projects", "professional experience and responsibilities", "professional experience and duties", "professional experience and tasks", "professional experience and projects"]
    education = ["education", "academic", "academics", "academic background", "academic qualifications", "academic experience", "academic education", "academic training", "academic certification", "academic licenses", "academic awards", "academic achievements", "academic accomplishments", "academic contributions", "academic responsibilities", "academic duties", "academic tasks", "academic projects", "academic responsibilities", "academic duties", "academic tasks", "academic projects"]
    projects = ["projects", "personal projects", "projects and duties", "projects and tasks", "projects and projects", "projects and responsibilities", "projects and duties", "projects and tasks"]
    certifications = ["certifications", "certificates", "certification", "certificate", "certifications and certifications", "certifications and certificates", "certifications and certification", "certifications and certificate"]
    skills_headers = sorted(skills, key=len, reverse=True)
    experience_headers = sorted(experience, key=len, reverse=True)
    education_headers = sorted(education, key=len, reverse=True)
    projects_headers = sorted(projects, key=len, reverse=True)
    certifications_headers = sorted(certifications, key=len, reverse=True)
    original_text = extracted_text
    normalized_text = extracted_text.lower()
    sections_found = []
    for header in skills_headers:
        start_index = normalized_text.find(header)
        if start_index != -1:
            if not is_overlapping(start_index, sections_found):
                sections_found.append({"section_name": header, "start_index": start_index, "end_index": start_index + len(header), "matched_header": header})
    for header in experience_headers:
        start_index = normalized_text.find(header)
        if start_index != -1:
            if not is_overlapping(start_index, sections_found):
                sections_found.append({"section_name": header, "start_index": start_index, "end_index": start_index + len(header), "matched_header": header})
    for header in education_headers:
        start_index = normalized_text.find(header)
        if start_index != -1:
            if not is_overlapping(start_index, sections_found):
                sections_found.append({"section_name": header, "start_index": start_index, "end_index": start_index + len(header), "matched_header": header})
    for header in projects_headers:
        start_index = normalized_text.find(header)
        if start_index != -1:
            if not is_overlapping(start_index, sections_found):
                sections_found.append({"section_name": header, "start_index": start_index, "end_index": start_index + len(header), "matched_header": header})
    for header in certifications_headers:
        start_index = normalized_text.find(header)
        if start_index != -1:
            if not is_overlapping(start_index, sections_found):
                sections_found.append({"section_name": header, "start_index": start_index, "end_index": start_index + len(header), "matched_header": header})
    sections_found_sorted = sorted(sections_found, key=lambda x: x["start_index"])
    sections_dict = {}
    for i in range(len(sections_found_sorted)):
        start = sections_found_sorted[i]["start_index"]
        if i < len(sections_found_sorted) - 1:
            end = sections_found_sorted[i + 1]["start_index"]
        else:
            end = len(original_text)
        section_chunk = original_text[start:end].strip()
        sections_dict[sections_found_sorted[i]["section_name"]] = section_chunk
    return sections_dict


# --------------------------------------------------
# Scoring Engine
# --------------------------------------------------
def compute_scores(parsed_sections, job_description):
    """
    Compare resume (parsed sections) to job description and produce scores.
    Weights: technical/skills 50%, experience 30%, education 20%.
    """
    empty_result = {
        "skills_score": 0,
        "skills_matched": [],
        "skills_missing": [],
        "experience_score": 0,
        "education_score": 0,
        "overall_score": 0,
    }
    if not job_description or not job_description.strip():
        return empty_result
    stop_list = {"the", "and", "or", "a", "of", "to", "in", "for", "is", "on", "with"}
    min_word_len = 2
    job_lower = re.sub(r"[^\w\s]", "", job_description.lower()).strip()
    words = [w for w in job_lower.split() if w not in stop_list and len(w) > min_word_len]
    job_skills = set(words)
    skills_keys = ["skills", "technical skills", "core competencies"]
    resume_skills_text = ""
    for key in parsed_sections:
        if any(sk in key.lower() for sk in skills_keys):
            resume_skills_text = parsed_sections[key]
            break
    resume_lower = resume_skills_text.lower().strip()
    tokens = re.split(r"[,;\n]", resume_lower)
    resume_skills = {s.strip() for s in tokens if s.strip() and len(s.strip()) > 1}
    for js in list(job_skills):
        for rs in resume_skills:
            if js in rs or rs in js:
                resume_skills.add(js)
                break
    exp_keys = ["experience", "work experience", "professional experience"]
    edu_keys = ["education", "academic"]
    other_text = ""
    for key in parsed_sections:
        if any(k in key.lower() for k in exp_keys + edu_keys):
            other_text += " " + parsed_sections[key].lower()
    for js in job_skills:
        if js in other_text:
            resume_skills.add(js)
    matched_skills = job_skills & resume_skills
    skills_missing = job_skills - resume_skills
    skills_score_pct = round(100 * len(matched_skills) / len(job_skills)) if job_skills else 0
    experience_text = ""
    for key in parsed_sections:
        if any(k in key.lower() for k in exp_keys):
            experience_text = parsed_sections[key].lower()
            break
    matched_exp = sum(1 for s in job_skills if s in experience_text)
    experience_score = round(100 * matched_exp / len(job_skills)) if job_skills else 0
    education_text = ""
    for key in parsed_sections:
        if any(k in key.lower() for k in edu_keys):
            education_text = parsed_sections[key].lower()
            break
    degree_markers = ["bachelor", "master", "phd", "bs ", "ms ", "b.s.", "m.s.", "degree", "computer science"]
    education_score = 100 if any(m in education_text for m in degree_markers) else 0
    overall_score = round(0.5 * skills_score_pct + 0.3 * experience_score + 0.2 * education_score)
    return {
        "skills_score": skills_score_pct,
        "skills_matched": sorted(matched_skills),
        "skills_missing": sorted(skills_missing),
        "experience_score": experience_score,
        "education_score": education_score,
        "overall_score": min(100, overall_score),
    }


# --------------------------------------------------
# AI Analysis via Hugging Face Inference API
# --------------------------------------------------
AI_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

def analyze_with_ai(resume_text, job_description, token):
    if not token:
        return {"error": "Please enter your Hugging Face API token in the sidebar."}

    prompt = f"""You are an expert ATS resume analyst.

Analyze the resume against the job description below.
You MUST return ONLY a valid JSON object — no markdown, no backticks, no explanation, nothing else before or after the JSON.

The JSON must have exactly these keys:
{{
  "summary": "2-3 sentence overall assessment",
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "strengths": ["point1", "point2", "point3"],
  "improvements": ["suggestion1", "suggestion2", "suggestion3"],
  "fit_rating": 7
}}

---RESUME---
{resume_text[:4000]}

---JOB DESCRIPTION---
{job_description[:2000]}

Remember: Return ONLY the JSON object. Start your response with {{ and end with }}"""

    try:
        client = InferenceClient(token=token)
        response = client.chat_completion(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.1,  # lower = more deterministic
        )
        raw = response.choices[0].message.content.strip()

        # Attempt 1: try parsing as-is
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # Attempt 2: extract content between first { and last }
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(raw[start:end])
            except json.JSONDecodeError:
                pass

        # Attempt 3: strip markdown code blocks
        cleaned = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        return {"error": "The AI returned an unparsable response. Try again.", "raw": raw}

    except Exception as e:
        return {"error": str(e)}


# ============================================
# STEP 5: MAIN AREA LOGIC
# ============================================
if uploaded_file is not None:
    st.info("Resume uploaded successfully")
    extracted_text = extract_resume_text(uploaded_file)
    if extracted_text:
        parsed_sections = parse_sections(extracted_text)
        scores = compute_scores(parsed_sections, job_description or "")

        st.subheader("Scoring Engine")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Skills Match", f"{scores['skills_score']}%")
        with c2:
            st.metric("Experience Relevance", f"{scores['experience_score']}%")
        with c3:
            st.metric("Education", f"{scores['education_score']}%")
        with c4:
            st.metric("Overall Fit", f"{scores['overall_score']}%")

        with st.expander("Skills matched"):
            st.write(scores["skills_matched"] if scores["skills_matched"] else "None")
        with st.expander("Skills missing (from job description)"):
            st.write(scores["skills_missing"] if scores["skills_missing"] else "None")

        # -------------------------------------------------------------------------
        # Visualizations (only when job description is provided)
        # -------------------------------------------------------------------------
        has_job_desc = job_description and str(job_description).strip()
        if not has_job_desc:
            st.warning("Enter a job description to see match and skill gap.")
        else:
            st.subheader("Match & skill gap")
            # ---- 1) Overall fit gauge ----
            overall = scores["overall_score"]
            if overall >= 70:
                gauge_color = "#22c55e"
            elif overall >= 40:
                gauge_color = "#eab308"
            else:
                gauge_color = "#ef4444"
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=overall,
                number={"suffix": "%", "font": {"size": 32}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": gauge_color},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "gray",
                    "steps": [
                        {"range": [0, 40], "color": "#fecaca"},
                        {"range": [40, 70], "color": "#fef08a"},
                        {"range": [70, 100], "color": "#bbf7d0"},
                    ],
                    "threshold": {
                        "line": {"color": gauge_color, "width": 4},
                        "thickness": 0.75,
                        "value": overall,
                    },
                },
                title={"text": "Overall fit", "font": {"size": 18}},
            ))
            fig_gauge.update_layout(
                height=280,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(size=12),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # ---- 2) Skill gap bar chart (matched vs missing, max 15 each) ----
            matched = (scores["skills_matched"] or [])[:15]
            missing = (scores["skills_missing"] or [])[:15]
            if matched or missing:
                rows = []
                for s in matched:
                    rows.append({"skill": s, "count": 1, "status": "Matched"})
                for s in missing:
                    rows.append({"skill": s, "count": 1, "status": "Missing"})
                df_gap = pd.DataFrame(rows)
                if not df_gap.empty:
                    fig_gap = px.bar(
                        df_gap,
                        x="count",
                        y="skill",
                        orientation="h",
                        color="status",
                        color_discrete_map={"Matched": "#22c55e", "Missing": "#ef4444"},
                        category_orders={"status": ["Matched", "Missing"]},
                    )
                    fig_gap.update_layout(
                        title="Skill gap (job wants vs resume)",
                        xaxis_title="",
                        yaxis_title="",
                        yaxis={"categoryorder": "total ascending"},
                        height=max(300, 24 * len(df_gap)),
                        margin=dict(l=20, r=20, t=40, b=20),
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    )
                    fig_gap.update_xaxes(showticklabels=False)
                    st.plotly_chart(fig_gap, use_container_width=True)
            else:
                st.caption("No skill keywords found in job description to compare.")

            # ---- 3) Sub-score breakdown ----
            sub_names = ["Skills", "Experience", "Education"]
            sub_values = [
                scores["skills_score"],
                scores["experience_score"],
                scores["education_score"],
            ]
            fig_sub = go.Figure(
                go.Bar(
                    x=sub_names,
                    y=sub_values,
                    marker_color=["#3b82f6", "#8b5cf6", "#06b6d4"],
                    text=[f"{v}%" for v in sub_values],
                    textposition="outside",
                )
            )
            fig_sub.update_layout(
                title="Score breakdown (0–100)",
                yaxis=dict(range=[0, 100], title="Score %"),
                height=320,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False,
            )
            st.plotly_chart(fig_sub, use_container_width=True)

        # -------------------------------------------------------------------------
        # AI-Powered Analysis Section
        # -------------------------------------------------------------------------
        st.write("---")
        st.subheader("AI-Powered Analysis")

        if not has_job_desc:
            st.warning("Enter a job description in the sidebar to enable AI analysis.")
        else:
            if st.button("Run AI Analysis", type="primary", use_container_width=True):
                with st.spinner(f"Analyzing with {AI_MODEL}... this may take a moment."):
                    ai_result = analyze_with_ai(extracted_text, job_description, hf_token)

                if "error" in ai_result:
                    st.error(f"AI analysis failed: {ai_result['error']}")
                    if "raw" in ai_result:
                        with st.expander("Raw AI response"):
                            st.code(ai_result["raw"])
                else:
                    st.session_state["ai_result"] = ai_result

            if "ai_result" in st.session_state:
                ai = st.session_state["ai_result"]

                fit = ai.get("fit_rating", "?")
                if isinstance(fit, int):
                    if fit >= 7:
                        fit_color = "green"
                    elif fit >= 4:
                        fit_color = "orange"
                    else:
                        fit_color = "red"
                    st.markdown(f"### AI Fit Rating: :{fit_color}[{fit} / 10]")
                
                st.markdown(f"**Summary:** {ai.get('summary', 'N/A')}")

                col_left, col_right = st.columns(2)
                with col_left:
                    st.markdown("**Matched Skills (AI)**")
                    for skill in ai.get("matched_skills", []):
                        st.markdown(f"- :green[{skill}]")
                with col_right:
                    st.markdown("**Missing Skills (AI)**")
                    for skill in ai.get("missing_skills", []):
                        st.markdown(f"- :red[{skill}]")

                st.markdown("---")
                col_s, col_i = st.columns(2)
                with col_s:
                    st.markdown("**Strengths**")
                    for point in ai.get("strengths", []):
                        st.markdown(f"- {point}")
                with col_i:
                    st.markdown("**Suggested Improvements**")
                    for point in ai.get("improvements", []):
                        st.markdown(f"- {point}")

        st.write("---")
        with st.expander("Raw resume text"):
            st.write(extracted_text)
else:
    st.info("Please upload a resume to begin")




