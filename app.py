from flask import Flask, redirect, url_for, g
from neo4j import GraphDatabase
import config

app = Flask(__name__)
app.config.from_envvar()


######## 路由操作

@app.route('/')
def hello_world():
    return redirect(url_for('graph'))


@app.route('/graph', methods=['GET'])
def graph():
    return ''


@app.route('/graph/query', methods=['POST'])
def graph_query():
    return ''


@app.route('/user/sign', methods=['GET', 'POST', 'DELETE'])
def user_sign():
    return


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    return


######## 数据库操作

driver = GraphDatabase.driver(config.DATABASE_URL, auth=(config.DATABASE_USERNAME, config.DATABASE_PASSWORD))


def get_db(self):
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = self.driver.session()
    return g.neo4j_db


# 程序上下文销毁钩子
@app.teardown_appcontext
def close_db(self, error):
    if hasattr(g, 'neo4j_db'):
        print('db close')
        g.neo4j_db.close()



if __name__ == '__main__':
    app.run()
