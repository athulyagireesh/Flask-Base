from flask import Flask
app = Flask(__name__)
@app_route('/')
def home():
    return 'Welcome to flask'
if __name__="__main__":
    app.run(debug=True)