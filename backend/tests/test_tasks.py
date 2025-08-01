import pytest
from flaskr.models.user_model import UserModel
from flaskr.models.task_model import TaskModel
from flaskr.models.tag_model import TagModel
from flaskr.db import db


class TestTasks:
    """Test task endpoints."""
    
    @pytest.fixture
    def test_user(self, app):
        """Create a test user."""
        with app.app_context():
            from flaskr.utils import generate_password
            user = UserModel(
                username='testuser',
                email='test@example.com',
                password=generate_password('testpassword123')
            )
            db.session.add(user)
            db.session.commit()
            # Refresh the user to ensure it's attached to the session
            db.session.refresh(user)
            return user
    
    @pytest.fixture
    def test_tag(self, app):
        """Create a test tag."""
        with app.app_context():
            tag = TagModel(name='Test Tag')
            db.session.add(tag)
            db.session.commit()
            # Refresh the tag to ensure it's attached to the session
            db.session.refresh(tag)
            return tag
    
    @pytest.fixture
    def auth_token(self, client, test_user):
        """Get authentication token for tests."""
        response = client.post('/api/v1/auth/sign-in', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        data = response.get_json()
        return data['token']
    
    def test_create_task_success(self, client, auth_token, test_tag):
        """Test successful task creation."""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/v1/tasks', json={
            'title': 'Test Task',
            'content': 'Test content',
            'status': 'PENDING',
            'tagId': test_tag.id
        }, headers=headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'title' in data
        assert data['title'] == 'Test Task'
    
    def test_create_task_unauthorized(self, client, test_tag):
        """Test task creation without authentication."""
        response = client.post('/api/v1/tasks', json={
            'title': 'Test Task',
            'content': 'Test content',
            'status': 'PENDING',
            'tag_id': test_tag.id
        })
        
        assert response.status_code == 401
    
    def test_create_task_invalid_data(self, client, auth_token):
        """Test task creation with invalid data."""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/v1/tasks', json={
            'title': '',  # Empty title
            'content': 'Test content',
            'status': 'INVALID_STATUS'
        }, headers=headers)
        
        assert response.status_code == 422
    
    def test_get_user_tasks(self, client, auth_token, test_user, test_tag):
        """Test getting user's tasks."""
        # Create a task first
        headers = {'Authorization': f'Bearer {auth_token}'}
        client.post('/api/v1/tasks', json={
            'title': 'Test Task',
            'content': 'Test content',
            'status': 'PENDING',
            'tagId': test_tag.id
        }, headers=headers)
        
        # Get user tasks
        response = client.get('/api/v1/tasks/user', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_user_tasks_unauthorized(self, client):
        """Test getting user tasks without authentication."""
        response = client.get('/api/v1/tasks/user')
        assert response.status_code == 401
    
    def test_update_task_success(self, client, auth_token, test_user, test_tag):
        """Test successful task update."""
        # Create a task first
        headers = {'Authorization': f'Bearer {auth_token}'}
        create_response = client.post('/api/v1/tasks', json={
            'title': 'Original Task',
            'content': 'Original content',
            'status': 'PENDING',
            'tagId': test_tag.id
        }, headers=headers)
        
        task_id = create_response.get_json()['id']
        
        # Update the task
        response = client.put(f'/api/v1/tasks/{task_id}', json={
            'title': 'Updated Task',
            'content': 'Updated content',
            'status': 'COMPLETED',
            'tagId': test_tag.id
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Task'
        assert 'COMPLETED' in data['status']
    
    def test_delete_task_success(self, client, auth_token, test_user, test_tag):
        """Test successful task deletion."""
        # Create a task first
        headers = {'Authorization': f'Bearer {auth_token}'}
        create_response = client.post('/api/v1/tasks', json={
            'title': 'Task to Delete',
            'content': 'Content to delete',
            'status': 'PENDING',
            'tagId': test_tag.id
        }, headers=headers)
        
        task_id = create_response.get_json()['id']
        
        # Delete the task
        response = client.delete(f'/api/v1/tasks/{task_id}', headers=headers)
        
        assert response.status_code == 204
    
    def test_delete_task_not_found(self, client, auth_token):
        """Test deleting non-existent task."""
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.delete('/api/v1/tasks/999', headers=headers)
        
        assert response.status_code == 404 