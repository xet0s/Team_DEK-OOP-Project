from models.interaction_module.interaction_base import InteractionModel
from peewee import DoesNotExist

class InteractionRepository:
    def add_interaction(self,interaction_data):
        #Veritabanına yeni bir etkileşim satırı eklenir
        try:
              return InteractionModel.create(
                    user =interaction_data["user"],
                    video=interaction_data["video"],
                    interaction_type=interaction_data["interaction_type"],
                    content = interaction_data["content"],
                    status = interaction_data["status"]
              )
        except DoesNotExist:
              print(f"Hata !")
              return None
        
    #Kontrol -> kullanıcı daha önce videoya tepki vermiş mi
    def find_interaction(self,user_id,video_id,interaction_type):

        try:
                return InteractionModel.select().where(
                    (InteractionModel.user == user_id) &
                    (InteractionModel.video == video_id) &
                    (InteractionModel.interaction_type == interaction_type)
                ).get()
        except DoesNotExist:
                # Böyle bir kayıt yoksa (yani kullanıcı ilk defa basıyorsa)
                return None
    
    #Yorum Listeleme
    def get_comments_by_video(self, video_id): # Videoya ait yorumları listeleme
            """
            Sadece yorumları ve 'active' durumunda olanları getirir.
            Yeniden eskiye doğru sıralanır.
            """
            try:
                return (InteractionModel
                        .select()
                        .where(
                            (InteractionModel.video == video_id) &
                            (InteractionModel.interaction_type == InteractionModel.TYPE_COMMENT) &
                            (InteractionModel.status == 'active')
                        )
                        .order_by(InteractionModel.created_at.desc())) # En yeni en üstte
            except DoesNotExist:
                return []
            
    #Sayı Hesaplama (like,dislike)        
    def count_interactions(self, video_id, interaction_type): # Beğeni/Dislike sayısını hesaplama
            """
            Videonun kaç like veya dislike aldığını sayar.
            """
            return (InteractionModel
                    .select()
                    .where(
                        (InteractionModel.video == video_id) & 
                        (InteractionModel.interaction_type == interaction_type) &
                        (InteractionModel.status == 'active')
                    )
                    .count()) # Liste döndürmez sadece tam sayı döndürür

    # Id ile bulma
    def get_interaction_by_id(self, interaction_id): # ID'ye göre tek bir etkileşimi çekme
            try:
                return InteractionModel.get_by_id(interaction_id)
            except DoesNotExist:
                print("Böyle bir etkileşim bulunamadı")
                return None


    #  Durum güncelleme 
    def update_status(self, interaction, new_status): # Durum güncelleme (Örn: Silme işlemi için)
            """
            Var olan bir etkileşimin durumunu (active -> deleted) değiştirir.
            """
            if interaction:
                interaction.status = new_status
                interaction.save()
                return interaction
            return None
    
    def get_liked_videos_by_ids_by_user(self, user_id):
          query = InteractionModel.select().where(
                (InteractionModel.user == user_id) &
                (InteractionModel.interaction_type == "like") &
                (InteractionModel.status == "active")
          )

          return [i.video.id for i in query]
    
    def count_likes(self, video_id, type_filter="like"):
          return InteractionModel.select().where(
                (InteractionModel.video == video_id),
                (InteractionModel.interaction_type == type_filter),
                (InteractionModel.status == "active")
          ).count()