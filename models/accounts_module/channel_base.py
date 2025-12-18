from peewee import (CharField,
                    ForeignKeyField,
                    IntegerField,
                    TextField)
from models.base_model import BaseModel
from models.accounts_module.user import User
from abc import ABC, abstractmethod

class ChannelModel(BaseModel):
    #Foreign Key --> Bağlantı ve özel veri 
    channel_owner=ForeignKeyField(User,backref="channel")   #Kanal sahibi (kullanıcı tablosuna bağlantı)
    channel_name=CharField(unique=True,null=False)          #Kanal ismi
    channel_category=CharField(null=False)                  #Kanal kategorisi
    channel_status=CharField(default="pending_verification")#Kanal durumu
    channel_type=CharField(null=False)                      #Kanal Tipi
    channel_upload_limit=IntegerField(null=False)           #İçerik Yükleme Limiti
    channel_link=CharField(unique=True,null=False)          #Kanal linki
    channel_info=TextField(default="Hakkımda...",null=True) #Kanal Hakkında Kısmı
    class Meta:                                             #Sql Tablosu
        table_name="channels"