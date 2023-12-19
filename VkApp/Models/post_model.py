from typing import Optional
from datetime import datetime
from VkApp.Models.post_comment import PostComment


class PostModel:
    def __init__(self, post_json):
        self.comments: list[PostComment] = []
        self.text: Optional[str] = post_json["text"]
        self.post_id: int = post_json["id"]
        self.count_views: int = post_json["views"]["count"]
        self.count_likes: int = post_json["likes"]["count"]
        self.count_reposts: int = post_json["reposts"]["count"]
        self.count_comments: int = post_json["comments"]["count"]
        self.count_attachments: int = len(post_json["attachments"])
        self.date: datetime = datetime.utcfromtimestamp(post_json["date"])

    def add_comments(self, comments):
        for comment in comments:
            self.comments.append(comment)

    def to_dict(self):
        return {
            "text": self.text if self.date else "",
            "post_id": self.post_id,
            "count_views": self.count_views,
            "count_likes": self.count_likes,
            "count_reposts": self.count_reposts,
            "count_comments": self.count_comments,
            "count_attachments": self.count_attachments,
            "date": self.date.timestamp() if self.date else None
        }
