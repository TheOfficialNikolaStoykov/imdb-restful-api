from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):
    
    def test_register(self):
        """Test successful user registration."""
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "password",
            "confirm_password": "password"
        }
        
        response = self.client.post(reverse('register'), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testcase").exists())
        self.assertEqual(User.objects.get(username="testcase").email, "testcase@example.com")
    
    def test_register_password_mismatch(self):
        """Test registration fails due to mismatched passwords."""
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "password123",
            "confirm_password": "password456"
        }
        
        response = self.client.post(reverse('register'), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Password and Confirm Password fields must be the same!")
        
    def test_register_email_exists(self):
        """Test registration fails when email already exists."""

        User.objects.create_user(username="existinguser", email="testcase@example.com", password="password")

        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "password",
            "confirm_password": "password"
        }
        
        response = self.client.post(reverse('register'), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Email already exists!")
    
    def test_register_invalid_email(self):
        """Test registration fails due to invalid email format."""
        data = {
            "username": "testcase",
            "email": "invalid-email",
            "password": "password",
            "confirm_password": "password"
        }
        
        response = self.client.post(reverse('register'), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="password")
        
    def test_login(self):
        """Test successful login."""
        data = {
            "username": "testcase",
            "password": "password"
        }
        
        response = self.client.post(reverse('login'), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_logout(self):
        """Test successful logout."""
        self.token = Token.objects.get(user__username="testcase")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.post(reverse('logout'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserTokenSignalTestCase(APITestCase):

    def test_token_created_on_user_creation(self):
        """Test that a token is created for a newly registered user."""
        user = User.objects.create_user(username="testuser", password="password")
        token = Token.objects.filter(user=user).first()
        self.assertIsNotNone(token)

    def test_token_not_created_for_existing_user(self):
        """Test that no duplicate token is created for an existing user."""
        user = User.objects.create_user(username="testuser", password="password")
        initial_token = Token.objects.get(user=user)
        
        user.username = "testuserupdated"
        user.save()
        
        token_count = Token.objects.filter(user=user).count()
        
        self.assertEqual(token_count, 1)

        updated_token = Token.objects.get(user=user)
        
        self.assertEqual(initial_token.key, updated_token.key)

