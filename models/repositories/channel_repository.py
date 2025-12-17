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
    #Kullanıcı ID si üzerinden kanal durumunu kontrol eden sistem
    def get_channel_by_owner(self,owner_id):
        return ChannelModel.get_or_none(ChannelModel.channel_owner ==owner_id)

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
    #Kanalı güncelleyebilmek için veriyi çeken fonksiyon
    def update_channel(self,channel_id,updated_information):
        #Değiştirme ve nerede değişiklik yapılacağı sorgusu
        query=ChannelModel.update(**updated_information).where(ChannelModel.id==channel_id)
        #Değişen satır sayısı
        changed_row_num=query.execute()
        return changed_row_num>0
    #Kanal kategorisine göre kanalları listeler
    def list_by_category(self,searched_category):
        #Tag'i içeren tabloyu çeker
        query=ChannelModel.select().where(ChannelModel.channel_category==searched_category)
        return list(query)
    #Kanal tipine göre kanalları listeler
    def list_by_tag(self,searched_tag):
        #Tag'i içeren tabloyu çeker
        query=ChannelModel.select().where(ChannelModel.channel_type==searched_tag)
        return list(query)
    #Kanal ismine göre kanalları listeler
    def search_by_name(self,keyword):
        #Keyword içeren kanalları çeker
        query=ChannelModel.select().where(ChannelModel.channel_name.contains(keyword))
        return list(query)
