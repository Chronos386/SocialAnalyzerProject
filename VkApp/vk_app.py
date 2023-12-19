import vk_api
from Utils.logger_file import logger
from VkApp.Models.post_model import PostModel
from VkApp.Models.user_model import UserModel
from VkApp.Models.post_comment import PostComment


class VkApp(object):
    def __init__(self):
        self.wall = []
        self.__vk = None
        self.__tools = None
        self.__app_id = 2685278
        self.__vk_session = None
        self.__photos_folder = "VkApi/files/"

    @staticmethod
    def __auth_handler():
        key = input("Введите код двухфакторной аутентификации: ")
        remember_device = True
        return key, remember_device

    def __auth(self, login, password):
        self.__vk_session = vk_api.VkApi(
            login, password,
            auth_handler=self.__auth_handler,
            app_id=self.__app_id
        )
        try:
            self.__vk_session.auth()
        except vk_api.AuthError as error_msg:
            logger.error(f'Error occurred: {str(error_msg)}', exc_info=True)
            return

    def __get_comments(self, group_id, post_id, count):
        comments = []
        try:
            comments_json = self.__vk.wall.getComments(owner_id=group_id, post_id=post_id, count=count, extended=1)
            iterator = 0
            for comment in comments_json['items']:
                old_iterator = iterator
                comments.append(PostComment(comment_json=comment))
                iterator += 1
                if comments[old_iterator].thread_len > 0:
                    thread_comments = self.__vk.wall.getComments(owner_id=group_id, post_id=post_id,
                                                                 comment_id=comments[old_iterator].id_comment,
                                                                 count=comments[old_iterator].thread_len, extended=1)
                    for thread_comment in thread_comments['items']:
                        comments.append(PostComment(comment_json=thread_comment))
                        iterator += 1
        except vk_api.VkApiError as error_msg:
            logger.error(f'Error occurred: {str(error_msg)}', exc_info=True)
            return
        return comments

    def start_app(self, login, password):
        self.__auth(login, password)
        self.__tools = vk_api.VkTools(self.__vk_session)
        self.__vk = self.__vk_session.get_api()

    def clear_self(self):
        self.wall = []
        self.__vk = None
        self.__tools = None
        self.__vk_session = None

    def download_some_numb_posts(self, group_id, count_posts=None):
        try:
            if count_posts is not None:
                max_count = count_posts / 25
                response = self.__tools.get_all(method='wall.get', max_count=max_count, values={'owner_id': group_id},
                                                limit=count_posts)
            else:
                response = self.__tools.get_all(method='wall.get', max_count=0, values={'owner_id': group_id})
            wall = response['items']
            iterator = 0
            summa = 0
            for post in wall:
                self.wall.append(PostModel(post_json=post))
                comments = self.__get_comments(group_id, self.wall[iterator].post_id,
                                               self.wall[iterator].count_comments)
                if comments is not None:
                    summa += len(comments)
                self.wall[iterator].add_comments(comments=comments)
                iterator += 1
            print('Posts count:', len(self.wall))
            print('Comments count:', summa)
        except vk_api.VkApiError as error_msg:
            logger.error(f'Error occurred: {str(error_msg)}', exc_info=True)
            return
        return self.wall

    def get_user(self, user_id):
        user_info = self.__vk.users.get(user_ids=str(user_id), fields='photo_100, city')
        user = UserModel(user_info[0])
        return user
