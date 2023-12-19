import matplotlib
import numpy as np
from datetime import datetime
from googletrans import Translator
from matplotlib import pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
matplotlib.use('Agg')


class Analyzer(object):
    def __init__(self):
        # Посты
        self.__posts = []
        # Лайки
        self.__post_likes = []
        # Комментарии
        self.__post_comments = []
        # Репосты
        self.__post_reposts = []
        # Популярность
        self.__post_popularity_rating = []
        # Номера постов
        self.__post_numbers = []

        self.__post_likes_ = []
        self.__post_comments_ = []
        self.__post_reposts_ = []
        self.__post_popularity_rating_ = []

        # Популярность постов по дням
        self.__days = []
        self.__day_likes = []
        self.__day_comments = []
        self.__day_reposts = []

        # Соотношение постов и количества комментариев
        self.__user_comments = {}

        # Переводчик и анализатор настроения
        self.__translator = Translator()
        self.__sia = SentimentIntensityAnalyzer()

    def init_self(self, posts):
        self.__posts = posts
        iterator = 0
        self.__post_numbers = list(range(1, len(posts) + 1))
        for post in posts:
            self.__post_likes.append(post.count_likes)
            self.__post_comments.append(post.count_comments)
            self.__post_reposts.append(post.count_reposts)
            self.__post_popularity_rating.append(post.count_likes + (post.count_comments * 1.5) +
                                                 (post.count_reposts * 2))

            self.__post_likes_.append([post.count_likes, iterator])
            self.__post_comments_.append([post.count_comments, iterator])
            self.__post_reposts_.append([post.count_reposts, iterator])
            self.__post_popularity_rating_.append([post.count_likes + (post.count_comments * 1.5) +
                                                   (post.count_reposts * 2), iterator])
            iterator += 1

            day = post.date.day
            month = post.date.month
            year = post.date.year
            day_identifier = datetime(year, month, day)
            if day_identifier not in self.__days:
                self.__days.append(day_identifier)
                self.__day_likes.append(0)
                self.__day_comments.append(0)
                self.__day_reposts.append(0)
            self.__day_likes[self.__days.index(day_identifier)] += post.count_likes
            self.__day_comments[self.__days.index(day_identifier)] += post.count_comments
            self.__day_reposts[self.__days.index(day_identifier)] += post.count_reposts

            for comment in post.comments:
                user_id = comment.author_id
                if user_id in self.__user_comments:
                    self.__user_comments[user_id] += 1
                else:
                    self.__user_comments[user_id] = 1

    def clear_self(self):
        self.__posts = []
        self.__post_likes = []
        self.__post_comments = []
        self.__post_reposts = []
        self.__post_popularity_rating = []
        self.__post_numbers = []
        self.__post_likes_ = []
        self.__post_comments_ = []
        self.__post_reposts_ = []
        self.__post_popularity_rating_ = []
        self.__days = []
        self.__day_likes = []
        self.__day_comments = []
        self.__day_reposts = []
        self.__user_comments = {}
        self.__translator = Translator()
        self.__sia = SentimentIntensityAnalyzer()

    def plot_likes(self):
        plt.plot(self.__post_numbers, self.__post_likes, marker='o', linestyle='-', color='red', label='Лайки')
        plt.xlabel('Номер поста')
        plt.ylabel('Количество')
        plt.title('График популярности постов (в лайках)')
        plt.legend()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f'Analyzer/files/{formatted_datetime}_likes.png')
        plt.clf()
        return f"{formatted_datetime}_likes.png"

    def plot_comments(self):
        plt.plot(self.__post_numbers, self.__post_comments, marker='o', linestyle='-', color='blue',
                 label='Комментарии')
        plt.xlabel('Номер поста')
        plt.ylabel('Количество')
        plt.title('График популярности постов (в комментариях)')
        plt.legend()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f'Analyzer/files/{formatted_datetime}_comments.png')
        plt.clf()
        return f"{formatted_datetime}_comments.png"

    def plot_reposts(self):
        plt.plot(self.__post_numbers, self.__post_reposts, marker='o', linestyle='-', color='green',
                 label='Репосты')
        plt.xlabel('Номер поста')
        plt.ylabel('Количество')
        plt.title('График популярности постов (в репостах)')
        plt.legend()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f'Analyzer/files/{formatted_datetime}_reposts.png')
        plt.clf()
        return f"{formatted_datetime}_reposts.png"

    def plot_popularity(self):
        plt.plot(self.__post_numbers, self.__post_popularity_rating, marker='o', linestyle='-', color='purple',
                 label='Рейтинг популярности')
        plt.xlabel('Номер поста')
        plt.ylabel('Количество')
        plt.title('График популярности постов')
        plt.legend()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f'Analyzer/files/{formatted_datetime}_popularity.png')
        plt.clf()
        return f"{formatted_datetime}_popularity.png"

    def plot_popularity_by_day(self):
        bar_width = 0.2
        bar_positions = np.arange(len(self.__days))
        plt.bar(bar_positions - bar_width, self.__day_likes, width=bar_width, label='Лайки')
        plt.bar(bar_positions, self.__day_comments, width=bar_width, label='Комментарии')
        plt.bar(bar_positions + bar_width, self.__day_reposts, width=bar_width, label='Репосты')
        plt.ylabel('Количество')
        plt.title('Активность сообщества по дням')
        plt.xticks(bar_positions, [date.strftime('%d.%m') for date in self.__days], rotation=90, fontsize='small')
        plt.legend()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f'Analyzer/files/{formatted_datetime}_activity_by_day.png')
        plt.clf()
        return f"{formatted_datetime}_activity_by_day.png"

    def get_top_posts(self):
        post_likes = sorted(self.__post_likes_, key=lambda x: x[0], reverse=True)
        post_comments = sorted(self.__post_comments_, key=lambda x: x[0], reverse=True)
        post_reposts = sorted(self.__post_reposts_, key=lambda x: x[0], reverse=True)
        post_popularity_rating = sorted(self.__post_popularity_rating_, key=lambda x: x[0], reverse=True)
        top_likes = []
        top_comments = []
        top_reposts = []
        top_popularity_rating = []
        if len(post_likes) >= 3:
            for i in range(3):
                top_likes.append(self.__posts[post_likes[i][1]])
                top_comments.append(self.__posts[post_comments[i][1]])
                top_reposts.append(self.__posts[post_reposts[i][1]])
                top_popularity_rating.append(self.__posts[post_popularity_rating[i][1]])
        else:
            for i in range(len(post_likes)):
                top_likes.append(self.__posts[post_likes[i][1]])
                top_comments.append(self.__posts[post_comments[i][1]])
                top_reposts.append(self.__posts[post_reposts[i][1]])
                top_popularity_rating.append(self.__posts[post_popularity_rating[i][1]])
        return top_likes, top_comments, top_reposts, top_popularity_rating

    def get_top_commentators(self):
        filtered_commentators = filter(lambda x: x[0] >= 0, self.__user_comments.items())
        sorted_commentators = sorted(filtered_commentators, key=lambda x: x[1], reverse=True)
        top_commentators = sorted_commentators[:5]
        return top_commentators

    def get_emotional_statistic_post(self, post, numb):
        count_pos = 0
        count_neg = 0
        count_neutral = 0
        for comment in post.comments:
            text_ru = comment.text
            if text_ru != "":
                translation = self.__translator.translate(text_ru, src='ru', dest='en')
                text_en = translation.text
                polarity = self.__sia.polarity_scores(text_en)
                if polarity['neu'] == 1:
                    count_neutral += 1
                else:
                    if polarity['pos'] > polarity['neg']:
                        count_pos += 1
                    else:
                        count_neg += 1
            else:
                count_neutral += 1
        labels = ['Положительные', 'Отрицательные', 'Нейтральные']
        sizes = [count_pos, count_neg, count_neutral]
        colors = ['green', 'red', 'gray']
        explode = (0.1, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title(f'Анализ тональности комментариев топового поста №{numb}')
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        plt.savefig(f'Analyzer/files/{formatted_datetime}_comments_analiz_{numb}.png')
        plt.clf()
        return f"{formatted_datetime}_comments_analiz_{numb}.png"
