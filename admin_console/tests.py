from django.test import TestCase
from .models import Admin, User  # Importing the correct models
from django.db.utils import IntegrityError

class UserModelTests(TestCase):
    def setUp(self):
        # Sample data for user and admin
        self.user_data = {
            'email': 'johndoe@example.com',
            'password': 'Password@123',
            'firstname': 'John',
            'lastname': 'Doe',
        }
        self.admin_data = {
            'email': 'adminuser@example.com',
            'password': 'Adminpassword@123',
            'firstname': 'Admin',
            'lastname': 'User',
        }

    def test_create_user(self):
        """Test creating a new user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'johndoe@example.com')
        self.assertTrue(user.check_password('Password@123'))  # Test if password is hashed

    def test_create_user_without_email(self):
        """Test creating a user without an email should raise an error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='Password@123')

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(**self.admin_data)
        self.assertEqual(user.email, 'adminuser@example.com')
        self.assertTrue(user.check_password('Adminpassword@123'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_with_invalid_email(self):
        """Test creating a user with invalid email should raise an error"""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='invalid-email', password='password123')

    def test_user_login(self):
        """Test logging in a user with correct credentials"""
        user = User.objects.create_user(**self.user_data)
        # Simulate user login
        user_logged_in = User.objects.get(email='johndoe@example.com')
        self.assertTrue(user_logged_in.check_password('Password@123'))

    def test_user_login_wrong_password(self):
        """Test logging in a user with wrong password"""
        user = User.objects.create_user(**self.user_data)
        # Attempt to log in with incorrect password
        user_logged_in = User.objects.get(email='johndoe@example.com')
        self.assertFalse(user_logged_in.check_password('wrongpassword'))

    def test_reset_password(self):
        """Test resetting user password"""
        user = User.objects.create_user(**self.user_data)
        # Reset password (this would typically involve calling a password reset view, but we're simplifying it here)
        user.set_password('Newpassword@123')
        user.save()

        # Verify the new password works
        self.assertTrue(user.check_password('Newpassword@123'))

    def test_admin_login(self):
        """Test logging in an admin with correct credentials"""
        admin = Admin.objects.create(**self.admin_data)  # Assuming Admin model is used directly
        # Simulate admin login
        admin_logged_in = Admin.objects.get(email='adminuser@example.com')
        self.assertTrue(admin_logged_in.check_password('Adminpassword@123'))

    def test_admin_login_wrong_password(self):
        """Test logging in an admin with incorrect password"""
        admin = Admin.objects.create(**self.admin_data)
        # Attempt to log in with incorrect password
        admin_logged_in = Admin.objects.get(email='adminuser@example.com')
        self.assertFalse(admin_logged_in.check_password('wrongpassword'))

    def test_user_creation_with_duplicate_email(self):
        """Test creating a user with duplicate email should raise an error"""
        User.objects.create_user(email='johndoe@example.com', password='password123')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='johndoe@example.com', password='anotherpassword')

    def test_admin_creation_with_duplicate_email(self):
        """Test creating an admin with duplicate email should raise an error"""
        Admin.objects.create(**self.admin_data)
        with self.assertRaises(IntegrityError):
            Admin.objects.create(**self.admin_data)  # Duplicate admin email

# Add additional test cases as necessary
