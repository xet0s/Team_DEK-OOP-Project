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

    @property
    def status_text(self):
        """
        Playlist'in anlık durum metnini (Public/Private) döndüren property.
        """
        # Circular import önlemek için burada import ediyoruz
        from models.interaction_module.playlist_type import PlaylistLogicBase
        logic = PlaylistLogicBase.get_playlist_logic(self)
        return logic.get_status_text()
        