from .user import User
from abc import ABC,abstractmethod
class UserBase(ABC):
    def __init__(self,model):
        self.data=model
    @abstractmethod
    def has_admin_access(self):
        pass
    @abstractmethod
    def upload_video(self):
        pass
    @staticmethod
    def get_user_policy(user_role_string,user_model=None):
        role= user_role_string.capitalize()
        if role == "Admin":
            return AdminUser(user_model)
        if role == "Standard":
            return StandardUser(user_model)
        if role == "Guest":
            return GuestUser(user_model)
class AdminUser(UserBase):
    def __init__(self, model):
        super().__init__(model)
    def has_admin_access(self):
        return True
    def upload_video(self):
        return True
class StandardUser(UserBase):
    def __init__(self, model):
        super().__init__(model)
    def has_admin_access(self):
        return False
    def upload_video(self):
        return True
class GuestUser(UserBase):
    def __init__(self, model):
        super().__init__(model)
    def has_admin_access(self):
        return False
    def upload_video(self):
        return False