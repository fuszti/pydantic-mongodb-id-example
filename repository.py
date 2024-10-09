from pymongo import MongoClient
from bson import ObjectId
from models import User, Post

class MongoRepository:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client.blog_database

    def create_user(self, user: User) -> User:
        user_dict = User.to_db(user)
        result = self.db.users.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    def get_user(self, user_id: str) -> User:
        user_dict = self.db.users.find_one({"_id": ObjectId(user_id)})
        if user_dict:
            return User(**User.from_db(user_dict))
        return None

    def create_post(self, post: Post) -> Post:
        post_dict = Post.to_db(post)
        result = self.db.posts.insert_one(post_dict)
        post.id = str(result.inserted_id)
        return post

    def get_post(self, post_id: str) -> Post:
        post_dict = self.db.posts.find_one({"_id": ObjectId(post_id)})
        if post_dict:
            return Post(**Post.from_db(post_dict))
        return None
