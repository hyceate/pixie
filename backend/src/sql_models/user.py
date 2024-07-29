from tortoise import fields, models
from .post import Post
from .comment import Comment
import bcrypt

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=80, unique=True)
    password_hash = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    posts = fields.ReverseRelation['Post']
    comments = fields.ReverseRelation['Comment']

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    