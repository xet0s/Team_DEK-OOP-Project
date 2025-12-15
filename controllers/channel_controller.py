import random

from models.accounts_module.channel_base import ChannelModel
from models.accounts_module.channel_type import(ChannelBase,
                                                PersonalChannel,
                                                BrandChannel,
                                                KidChannel,
                                                )

from models.repositories.channel_repository import ChannelRepository

class ChannelController:
    
    #repository bağlantısı
    def __init__(self):
        self.repo=ChannelRepository()
    #Kanal oluşumunu sağlayan fonksiyon.
    #Kanal oluşum kurallarını,şartlarını ve hata durumlarını içinde barındırır
    def create_channel(self,channel_owner,channel_name,channel_category,channel_type):
        
        #Kanal Türü belirleme ve türe göre sınıf ataması yapma
        prepared_channel=ChannelBase.get_channel_policy(channel_type)

        #hata kontrol sistemi
        if prepared_channel is None:
            return "Hata! Kanal türü doğru şekilde belirlenemedi"
        #Limit Belirleme
        upload_limit=prepared_channel.get_upload_limit()
        #Kanal linki oluşturma
        clean_channel_name=channel_name.replace(" ","").lower()
        owner_id=channel_owner.id
        created_channel_link=f"https://dek.video.com/c/{owner_id}/{clean_channel_name}/?s={random.randint(1000,9999)}"

        #Kayıt Şeması
        channel_information={
            "channel_owner":channel_owner,
            "channel_name":channel_name,
            "channel_category":channel_category,
            "channel_type":channel_type,
            "channel_upload_limit":upload_limit,
            "channel_link":created_channel_link,
        }
        #Halihazırda kayıtlı bir kanal girilmeye çalışılırsa uyarı vermesi için ayarlanmış sistem
        try:
            saved_channel=self.repo.add_channel(channel_information) #Kanal kayıt sistemi
        except Exception as e:
            return f"Veritabanı hatası : {str(e)}"
        #Kanal bilgisi döndürme
        return (
f"""
------------------------------------------
            [✓] KANAL OLUŞTURULDU
------------------------------------------
Kanal Sahibi     : {saved_channel.channel_owner.username}
Kanal İsmi       : {saved_channel.channel_name}
Kanal Kategorisi : {saved_channel.channel_category}
Kanal Türü       : {saved_channel.channel_type}
Yükleme Limiti   : {saved_channel.channel_upload_limit}
Kanal Linki      : {saved_channel.channel_link}
------------------------------------------
""")
        

    #Kanal silme yolu
    def delete_existing_channel(self,channel_id,current_user):
        #Kanalı çeker
        channel=self.repo.get_channel_by_id(channel_id)
        #Kanalın varlığını sorgular
        if channel is None:
            return "Böyle bir kanal bulunmamakta"
        #Kanal ile kullanıcı bağlantısı kurar
        if current_user.id!=channel.channel_owner.id:
            return "Bu işlemi yapmak için gereken yetkiye sahip değilsiniz"
        self.repo.delete_channel(channel_id) #siler
        return "Kanal başarıyla silindi"
    
    def update_existing_channel(self,channel_id,current_user,updated_channel_name=None,updated_status=None):
        
        channel=self.repo.get_channel_by_id(channel_id) #Id üzerinden kanalı çeker

        if channel is None:                             #kanalın varlığını kontrol eder
            return "Bu id'ye sahip bir kanal bulunmamakta!"

        if channel.channel_owner.id != current_user.id: #Kanal sahibi ile mevcut kullanıcı aynı kişi mi diye kontrol eder
            return "Mevcut kanal üzerinde değişiklik yapacak yetkiniz bulunmamakta!"
        
        updated_information={}                          #değişikliklerin işleneceği boş kume

        if updated_channel_name != None:                #Değiştirilecek isim girilmişse değişim  yapar
            updated_information["channel_name"]=updated_channel_name
            
        if updated_status != None:                      #Değiştirilicek durum girildiyse değişim yapar
            updated_information["channel_status"]=updated_status

        if updated_information=={}:                     #Değişiklik kontrolü
            return "Değişiklik yapılmadı"
        
        is_updated=self.repo.update_channel(channel_id,updated_information)#Başarı durumunu sorgular

        if is_updated:
            return "Kanal Başarı ile güncellendi"
        else:
            return "Güncelleme esnasında bir hata oluştu"