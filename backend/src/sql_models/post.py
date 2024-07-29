from tortoise import fields, models
from .comment import Comment
from .images import Images

class Post(models.Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=255)
    images = fields.ReverseRelation['Images']
    author = fields.ForeignKeyField('models.User', related_name='posts')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    comments = fields.ReverseRelation['Comment']
