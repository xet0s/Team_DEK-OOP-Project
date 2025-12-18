from email import policy
import string
import random
from models.accounts_module.user_type import UserBase
from models.content_module.category_type import CategoryBase
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from models.repositories.channel_repository import ChannelRepository
from models.repositories.video_repository import VideoRepository
from models.content_module.video_type import get_video_logic
from models.content_module.category_type import get_category_policy

class VideoController:
    def __init__(self): #Repository klasörüne bağlantı
        self.repo=VideoRepository()
        self.channel_repo=ChannelRepository()

    #Video oluşturma fonksiyonu
    def create_video(self, current_user, channel_id, video_title, video_description, video_duration, video_type_input, video_category_input):
        user_policy = UserBase.get_user_policy(current_user.role, current_user)
        if not user_policy.upload_video():
            return "Video yükleme yetkiniz bulunmamaktadır."
        
        type_mapping = {"Standard": "standard", "Short": "short", "LiveStream": "live"} #Kullanıcıdan alınan video türünü veritabanı türüne eşleme
        #Geçerlilik kontrolü
        if video_type_input not in type_mapping:
            return "Lütfen geçerli bir video türü seçiniz (Standard, Short, LiveStream)!"
        db_video_type = type_mapping[video_type_input]

        #Kanal varlık ve yetki kontrolü
        channel = self.channel_repo.get_channel_by_id(channel_id)
        if channel is None:
            return "Video yükleyebilmek için önce bir kanal oluşturmalısınız."
        if channel.channel_owner.id != current_user.id:
            return "Bu kanala video yükleme yetkiniz yoktur."

        #Yükleme limiti kontrolü
        existing_videos = self.repo.get_videos_by_channel(channel.id)
        limit = channel.channel_upload_limit
        if len(existing_videos) >= limit:
            return f"Yükleme limiti aşıldı! Limit: {limit}"
        
        #Kategori mantığı belirleme
        category_logic = get_category_policy(video_category_input)
        auto_tags = category_logic.get_suggested_tags()
        cat_desc = category_logic.get_category_description()

        #Rastgele video linki oluşturma
        link = self.generate_video_link()

        #Kaydedilecek video bilgileri
        video_information={
            "channel": channel,              
            "title": video_title,            
            "description": video_description + "\n\nKategori Açıklaması: " + cat_desc + "\nTags: " + auto_tags,
            "duration_seconds": video_duration, 
            "video_type_id": db_video_type,
            "video_category": video_category_input,
            "tags": auto_tags,
            "status": "uploaded",
            "visibility": "public",
            "video_link": link
        }

        #Kayıt işlemi
        try:
            saved_video=self.repo.add_video(video_information)
        except Exception as e:
            return f"Veritabanı hatası: {str(e)}"

        #Video türü belirleme ve sınıf ataması
        prepared_video = None
        prepared_video = get_video_logic(saved_video)

        #Hata kontrolü
        if prepared_video is None:
            return "Hata! Video türü doğru şekilde belirlenemedi"

        processing_time = prepared_video.get_processing_time_estimate()
        process_msg = self.simulate_video_processing(saved_video.id)
        final_video = self.repo.get_video_by_id(saved_video.id)

        return f""" 
        Video Başarıyla Yüklendi!
        -------------------------
        Kanal: {final_video.channel.channel_name}
        Başlık: {final_video.title}
        Link: {final_video.video_link}
        Açıklama: {final_video.description}
        Tür: {db_video_type} 
        Durum: {final_video.status}
        Sistem Mesajı: {process_msg}
        İşleme Süresi: {processing_time} saniye"""

    #Video silme fonksiyonu
    def delete_existing_video(self,video_id,current_user):
        #Video varlık ve yetki kontrolü
        video=self.repo.get_video_by_id(video_id)
        user_policy = UserBase.get_user_policy(current_user.role, current_user)
        if video is None:
            return "Böyle bir video bulunmamakta"
        if video.channel.channel_owner.id != current_user.id and not user_policy.has_admin_access():
            return "Bu videoyu silme yetkiniz yoktur"

        #Silme işlemi
        try:
            self.repo.delete_video(video_id)
        except Exception as e:
            return f"Veritabanı hatası: {str(e)}"   
        return "Video başarıyla silindi"

    #Video güncelleme fonksiyonu
    def update_existing_video(self,video_id,current_user,new_title=None,new_description=None):
        #Video varlık ve yetki kontrolü
        video=self.repo.get_video_by_id(video_id)
        user_policy = UserBase.get_user_policy(current_user.role, current_user)
        if video is None:
            return "Böyle bir video bulunmamakta"
        if video.channel.channel_owner.id != current_user.id and not user_policy.has_admin_access():
            return "Bu videoyu güncelleme yetkiniz yoktur"

        #Güncellenecek bilgiler
        updated_information={}
        if new_title is not None:
            updated_information["title"]=new_title
        if new_description is not None:
            updated_information["description"]=new_description

        #Güncelleme
        try:
            is_updated = self.repo.update_video(video_id,updated_information)
        except Exception as e:
            return f"Veritabanı hatası: {str(e)}"

        if is_updated:
            updated_video = self.repo.get_video_by_id(video_id)
            return f"""
                    Video başarıyla güncellendi!
                    Video ID: {updated_video.id}
                    Yeni Başlık: {updated_video.title}
                    Yeni Açıklama: {updated_video.description}
                    """
        else:
            return "Video güncellenemedi"

    #Video listesi şeklinde görüntüleme fonksiyonu
    def list_all_videos(self):
        videos = self.repo.get_all_videos()
        if not videos:
            return "Hiç video bulunmamaktadır."
        
        video_list = "Mevcut Videolar:\n"
        for video in videos:
            video_list += f"ID: {video.id}, Başlık: {video.title}, Kanal: {video.channel.channel_name}, Durum: {video.status}\n"
        return video_list

    #Duruma göre video listeleme fonksiyonu
    def list_videos_by_status(self, status):
        videos = self.repo.filter_by_status(status)
        if not videos:
            return f"'{status}' durumunda video bulunmamaktadır."
        
        video_list = f"'{status}' Durumundaki Videolar:\n"
        for video in videos:
            video_list += f"ID: {video.id}, Başlık: {video.title}, Kanal: {video.channel.channel_name}\n"
        return video_list

    #Görünürlüğe göre video listeleme fonksiyonu
    def list_videos_by_visibility(self, visibility):
        videos = self.repo.filter_by_visibility(visibility)
        if not videos:
            return f"'{visibility}' görünürlüğünde video bulunmamaktadır."
        
        video_list = f"'{visibility}' Görünürlüğündeki Videolar:\n"
        for video in videos:
            video_list += f"ID: {video.id}, Başlık: {video.title}, Kanal: {video.channel.channel_name}\n"
        return video_list

    #Tarihe göre sıralanmış video listeleme fonksiyonu
    def list_recent_videos(self):
        videos = self.repo.get_sorted_videos_by_date()
        if not videos:
            return "Hiç video bulunmamaktadır."
        
        video_list = "Son Yüklenen Videolar:\n"
        for video in videos:
            video_list += f"ID: {video.id}, Başlık: {video.title}, Kanal: {video.channel.channel_name}, Yüklenme Tarihi: {video.created_at}\n"
        return video_list

    #Video işleme simülasyonu
    def simulate_video_processing(self,video_id):
        video=self.repo.get_video_by_id(video_id)
        if video is None:
            return "Böyle bir video bulunmamakta"
        
        video_logic=get_video_logic(video)
        if video_logic is None:
            return "Video türü belirlenemediği için işleme yapılamıyor"
        
        wait_time=video_logic.get_processing_time_estimate()
        self.repo.update_video_status(video_id,"published")

        return f"Video işleme {wait_time} saniye içinde tamamlandı. Yeni durum: {video_logic.data.status}"
    
    #Video izleme fonksiyonu (izlenme sayısını artırma)
    def watch_video(self, video_id):
        video = self.repo.get_video_by_id(video_id)
        if video is None:
            return "Böyle bir video bulunmamaktadır."
        
        self.repo.increment_view_count(video_id)
        updated_video = self.repo.get_video_by_id(video_id)
        return f"Video izlendi. Yeni İzlenme Sayısı: {updated_video.view_count}"
    
    #Oynatma listesine göre video listeleme fonksiyonu
    def list_playlist_videos(self, video_id_list):
        videos = self.repo.get_videos_by_id_list(video_id_list)

        if not videos:
            return "Oynatma listesinde video bulunmamaktadır."
        result = f"--- Playlist İçeriği ({len(videos)}) ---\n"
        for v in videos:
            result += f"{v.title} | İzlenme: {v.view_count} | Kategori: {v.video_category}\n"
        return result
    
    #Yardımcı fonksiyon: Rastgele video linki oluşturma
    def generate_video_link(self):
        chars = string.ascii_letters + string.digits
        random_link = ''.join(random.choice(chars) for _ in range(8)) #Uzunluk 8 karakter
        return f"https://dek.video/v/{random_link}"