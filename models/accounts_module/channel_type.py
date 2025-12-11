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

class PersonalChannel(ChannelBase):
    def __init__(self, model):
        super().__init__(model)

    def calculate_visibility_score(self):
        return 10
    
    def get_upload_limit(self):
        return 5
    
class BrandChannel(ChannelBase):
    def __init__(self, model):
        super().__init__(model)

    def calculate_visibility_score(self):
        return 7
    
    def get_upload_limit(self):
        return 999
    
class KidChannel(ChannelBase):
    def __init__(self, model):
        super().__init__(model)

    def calculate_visibility_score(self):
        return 5
    
    def get_upload_limit(self):
        return 2
    
