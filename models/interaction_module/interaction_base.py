from peewee import CharField, ForeignKeyField, TextField
from models.base_model import BaseModel  #zamanı çekiyor
from models.accounts_module.user import User #kullanıcıyı çekecek
from models.content_module.video_base import VideoModel #videoyu çekecek

class InteractionModel(BaseModel):
    User=ForeignKeyField(User, backref='interactions', null=False)
    VideoModel=ForeignKeyField(VideoModel, backref='interactions', null=False)
    interaction_type = CharField(null=False)  #yorum mu beğeni mi 
    content = TextField(null=True) #yorum metni. Like ise boş dolu
    status = CharField(default='active') #duruma bakıcaz aktif ya da silindi
    
class Meta:
    table_name="interactions" #veri tabanına çekicek
    