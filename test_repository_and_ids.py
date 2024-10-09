import pytest
from mongomock import MongoClient
from bson import ObjectId
from models import User, Post
from repository import MongoRepository

@pytest.fixture
def mock_mongo_repo():
    client = MongoClient()
    return MongoRepository(client)

def test_create_user(mock_mongo_repo):
    new_user = User(username="testuser", email="test@example.com")
    created_user = mock_mongo_repo.create_user(new_user)
    
    assert created_user.id is not None
    assert len(created_user.id) == 24
    assert created_user.username == "testuser"
    assert created_user.email == "test@example.com"

def test_get_user(mock_mongo_repo):
    new_user = User(username="testuser", email="test@example.com")
    created_user = mock_mongo_repo.create_user(new_user)
    
    retrieved_user = mock_mongo_repo.get_user(created_user.id)
    
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == created_user.username
    assert retrieved_user.email == created_user.email

def test_create_post(mock_mongo_repo):
    new_user = User(username="testuser", email="test@example.com")
    created_user = mock_mongo_repo.create_user(new_user)
    
    new_post = Post(title="Test Post", content="This is a test post", author_id=created_user.id)
    created_post = mock_mongo_repo.create_post(new_post)
    
    assert created_post.id is not None
    assert len(created_post.id) == 24
    assert created_post.title == "Test Post"
    assert created_post.content == "This is a test post"
    assert created_post.author_id == created_user.id

def test_get_post(mock_mongo_repo):
    new_user = User(username="testuser", email="test@example.com")
    created_user = mock_mongo_repo.create_user(new_user)
    
    new_post = Post(title="Test Post", content="This is a test post", author_id=created_user.id)
    created_post = mock_mongo_repo.create_post(new_post)
    
    retrieved_post = mock_mongo_repo.get_post(created_post.id)
    
    assert retrieved_post is not None
    assert retrieved_post.id == created_post.id
    assert retrieved_post.title == created_post.title
    assert retrieved_post.content == created_post.content
    assert retrieved_post.author_id == created_post.author_id

def test_id_consistency():
    user = User(id="507f1f77bcf86cd799439011", username="testuser", email="test@example.com")
    assert isinstance(user.id, str)
    assert len(user.id) == 24
    
    db_dict = User.to_db(user, include_id=True)
    assert isinstance(db_dict["_id"], ObjectId)
    
    user_from_db = User(**User.from_db(db_dict))
    assert isinstance(user_from_db.id, str)
    assert user_from_db.id == user.id

def test_required_id():
    post = Post(title="Test", content="Content", author_id="507f1f77bcf86cd799439011")
    assert isinstance(post.author_id, str)
    assert len(post.author_id) == 24
    
    db_dict = Post.to_db(post)
    assert isinstance(db_dict["author_id"], ObjectId)

def test_optional_id():
    user = User(username="testuser", email="test@example.com")
    assert user.id is None
    
    db_dict = User.to_db(user)
    assert "_id" not in db_dict

    user_with_id = User(id="507f1f77bcf86cd799439011", username="testuser", email="test@example.com")
    assert user_with_id.id is not None
    assert len(user_with_id.id) == 24
