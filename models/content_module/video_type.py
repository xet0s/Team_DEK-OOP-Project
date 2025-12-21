from .video_base import VideoModel
from abc import ABC, abstractmethod
import random

class VideoBase(ABC):
    def __init__(self, model):
        self.data = model

    #calculate_listing_score --> Videonun listeleme puanı
    @abstractmethod
    def calculate_listing_score(self):
        pass
    
    #get_processing_time_estimate --> Videonun işlenme süresi tahmini
    @abstractmethod
    def get_processing_time_estimate(self):
        pass


class StandardVideo(VideoBase):
    def __init__(self, model):
        super().__init__(model)

    def calculate_listing_score(self):
        base_score = 50
        duration_bonus = min(self.data.duration // 60, 20)  
        base_score += duration_bonus            # Videonun süresine göre listeleme puanı bonusu
        return base_score   

    def get_processing_time_estimate(self):
        return self.data.duration * 0.5 # İşlenme süresi tahmini (saniye cinsinden)


class ShortVideo(VideoBase):
    def __init__(self, model):
        super().__init__(model)

    def calculate_listing_score(self):
        return random.randint(70, 100)          # Kısa videolar anlık tüketildiği için rastgele yüksek listeleme puanı

    def get_processing_time_estimate(self):
        return 15                               # Kısa videolar için sabit işlenme süresi


class LiveStreamVideo(VideoBase):
    def __init__(self, model):
        super().__init__(model)

    def calculate_listing_score(self):
        if self.data.status == 'published':
            return 40                           # Yayınlanan canlı yayınlar için düşük listeleme puanı
        return 99                               # Güncel canlı yayınlar için yüksek listeleme puanı

    def get_processing_time_estimate(self):
        return 0                                # Canlı yayınlar anlık işlendiği için işlenme süresi yok

def get_video_logic(model):                     # Veritabanından çekilen modele göre doğru video tipini döndüren fabrika fonksiyonu
    if model.video_type_id == 'short':
        return ShortVideo(model)
    elif model.video_type_id == 'live':
        return LiveStreamVideo(model)
    else:
        return StandardVideo(model)