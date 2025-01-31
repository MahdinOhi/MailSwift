from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import csv
import os
import smtplib
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
        # Handle file uploads
        csv_file = request.files['csv_file']
        template = request.form['template']
        subject = request.form['subject']
        attachments = request.files.getlist('attachments')
        
        # Save files
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(csv_file.filename))
        csv_file.save(csv_path)
        
        # Process CSV and send emails
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg = MIMEMultipart()
                msg['From'] = session['sender_email']
                msg['Subject'] = subject
                
                # Replace template variables
                body = template
                for key, value in row.items():
                    body = body.replace(f'{{{{{key}}}}}', value)
                msg.attach(MIMEText(body, 'html'))
                
                # Add attachments
                for attachment in attachments:
                    if attachment.filename:
                        attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(attachment.filename))
                        attachment.save(attachment_path)
                        with open(attachment_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=secure_filename(attachment.filename))
                        part['Content-Disposition'] = f'attachment; filename="{secure_filename(attachment.filename)}"'
                        msg.attach(part)
                
                # Send email
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                        server.login(session['sender_email'], session['sender_password'])
                        server.sendmail(session['sender_email'], row['email'], msg.as_string())
                except Exception as e:
                    return f"Error sending email: {str(e)}"
        
        return "Emails sent successfully!"
    
    return render_template('main.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)