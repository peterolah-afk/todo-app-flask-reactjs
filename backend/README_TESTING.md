# Backend Testing Guide

This document provides comprehensive testing solutions for the Flask backend of the todo app.

## Testing Stack

- **pytest**: Main testing framework
- **pytest-flask**: Flask-specific testing utilities
- **pytest-cov**: Coverage reporting
- **factory-boy**: Test data generation

## Setup

1. Install testing dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run tests:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=flaskr --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run tests with verbose output
pytest -v

# Run tests and watch for changes
pytest --watch
```

## Test Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── test_auth.py         # Authentication tests
│   ├── test_tasks.py        # Task CRUD tests
│   └── test_tags.py         # Tag CRUD tests
├── pytest.ini              # Pytest configuration
└── requirements.txt         # Includes testing dependencies
```

## Test Categories

### 1. Authentication Tests (`test_auth.py`)
- User registration (success/failure cases)
- User sign-in (success/failure cases)
- Input validation
- Duplicate email handling

### 2. Task Tests (`test_tasks.py`)
- Task creation, reading, updating, deletion
- Authentication requirements
- Data validation
- Error handling

### 3. Tag Tests (`test_tags.py`)
- Tag CRUD operations
- Validation and error handling

## Key Features

### Test Database
- Uses in-memory SQLite database for tests
- Each test gets a clean database state
- No interference between tests

### Authentication Testing
- JWT token generation and validation
- Protected endpoint testing
- Token expiration handling

### Coverage Reporting
- HTML coverage reports in `htmlcov/` directory
- Terminal coverage output
- Identifies untested code paths

## Best Practices

1. **Test Isolation**: Each test is independent and doesn't affect others
2. **Fixtures**: Reusable test data and setup
3. **Mocking**: External dependencies are mocked when needed
4. **Assertions**: Clear, descriptive assertions
5. **Error Cases**: Both success and failure scenarios are tested

## Running Tests in CI/CD

```yaml
# Example GitHub Actions workflow
- name: Run Backend Tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest --cov=flaskr --cov-report=xml
```

## Coverage Goals

- Aim for >80% code coverage
- Focus on critical business logic
- Test all API endpoints
- Include error handling paths

## Debugging Tests

```bash
# Run single test with debugger
pytest tests/test_auth.py::TestAuth::test_user_registration_success -s

# Run with print statements
pytest -s

# Run with detailed output
pytest -vv
``` 