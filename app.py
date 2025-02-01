from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import csv
import os
import smtplib
import markdown
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def detect_template_type(template):
    """
    Automatically detect the template type based on its content.
    
    Detection criteria:
    1. If template contains HTML-specific tags, it's HTML
    2. If template contains Markdown-specific syntax, it's Markdown
    3. Default to Markdown if no clear indicators are found
    
    Args:
        template (str): The input template string
    
    Returns:
        str: 'html' or 'markdown'
    """
    # Check for HTML-specific tags
    html_indicators = [
        r'<[a-z0-9]+[^>]*>',  # Opening HTML tag
        r'<!DOCTYPE\s+html',  # DOCTYPE declaration
        r'<html',             # HTML root tag
        r'<head>',            # Head tag
        r'<body>',            # Body tag
        r'&[a-z]+;',          # HTML entities
    ]
    
    # Check for Markdown-specific syntax
    markdown_indicators = [
        r'^#+\s',             # Headers (# Header 1, ## Header 2)
        r'\*\*[^*]+\*\*',     # Bold text
        r'\*[^*]+\*',         # Italic text
        r'\[.*\]\(.*\)',      # Links
        r'>\s',               # Blockquotes
        r'^\-\s',             # Unordered list
        r'^\d+\.\s',          # Ordered list
    ]
    
    # Check for HTML
    for pattern in html_indicators:
        if re.search(pattern, template, re.IGNORECASE | re.MULTILINE):
            return 'html'
    
    # Check for Markdown
    for pattern in markdown_indicators:
        if re.search(pattern, template, re.MULTILINE):
            return 'markdown'
    
    # Default to Markdown
    return 'markdown'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['sender_email'] = request.form['email']
        session['sender_password'] = request.form['password']
        return redirect(url_for('main'))
    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'sender_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        csv_file = request.files['csv_file']
        template = request.form['template']
        
        # Automatically detect template type
        template_type = detect_template_type(template)
        
        subject = request.form['subject']
        attachments = request.files.getlist('attachments')
        
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(csv_file.filename))
        csv_file.save(csv_path)
        
        success_list = []
        error_list = []
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg = MIMEMultipart()
                msg['From'] = session['sender_email']
                msg['Subject'] = subject
                
                # Process template based on detected type
                if template_type == 'markdown':
                    body = markdown.markdown(template)
                elif template_type == 'html':
                    body = template
                
                # Replace placeholders in the template
                for key, value in row.items():
                    body = body.replace(f'{{{{{key}}}}}', str(value))
                
                msg.attach(MIMEText(body, 'html'))
                
                for attachment in attachments:
                    if attachment.filename:
                        attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(attachment.filename))
                        attachment.save(attachment_path)
                        with open(attachment_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=secure_filename(attachment.filename))
                        part['Content-Disposition'] = f'attachment; filename="{secure_filename(attachment.filename)}"'
                        msg.attach(part)
                
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                        server.login(session['sender_email'], session['sender_password'])
                        server.sendmail(session['sender_email'], row['email'], msg.as_string())
                    success_list.append(row['email'])
                except Exception as e:
                    error_list.append((row['email'], str(e)))
        
        return render_template('success.html', success_list=success_list, error_list=error_list)
    
    return render_template('main.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)