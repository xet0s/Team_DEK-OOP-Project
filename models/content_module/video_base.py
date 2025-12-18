from peewee import CharField, ForeignKeyField, IntegerField, TextField
from models.base_model import BaseModel
from models.accounts_module.channel_base import ChannelModel
from abc import ABC, abstractmethod

class VideoModel(BaseModel):
    channel = ForeignKeyField(ChannelModel, backref='videos', null=False)   # Video'nun ait olduğu kanal
    title = CharField(max_length=150, null=False)                           # Video başlığı
    description = TextField(null=True)                                      # Video açıklaması
    duration_seconds = IntegerField(default=0)                              # Video süresi (saniye cinsinden)
    visibility = CharField(default='private')                               # Video görünürlüğü
    status = CharField(default='uploaded')                                  # Video durumu
    video_type_id = CharField(null=False)                                   # Video tipi ('standard', 'short', 'live')
    video_link = CharField(max_length=255, unique=True, null=False)         # Video bağlantısı
    video_category = CharField(default="General")                           # Video kategorisi
    tags = CharField(null=True)                                             # Video etiketleri
    view_count = IntegerField(default=0)                                    # Video görüntülenme sayısı
    class Meta:                                                             # SQL Tablosu
        table_name = "videos"