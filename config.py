import os

class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = os.path.join('uploads', 'resumes')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Patna@1234'
    MYSQL_DB = 'job_portal'