import streamlit as st
from datetime import datetime
import io
import PyPDF2
from docx import Document
import re

# Set page configuration
st.set_page_config(page_title="Cover Letter Generator", page_icon="📝", layout="wide")

# Title and description
st.title("📝 Cover Letter Generator")
st.write("Upload your resume (PDF or DOCX) to auto-fill your details or enter them manually to generate a professional cover letter.")

# Function to extract text from PDF
def extract_pdf_text(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Failed to read PDF: {e}. Please ensure the file is not corrupted.")
        return ""

# Function to extract text from DOCX
def extract_docx_text(file):
    try:
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Failed to read DOCX: {e}. Please ensure the file is valid.")
        return ""

# Function to parse resume for relevant details
def parse_resume(text):
    name = ""
    email = ""
    phone = ""
    skills = []
    experience = ""

    # Normalize text: replace multiple newlines/spaces
    text = re.sub(r"\n\s*\n", "\n", text)
    lines = text.split("\n")

    # Extract name (first line that looks like a full name, typically at the top)
    for line in lines[:10]:  # Check first 10 lines to account for headers
        line = line.strip()
        if re.match(r"^[A-Za-z\s]+$", line) and len(line.split()) in [2, 3, 4]:
            name = line
            break

    # Extract email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text, re.IGNORECASE)
    if email_match:
        email = email_match.group(0)

    # Extract phone number (supports common formats like (123) 456-7890, 123-456-7890, etc.)
    phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    if phone_match:
        phone = phone_match.group(0)

    # Extract skills (look for "Skills" section or common keywords)
    skills_section = re.search(r"(Skills|Technical Skills|Key Skills|Core Competencies)[\s\S]*?(?=\n[A-Z][a-z]*:|\n[A-Z][a-z]*\s[A-Z][a-z]*:|$)", text, re.IGNORECASE)
    if skills_section:
        skills_text = skills_section.group(0)
        # Split by commas, bullets, or newlines
        skills = []
        for s in re.split(r"[,\n•-]", skills_text):
            s = s.strip()
            if s and not s.lower().startswith(("skills", "technical skills", "key skills", "core competencies")):
                skills.append(s)
    else:
        # Fallback: common skill keywords
        common_skills = ["Python", "Java", "SQL", "Project Management", "Data Analysis", "Communication", "Leadership", "JavaScript", "Cloud Computing", "Machine Learning"]
        skills = [skill for skill in common_skills if skill.lower() in text.lower()]

    # Extract experience (look for "Experience" section)
    exp_section = re.search(r"(Experience|Work Experience|Professional Experience|Employment History)[\s\S]*?(?=\n[A-Z][a-z]*:|\n[A-Z][a-z]*\s[A-Z][a-z]*:|$)", text, re.IGNORECASE)
    if exp_section:
        experience = exp_section.group(0).replace("\n", " ").strip()
        experience = re.sub(r"(Experience|Work Experience|Professional Experience|Employment History)\s*:\s*", "", experience, flags=re.IGNORECASE)
        experience = " ".join(experience.split()[:100])[:500]  # Limit to ~100 words
    else:
        # Fallback: extract a chunk of text likely to contain experience
        experience = " ".join([line.strip() for line in lines if line.strip()][:200])[:500]

    return name, email, phone, skills, experience

# Create a form for user input
with st.form("cover_letter_form"):
    st.header("Resume Upload (Optional)")
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    st.header("Your Information")
    col1, col2 = st.columns(2)

    # Initialize session state for form fields
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "email" not in st.session_state:
        st.session_state.email = ""
    if "phone" not in st.session_state:
        st.session_state.phone = ""
    if "skills" not in st.session_state:
        st.session_state.skills = ""
    if "experience" not in st.session_state:
        st.session_state.experience = ""

    # Process uploaded resume
    if resume_file:
        with st.spinner("Parsing resume..."):
            if resume_file.name.endswith(".pdf"):
                resume_text = extract_pdf_text(resume_file)
            elif resume_file.name.endswith(".docx"):
                resume_text = extract_docx_text(resume_file)
            else:
                resume_text = ""
                st.warning("Unsupported file format. Please upload a PDF or DOCX file.")

            if resume_text:
                name, email, phone, skills, experience = parse_resume(resume_text)
                st.session_state.name = name if name else st.session_state.name
                st.session_state.email = email if email else st.session_state.email
                st.session_state.phone = phone if phone else st.session_state.phone
                st.session_state.skills = ", ".join(skills) if skills else st.session_state.skills
                st.session_state.experience = experience if experience else st.session_state.experience
                st.success("Resume parsed successfully! Please review and edit the fields below as needed.")

    with col1:
        your_name = st.text_input("Your Full Name", value=st.session_state.name, placeholder="John Doe", key="your_name")
        your_address = st.text_area("Your Address", placeholder="123 Main St, City, State, ZIP")
        your_email = st.text_input("Your Email", value=st.session_state.email, placeholder="john.doe@example.com")
        your_phone = st.text_input("Your Phone Number", value=st.session_state.phone, placeholder="(123) 456-7890")
    
    with col2:
        company_name = st.text_input("Company Name", placeholder="ABC Corporation")
        company_address = st.text_area("Company Address", placeholder="456 Business Rd, City, State, ZIP")
        hiring_manager = st.text_input("Hiring Manager's Name (Optional)", placeholder="Jane Smith")
        job_title = st.text_input("Job Title", placeholder="Software Engineer")
    
    st.header("Letter Details")
    skills = st.text_area("Your Key Skills (comma-separated)", value=st.session_state.skills, placeholder="Python, Data Analysis, Project Management")
    experience = st.text_area("Brief Description of Relevant Experience", value=st.session_state.experience, placeholder="Describe your relevant work experience...")
    
    # Submit button
    submitted = st.form_submit_button("Generate Cover Letter")

# Function to generate cover letter
def generate_cover_letter(your_name, your_address, your_email, your_phone, 
                         company_name, company_address, hiring_manager, 
                         job_title, skills, experience):
    # Format today's date
    today = datetime.now().strftime("%B %d, %Y")
    
    # Determine greeting
    greeting = f"Dear {hiring_manager}," if hiring_manager else "Dear Hiring Manager,"
    
    # Split skills into a list
    skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
    skills_formatted = ", ".join(skills_list[:-1]) + f", and {skills_list[-1]}" if len(skills_list) > 1 else skills_list[0] if skills_list else "relevant skills"
    
    # Create cover letter content
    letter = f"""{your_name}
{your_address}
{your_email}
{your_phone}

{today}

{company_name}
{company_address}

{greeting}

I am excited to apply for the {job_title} position at {company_name}. With my skills in {skills_formatted} and my relevant experience, I am confident in my ability to contribute effectively to your team.

{experience}

I am particularly drawn to {company_name}'s commitment to innovation and excellence. My background aligns well with the requirements of the {job_title} role, and I am eager to bring my expertise to your organization. I would welcome the opportunity to discuss how my skills and experiences can benefit {company_name}.

Thank you for considering my application. I look forward to the possibility of contributing to your team and am available at your convenience for an interview. Please feel free to contact me at {your_email} or {your_phone}.

Sincerely,
{your_name}
"""
    return letter

# Generate and display cover letter if form is submitted
if submitted:
    if not all([your_name, your_address, your_email, your_phone, company_name, company_address, job_title, skills, experience]):
        st.error("Please fill in all required fields.")
    else:
        with st.spinner("Generating cover letter..."):
            cover_letter = generate_cover_letter(
                your_name, your_address, your_email, your_phone,
                company_name, company_address, hiring_manager,
                job_title, skills, experience
            )
        
        st.subheader("Your Cover Letter")
        st.text_area("Generated Cover Letter", cover_letter, height=400)
        
        # Create a downloadable text file
        buffer = io.StringIO()
        buffer.write(cover_letter)
        st.download_button(
            label="Download Cover Letter",
            data=buffer.getvalue(),
            file_name=f"cover_letter_{your_name.replace(' ', '_')}.txt",
            mime="text/plain"
        )

# Add updated styling for better readability
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
    }
    .stTextInput[key="your_name"] > div > div > input {
        color: #ffffff;
        background-color: #333333;
    }
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
    }
    .stButton > button {
        background-color: #0066cc;
        color: #ffffff;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #0055aa;
        color: #ffffff;
    }
    .stTextArea > label, .stTextInput > label {
        color: #333333;
    }
    .stMarkdown, .stText {
        color: #333333;
    }
    .stMarkdown p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)