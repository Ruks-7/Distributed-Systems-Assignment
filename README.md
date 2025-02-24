# Flask Contact Management Application

A web application built with Flask and MongoDB for managing contacts with user authentication.

## Features

- User Authentication (Register/Login)
- Password Reset via Email
- Contact Management
- Contact Search by Registration Number

## Prerequisites

- Python 3.7+
- MongoDB
- Gmail Account (for password reset emails)

## Project Structure

```plaintext
contact-system/
├── run.py
├── requirements.txt
├── config.py
├── .env
├── README.md
├── .venv/
└── app/
   ├── __init__.py
   ├── routes/
   │   ├── __init__.py
   │   └── auth.py
   ├── templates/
   │   ├── base.html
   │   └── auth/
   │       ├── login.html
   │       ├── register.html
   │       ├── forgot_password.html
   │       ├── reset_password.html
   │       ├── contact_form.html
   │       └── search.html
   └── static/
      └── css/
            └── style.css
```

## Quick Start Guide

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd contact-system
   python -m venv .venv
   .venv\Scripts\activate
   pip install flask flask-pymongo flask-mail python-dotenv
   ```

2. **Configure Environment**
   Create `.env` file:
   ```plaintext
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   MONGO_URI=mongodb://localhost:27017/contact_system
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-specific-password
   ```

3. **Start Services**
   ```bash
   net start MongoDB
   python -m flask run
   ```

## Detailed Setup

### Gmail Configuration
1. Enable 2FA on Google Account
2. Generate App Password:
   - Google Account → Security → App Passwords
   - Select "Mail" and "Other"
   - Copy password to .env file

### MongoDB Setup
1. Install MongoDB
2. Start service:
   ```bash
   net start MongoDB
   ```
3. Verify connection:
   ```bash
   mongodb://localhost:27017
   ```

### Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage Guide

### 1. Registration/Login
- Visit `http://127.0.0.1:5000`
- Register new account or login
- Reset password via email if forgotten

### 2. Contact Management
Add contacts with:
- Mobile number
- Email
- Address
- Registration number

### 3. Search Functionality
- Search contacts by registration number
- View complete contact details

## Troubleshooting

### Common Issues

1. **Email Errors**
   - Verify Gmail credentials
   - Check App Password configuration
   - Confirm SMTP settings

2. **MongoDB Connection**
   - Verify MongoDB is running
   - Check connection string
   - Confirm port availability

3. **Module Import Errors**
   - Activate virtual environment
   - Reinstall requirements
   - Check Python path

## Development

### VS Code Setup
1. Select Python Interpreter:
   - Ctrl+Shift+P
   - "Python: Select Interpreter"
   - Choose .venv environment

2. Required Extensions:
   - Python
   - MongoDB for VS Code

## Support

For issues and questions, please create an issue in the repository.

## License

This project is provided for educational purposes.
