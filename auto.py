import streamlit as st
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
import tempfile

# ---- CUSTOM THEME CONFIGURATION ----
# Apply custom theme with user-friendly colors
st.set_page_config(
    page_title="Bulk Resume Sender",
    layout="wide"
)

# Custom CSS with a more attractive and user-friendly color scheme
st.markdown("""
<style>
    /* Main background - very light mint green */
    .stApp {
        background-color: #f0f7f0;
    }
    
    /* Primary accent color - teal green */
    .stButton>button {
        background-color: #2c9c8c;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.4rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #38b2a0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Headings - dark teal */
    h1, h2, h3, .stTitle {
        color: #1a6657;
        font-weight: 600;
    }
    
    /* Regular text - dark gray for contrast */
    p, li, div, .stMarkdown, .stText {
        color: #333333;
        font-weight: 500;
    }
    
    /* Container backgrounds */
    .css-1d391kg, .css-1wrcr25 {
        background-color: #dbefe7;
        border-radius: 0.6rem;
        padding: 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border-left: 4px solid #2c9c8c;
    }
    
    /* File upload confirmation */
    .uploadedFile {
        background-color: #e4f4eb;
        border-radius: 0.5rem;
        padding: 0.7rem;
        color: #1a6657;
        font-weight: bold;
        margin: 0.5rem 0;
        border-left: 3px solid #38b2a0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Success message - light green */
    .stSuccess {
        background-color: #e4f4eb;
        color: #1a6657;
        font-weight: 500;
        border-radius: 0.4rem;
        border: none;
    }
    
    /* Warning message - light amber */
    .stWarning {
        background-color: #f7f4e0;
        color: #66561a;
        font-weight: 500;
        border-radius: 0.4rem;
        border: none;
    }
    
    /* Info message - light blue-green */
    .stInfo {
        background-color: #e0f4f4;
        color: #1a5e66;
        font-weight: 500;
        border-radius: 0.4rem;
        border: none;
    }
    
    /* Error message - light red */
    .stError {
        color: #661a1a;
        font-weight: 500;
        border-radius: 0.4rem;
    }
    
    /* File uploader styling */
    .stFileUploader {
        padding: 1rem;
        background-color: #e4f4eb;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .stFileUploader label {
        color: #1a6657;
        font-weight: bold;
    }
    
    /* Separators */
    hr {
        border-top: 1px solid #c9e5db;
        margin: 2rem 0;
    }
    
    /* Add a subtle raised effect to sections */
    .section-card {
        background-color: white;
        border-radius: 0.8rem;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border-top: 4px solid #2c9c8c;
    }
    
    /* Custom progress bar */
    .stProgress > div > div {
        background-color: #2c9c8c;
    }
    
    /* Make all inputs more visible */
    input, select {
        color: #333333 !important;
        border-radius: 0.3rem !important;
    }
    
    /* Email status */
    .email-sent {
        background-color: #e4f4eb;
        padding: 0.5rem 1rem;
        border-radius: 0.4rem;
        color: #1a6657;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
    }
    
    .email-sent svg {
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---- CONFIGURATION ----

YOUR_EMAIL = 'sahilchandel.anee@gmail.com'
YOUR_PASSWORD = 'pcwxeyrmyrcbfffu'  # App password, keep safe
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # SSL Port

EMAIL_SUBJECT = 'Exploring AI/ML, GenAI Opportunities'

EMAIL_BODY = """
Hi,

I hope this message finds you well.

I am Sahil Chandel, a Machine Learning Engineer 1+ YOE with expertise in Computer Vision, NLP, Generative AI, and AI-driven automation solutions. Currently, I am working at GarudaUAV Soft Solution where I have developed and deployed scalable ML models, automated inspection processes, and built AI solutions that significantly reduced manual efforts and improved efficiency.

My experience includes:
- Developing drone-based automated inspection systems for organizations like NHAI and NTPC.
- Building a Conversational PDF Assistant capable of analyzing large documents efficiently using Retrieval Augmented Generation (RAG).
- Working with advanced frameworks like TensorFlow, PyTorch, HuggingFace, LangChain, and MLOps tools like Docker and BentoML.

I am passionate about leveraging AI and Machine Learning to solve complex, real-world problems and would love to explore potential opportunities within your organization. I have attached my resume for your review and would be thrilled to connect and discuss how I can contribute to your team.

Thank you for your time and consideration.
Looking forward to hearing from you!

Best regards,
Sahil Chandel
📧 sahilchandel.anee@gmail.com | 📞 +91-9717891203
🔗 LinkedIn: https://www.linkedin.com/in/sahil-chandel/
🔗 GitHub: https://github.com/Sahil-Chandel
"""

# ---- STREAMLIT APP ----

st.markdown("<h1 style='text-align: center; color: #1a6657;'>📤 Bulk Resume Sender</h1>", unsafe_allow_html=True)

# Introduction section
st.markdown("""
<div class="section-card">
    <h3 style='color: #1a6657; margin-top: 0;'>Welcome to Your Resume Sending Assistant</h3>
    <p>This tool helps you efficiently send your resume to multiple recruiters or companies at once. 
    Just upload your Excel file with email addresses and your resume PDF to get started.</p>
</div>
""", unsafe_allow_html=True)

# Upload section
st.markdown("""
<div class="section-card">
    <h3 style='color: #1a6657; margin-top: 0;'>Upload Your Files</h3>
    <p>Please upload both files to continue:</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<p style='font-weight: bold; color: #1a6657;'>1. Excel File with Emails</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-size: 0.9rem;'>Must contain an 'Email' column</p>", unsafe_allow_html=True)
    uploaded_excel = st.file_uploader("Upload Excel file", type=["xlsx"], label_visibility="collapsed")
    if uploaded_excel:
        st.markdown(f"<div class='uploadedFile'>✅ Excel file uploaded: {uploaded_excel.name}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<p style='font-weight: bold; color: #1a6657;'>2. Your Resume (PDF)</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-size: 0.9rem;'>Will be attached to all emails</p>", unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed")
    if uploaded_resume:
        st.markdown(f"<div class='uploadedFile'>✅ Resume uploaded: {uploaded_resume.name}</div>", unsafe_allow_html=True)

# Action section
st.markdown("""
<div class="section-card">
    <h3 style='color: #1a6657; margin-top: 0;'>Send Your Resume</h3>
</div>
""", unsafe_allow_html=True)

if uploaded_excel and uploaded_resume:
    st.success("All files are ready! Click the button below to start sending emails.")
    
    send_btn = st.button("🚀 Send Emails")
    if send_btn:
        # Save uploaded files temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_excel:
            tmp_excel.write(uploaded_excel.read())
            excel_path = tmp_excel.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_resume:
            tmp_resume.write(uploaded_resume.read())
            resume_path = tmp_resume.name

        # Read emails
        df = pd.read_excel(excel_path)

        if 'Email' not in df.columns:
            st.error("Error: No 'Email' column found in Excel file!")
        else:
            emails = df['Email'].dropna().unique()
            st.info(f"Found {len(emails)} unique email addresses. Starting to send...")

            # Create a progress bar
            st.markdown("<p style='font-weight: bold; color: #1a6657; margin-top: 1rem;'>Progress:</p>", unsafe_allow_html=True)
            progress_bar = st.progress(0)
            
            status_container = st.container()
            
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                    server.login(YOUR_EMAIL, YOUR_PASSWORD)

                    for i, email in enumerate(emails):
                        msg = EmailMessage()
                        msg['From'] = YOUR_EMAIL
                        msg['To'] = email
                        msg['Subject'] = EMAIL_SUBJECT
                        msg.set_content(EMAIL_BODY)

                        with open(resume_path, 'rb') as f:
                            file_data = f.read()
                            file_name = 'Sahil_CV.pdf'

                        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
                        server.send_message(msg)
                        
                        with status_container:
                            st.markdown(f"""
                            <div class="email-sent">
                                <div>✅ Email sent to <strong>{email}</strong></div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Update progress bar
                        progress_bar.progress((i + 1) / len(emails))

                st.balloons()
                st.success("🎉 All emails sent successfully!")
                
                # Summary section
                st.markdown(f"""
                <div class="section-card">
                    <h3 style='color: #1a6657; margin-top: 0;'>Summary</h3>
                    <p>✅ Total emails sent: <strong>{len(emails)}</strong></p>
                    <p>📤 Sent from: <strong>{YOUR_EMAIL}</strong></p>
                    <p>📎 Resume attached: <strong>{uploaded_resume.name}</strong></p>
                    <p>🎯 Mission accomplished! Your resume has been sent to all recipients.</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred while sending emails: {e}")

else:
    st.warning("Please upload both the Excel file with emails and your Resume PDF to continue.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <p style='color: #1a6657; font-weight: bold; margin-bottom: 0.5rem;'>© 2025 Sahil Chandel | AI/ML Engineer</p>
    <p style='color: #666666; font-size: 0.9rem;'>Streamline your job application process with this tool</p>
</div>
""", unsafe_allow_html=True)