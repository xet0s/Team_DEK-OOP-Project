from models.interaction_module.playlist_base import PlaylistModel
from models.interaction_module.playlist_type import PlaylistLogicBase#BUNA Bİ BAKK
from peewee import DoesNotExist   #Böyle bir kayıt yok hatsını yakalıcaz

class PlaylistRepository:
    def create_playlist(self,playlist_data): #playlist oluşturma
        """yeni bir oynatma listesi oluşturur."""
        return PlaylistModel.create(**playlist_data)
    
    def get_playlist_by_id(self,playlist_id): #Id ye göre playlist bulma
        return PlaylistModel.get_or_none(PlaylistModel.id == playlist_id)

    def get_playlists_by_user(self, user_id): #Kullanıcıya ait playlistleri listeleme
        return list(PlaylistModel.select().where(PlaylistModel.user == user_id))   
    
    def get_all_public_playlists(self): #Herkese açık bütün playlistleri listeleme
        return list(PlaylistModel.select().where(PlaylistModel.is_public == True))
    
    def delete_playlist(self, playlist_id): #Playlist silme işlemi
        playlist = self.get_playlist_by_id(playlist_id)
        if playlist:
            # recursive=True sayesinde içindeki videolar (itemlar) da silinir
            playlist.delete_instance(recursive=True) 
            return True
        else:
            print("Silinecek playlist bulunamadı")
            return False
        
# PLAYLİST İÇİ VİDEO İŞLEMLERİ

    def add_video_to_playlist(self,playlist,video): #Listeye video ekleme 
        #PlaylistItem tablosuna kayıt atar.
        return PlaylistLogicBase.create(playlist=playlist, video=video)

    def remove_video_from_playlist(self,playlist_id,video_id): #videoyu listeden çıkarma
        try:
            query = PlaylistLogicBase.delete().where(
                (PlaylistLogicBase.playlist == playlist_id) &
                (PlaylistLogicBase.video == video_id)
            )
            return query.execute() # Silinen satır sayısını döner
        except Exception as e:
            print(f"Hata oluştu: {e}")
            return 0  

    def get_playlist_items(self, playlist_id): #Listenin içindeki videoları getirme
        # O listeye ait tüm ara tablo kayıtlarını çeker
        return list(PlaylistLogicBase.select().where(PlaylistLogicBase.playlist == playlist_id))

    def check_video_in_playlist(self, playlist_id, video_id): #Video listede var mı kontrolü
        try:
            return PlaylistLogicBase.select().where(
                (PlaylistLogicBase.playlist == playlist_id) &
                (PlaylistLogicBase.video == video_id)
            ).get()
        except DoesNotExist:
            # Eğer yoksa hata basmaya gerek yok, sadece None dönelim
            return None          