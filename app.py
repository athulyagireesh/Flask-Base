# from flask import Flask,render_template
# app = Flask(__name__)
# @app.route('/')
# def home():
#     return render_template ("index.html")
# if __name__=="__main__":
#     app.run(debug=True)



from flask import Flask , render_template , request , redirect , url_for,g
from flask_mail import Mail , Message
import sqlite3

app = Flask(__name__)
DATABASE ="database.db"

app.secret_key = "secretkey"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'athulyatg721@gmail.com'
app.config['MAIL_PASSWORD'] = 'cdox iter gufe febc'
app.config['MAIL_DEFAULT_SENDER'] = 'athulyatg721@gmail.com'

mail=Mail(app)



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db=g.pop('db',None)
    if db is not None:
        db.close()

def create_table():
    db=get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users(email TEXT NOT NULL)")
    db.commit()


@app.before_request
def before_request():
    create_table()


@app.route('/',methods =["GET","POST"])
def send_mail():
    if request.method == 'POST':
        recipient = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        db=get_db()
        db.execute("INSERT INTO users(email) VALUES(?)",(recipient,))
        db.commit()
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=message
        )

        mail.send(msg)
        return redirect(url_for("send_mail"))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

