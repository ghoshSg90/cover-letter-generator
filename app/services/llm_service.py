import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_cover_letter(
        company,
        role,
        job_description):

    prompt = f"""
    Company: {company}

    Role: {role}

    Job Description:
    {job_description}

    Generate a professional ATS-friendly
    cover letter.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi4-mini",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
