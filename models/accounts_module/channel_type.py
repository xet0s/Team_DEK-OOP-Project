from .channel_base import ChannelModel
from abc import ABC, abstractmethod

class ChannelBase(ABC):
    def __init__(self,model):
        self.data=model    
    #calculate_visibility_score --> Kanalın görünürlük parametresi
    #get_upload_limit-------------> Kanala içerik yükleme limiti
    
    @abstractmethod
    def calculate_visibility_score(self):
        pass

    @abstractmethod
    def get_upload_limit(self):
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

    def calculate_visibility_score(self):
        return 10
    
    def get_upload_limit(self):
        return 5
#Şirket/Marka Kanalı
class BrandChannel(ChannelBase):

    def __init__(self, model):
        super().__init__(model)
        
    def calculate_visibility_score(self):
        return 7
    
    def get_upload_limit(self):
        return 99
#Çocuk Kanalı
class KidChannel(ChannelBase):

    def __init__(self, model):
        super().__init__(model)
        
    def calculate_visibility_score(self):
        return 5
    
    def get_upload_limit(self):
        return 2
#Müzik Kanalı
class MusicChannel(ChannelBase):
    
    def __init__(self, model):
        super().__init__(model)

    def calculate_visibility_score(self):
        return 99
    
    def get_upload_limit(self):
        return 50
#Eğitim Kanalı
class EducationChannel(ChannelBase):
    
    def __init__(self, model):
        super().__init__(model)
    
    def calculate_visibility_score(self):
        return 10
    
    def get_upload_limit(self):
        return 15
#Reklam Kanalı
class AdvertisingChannel(ChannelBase):
    
    def __init__(self, model):
        super().__init__(model)

    def calculate_visibility_score(self):
        return 2
    
    def get_upload_limit(self):
        return 999