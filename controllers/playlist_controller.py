from models.accounts_module.user import User
from models.interaction_module.playlist_type import PlaylistLogicBase
from models.repositories.playlist_repository import PlaylistRepository          
from models.repositories.video_repository import VideoRepository                #Video var mı diye bakmak için

class PlaylistController:
    def __init__(self):
        self.repo=PlaylistRepository()
        self.video_repo=VideoRepository() #Video var mı diye bakmak için

    #PLAYLİST OLUŞTURMA
    def create_playlist(self,current_user,title,is_public_choice):
        if not title or title.strip()=="":
            return "Lütfen geçerli bir playlist başlığı giriniz!"
        #Görünürlük ayarı (E ise True, değilse False)
        is_public_bool=True if is_public_choice.upper()=="E" else False
        #Kaydedilecek veri
        playlist_data={
            "user":current_user,
            "title":title,
            "is_public":is_public_bool
        }   
        #Repoya gönderip kaydet      
        try:
            saved_playlist=self.repo.create_playlist(playlist_data)
        except Exception as e:
            return f"Veritabanı hatası"    
        #Playlist herkese açık/gizli 
        playlist_logic = PlaylistLogicBase.get_playlist_logic(saved_playlist)
        status_text = playlist_logic.get_status_text()

        return f"""
            Playlist başarıyla oluşturuldu
            ------------------------------
            ID: {saved_playlist.id}
            Playlist adı: {saved_playlist.title}
            Durum: {status_text}

            """


    #Video ekleme 
    def add_video(self,current_user,playlist_id,video_id):
        playlist=self.repo.get_playlist_by_id(playlist_id)

        if not playlist:
            return "Böyle bir playlist bulunamadı."
        #Sadece playlist sahibi video ekleyebilir
        if playlist.user.id != current_user.id:
            return "Bu listeye video ekleyemezsiniz."
        #video kontrol
        video = self.video_repo.get_video_by_id(video_id)
        if not video:
            return "Eklemek istediğiniz video bulunamadı. "
        #Önceden eklenmiş mi?
        if self.repo.check_video_in_playlist(playlist_id,video_id):
            return "Bu video zaten listede var."
        try:
            self.repo.add_video_to_playlist(playlist,video)
            return f"{video.title} listeye eklendi"
        except Exception as e:
            return f"Hata. {str(e)}"
        
    #Video silme 
    def remove_video(self,current_user,playlist_id,video_id):
        playlist=self.repo.get_playlist_by_id(playlist_id)
        if not playlist:
            return "Playlist bulunamadı."
        #Sadece sahibi silebilir
        if playlist.user.id !=current_user.id:
            return "Bu listeden video silme yetkiniz yok."
        try:
            count = self.repo.remove_video_from_playlist(playlist_id, video_id)
            if count > 0:
                return " Video listeden çıkarıldı."
            else:
                return " Video listede bulunamadı."
        except Exception as e:
            return f"Hata: {str(e)}"
        
    #Playlist silme
    def delete_playlist(self,current_user,playlist_id):
        playlist=self.repo.get_playlist_by_id(playlist_id)  
        if not playlist:
            return "Playlist bulunamadı."
        #Sadece sahibi silebilir.
        if playlist.user.id !=current_user.id:
            return "Bu playlisti silme yetkiniz yok."  
        if self.repo.delete_playlist(playlist_id):
            return "Playlist başarıyla silindi."
        else:
            return "Silme işlemi başarısız oldu."
        
    #Playlist listelerini göster
    def list_my_playlist(self,current_user_id):
        playlist=self.repo.get_playlists_by_user(current_user_id)
        if not playlist:
            return "Henüz bir listeniz yok."
        
        output=  "/n LİSTELERİNİZ:/n " #çıktı
        for pl in playlist:
            logic=PlaylistLogicBase.get_playlist_logic(pl)
            status=logic.get_status_text()
            #kaç video var
            count=len(self.repo.get_playlist_items(pl.id))
            output+=f"ID:{pl.id}  |{pl.title}  {status} ({count})"
        return output      
    
    #Liste içeriğini göster
    def show_playlist_countent(self,playlist_id):
        playlist=self.repo.get_playlist_by_id(playlist_id)
        if not playlist:
            return "Playlist bulunamadı"
        
        items=self.repo.get_playlist_items(playlist_id)
        if not items:
            return f"{playlist.title} listesi boş"
        
        output= f"{playlist.title} içeriği:"
        for item in items:
            #asıl videoya gidicek
            output += f"{item.video.title}"
        return output
        
    #ID ile detay getirme 
    def get_playlist_details(self,playlist_id):
        playlist =self.repo.get_playlist_by_id(playlist_id)
        if not playlist:
            return "Hata: Playlist bulunamadı."
        
        items = self.repo.get_playlist_items(playlist_id)
        video_count = len(items)
        
        logic = PlaylistLogicBase.get_playlist_logic(playlist)
        status_text = logic.get_status_text()

        return f"""
          Playlist 
         -------------
         ID: {playlist.id}
         Playlist adı: {playlist.title}
         Playlist sahibi:{playlist.user.username}
         Durum: {status_text}
         Video sayısı: {video_count}
         """



