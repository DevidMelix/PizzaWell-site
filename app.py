from flask import Flask, render_template, url_for, request, redirect # (Flask-импорт класса) (render_template-импорт функции обрабатывающий html)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime                                                   # url_for- 
           
app = Flask(__name__)    # на основе класса Flask создаем обьект app, __name__ деректива передает название файла
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'

db = SQLAlchemy(app)



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id 



@app.route("/") # @ это декоратор - расширение функциональности класса, функции
@app.route("/home") # при записи этого url открывается тот же самый текст
def index():
    return render_template("index.html") # обращаем функции к файлу index.html


@app.route("/posts") 
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()

    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id>") 
def post_detail(id):
    article = Article.query.get(id)

    return render_template("post_detail.html", article=article)


@app.route("/posts/<int:id>/del") 
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"

    



@app.route("/about")     # при вводе в url строку /about нам будет выводится следующая функция
def about():
    return render_template("about.html")


@app.route("/posts/<int:id>/update", methods=['POST', 'GET'] )
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        
        

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании произошла ошибка"
    else:
        
        return render_template("post_update.html", article=article)






@app.route("/create-article", methods=['POST', 'GET'] )
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        
        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При произошла ошибка"
    else:
        return render_template("create-article.html")
    


@app.route("/user/<string:name>/<int:id>") # получаем данные пользователя с помощью <тип данных:название>       
def user(name,id):                         # эти параметры принимаем в функции user                         
    return "User page:" + name + str(id)        # return принимает строковые данные


if __name__ == "__main__": # условие при котором мы проверяем основной файл, при запуске вставляется __main__ и мы проверяем тот это файл или нет
    app.run(debug=True)    # .run() запускает локальный сервер, параметр debug-откладчик багов, ищет баги 




#def create_app():
#    app = Flask(__name__, static_folder='static', instance_relative_config=True)
#    app.config.from_pyfile('app_config.py')
#    return app
#app = create_app()
#db = SQLAlchemy(app)