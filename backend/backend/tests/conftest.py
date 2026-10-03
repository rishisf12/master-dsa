import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import get_session
from app.core.config import settings


# Create test database engine
test_engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False}
)


def get_test_session():
    """Get test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def session():
    """Create a test database session."""
    # Create tables
    SQLModel.metadata.create_all(test_engine)
    
    # Override dependency
    app.dependency_overrides[get_session] = get_test_session
    
    with Session(test_engine) as session:
        yield session
    
    # Clean up after test
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_solution_data():
    """Sample solution data for testing."""
    return {
        "problem_number": 1,
        "problem_name": "Two Sum",
        "problem_url": "https://leetcode.com/problems/two-sum/",
        "difficulty": "easy",
        "pattern": "array",
        "python_code": "class Solution:\n    def twoSum(self, nums, target):\n        return [0, 1]",
        "cpp_code": "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        return {0, 1};\n    }\n};",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "notes": "Use hashmap for O(1) lookup",
        "day_id": 1
    }