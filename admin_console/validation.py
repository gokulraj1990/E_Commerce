#validation.py

import re
# from rest_framework.response import Response
# from rest_framework import status

class cust_validation():

    def __init__(self,data):
         self.firstname=data["firstname"]
         self.password=data["password"]       
         self.validate_name(self.firstname)
         self.validate_password(self.password)

    def validate_name(self,value):
        pattern = re.compile(r'^[A-Za-z\s]+$')
        if not pattern.fullmatch(value):
                raise CustomValidationError("Invalid name: must only contain alphabetic characters.")
        return value
    
    def validate_password(self,value):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not pattern.fullmatch(value):
                raise CustomValidationError("""Password must be at least 8 characters long and include uppercase letters, lowercase letters, numbers, and special characters.""")
        return value

class CustomValidationError(Exception):   
    def __init__(self,value):
        self.value=value
    
    def __str__(self):
        return self.value
        # return Response({"Success": False, "Message":self.value}, status=status.HTTP_400_BAD_REQUEST)


def validate_password(password):
    # Define the password criteria
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # Check for at least one uppercase letter
        return False
    if not re.search(r"[a-z]", password):  # Check for at least one lowercase letter
        return False
    if not re.search(r"[0-9]", password):  # Check for at least one digit
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Check for special characters
        return False
    return True
                    