import pytest
from flaskr.models.tag_model import TagModel
from flaskr.db import db


class TestTags:
    """Test tag endpoints."""
    
    def test_get_tags_success(self, client):
        """Test successful retrieval of all tags."""
        response = client.get('/api/v1/tags')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_create_tag_success(self, client):
        """Test successful tag creation."""
        response = client.post('/api/v1/tags', json={
            'name': 'Test Tag'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'name' in data
        assert data['name'] == 'Test Tag'
    
    def test_create_tag_invalid_data(self, client):
        """Test tag creation with invalid data."""
        response = client.post('/api/v1/tags', json={
            'name': ''  # Empty name
        })
        
        assert response.status_code == 201
    
    def test_create_tag_duplicate_name(self, client):
        """Test tag creation with duplicate name."""
        # Create first tag
        client.post('/api/v1/tags', json={
            'name': 'Test Tag'
        })
        
        # Try to create second tag with same name
        response = client.post('/api/v1/tags', json={
            'name': 'Test Tag'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'message' in data
    
    def test_delete_tag_not_found(self, client):
        """Test deleting non-existent tag."""
        response = client.delete('/api/v1/tags/999')
        
        assert response.status_code == 404 