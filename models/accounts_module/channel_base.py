from peewee import (CharField,
                    ForeignKeyField,
                    IntegerField,
                    TextField)
from models.base_model import BaseModel
from models.accounts_module.user import User

class ChannelModel(BaseModel):
    #Foreign Key --> Bağlantı ve özel veri 
    channel_owner=ForeignKeyField(User,on_delete="CASCADE",backref="channel")   #Kanal sahibi (kullanıcı tablosuna bağlantı)
    channel_name=CharField(unique=True,null=False)          #Kanal ismi
    channel_category=CharField(null=False)                  #Kanal kategorisi
    channel_status=CharField(default="pending_verification")#Kanal durumu
    channel_type=CharField(null=False)                      #Kanal Tipi
    channel_upload_limit=IntegerField(null=False)           #İçerik Yükleme Limiti
    channel_link=CharField(unique=True,null=False)          #Kanal linki
    channel_info=TextField(default="Hakkımda...",null=True) #Kanal Hakkında Kısmı
    class Meta:                                             #Sql Tablosu
        table_name="channels"
    @property
    def status(self):
        return self.channel_status
    @status.setter
    def status(self,new_status):
        valid_statuses=["active","suspended","pending"]
        if new_status not in valid_statuses:
            raise ValueError(f"Geçersiz durum! Bu liste içinde olan bir durum seçiniz :\n{valid_statuses}")
        self.channel_status=new_status
    @classmethod
    def get_active_channel(cls):
        return cls.select().where(cls.channel_status=="active")
    @classmethod
    def filter_by_category(cls,category_name):
        return cls.select().where(cls.channel_category==category_name)
    @classmethod
    def check_user_has_channel(cls,user_id):
        return cls.select().where(cls.channel_owner==user_id).exists()