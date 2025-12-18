from models.content_module.video_base import VideoModel
from peewee import DoesNotExist

class VideoRepository:
    #Video oluşturma
    def add_video(self, video_data):
        return VideoModel.create(**video_data)

    #ID ye göre videoları listeleme
    def get_video_by_id(self, video_id): 
        try:
            return VideoModel.get_or_none(VideoModel.id == video_id)
        except DoesNotExist:
            print("Böyle bir video yok")
            return None

    #Kanal ID'sine göre videoları listeleme
    def get_videos_by_channel(self, channel_id): 
        return VideoModel.select().where(VideoModel.channel == channel_id)

    #Bütün videoları listeleme
    def get_all_videos(self):
        return list(VideoModel.select())

    #Video durumunu güncelleme
    def update_video_status(self, video_id, new_status):
        video = self.get_video_by_id(video_id)
        if video:
            video.status = new_status
            video.save()
            return video
        else:
            print("Güncellenecek video bulunamadı")
            return None

    #Video durumuna göre videoları listeleme
    def filter_by_status(self, status):
        try:
            return list(VideoModel.select().where(VideoModel.status == status))
        except DoesNotExist:
            print("Aranan statüde bir video bulunmamakta")
            return []

    #Video silme
    def delete_video(self, video_id):
        #Silinecek videoyu ID'den çekme           
        video = self.get_video_by_id(video_id)  
        if video:
            video.delete_instance()
            return True
        else:
            print("Silinecek video bulunamadı")
            return False

    #Video güncelleme
    def update_video(self, video_id, updated_information): 
        query = VideoModel.update(**updated_information).where(VideoModel.id == video_id)
        changed_row_num = query.execute()
        return changed_row_num > 0

    #Görünürlüğe göre videoları listeleme
    def filter_by_visibility(self, visibility):
        try:
            return VideoModel.select().where(VideoModel.visibility == visibility)
        except DoesNotExist:
            print("Aranan görünürlükte bir video bulunmamakta")
            return []

    #Tarihe göre videoları sıralama
    def get_sorted_videos_by_date(self, descending=True):
        if descending:
            return VideoModel.select().order_by(VideoModel.created_at.desc())
        else:
            return VideoModel.select().order_by(VideoModel.created_at.asc())

    #Kategoriye göre videoları filtreleme
    def filter_by_category(self, category_name):
        try:
            return list(VideoModel.select().where(VideoModel.video_category == category_name))
        except DoesNotExist:
            return []
        
    #İzlenme sayısı arttırma
    def increment_view_count(self, video_id):
        query = VideoModel.update(view_count=VideoModel.view_count + 1).where(VideoModel.id == video_id)
        return query.execute() > 0

    #Oynatma listesine göre videoları listeleme
    def get_videos_by_id_list(self, video_id_list):
        if not video_id_list:
            return []
        try:
            return list(VideoModel.select().where(VideoModel.id.in_(video_id_list)))
        except DoesNotExist:
            print("Bu oynatma listesinde video bulunmamaktadır.")
            return []