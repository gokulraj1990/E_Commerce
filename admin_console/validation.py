#validation.py

import re
# from rest_framework.response import Response
# from rest_framework import status

class cust_validation():

    def __init__(self,data):
         self.mobile=data["mobile_number"]
         self.first_name=data["first_name"]
         self.last_name=data["last_name"]
         self.password=data["password"]
                
         self.validate_mobile(self.mobile)
         self.validate_name(self.first_name)
         self.validate_name(self.last_name)
         self.validate_password(self.password)

    def validate_mobile(self,value):
        pattern = re.compile(r"\d{10}$")
        if not pattern.match(value):
            raise CustomValidationError('Invalid Mobile Number, must be 10 digits.')
        return value

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

                         
                         