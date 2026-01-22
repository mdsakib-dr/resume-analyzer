import pdfplumber
import re
import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer



nlp = spacy.load("en_core_web_sm")




SKILLS = {
    # Programming
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c++"],
    "JavaScript": ["javascript", "js"],

    # Backend
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Node.js": ["node", "node.js", "nodejs"],
    "Spring Boot": ["spring boot", "springboot"],

    # Frontend
    "React": ["react", "react.js", "reactjs"],
    "Next.js": ["next.js", "nextjs"],
    "HTML": ["html"],
    "CSS": ["css"],

    # ML / AI
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision"],

    # Data
    "SQL": ["sql", "mysql", "postgresql"],
    "NoSQL": ["nosql", "mongodb"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],

    # DevOps / Cloud
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "GCP": ["gcp", "google cloud"],
    "Azure": ["azure"],

    # Tools
    "Git": ["git", "github", "gitlab"],
}

GENERIC_BLACKLIST = {
    "experience", "project", "projects", "profile", "summary",
    "education", "university", "degree", "responsibility",
    "responsibilities", "company", "role", "team", "skills",
    "system", "systems"
}

# STOP_VERBS = {"work", "worked", "using", "use", "developed", "building"}


EMAIL_REGEX = re.compile(
    r"""
    (?<![A-Za-z0-9._%+-])
    ([A-Za-z0-9._%+-]+
    @
    [A-Za-z0-9.-]+
    \.[A-Za-z]{2,})
    """,
    re.VERBOSE
)

PHONE_REGEX = re.compile(
    r"""
    (?<!\d)                    # no digit before
    (?:\+?\d{1,3}[\s\-()]*)?   # optional country code (+1, +44, +880, etc.)
    (?:\d{2,4}[\s\-()]*){2,4}  # area/operator codes
    \d{3,4}                    # subscriber number
    (?!\d)                     # no digit after
    """,
    re.VERBOSE
)








NAME_BLACKLIST = {
    "resume", "curriculum vitae", "cv", "profile",
    "summary", "objective", "experience"
}

def clean_line(line):
    return re.sub(r"[^A-Za-z ]", "", line).strip()

def looks_like_name(line):
    """
    Heuristic checks for a real human name
    """
    if not line:
        return False

    words = line.split()
    if len(words) < 2 or len(words) > 4:
        return False

    if any(word.lower() in NAME_BLACKLIST for word in words):
        return False

    if not all(word[0].isupper() for word in words):
        return False

    return True


def extract_name_from_header(text):
    """
    Best accuracy: header-based detection
    """
    lines = text.splitlines()[:5]  # top of resume
    for line in lines:
        line = clean_line(line)
        if looks_like_name(line):
            return line
    return ""


def extract_name_with_spacy(text):
    """
    NLP fallback
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = clean_line(ent.text)
            if looks_like_name(name):
                return name
    return ""


def extract_name(text):
    """
    Final layered name extractor
    """
    name = extract_name_from_header(text)
    if name:
        return name

    name = extract_name_with_spacy(text)
    if name:
        return name

    return ""



def extract_email(text: str) -> str:
    """
    Extract primary email, prioritizing header
    """
    lines = text.splitlines()[:10]  # header priority

    # 1️⃣ Header scan
    for line in lines:
        match = EMAIL_REGEX.search(line)
        if match:
            return match.group(1)

    # 2️⃣ Full text fallback
    match = EMAIL_REGEX.search(text)
    if match:
        return match.group(1)

    return ""

#  ---------------- Parsing phon Number from pdf ------------------------

def normalize_phone(country, number):
    """
    Normalize to +8801XXXXXXXXX
    """
    if number.startswith("01"):
        return "+880" + number[1:]
    if country:
        return "+880" + number
    return "+880" + number


def extract_phone(text: str) -> str:
    """
    International & national phone extraction with normalization
    """
    matches = PHONE_REGEX.findall(text)

    for match in matches:
        # Extract digits only
        digits = "".join(ch for ch in match if ch.isdigit())

        # Ignore very short or very long numbers
        if len(digits) < 10 or len(digits) > 15:
            continue

        # Normalize common cases
        # Bangladesh
        if digits.startswith("01") and len(digits) == 11:
            return "+880" + digits[1:]

        if digits.startswith("880") and len(digits) in [12, 13]:
            return "+" + digits

        # Generic international
        if digits.startswith("1") and len(digits) == 11:     # US/Canada
            return "+" + digits

        if len(digits) >= 10:
            return "+" + digits

    return ""


# ---------------------------- parsing skills from pdf ---------------------------


def extract_skills_from_dictionary(text: str):
    text = text.lower()
    found = []

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            if re.search(rf"\b{re.escape(alias)}\b", text):
                found.append(skill)
                break

    return found
def extract_skills_with_nlp(text: str, blacklist: set):
    doc = nlp(text.lower())
    skills = []

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()

        if len(phrase.split()) > 3:
            continue

        if phrase in blacklist:
            continue

        if any(tok.is_stop for tok in nlp(phrase)):
            continue

        skills.append(phrase.title())

    return skills
def extract_skills(text: str, name: str = "", max_skills: int = 10):
    blacklist = set(GENERIC_BLACKLIST)

    # add candidate name to blacklist
    if name:
        blacklist |= set(name.lower().split())
        blacklist.add(name.lower())

    # 1️⃣ dictionary-based (primary)
    skills = extract_skills_from_dictionary(text)

    # 2️⃣ NLP fallback only if needed
    if len(skills) < 4:
        nlp_skills = extract_skills_with_nlp(text, blacklist)
        skills.extend(nlp_skills)

    # 3️⃣ clean + deduplicate
    final = []
    seen = set()

    for s in skills:
        if s.lower() not in seen:
            seen.add(s.lower())
            final.append(s)

    return final[:max_skills]


def parse_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "text": text
    }

def parse_text(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "text": text
    }
