from models.base_model import BaseModel 
from peewee import CharField,ForeignKeyField,BooleanField
from models.accounts_module.user import User

class PlaylistModel(BaseModel):
    #Playlisti oluşturan kullanıcı
    user=ForeignKeyField(User, backref='playlist') 
    #Görünürlük durumunu belirleyen Boolean tablosu
    is_public=BooleanField(default=True)
    #Playlist Bağlığı
    title=CharField(null=False)

    class Meta:
        #database e kaydedilecek tablo ismi
        table_name="playlist"
        