from peewee import CharField, ForeignKeyField, IntegerField, TextField
from models.base_model import BaseModel
from models.accounts_module.channel_base import ChannelModel

class VideoModel(BaseModel):
    channel = ForeignKeyField(ChannelModel,on_delete="CASCADE", backref='videos', null=False)       # Video'nun ait olduğu kanal
    title = CharField(max_length=150, null=False)                               # Video başlığı
    description = TextField(null=True)                                          # Video açıklaması
    __duration_seconds = IntegerField(column_name="duration_seconds",default=0) # Video süresi (saniye cinsinden)(private)
    visibility = CharField(default='private')                                   # Video görünürlüğü
    __status = CharField(column_name="status", default='uploaded')              # Video durumu (private)
    video_type_id = CharField(null=False)                                       # Video tipi ('standard', 'short', 'live')
    video_link = CharField(max_length=255, unique=True, null=False)             # Video bağlantısı
    video_category = CharField(default="General")                               # Video kategorisi
    tags = CharField(null=True)                                                 # Video etiketleri
    view_count = IntegerField(default=0)                                        # Video görüntülenme sayısı
    class Meta:                                                             # SQL Tablosu
        table_name = "videos"

    @property
    def duration(self):
        return self.__duration_seconds

    @property
    def status(self):
        return self.__status
    
    @duration.setter
    def duration(self, seconds):
        if seconds < 0:
            raise ValueError("Süre negatif olamaz.")
        self.__duration_seconds = seconds

    @status.setter
    def status(self, new_status):
        valid_statuses = ['uploaded', 'processing', 'live', 'completed', 'removed', 'published']
        if new_status not in valid_statuses:
            raise ValueError(f"Geçersiz durum: {new_status}. Geçerli durumlar: {valid_statuses}")
        self.__status = new_status  

    @property
    def formatted_duration(self):
        minutes = self.__duration_seconds // 60
        seconds = self.__duration_seconds % 60
        return f"{minutes:02}:{seconds:02}"
    
    # Yayınlanmış videoları döndüren sınıf metodu
    @classmethod
    def get_published_videos(cls):
        return list(cls.select().where(
            (cls.visibility == 'public') & 
            (cls.__status == 'completed')
        ))
    
    # Tüm videoların toplam görüntülenme sayısını döndüren sınıf metodu
    @classmethod
    def get_total_view_count(cls):
        videos = cls.select()
        total_views = sum(video.view_count for video in videos)
        return total_views
    
    # Kapsüllenmiş status field'ına sınıf içerisinden erişen metod
    @classmethod
    def filter_videos_by_status(cls, status_input):
        status_input = status_input.lower().strip()
        return list(cls.select().where(cls.__status == status_input))