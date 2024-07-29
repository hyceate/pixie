from tortoise import fields, models

class Images(models.Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    post = fields.ForeignKeyField('models.Post', related_name='images') 

    class Meta:
        table = "images"
