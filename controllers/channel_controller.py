import random
from models.accounts_module.channel_type import ChannelBase
from models.repositories.channel_repository import ChannelRepository
from utils.exceptions.channel_error import (
    ChannelLimitExceededError,
    InvalidNameError,
    InvalidChannelTypeError,
    ChannelNotFoundError,
    ChannelAlreadyExistError,
    ChannelUploadLimitError
)
class ChannelController:
    #repository bağlantısı
    def __init__(self):
        self.repo=ChannelRepository()
    #Kanal oluşumunu sağlayan fonksiyon.
    #Kanal oluşum kurallarını,şartlarını ve hata durumlarını içinde barındırır
    def create_channel(self,channel_owner,channel_name,channel_category,channel_type,channel_info=None):
        #Kanal var mı kontrolü
        existing_channel= self.repo.get_channel_by_owner(channel_owner.id)
        #Kanal varsa hata veren kısıms
        if existing_channel != None:
            raise ChannelLimitExceededError(channel_owner.username)
        #İsim uzunluk kontrolü
        if len(channel_name)<3:
            raise InvalidNameError(channel_name,3)
        #Kanal isim kontrol sistemi
        search_result= self.repo.search_by_name(channel_name)
        for ch in search_result:
            if channel_name.lower()==ch.channel_name.lower():
                raise ChannelAlreadyExistError(channel_name)
        #Kanal Türü belirleme ve türe göre sınıf ataması yapma
        prepared_channel=ChannelBase.get_channel_policy(channel_type)
        #hata kontrol sistemi
        if prepared_channel is None:
            raise InvalidChannelTypeError(channel_type)
        #Limit Belirleme
        upload_limit=prepared_channel.get_upload_limit()
        #Kanal linki oluşturma
        clean_channel_name=channel_name.replace(" ","").lower()
        created_channel_link=f"https://dek.video.com/c/{clean_channel_name}/?s={random.randint(1000,9999)}"
        #Kayıt Şeması
        channel_information={
            "channel_owner":channel_owner,
            "channel_name":channel_name,
            "channel_category":channel_category,
            "channel_type":channel_type,
            "channel_upload_limit":upload_limit,
            "channel_link":created_channel_link,
            "channel_info":channel_info,
        }
        #Halihazırda kayıtlı bir kanal girilmeye çalışılırsa uyarı vermesi için ayarlanmış sistem
        try:
            saved_channel=self.repo.add_channel(channel_information) #Kanal kayıt sistemi
        except Exception as e:
            return (False,f"Veritabanı hatası : {str(e)}")
        #Kanal bilgisi döndürme
        return (True,
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
            raise ChannelNotFoundError(channel_id=channel)
        #Kanal ile kullanıcı bağlantısı kurar
        if current_user.id!=channel.channel_owner.id:
            return False,"Yetkisiz deneme"
        self.repo.delete_channel(channel_id) #siler
        return (True,"Kanal başarıyla silindi")
    def update_existing_channel(self,channel_id,current_user,updated_channel_name=None,updated_status=None,updated_info=None):
        #Id üzerinden kanalı çeker
        channel=self.repo.get_channel_by_id(channel_id) 
        #kanalın varlığını kontrol eder
        if channel is None:                             
            raise ChannelNotFoundError(channel_id=channel_id)
        #Kanal sahibi ile mevcut kullanıcı aynı kişi mi diye kontrol eder
        if channel.channel_owner.id != current_user.id: 
            return False, "Kanal bulunamadı"
        #değişikliklerin işleneceği boş kume
        updated_information={}                          
        #Değiştirilecek isim girilmişse değişim  yapar
        if updated_channel_name != None:                 
            updated_information["channel_name"]=updated_channel_name
        #Değiştirilicek durum girildiyse değişim yapar
        if updated_status != None:                      
            updated_information["channel_status"]=updated_status
        if updated_info != None:
            updated_information["channel_info"]=updated_info
        #Değişiklik kontrolü
        if updated_information=={}:                     
            return (False,"Değişiklik yapılmadı")
        #Başarı durumunu sorgular
        is_updated=self.repo.update_channel(channel_id,updated_information)
        if is_updated:
            return (True,"Kanal Başarı ile güncellendi")
        else:
            return (False,"Güncelleme esnasında bir hata oluştu")
    def search_channels(self,search_key,search_value):
        #Boş sonuç listesi
        result=[]
        #arama türünü belirleyen kısım
        if search_key=="name":
            result=self.repo.search_by_name(search_value)
        if search_key=="category":
            result=self.repo.list_by_category(search_value)
        if search_key=="type":
            result=self.repo.list_by_tag(search_value)
        #Sonuç yoksa hata fırlatan kısım
        if not result:
            if search_key=="name":
                return False, "Kriterlere uygun kanal bulunamadı."
        #Sonuç
        output="="*50+f"ARAMA SONUÇLARI ({len(result)} Kanal bulundu)\n"+"="*50
        for ch in result:
            output+= f"ID: {ch.id}|İsim: {ch.channel_name:<20}|Kategori: {ch.channel_category}\n"+"-"*50
        return True,output