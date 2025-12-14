import string
import random
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from models.repositories.channel_repository import ChannelRepository
from models.repositories.video_repository import VideoRepository
from models.content_module.video_type import get_video_logic
from models.accounts_module.channel_type import(
                                                PersonalChannel,
                                                BrandChannel,
                                                KidChannel)

class VideoController:
    def __init__(self): #Repository klasörüne bağlantı
        self.repo=VideoRepository()
        self.channel_repo=ChannelRepository()

    #Video oluşturma fonksiyonu
    def create_video(self, current_user, channel_id, video_title, video_description, video_duration, video_type_input):
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
        
        #Rastgele video linki oluşturma
        link = self.generate_video_link()

        #Kaydedilecek video bilgileri
        video_information={
            "channel": channel,              
            "title": video_title,            
            "description": video_description,
            "duration_seconds": video_duration, 
            "video_type_id": db_video_type,  
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

        return f""" 
        Video Başarıyla Yüklendi!
        -------------------------
        Kanal: {saved_video.channel.channel_name}
        Başlık: {saved_video.title}
        Link: {saved_video.video_link}
        Açıklama: {saved_video.description}
        Tür: {db_video_type} 
        Durum: {saved_video.status}
        Tahmini İşleme Süresi: {processing_time} saniye"""

    #Video silme fonksiyonu
    def delete_existing_video(self,video_id,current_user):
        #Video varlık ve yetki kontrolü
        video=self.repo.get_video_by_id(video_id)
        if video is None:
            return "Böyle bir video bulunmamakta"
        if video.channel.channel_owner.id != current_user.id:
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
        if video is None:
            return "Böyle bir video bulunmamakta"
        if video.channel.channel_owner.id != current_user.id:
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

    #Yardımcı fonksiyon: Rastgele video linki oluşturma
    def generate_video_link(self):
        chars = string.ascii_letters + string.digits
        random_link = ''.join(random.choice(chars) for _ in range(8)) #Uzunluk 8 karakter
        return f"https://dek.video/v/{random_link}"