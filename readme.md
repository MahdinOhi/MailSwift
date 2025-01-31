# MailBlaster: Advanced Bulk Email Sender Application

## 🚀 Project Overview

MailBlaster is a sophisticated Flask-based web application designed to simplify and streamline the process of sending personalized bulk emails. By leveraging the power of CSV data, dynamic email templating, and secure file management, this tool empowers users to efficiently communicate with large groups while maintaining a personal touch.

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Advanced Templating](#advanced-templating)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Features

### 1. Secure Authentication

- Gmail-based login with App Password support
- Session management using Flask-Session
- Secure credential handling

### 2. Dynamic Email Templating

- Variable substitution from CSV data
- HTML email support
- Flexible template design

### 3. Bulk Email Processing

- CSV-driven recipient management
- Personalized email generation
- Batch email sending

### 4. Attachment Handling

- Multiple file attachment support
- Secure file upload mechanisms
- File type flexibility

## 🏗️ System Architecture

### Components

1. **Frontend**

   - Login Page (`login.html`)
   - Main Interface (`main.html`)
   - Responsive Design
   - Modern UI/UX with gradient backgrounds

2. **Backend**

   - Flask Web Framework
   - SMTP Email Sending
   - File Management
   - Session Handling

3. **Data Flow**

```
User Login → Upload CSV/Template → Process Recipients → Send Emails
   ↑               ↓                    ↓                ↓
Credentials    File Parsing        Email Generation   SMTP Transmission
```

## 🔧 Prerequisites

### Software Requirements

- Python 3.8+
- pip (Python Package Manager)
- Virtual Environment (recommended)

### Gmail Account Configuration

- Google Account
- 2-Step Verification Enabled
- App Password Generated

## 💻 Installation

### 1. Repository Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mailblaster.git
cd mailblaster

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Unix/macOS
# venv\Scripts\activate   # Windows
```

### 2. Dependency Installation

```bash
# Install required packages
pip install -r requirements.txt
```

## 🔐 Configuration

### Gmail App Password Generation

1. Visit [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Navigate to App Passwords
4. Generate a new App Password for "Flask Application"

### Environment Variables (Optional)

Create a `.env` file for sensitive configurations:

```
FLASK_SECRET_KEY=your_secure_random_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
```

## 🚀 Usage Guide

### 1. Launch Application

```bash
flask run
```

Access via `http://localhost:5000`

### 2. Login Process

- Enter Gmail Address
- Use Generated App Password
- Securely managed session

### 3. Email Composition Workflow

1. Enter Email Subject
2. Design Email Template
3. Upload Recipient CSV
4. Add Optional Attachments
5. Click "Send Emails"

## 📧 Advanced Templating

### Variable Placeholders

Use `{{column_name}}` to dynamically insert data:

```html
Hello {{name}}! Your unique ID is {{id}}. We're excited to connect with you.
```

### CSV Structure Example

```csv
email,id,name,department
john@example.com,001,John Doe,Marketing
jane@example.com,002,Jane Smith,Sales
```

## 🛡️ Security Considerations

### Authentication

- Never use primary Gmail password
- Always use App Passwords
- Implement strong, unique passwords

### File Handling

- Sanitize filenames
- Limit file sizes
- Validate file types
- Use secure_filename() for uploads

### Data Protection

- Temporary file storage
- Session-based access control
- No persistent storage of credentials

## 🔍 Troubleshooting

### Common Issues

1. **SMTP Authentication Errors**

   - Verify App Password
   - Check internet connectivity
   - Ensure 2-Step Verification is active

2. **CSV Parsing Problems**

   - Validate CSV structure
   - Use consistent column names
   - Check for extra spaces or formatting issues

3. **Email Sending Limitations**
   - Gmail daily sending limits
   - Large attachment restrictions

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

### Suggested Improvements

- OAuth2 Authentication
- Logging and Error Tracking
- Email Delivery Status Tracking

## 📄 License

MIT License

## 🌐 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python SMTP Guide](https://docs.python.org/3/library/smtplib.html)
- [Google App Passwords](https://support.google.com/accounts/answer/185833)

---

**Disclaimer**: This application is for educational and personal use. Always comply with email service provider policies and anti-spam regulations.
