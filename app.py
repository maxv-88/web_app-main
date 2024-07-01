from flask import Flask, request, render_template
import sqlite3
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    rating = FloatField('rating', validators=[DataRequired()])
    year = IntegerField('year', validators=[DataRequired()])
    genre = StringField('genre', validators=[DataRequired()])


# Инициализация Flask приложения
app = Flask(__name__)

# Создание соединения с базой данных
con = sqlite3.connect('films.db', check_same_thread=False)
# Создание курсора для выполнения SQL запросов
cur = con.cursor()

# Маршрут для корневой страницы
@app.route("/")
def hello_world():
    # Возвращение приветственного сообщения
    return render_template('main.html')

# Маршрут для получения информации о фильме по ID
@app.route("/film/<id>")
def film(id):
    # Выполнение SQL запроса для получения данных о фильме по ID
    res = cur.execute(f"select * from Movies where id = ?", (id,))
    # Получение результата запроса
    film = res.fetchone()
    print(film)
    # Проверка, найден ли фильм
    if film != None:
        # Возвращение результата
        return render_template('film.html', film = film )
    else:
        # Сообщение о том, что фильма не существует   
        return "Такого фильма нет"

@app.route("/films")
def films():
    return render_template('films.html')

#Страница с таблицей фильмов
@app.route("/film_table")
def tablica():
    res = cur.execute("select * from Movies")
    films = res.fetchall()
    print(films)
    return render_template('film_table.html', films = films)


# Страница с формой для добавления нового фильма
@app.route("/film_form", methods=['GET', 'POST'])
def film_form():
    form = MyForm()
    if form.validate_on_submit():
        return 'Форма отправлена на сервер'
    return render_template('form.html', form=form)

# Пример из документации https://pythonru.com/uroki/11-rabota-s-formami-vo-flask
# Передеалать для сохранения данных введеных в форму добавления фильмов
'''
from flask import Flask, render_template, request, redirect,  url_for
from flask_script import Manager, Command, Shell
from forms import ContactForm
#...
@app.route('/contact/', methods=['get', 'post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
	name = form.name.data
	email = form.email.data
	message = form.message.data
	print(name)
	print(email)
	print(message)
	# здесь логика базы данных
	print("\nData received. Now redirecting ...")
	return redirect(url_for('contact'))

    return render_template('contact.html', form=form)
'''

# Маршрут для добавления нового фильма
@app.route("/film_add")
def film_add():
    # Получение данных о фильме из параметров запроса
    name = request.args.get('name')
    genre = request.args.get('genre')
    year = request.args.get('year')
    rating = request.args.get('rating')
    # Формирование кортежа с данными о фильме
    film_data = (name, genre, year, rating)
    # Выполнение SQL запроса для добавления фильма в базу данных
    cur.execute('INSERT INTO Movies (name, genre, year, rating) VALUES (?, ?, ?, ?)', film_data)
    # Сохранение изменений в базе данных
    con.commit()
    # Возвращение подтверждения о добавлении фильма
    return "name = {};genre = {}; year = {}; rating = {} ".format(name, genre, year, rating) 

# Запуск приложения, если оно выполняется как главный модуль
if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False  # Отключаем проверку CSRF для WTForms
    app.run(debug=True)
