from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('graph'))


@app.route('/graph', methods=['GET'])
def graph():
    return


@app.route('/graph/query', methods=['POST'])
def graph_query():
    return


@app.route('/user/sign', methods=['GET', 'POST', 'DELETE'])
def user_sign():
    return


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    return


if __name__ == '__main__':
    app.run()
