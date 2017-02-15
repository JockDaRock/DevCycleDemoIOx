from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('tourDeCisco1.html')


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8181)
