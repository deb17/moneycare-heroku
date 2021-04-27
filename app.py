from flask import Flask, redirect, request, abort

app = Flask(__name__)


@app.route('/')
def index():

    url = request.url.replace(
        'https://debs-moneycare.herokuapp.com',
        'https://moneycare.pythonanywhere.com/google/authorized'
    )

    if url == request.url:
        abort(400)

    return redirect(url)
