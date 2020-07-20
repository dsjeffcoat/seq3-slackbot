from flask import Flask, escape, request

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/goodbye')
def goodbye():
    name = request.args.get("name", "My Friend")
    return f'Goodbye, {escape(name)}!'

@app.route('/sunshine')
def sunshine():
    name = request.args.get("name", "My Friend")
    return f'It is Always Sunny, {escape(name)}!'