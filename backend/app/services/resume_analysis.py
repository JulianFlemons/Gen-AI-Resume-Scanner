import re


def contains_skill(text, skill):
    """Return whether text contains a skill as a whole term or phrase."""
    pattern = rf"(?<!\w){re.escape(skill.lower())}(?!\w)"
    return re.search(pattern, text.lower()) is not None


SKILL_TERMS = [
    # Programming languages
    "python", "r", "sql", "scala", "java", "javascript", "typescript",
    "c", "c++", "c#", "go", "rust", "bash", "matlab", "julia",

    # Data analysis and statistics
    "data analysis", "exploratory data analysis", "statistical analysis",
    "descriptive statistics", "inferential statistics", "hypothesis testing",
    "regression analysis", "time series analysis", "causal inference",
    "A/B testing", "data cleaning", "data wrangling", "feature engineering",
    "data mining", "data visualization", "business intelligence",
    "requirements analysis", "metrics design", "cohort analysis",

    # Analytics and visualization tools
    "pandas", "numpy", "scipy", "polars", "jupyter", "excel",
    "tableau", "power bi", "looker", "matplotlib", "seaborn",
    "plotly", "superset", "streamlit", "dash",

    # Machine learning
    "machine learning", "supervised learning", "unsupervised learning",
    "semi-supervised learning", "reinforcement learning", "deep learning",
    "classification", "clustering", "dimensionality reduction",
    "anomaly detection", "recommendation systems", "ranking systems",
    "natural language processing", "computer vision", "forecasting",
    "model training", "model evaluation", "model selection",
    "hyperparameter tuning", "cross-validation", "scikit-learn",
    "xgboost", "lightgbm", "catboost", "imbalanced-learn",

    # Deep learning frameworks
    "pytorch", "tensorflow", "keras", "jax", "hugging face transformers",
    "onnx", "cuda", "distributed training", "model quantization",

    # Generative AI and language models
    "generative ai", "large language models", "transformer models",
    "prompt engineering", "prompt design", "fine-tuning",
    "retrieval-augmented generation", "semantic search", "embeddings",
    "vector search", "information retrieval", "reranking",
    "llm evaluation", "ai agents", "tool calling", "structured outputs",
    "guardrails", "text generation", "speech recognition",
    "mistral", "openai api", "anthropic api", "hugging face",

    # Data engineering and pipelines
    "data engineering", "data pipelines", "etl", "elt",
    "batch processing", "stream processing", "apache spark", "pyspark",
    "apache flink", "apache kafka", "airflow", "dagster", "prefect",
    "dbt", "data orchestration", "data lake", "data lakehouse",
    "data warehouse", "data modeling", "dimensional modeling",
    "change data capture", "data lineage", "schema evolution",

    # Databases and storage
    "postgresql", "mysql", "sqlite", "microsoft sql server", "oracle database",
    "mongodb", "redis", "elasticsearch", "opensearch", "cassandra",
    "dynamodb", "snowflake", "databricks", "bigquery", "redshift",
    "google cloud storage", "amazon s3", "delta lake", "iceberg",

    # Cloud and infrastructure
    "aws", "microsoft azure", "google cloud platform", "vertex ai",
    "azure machine learning", "amazon sagemaker", "docker",
    "kubernetes", "terraform", "linux", "serverless computing",

    # APIs and application development
    "fastapi", "flask", "django", "rest api", "graphql",
    "api development", "microservices", "web applications",
    "pydantic", "streamlit", "authentication", "authorization",

    # MLOps and model deployment
    "mlops", "model deployment", "model serving", "model monitoring",
    "model registry", "experiment tracking", "mlflow", "weights and biases",
    "kubeflow", "feature store", "data drift", "model drift",
    "continuous integration", "continuous deployment",

    # Software quality and collaboration
    "git", "github", "github actions", "pytest", "unit testing",
    "integration testing", "test automation", "code review",
    "technical documentation", "agile development",
]
#Parse the extracted text into sections based on common resume section headers
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

#Score the resume based on parsed sections and job description
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
    job_text = job_description.lower()
    resume_text = " ".join(parsed_sections.values()).lower()

    job_skills = {
        skill for skill in SKILL_TERMS
        if contains_skill(job_text, skill)
    }
    resume_skills = {
        skill for skill in SKILL_TERMS
        if contains_skill(resume_text, skill)
    }

    matched_skills = job_skills & resume_skills
    skills_missing = job_skills - matched_skills
    skills_score_pct = (
        round(100 * len(matched_skills) / len(job_skills))
        if job_skills else 0
    )

    exp_keys = ["experience", "work experience", "professional experience"]
    edu_keys = ["education", "academic"]

    experience_text = ""
    for key in parsed_sections:
        if any(k in key.lower() for k in exp_keys):
            experience_text = parsed_sections[key].lower()
            break
    matched_exp = sum(
        1 for skill in job_skills
        if contains_skill(experience_text, skill)
    )
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
