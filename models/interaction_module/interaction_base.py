from peewee import CharField, ForeignKeyField, TextField
from models.base_model import BaseModel                 #zamanı çekiyor
from models.accounts_module.user_base import UserModel            #kullanıcıyı çekecek
from models.content_module.video_base import VideoModel #videoyu çekecek
from abc import ABC, abstractmethod


class InteractionModel(BaseModel):
    user=ForeignKeyField(UserModel, backref='interactions', null=False)
    videoModel=ForeignKeyField(VideoModel, backref='interactions', null=False)
    interaction_type = CharField(null=False)  #yorum mu beğeni mi 
    content = TextField(null=True)            #yorum metni. Like ise boş dolu
    status = CharField(default='active')      #duruma bakıcaz aktif ya da silindi
    
class Meta:
    #Veri tabanında interactions adında tablo açacak
    table_name="interactions" 
    