pip install streamlit pandas openpyxl


🧠 How this works:
Upload Excel ➔ reads all emails from Email column
Upload Resume ➔ attaches your PDF
Click Send ➔ sends email + attachment to everyone
Shows success/failure live on screen


🔥 Important Notes:
Gmail: If you use Gmail, you need to create an App Password (not your normal password) because Google blocks less secure apps.
Excel Format: Make sure your Excel file has a column named Email exactly, or change the EMAIL_COLUMN in the script.
Attachment: The resume should be a PDF, but you can change it to any    file.
Mass Sending: Be cautious; sending too many emails at once can get you flagged for spam. Add delays if necessary (time.sleep(1) between emails).