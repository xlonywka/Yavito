from flask import *
from loginform import LoginForm
from signupform import SignUpForm
from add_news import AddNewsForm
from db_connect import *

db = DB()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found 404'}), 404)

#WORK WITH LOGIN AND LOGOUT-------------------------------------------------

@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(db.get_connection()).get_all()
    return render_template('index.html', username=session['username'],
                           news=news)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        user_model.init_table()
        exists = user_model.exists(user_name, password)
        if (not exists[0]):
            user_model.insert(user_name, password)
        return redirect("/index")
    return render_template('signup.html', title='Регистрация', form=form)    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        user_model.init_table()
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form)

   
@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('succes.html', title='Заработало')

@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/login')

#WORK WITH LOGIN AND LOGOUT-------------------------------------------------


#WORK WITH NEWS-------------------------------------------------------------
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        price = form.price.data
        place = form.place.data
        phonenumber = form.phonenumber.data
        nm = NewsModel(db.get_connection())
        nm.insert(session['user_id'], phonenumber, title, content, price, place)
        return redirect("/index")
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'])

@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news1(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/news',  methods=['GET'])
def get_news():
    news = NewsModel(db.get_connection()).get_all()
    return jsonify({'news': news})

@app.route('/news/<int:news_id>',  methods=['GET'])
def get_one_news(news_id):
    news = NewsModel(db.get_connection()).get(news_id)
    if not news:
        return jsonify({'error': 'Not found this news'})
    return jsonify({'news': news})

@app.route('/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['user_id', 'content', 'title', 'phonenumber', 'price', 'place']):
        return jsonify({'error': 'Bad request'})
    news = NewsModel(db.get_connection())
    news.insert(request.json['user_id'], request.json['content'],
                request.json['title'], request.json['phonenumber'], request.json['price'], request.json['place'])
    return jsonify({'success': 'OK'})

@app.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    news = NewsModel(db.get_connection())
    if not news.get(news_id):
        return jsonify({'error': 'Not found'})
    news.delete(news_id)
    return jsonify({'success': 'OK'})

#WORK WITH NEWS-------------------------------------------------------------


#OLD EXAMPLES---------------------------------------------------------------
@app.route('/news_old')
def news():
    with open("sp.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list)



@app.route('/odd')
def odd_even():
    return render_template('odd_even.html', number=255)


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return '''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport"
                            content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                            crossorigin="anonymous">
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Форма для регистрации в суперсекретной системе</h1>
                            <form method="post">
                                <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                <div class="form-group">
                                    <label for="classSelect">В каком вы классе</label>
                                    <select class="form-control" id="classSelect" name="class">
                                      <option>7</option>
                                      <option>8</option>
                                      <option>9</option>
                                      <option>10</option>
                                      <option>11</option>
                                    </select>
                                 </div>
                                <div class="form-group">
                                    <label for="about">Немного о себе</label>
                                    <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                </div>
                                <div class="form-group">
                                    <label for="photo">Приложите фотографию</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <div class="form-group">
                                    <label for="form-check">Укажите пол</label>
                                    <div class="form-check">
                                      <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                      <label class="form-check-label" for="male">
                                        Мужской
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                      <label class="form-check-label" for="female">
                                        Женский
                                      </label>
                                    </div>
                                </div>
                                <div class="form-group form-check">
                                    <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                    <label class="form-check-label" for="acceptRules">Готов быть добровольцем</label>
                                </div>
                                <button type="submit" class="btn btn-primary">Записаться</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        return "Форма отправлена"

#OLD EXAMPLES---------------------------------------------------------------

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

