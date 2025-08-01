import pytest
from flaskr.models.user_model import UserModel
from flaskr.db import db


class TestAuth:
    """Test authentication endpoints."""
    
    def test_user_registration_success(self, client):
        """Test successful user registration."""
        response = client.post('/api/v1/users', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        assert response.status_code == 201
    
    def test_user_registration_duplicate_email(self, client):
        """Test user registration with duplicate email."""
        # Create first user
        client.post('/api/v1/users', json={
            'username': 'testuser1',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        # Try to create second user with same email
        response = client.post('/api/v1/users', json={
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'message' in data
    
    def test_user_registration_invalid_data(self, client):
        """Test user registration with invalid data."""
        response = client.post('/api/v1/users', json={
            'username': 'test',
            'email': 'invalid-email',
            'password': '123'
        })
        
        assert response.status_code == 422
    
    def test_sign_in_success(self, client):
        """Test successful sign in."""
        # Create user first
        client.post('/api/v1/users', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        # Sign in
        response = client.post('/api/v1/auth/sign-in', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
    
    def test_sign_in_invalid_credentials(self, client):
        """Test sign in with invalid credentials."""
        response = client.post('/api/v1/auth/sign-in', json={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'message' in data
    
    def test_sign_in_missing_fields(self, client):
        """Test sign in with missing fields."""
        response = client.post('/api/v1/auth/sign-in', json={
            'email': 'test@example.com'
            # Missing password
        })
        
        assert response.status_code == 422 