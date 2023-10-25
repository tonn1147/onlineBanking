from django.core.exceptions import ValidationError
import re

def validate_email(email):
    email_pattern = r'^[A-Za-z0-9._-+%]\
        +@[A-Za-z0-9.+]+\.[A-Za-z]{2,}$'
    if not re.match(email_pattern,email): return ValidationError("Invalid email")