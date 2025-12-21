from models.accounts_module.user import User
from peewee import DoesNotExist
class UserRepository:
    #Kullanıcı Oluşturma
    def add_user(self,user_data):
        return User.create(**user_data)
    #Kullanıcı adına göre kullanıcı bulma
    def get_user_by_name(self,username):
        try:
            return User.get_or_none(User.username==username)
        except DoesNotExist:
            print("Böyle bir kullanıcı bulunamadı")
            return None
    #kullanıcı id sine göre kullanıcı bulma
    def get_user_by_id(self,user_id):
        return User.get_or_none(User.id==user_id)
    #Kullanıcı silme
    def delete_user(self,user_id):
        user=self.get_user_by_id(user_id)
        if user:
            user.delete_instance()#Kullanıcı varsa siler
            return True
        return False
    #kullanıcı verilerini güncelleme
    def update_user(self,user_id,updated_information):
        #kullanıcı bulma 
        query=User.update(**updated_information).where(User.id==user_id)
        changed_row_num=query.execute() #Tetikleme
        return changed_row_num    
    def get_all_users(self):
        return User.select()