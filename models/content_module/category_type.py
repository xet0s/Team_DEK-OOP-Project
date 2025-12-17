from abc import ABC, abstractmethod

class CategoryBase(ABC):
    def __init__(self, category_name):
        self.name = category_name

    @abstractmethod
    def get_suggested_tags(self):
        pass

    @abstractmethod
    def get_category_description(self):
        pass
class GamingCategory(CategoryBase):
    def __init__(self):
        super().__init__("Gaming")

    def get_suggested_tags(self):
        return "#game #play #fun #esports"
    
    def get_category_description(self):
        return "Oyun videoları, oyun incelemeleri, oyun rehberleri ve canlı yayınlar."

class EducationCategory(CategoryBase):
    def __init__(self):
        super().__init__("Education")
    
    def get_suggested_tags(self):
        return "#learn #tutorial #howto #class"
    
    def get_category_description(self):
        return "Eğitim videoları, dersler, öğreticiler ve bilgilendirici içerikler."

class MusicCategory(CategoryBase):
    def __init__(self):
        super().__init__("Music")
    
    def get_suggested_tags(self):
        return "#song #listen #melody #sound"
    
    def get_category_description(self):
        return "Müzik videoları, klipler, canlı performanslar ve müzikle ilgili içerikler."

class GeneralCategory(CategoryBase):
    def __init__(self):
        super().__init__("General")
    
    def get_suggested_tags(self):
        return "#daily #vlog #video"
    
    def get_category_description(self):
        return "Genel içerikler, vloglar, günlük yaşam ve çeşitli videolar."
    
def get_category_policy(category_input):
    if category_input == "Gaming":
        return GamingCategory()
    elif category_input == "Education":
        return EducationCategory()
    elif category_input == "Music":
        return MusicCategory()
    else:
        return GeneralCategory()