from VkApp.Models.post_model import PostModel
from VkApp.Models.user_model import UserModel


class PostsAnalizModel:
    def __init__(self, likes_photo: str, comments_photo: str, reposts_photo: str, popularity_photo: str,
                 popularity_by_day_photo: str, users: list[UserModel], top_likes: list[PostModel],
                 top_comments: list[PostModel], top_reposts: list[PostModel],
                 top_popularity_rating: list[PostModel], emotional_photos: list[str]):
        self.likes_photo: str = likes_photo
        self.comments_photo: str = comments_photo
        self.reposts_photo: str = reposts_photo
        self.popularity_photo: str = popularity_photo
        self.popularity_by_day_photo: str = popularity_by_day_photo
        self.users: list[UserModel] = users
        self.top_likes: list[PostModel] = top_likes
        self.top_comments: list[PostModel] = top_comments
        self.top_reposts: list[PostModel] = top_reposts
        self.top_popularity_rating: list[PostModel] = top_popularity_rating
        self.emotional_photos: list[str] = emotional_photos

    def to_dict(self):
        url = "http://192.168.0.114/api/pictures/"
        return {
            "likes_photo": f"{url}{self.likes_photo}",
            "comments_photo": f"{url}{self.comments_photo}",
            "reposts_photo": f"{url}{self.reposts_photo}",
            "popularity_photo": f"{url}{self.popularity_photo}",
            "popularity_by_day_photo": f"{url}{self.popularity_by_day_photo}",
            "users": [user.to_dict() for user in self.users],
            "top_likes": [post_comment.to_dict() for post_comment in self.top_likes],
            "top_comments": [post_comment.to_dict() for post_comment in self.top_comments],
            "top_reposts": [post_comment.to_dict() for post_comment in self.top_reposts],
            "top_popularity_rating": [post_comment.to_dict() for post_comment in self.top_popularity_rating],
            "emotional_photos": [f"{url}{photo}" for photo in self.emotional_photos]
        }
