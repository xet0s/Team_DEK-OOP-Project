from models.accounts_module.channel_base import ChannelModel
from peewee import DoesNotExist 
#Database e veri gönderecek ana sınıf
class ChannelRepository:
    #Kanal oluşturma
    def add_channel(self,channel_data):
        return ChannelModel.create(**channel_data)
    #ID ye göre  kanalları listeleme
    def get_channel_by_id(self,channel_id):
        try:
            return ChannelModel.get_or_none(ChannelModel.id == channel_id)
        except DoesNotExist:
            print("Böyle bir kanal yok")
            return None
    #Bütün kanalları listeleme
    def get_all_channel(self):
        return list(ChannelModel.select())
    #Kategoriye göre kanalları listelem
    def filter_by_category(self,category_name):
        try:
            return ChannelModel.select().where(ChannelModel.channel_category==category_name)
        except DoesNotExist:
            print("Aranan kategoride kanal bulunmamakta")
            return None
    #Kanal durumuna göre kanalları listeleme
    def filter_by_status(self,status):
        try:
            return ChannelModel.select().where(ChannelModel.channel_status==status)
        except DoesNotExist:
            print("Aranan statüde bir kanal bulunmamakta")
            return None
    #Varolan kanalı ID'si sayesinde silme
    def delete_channel(self,channel_id):
        channel=self.get_channel_by_id(channel_id)#ID'den kanalı çekme

        if channel:
            channel.delete_instance()#DB'den veri silen satır
            return True#Veri Silindi
        
        return  False #Veri silinemedi veya bulunamadı