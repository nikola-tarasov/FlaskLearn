from flask import Flask, abort, make_response, redirect,render_template, url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user
from flask_httpauth import HTTPBasicAuth



menu = [{"name":"Главное", "url": 'main'},
        {"name":"О нас", "url": 'about'},
        {"name":"контакты", "url": 'contact'},
        {"name":"Статьи", "url": 'artiqul'}]

title = 'Главная'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hghghghghghg6545gggrrsk'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(username, password):
    if username == 'user' and password == '1234':
            
        return username


@app.route("/")
@auth.login_required
def index():
    
        return render_template('index.html', menu = menu)


@auth.get_user_roles
def get_user_roles(user):
    user = 'admin'
    return user

@app.route('/admin')
@auth.login_required(role='admin')
def admins_only():
    return "Hello {}, you are an admin!".format(auth.current_user())






@app.route("/contact", methods=["POST","GET"])
def contact():
        if request.method == 'POST':
                # print(request.form['fist-name'])
                if len(request.form['first-name']) > 3:
                        flash("сообщение отправлено")
                else:
                        flash("Ошибка! Проверьте правильность ввода! ")


       
        return render_template('contact.html', title = title, menu = menu)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text(10000), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.Integer, nullable=False)
    

with app.app_context():
    db.create_all()

@app.route("/artiqul", methods=["POST","GET"])
def artiqul():
        if request.method == 'POST':
                title=request.form["title"]
                text=request.form["text"]
                post = Post(title=title, text=text)
                try:
                        db.session.add(post)
                        db.session.commit()
                except:
                       redirect(url_for('artiqul'))
                return redirect(url_for('succsess'))
                
        if request.method == 'GET':
                        posts = Post.query.all()
                        
                        return render_template('artiqul.html', menu = menu, post=posts)

@app.route("/succsess'")
def succsess():
    return render_template('succsess.html', menu = menu)




@app.route("/register", methods=["POST","GET"])
def register():
        if request.method == 'POST':
                
                if len(request.form['login']) > 3 and len(request.form['password']) > 3 and request.form['password'] == request.form['re_password']:
                        login=request.form["login"]
                        password=request.form["password"]
                        register = User(login=login, password=password)
                        db.session.add(register)
                        db.session.commit()
        
                        flash("Вы зарегестрированы")
                else:
                        flash("Ошибка! Проверьте правильность ввода! ")
        return render_template('register.html', title = title, menu = menu)

                
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route("/login", methods=["POST","GET"])
def login():
        user = User.query.get(login='Андрей')
        
        if request.method == 'POST':
               login_user(user)
               return render_template ('test.html')
        return render_template('login.html')


@app.route("/test")
@login_required
def settings():
    return render_template('test.html')
               
               
               






                
                
                
              













