from .channel_base import ChannelModel
from abc import ABC, abstractmethod

class ChannelBase(ABC):

    
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
            return PersonalChannel()
        if channel_type_string=="Brand":
            return BrandChannel()
        if channel_type_string=="Kid":
            return KidChannel()
        return PersonalChannel()

class PersonalChannel(ChannelBase):

    def calculate_visibility_score(self):
        return 10
    
    def get_upload_limit(self):
        return 5
    
class BrandChannel(ChannelBase):

    def calculate_visibility_score(self):
        return 7
    
    def get_upload_limit(self):
        return 999
    
class KidChannel(ChannelBase):

    def calculate_visibility_score(self):
        return 5
    
    def get_upload_limit(self):
        return 2
    
