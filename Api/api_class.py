import os
import json
import schedule
from waitress import serve
from flask_cors import CORS
from flask_restful import Api
from VkApp.vk_app import VkApp
from Utils.logger_file import logger
from Analyzer.analyzer import Analyzer
from flask import Flask, request, send_file, Response
from Analyzer.models.posts_analiz_model import PostsAnalizModel


class ApiClass(object):
    def __init__(self, folder_path):
        self.__app = Flask(__name__)
        self.__app.secret_key = 'social key'
        self.__app.config['SESSION_TYPE'] = 'filesystem'
        self.__app.config['MAX_CONTENT_LENGTH'] = 20 * 1000 * 1000
        self.__app.config['UPLOAD_FOLDER'] = folder_path
        self.__folder_path = folder_path
        self.__api = Api()
        CORS(self.__app)
        self.__ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        self.__vk = VkApp()
        self.__analyzer = Analyzer()
        schedule.every(24).hours.do(self.__clear_folder)

    def __clear_folder(self):
        for filename in os.listdir(self.__folder_path):
            file_path = os.path.join(self.__folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.error(f"Error while deleting file {file_path}: {e}")

    def run(self):
        self.__api.init_app(app=self.__app)
        self.__add_routes()
        serve(self.__app, host="192.168.0.114", port=80)

    # Функция проверки расширения файла
    def __allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.__ALLOWED_EXTENSIONS

    def __get_top_users(self, commentators):
        new_users = []
        iterator = 0
        for top_commentator in commentators:
            new_users.append(self.__vk.get_user(top_commentator[0]))
            new_users[iterator].set_count_comments(top_commentator[1])
            iterator += 1
        return new_users

    def __create_analiz(self):
        # Сохранение графика лайков
        likes_photo = self.__analyzer.plot_likes()
        # Сохранение графика комментариев
        comments_photo = self.__analyzer.plot_comments()
        # Сохранение графика репостов
        reposts_photo = self.__analyzer.plot_reposts()
        # Сохранение графика популярности
        popularity_photo = self.__analyzer.plot_popularity()
        # Сохранение графика популярности по дням
        popularity_by_day_photo = self.__analyzer.plot_popularity_by_day()
        # Топ комментаторы
        top_commentators = self.__analyzer.get_top_commentators()
        users = self.__get_top_users(commentators=top_commentators)
        # Получение топ постов по лайкам, комментариям, репостам, и общей попуряности
        top_likes, top_comments, top_reposts, top_popularity_rating = self.__analyzer.get_top_posts()
        # Получение статистики эмоциональности комментариев топовых постов
        iterator = 1
        emotional_photos = []
        for top in top_popularity_rating:
            if top.count_comments != 0:
                emotional_photo = self.__analyzer.get_emotional_statistic_post(top, iterator)
                emotional_photos.append(emotional_photo)
            iterator += 1
        my_analiz = PostsAnalizModel(likes_photo=likes_photo, comments_photo=comments_photo,
                                     reposts_photo=reposts_photo, popularity_photo=popularity_photo,
                                     popularity_by_day_photo=popularity_by_day_photo, users=users, top_likes=top_likes,
                                     top_comments=top_comments, top_reposts=top_reposts,
                                     top_popularity_rating=top_popularity_rating, emotional_photos=emotional_photos)
        return my_analiz.to_dict()

    def __preparation_for_analysis(self, group_id, count_posts, login, password):
        self.__vk.start_app(login, password)
        posts = self.__vk.download_some_numb_posts(group_id=group_id, count_posts=count_posts)
        self.__analyzer.init_self(posts=posts)
        data = self.__create_analiz()

        self.__vk.clear_self()
        self.__analyzer.clear_self()
        return data

    def __add_routes(self):
        @self.__app.route('/api/pictures/<string:pict_name>/', methods=['GET'])
        def load_pict(pict_name: str):
            filename = f"{self.__folder_path}\\{pict_name}"
            parts = pict_name.split(".")
            return send_file(filename, mimetype=f'image/{parts[1]}')

        @self.__app.route('/api/analysis/', methods=['POST'])
        def process_data():
            if request.method == 'POST':
                try:
                    group_id = request.form['group_id']
                    count_posts = request.form['count_posts']
                    login = request.form['login']
                    password = request.form['password']
                    data = self.__preparation_for_analysis(group_id=int(group_id), count_posts=int(count_posts),
                                                           login=login, password=password)
                    json_data = json.dumps(data)
                    return Response(json_data, mimetype='application/json')
                except KeyError:
                    return {}, 400
            else:
                return {}, 400
