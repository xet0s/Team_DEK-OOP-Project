from peewee import CharField, ForeignKeyField, TextField
from models.base_model import BaseModel                 #zamanı çekiyor
from models.accounts_module.user import User            #kullanıcıyı çekecek
from models.content_module.video_base import VideoModel #videoyu çekecek
from abc import ABC, abstractmethod


class InteractionModel(BaseModel):
    user=ForeignKeyField(User, backref='interactions',on_delete="CASCADE", null=False)
    video=ForeignKeyField(VideoModel, backref='interactions',on_delete="CASCADE", null=False)
    
    TYPE_LIKE = 'like'
    TYPE_DISLIKE = 'dislike'
    TYPE_COMMENT = 'comment'
    TYPE_SUBSCRIPTION = 'subscription'
    TYPE_SAVE = 'save'
    TYPE_SHARE = 'share'

    interaction_type = CharField(null=False)    #yorum mu beğeni mi 
    content = TextField(null=True)              #yorum metni. Like ise boş dolu
    status = CharField(default='deactive')      #duruma bakıcaz aktif ya da silindi
        
    class Meta:
        #Veri tabanında interactions adında tablo açacak
        table_name="interactions" 

    @property
    def status_text(self):
        """
        Etkileşimin anlık durum mesajını döndürür.
        """
        from models.interaction_module.interaction_type import get_interaction_logic
        logic = get_interaction_logic(self)
        return logic.interaction_status() 
    