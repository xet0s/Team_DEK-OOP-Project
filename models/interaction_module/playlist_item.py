import datetime
from peewee import ForeignKeyField,DateTimeField
from models.base_model import BaseModel

#Playlist yapısını çeker
from models.interaction_module.playlist_base import PlaylistModel

#Video yapısını çeker
from models.content_module.video_base import VideoModel

class PlaylistItemModel(BaseModel):
    """
    Videoları ve Playliste bağlayan ara tablo yapısı
    on_delete='CASCADE'--->Playlistin silinmesi durumunda tabloyu siler

    """
    playlist=ForeignKeyField(PlaylistModel, backref="items", on_delete="CASCADE")
    video=ForeignKeyField(VideoModel, backref="included_playlist", on_delete="CASCADE")
    #Playlist eklenme zamanı
    added_at=DateTimeField(default=datetime.datetime.now)

    class Meta:
        #Tablo ismi
        table_name="playlist_item"