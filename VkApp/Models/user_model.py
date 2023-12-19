from typing import Optional


class UserModel:
    def __init__(self, user_json):
        self.id: int = user_json['id']
        self.first_name: str = user_json['first_name']
        self.last_name: str = user_json['last_name']
        if "photo_100" in user_json:
            self.photo: Optional[str] = user_json['photo_100']
        else:
            self.photo: Optional[str] = None
        self.count_comments: int = 0

    def set_count_comments(self, new_count: int):
        self.count_comments = new_count

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "photo": self.photo,
            "count_comments": self.count_comments
        }
