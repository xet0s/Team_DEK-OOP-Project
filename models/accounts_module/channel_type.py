from .channel_base import ChannelModel
from abc import ABC, abstractmethod
class ChannelBase(ABC):
    def __init__(self,model):
        self.data=model    
        self.__visibility_score=0
        self.__upload_limit=0
    #calculate_visibility_score --> Kanalın görünürlük parametresi
    @property
    @abstractmethod
    def visibility_score(self):
        pass
    #get_upload_limit-------------> Kanala içerik yükleme limiti
    @property
    @abstractmethod
    def upload_limit(self):
        pass
    
    @staticmethod
    def get_channel_policy(channel_type_string):
        if channel_type_string=="Personal":
            return PersonalChannel(None)
        if channel_type_string=="Brand":
            return BrandChannel(None)
        if channel_type_string=="Kid":
            return KidChannel(None)
        if channel_type_string=="Music":
            return MusicChannel(None)
        if channel_type_string=="Education":
            return EducationChannel(None)
        if channel_type_string=="Advertising":
            return AdvertisingChannel(None)
        return PersonalChannel(None)
#Kişisel Kanal
class PersonalChannel(ChannelBase):
    def __init__(self, model):
        super().__init__(model)
    @property
    def upload_limit(self):
        return 5 
    @property
    def visibility_score(self):
        return 10
#Şirket/Marka Kanalı
class BrandChannel(ChannelBase):
    def __init__(self, model):
        super().__init__(model)
    @property
    def upload_limit(self):
        return 50  
    @property
    def visibility_score(self):
        return 100
#Çocuk Kanalı
class KidChannel(ChannelBase):
    def __init__(self, model):
        super().__init__(model)
    @property
    def upload_limit(self):
        return 25  
    @property
    def visibility_score(self):
        return 75
#Müzik Kanalı
class MusicChannel(ChannelBase):
    
    def __init__(self, model):
        super().__init__(model)
    @property
    def upload_limit(self):
        return 150 
    @property
    def visibility_score(self):
        return 200
#Eğitim Kanalı
class EducationChannel(ChannelBase):
    def __init__(self, model):
        super().__init__(model)
    @property
    def upload_limit(self):
        return 25  
    @property
    def visibility_score(self):
        return 25
#Reklam Kanalı
class AdvertisingChannel(ChannelBase):
    
    def __init__(self, model):
        super().__init__(model)
    @property
    def upload_limit(self):
        return 500  

    @property
    def visibility_score(self):
        return 175