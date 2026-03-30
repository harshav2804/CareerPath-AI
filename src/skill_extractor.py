import fitz  # PyMuPDF


def extract_text_from_pdf(file):
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text.lower()


def extract_skills(text, skills_list):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill.lower())

    return list(set(found_skills))