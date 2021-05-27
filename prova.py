from flask import Flask, send_file

app = Flask( __name__)

@app.route('/')
def hello():
    return "Hello world"

@app.route('/flaskFiles/<path>')
def hello2(path):
    return send_file(path, as_attachment = True)

if __name__ == '__main__':
    app.run()
