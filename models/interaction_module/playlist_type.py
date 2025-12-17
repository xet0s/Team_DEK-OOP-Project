from models.interaction_module.playlist_base import PlaylistModel

class PlaylistLogicBase:

    def __init__(self,model):
        self.model=model
    #Playlist durumunu String olarak döndüren Polymorf fonksiyon
    def get_status_text(self):
        pass

    #Playlist görünürlüğünü belirleyen ve ona göre class ataması yapan fonksiyon
    @staticmethod
    def get_playlist_logic(playlist_model: PlaylistModel):
        if playlist_model.is_public:
            return PublicPlaylist(playlist_model)
        if playlist_model.is_public:
            return PrivatePlaylist(playlist_model)
#Herkese açık playlist
class PublicPlaylist(PlaylistLogicBase):
    def get_status_text(self):
        return f"{self.model.title} (Herkese Açık)"
#Kişiye özel playlist
class PrivatePlaylist(PlaylistLogicBase):
    def get_status_text(self):
        return f"{self.model.title} (Özel)"
    

