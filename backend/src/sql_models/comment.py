from tortoise import fields, models

class Comment(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.ForeignKeyField('models.User', related_name='comments')
    post = fields.ForeignKeyField('models.Post', related_name='comments')
    parent = fields.ForeignKeyField('models.Comment', related_name='replies', null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)