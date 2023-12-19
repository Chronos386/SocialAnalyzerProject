from datetime import datetime


class PostComment:
    def __init__(self, comment_json):
        self.text: str = comment_json["text"]
        self.id_comment: int = comment_json["id"]
        if "post_id" in comment_json:
            self.post_id: int = comment_json["post_id"]
        else:
            self.post_id: int = -1
        if "from_id" in comment_json:
            self.author_id: int = comment_json["from_id"]
        else:
            self.author_id: int = -1
        if "thread" in comment_json:
            self.thread_len: int = comment_json["thread"]["count"]
        else:
            self.thread_len: int = 0
        self.date: datetime = datetime.utcfromtimestamp(comment_json["date"])
