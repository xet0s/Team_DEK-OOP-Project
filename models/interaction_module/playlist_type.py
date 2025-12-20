from peewee import ForeignKeyField
from models.base_model import BaseModel
from models.interaction_module.playlist_base import PlaylistModel
from models.content_module.video_base import VideoModel

class PlaylistLogicBase(BaseModel):
    playlist = ForeignKeyField(PlaylistModel, backref='items')
    video = ForeignKeyField(VideoModel, backref='in_playlists')

    class Meta:
        table_name = "playlist_items"

    @staticmethod
    def get_playlist_logic(playlist_model: PlaylistModel):
        """
        Playlist durumuna göre uygun Logic sınıfını döndürür.
        Kullanım: PlaylistLogicBase.get_playlist_logic(playlist)
        """
        if playlist_model.is_public:
            return PublicPlaylist(playlist_model)
        else:
            return PrivatePlaylist(playlist_model)


class BasePlaylistStatus:
    def __init__(self, model):
        self.model = model
    
    def get_status_text(self):
        pass

class PublicPlaylist(BasePlaylistStatus):
    def get_status_text(self):
        return f"Herkese Açık (Public)"

class PrivatePlaylist(BasePlaylistStatus):
    def get_status_text(self):
        return f"Kişiye Özel (Private)"