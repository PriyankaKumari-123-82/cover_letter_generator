Cover Letter Generator
A Streamlit-based web application that generates professional cover letters by either uploading a resume (PDF or DOCX) to auto-fill details or manually entering information. The app extracts key details like name, email, phone, skills, and experience from the resume and creates a tailored cover letter that can be downloaded as a text file.
Features

Resume Upload: Upload a PDF or DOCX resume to automatically populate fields (name, email, phone, skills, experience).
Manual Input: Enter details manually if no resume is uploaded or to override parsed data.
Customizable Cover Letter: Generate a professional cover letter tailored to a specific job and company.
Downloadable Output: Save the generated cover letter as a .txt file.
User-Friendly Interface: Clean layout with form inputs and styled elements for better usability.

Installation

Clone the Repository:
git clone <repository-url>
cd cover-letter-generator


Install Dependencies:Ensure Python 3.7+ is installed, then install the required libraries:
pip install streamlit PyPDF2 python-docx


Run the Application:
streamlit run cover_letter_generator.py

Open your browser to http://localhost:8501.


Usage

Upload Resume (Optional):

Upload a PDF or DOCX resume to auto-fill your name, email, phone, skills, and experience.
Review and edit the prefilled fields if needed.


Enter Details:

Provide your address, company name, company address, hiring manager’s name (optional), and job title.
Add or modify skills (comma-separated) and a brief description of relevant experience.


Generate Cover Letter:

Click "Generate Cover Letter" to create a professional cover letter.
Review the output in the text area.
Click "Download Cover Letter" to save it as a .txt file.



Requirements

Python 3.7 or higher
Libraries:
streamlit
PyPDF2
python-docx



Install them using:
pip install -r requirements.txt

Notes

Resume Parsing: The app uses basic parsing to extract details from resumes. For best results, use resumes with clear sections (e.g., "Skills," "Experience") and standard formats for name, email, and phone.
Styling: The app uses custom CSS for better readability. If text is hard to read, consider adding a dark theme by creating a .streamlit/config.toml file:[theme]
base = "dark"
primaryColor = "#0066cc"
backgroundColor = "#1a1a1a"
secondaryBackgroundColor = "#333333"
textColor = "#ffffff"
font = "sans serif"


File Size Limit: Streamlit’s default upload limit is 200MB. For larger resumes, adjust the server settings with --server.maxUploadSize.

Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.
License
This project is licensed under the MIT License.