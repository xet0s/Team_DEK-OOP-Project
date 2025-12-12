from models.content_module.video_base import VideoModel
from peewee import DoesNotExist

class VideoRepository:
    def add_video(self, video_data): #Video oluşturma
        return VideoModel.create(**video_data)

    def get_video_by_id(self, video_id): #ID ye göre videoları listeleme
        try:
            return VideoModel.get_or_none(VideoModel.id == video_id)
        except DoesNotExist:
            print("Böyle bir video yok")
            return None

    def get_videos_by_channel(self, channel_id): #Kanal ID'sine göre videoları listeleme
        return VideoModel.select().where(VideoModel.channel == channel_id)

    def get_all_videos(self): #Bütün videoları listeleme
        return list(VideoModel.select())

    def filter_by_category(self, category_name): #Kategoriye göre videoları listeleme
        try:
            return VideoModel.select().where(VideoModel.video_category == category_name)
        except DoesNotExist:
            print("Aranan kategoride video bulunmamakta")
            return None

    def update_video_status(self, video_id, new_status): #Video durumunu güncelleme
        video = self.get_video_by_id(video_id)
        if video:
            video.status = new_status
            video.save()
            return video
        else:
            print("Güncellenecek video bulunamadı")
            return None

    def filter_by_status(self, status): #Video durumuna göre videoları listeleme
        try:
            return VideoModel.select().where(VideoModel.status == status)
        except DoesNotExist:
            print("Aranan statüde bir video bulunmamakta")
            return None