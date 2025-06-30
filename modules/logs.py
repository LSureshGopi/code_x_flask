from flask import session
from datetime import datetime

def log_user_activity(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"{message} - [{timestamp}]"
    if 'user_logs' not in session:
        session['user_logs'] = []
    session['user_logs'].append(entry)