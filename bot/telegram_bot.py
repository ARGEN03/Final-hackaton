import telebot
from telebot import types
import requests
from io import BytesIO
from decouple import config

TOKEN = config('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
session = requests.Session()

def api_get(url):
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_movie_data():
    return api_get("http://34.125.237.140/api/movie/")

def get_genres():
    genres_data = api_get("http://34.125.237.140/api/genre/")
    return [genre['title'] for genre in genres_data] if genres_data else []

def get_movie_description(movie_id):
    movies = get_movie_data()
    if movies and 'results' in movies:
        for movie in movies['results']:
            if str(movie['id']) == str(movie_id):
                return movie
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('🎥 Смотреть фильмы'), types.KeyboardButton('📚 Жанры фильмов'))
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку 'Смотреть фильмы', чтобы получить все фильмы или нажмите кнопку 'Жанры фильмов' для выбора фильмов по жанру.", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["🎥 Смотреть фильмы", "📚 Жанры фильмов"])
def handle_user_request(message):
    if message.text == "🎥 Смотреть фильмы":
        show_movies(message)
    elif message.text == "📚 Жанры фильмов":
        show_genres(message)

def show_movies(message):
    movies = get_movie_data()
    if movies and 'results' in movies:
        for movie in movies['results']:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Подробнее", callback_data=f'desc_{movie["id"]}'))
            bot.send_message(message.chat.id, movie["title"], reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Извините, не могу получить данные о фильмах.")

def show_genres(message):
    genres = get_genres()
    if genres:
        markup = types.InlineKeyboardMarkup()
        for genre in genres:
            markup.add(types.InlineKeyboardButton(genre, callback_data=f'genre_{genre}'))
        bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Не удалось загрузить список жанров.")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data.startswith('desc_'):
        movie_id = call.data.split('_')[1]
        show_movie_details(call, movie_id)
    elif call.data.startswith('genre_'):
        genre_title = call.data.split('_')[1]
        show_movies_by_genre(call, genre_title)

def show_movie_details(call, movie_id):
    movie_info = get_movie_description(movie_id)
    if movie_info:
        info = f'Название: {movie_info["title"]}\n\nОписание: {movie_info["content"]}\n\n<a href="{movie_info["video"]}">Смотреть</a>'
        response = session.get(movie_info["image"])
        if response.status_code == 200:
            photo = BytesIO(response.content)
            bot.send_photo(call.message.chat.id, photo, caption=info, parse_mode='HTML')
        else:
            bot.send_message(call.message.chat.id, info, parse_mode='HTML')
    else:
        bot.send_message(call.message.chat.id, "Информация о фильме не найдена.")
    bot.answer_callback_query(call.id)

def show_movies_by_genre(call, genre_title):
    movies = get_movie_data()
    if movies and 'results' in movies:
        filtered_movies = [movie for movie in movies['results'] if movie['genre'].lower() == genre_title.lower()]
        if filtered_movies:
            for movie in filtered_movies:
                markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Подробнее", callback_data=f'desc_{movie["id"]}'))
                bot.send_message(call.message.chat.id, movie["title"], reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "Фильмы этого жанра не найдены.")
    else:
        bot.send_message(call.message.chat.id, "Не могу получить данные о фильмах.")
    bot.answer_callback_query(call.id)

bot.polling()
