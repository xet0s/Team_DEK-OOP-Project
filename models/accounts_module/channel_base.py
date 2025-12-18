#Veritabanı bağlantıları oluşum için gerekli moduller
from peewee import (CharField,
                    ForeignKeyField,
                    IntegerField,
                    TextField)
from models.base_model import BaseModel
from models.accounts_module.user_base import UserBase

class ChannelModel(BaseModel):
    #Foreign Key --> Bağlantı ve özel veri 
    channel_owner=ForeignKeyField(UserBase,backref="channel")   #Kanal sahibi (kullanıcı tablosuna bağlantı)
    channel_name=CharField(unique=True,null=False)          #Kanal ismi
    channel_category=CharField(null=False)                  #Kanal kategorisi
    channel_status=CharField(default="pending_verification")#Kanal durumu
    channel_type=CharField(null=False)                      #Kanal Tipi
    channel_upload_limit=IntegerField(null=False)           #İçerik Yükleme Limiti
    channel_link=CharField(unique=True,null=False)          #Kanal linki
    channel_about=TextField(null=True,default="Hakkımda...")#Kanal hakkımda kısmı
    class Meta:                                             #Sql Tablosu
        table_name="channels"