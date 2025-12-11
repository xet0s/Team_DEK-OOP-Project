from models.accounts_module.channel_base import ChannelModel

from models.accounts_module.channel_type import(
    PersonalChannel,
    BrandChannel,
    KidChannel)

from models.repositories.channel_repository import ChannelRepository

class ChannelController:
    
    #repository bağlantısı
    def __init__(self):
        self.repo=ChannelRepository()
    #Kanal oluşumunu sağlayan fonksiyon.
    #Kanal oluşum kurallarını,şartlarını ve hata durumlarını içinde barındırır
    def create_channel(self,channel_owner,channel_name,channel_category,channel_type):
        #Kanal Türleri
        valid_types=["Personal","Brand","Kid"]
        #Kontrol komutu
        if channel_type not in valid_types:
            return "Lütfen belirtilen kanal türlerden birini seçiniz !"
        #Kayıt Şeması
        channel_information={
            "channel_owner":channel_owner,
            "channel_name":channel_name,
            "channel_category":channel_category,
            "channel_type":channel_type
        }
        #Halihazırda kayıtlı bir kanal girilmeye çalışılırsa uyarı vermesi için ayarlanmış sistem
        try:
            saved_channel=self.repo.add_channel(channel_information) #Kanal kayıt sistemi
        except Exception as e:
            return f"Veritabanı hatası: {str(e)}"
        prepared_channel=None
        #Kanal Türü belirleme ve türe göre sınıf ataması yapma
        if channel_type=="Personal":
            prepared_channel=PersonalChannel(saved_channel)
        elif channel_type=="Brand":
            prepared_channel=BrandChannel(saved_channel)
        elif channel_type=="Kid":
            prepared_channel=KidChannel(saved_channel)
        #2. hata kontrol sistemi
        if prepared_channel is None:
            return "Hata! Kanal türü doğru şekilde belirlenemedi"
        #Polimorfizm testi/Limit belirleme
        upload_limit=prepared_channel.get_upload_limit()
        #Kanal bilgisi döndürme
        return f""" 
                    Channel Owner: {saved_channel.channel_owner.username}|Channel Name: {saved_channel.channel_name}
                    Channel Category: {saved_channel.channel_category}|Channel Type: {channel_type} 
                    Channel Status: {saved_channel.channel_status}| Upload Limit : {upload_limit}"""
    
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