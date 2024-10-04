#validation.py
import re

class CustomValidationError(Exception):   
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value


class CustValidation:

    def __init__(self, data):
        self.firstname = data.get("firstname")
        self.lastname = data.get("lastname")
        self.mobilenumber = data.get("mobilenumber")
        self.password = data.get("password")
        if self.firstname is not None:
            self.validate_name(self.firstname)
        if self.lastname is not None:
            self.validate_name(self.lastname)
        if self.mobilenumber is not None:
            self.validate_mobilenumber(self.mobilenumber)
        if self.password is not None:
            self.validate_password(self.password)       

    def validate_name(self, value):
        pattern = re.compile(r'^[A-Za-z\s]+$')
        if not pattern.fullmatch(value):
            raise CustomValidationError("Invalid name: must only contain alphabetic characters.")
        return value
    
    def validate_password(self, value):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not pattern.fullmatch(value):
            raise CustomValidationError("Password must be at least 8 characters long and include uppercase letters, lowercase letters, numbers, and special characters.")
        return value

    def validate_mobilenumber(self, value):
        pattern = re.compile(r'^\d{10}$')
        if not pattern.fullmatch(value):
            raise CustomValidationError("Invalid mobile number: must be exactly 10 digits.")
        return value
