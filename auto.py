import streamlit as st
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
import tempfile

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

st.title("📤 Bulk Resume Sender")
st.write("Upload an Excel file with emails and send your resume easily!")

uploaded_excel = st.file_uploader("Upload Excel file with emails (must have 'Email' column)", type=["xlsx"])
uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_excel and uploaded_resume:
    st.success("Files uploaded successfully! Ready to send emails.")
    
    if st.button("🚀 Send Emails"):
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
            st.info(f"Found {len(emails)} emails. Sending...")

            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                    server.login(YOUR_EMAIL, YOUR_PASSWORD)

                    for email in emails:
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
                        st.success(f"✅ Email sent to {email}")

                st.balloons()
                st.success("🎉 All emails sent successfully!")
            except Exception as e:
                st.error(f"An error occurred while sending emails: {e}")

else:
    st.warning("Please upload both Excel and Resume files.")
