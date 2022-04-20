from flask import Flask, redirect, url_for, g, request, jsonify
from neo4j import GraphDatabase
from flask_restful_swagger_2 import Api, Resource
from py2neo import Graph, Node, NodeMatcher, Subgraph, Relationship, RelationshipMatcher
from flask_sqlalchemy import SQLAlchemy
import jwt
from flask_login import LoginManager

import config

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 避免json中文乱码
app.config.from_object(config)
api = Api(app, title='Knowledge Graph')

# 图数据库
graph = Graph(config.DATABASE_URL, auth=(app.config['DATABASE_USERNAME'], app.config['DATABASE_PASSWORD']))
# 关系型数据库
db = SQLAlchemy(app)

INVITATION_CODE = 'abcd'


######## 用户鉴权


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 自增主键
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.String(20))

    def __init__(self, username, password, email, type, code):
        self.username = username
        self.password = password
        self.email = email
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.username


def token_decode(token, username):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        if payload['username'] == username:
            if payload['type'] == 'common':
                return 0
            elif payload['type'] == 'specialist' or payload['type'] == 'administrator':
                return 3
        return 1  # invalid token
    except jwt.ExpiredSignatureError:
        return 2  # expired signature
    except jwt.InvalidTokenError:
        return 1  # invalid token


def login_required(func):
    def wrapper(*args, **kwargs):
        request_data = request.get_json()
        jwt_answer = token_decode(request_data.get('token'), request_data.get('username'))
        if jwt_answer == 3:
            return func(*args, **kwargs)
        if jwt_answer == 0:
            return return_exception_code(501, 'Insufficient Permissions')
        return return_exception_code(500, "Token invalid!")

    return wrapper



######## 路由操作


class KnowledgeGraph(Resource):
    def get(self):
        GET_ALL_NODES = 'MATCH (n) RETURN n'
        GET_ALL_RELATIONS = 'MATCH()-[r]-() RETURN r'
        results1 = exec_cypher(GET_ALL_NODES, ['N'])
        results2 = exec_cypher(GET_ALL_RELATIONS, ['R'])
        node_names = set()
        relation_names = set()
        for item in results1['nodes']:
            node_names = node_names.union({item['label']})
        for item in results2['edges']:
            relation_names = relation_names.union({item['type']})
        json_dic = {
            "code": 200,
            "msg": {
                "node_name_list": list(node_names),
                "edge_name_list": list(relation_names),
                "nodes": results1['nodes'],
                "edges": results2['edges']
            }
        }
        # 自动将congtent-type改成application/json
        return jsonify(json_dic)

    def post(self):
        # TODO: 检验是否是查询语句
        request_data = request.get_json()
        cypher_statement = request_data.get('Cypher-Statement')
        return_type = request_data.get('Return-Type')
        print("get query: ", cypher_statement)
        result = exec_cypher(cypher_statement, return_type)
        print("return msg number: nodes-", len(result['nodes']), " edges-", len(result['edges']))
        json_dic = {
            "code": 200,
            "msg": result
        }
        return jsonify(json_dic)
        # print(json.dumps(result))
        # print(json.dumps(result).replace('\\', ''))
        # return json.dumps(result).replace('\\', '')
        # return json.loads(str(result).replace('\'', '\"'))


class NodeRoute(Resource):
    @login_required
    def post(self):
        request_data = request.get_json()
        node_label = request_data.get('Node-Type')
        node_attributes = request_data.get('Node-Attribute')

        new_node = Node()
        new_node.add_label(node_label)
        new_node.update(node_attributes)

        # 不考虑重复节点
        graph.create(new_node)

        return return_deleted_relationship(1)

    @login_required
    def put(self):
        request_data = request.get_json()
        node_attributes = request_data.get('Node-Attribute')
        node_id = int(request_data.get('Node-Id'))

        node_matcher = NodeMatcher(graph)
        try:
            changed_node = node_matcher[node_id]
        except KeyError:
            return return_exception_code(411, "Can't find node by this ID!")
        changed_node.clear()  # 清楚所有属性
        changed_node.update(node_attributes)

        tx = graph.begin()
        tx.push(changed_node)
        tx.commit()

        return return_deleted_relationship(1)

    @login_required
    def delete(self):
        request_data = request.get_json()
        node_id = int(request_data.get('Node-Id'))

        node_matcher = NodeMatcher(graph)
        try:
            deleted_node = node_matcher[node_id]
        except KeyError:
            return return_exception_code(411, "Can't find node by this ID")
        graph.delete(deleted_node)

        return return_deleted_relationship(1)


class RelationshipRoute(Resource):
    @login_required
    def post(self):
        request_data = request.get_json()
        relationship_type = request_data.get('Edge-Type')
        relationship_attribute = request_data.get('Edge-Attribute')
        relationship_source_node_ID = int(request_data.get('Source-Node'))
        relationship_target_node_ID = int(request_data.get('Target-Node'))

        node_matcher = NodeMatcher(graph)
        try:
            start_node = node_matcher[relationship_source_node_ID]
            end_node = node_matcher[relationship_target_node_ID]
        except KeyError:
            return return_exception_code(410, "Can't find relationship by this ID!")
        new_relationship = Relationship(start_node, relationship_type, end_node)
        new_relationship.update(relationship_attribute)

        # 相同类型的关系最多有两条相反的边，但可以有多条不同类型的边
        graph.create(new_relationship)

        return return_deleted_relationship(1)

    @login_required
    def put(self):
        request_data = request.get_json()
        relationship_ID = int(request_data.get('Edge-Id'))
        relationship_attribute = request_data.get('Edge-Attribute')

        relationship_matcher = RelationshipMatcher(graph)
        try:
            changed_relationship = relationship_matcher[relationship_ID]
        except KeyError:
            return return_exception_code(410, "Can't find relationship by this ID!")
        changed_relationship.clear()
        changed_relationship.update(relationship_attribute)

        tx = graph.begin()
        tx.push(changed_relationship)
        tx.commit()

        return return_deleted_relationship(1)

    @login_required
    def delete(self):
        request_data = request.get_json()
        relationship_ID = int(request_data.get('Edge-Id'))

        relationship_matcher = RelationshipMatcher(graph)
        try:
            deleted_relationship = relationship_matcher[relationship_ID]
        except KeyError as e:
            return return_exception_code(410, "Can't find relationship by this ID!")

        graph.separate(deleted_relationship)

        return return_deleted_relationship(1)


# 注册
class User(Resource):

    def post(self):
        request_data = request.get_json()

        if UserModel.query.filter_by(username=request_data.get('username')).first():
            return return_exception_code(401, 'Duplicate Username!')
        elif request_data.get('type') != 'common' and request_data.get('code') != INVITATION_CODE:
            return return_exception_code(404, "Invalid Invitation Code!")
        elif UserModel.query.filter_by(email=request_data.get('email')).first():
            return return_exception_code(402, "Repeat email!")
        else:
            db.session.add(UserModel(**request_data))
            db.session.commit()
            return return_exception_code(200, 'Registration Completed!')


# 登录
class Session(Resource):

    def post(self):
        def token_encode(payload: dict):
            # header和payload可以直接利用base64解码出原文，从header中获取哈希签名的算法，从payload中获取有效数据
            # signature由于使用了不可逆的加密算法，无法解码出原文，它的作用是校验token有没有被篡改。
            return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

        request_data = request.get_json()
        user = UserModel.query.filter_by(username=request_data.get('username'),
                                         password=request_data.get('password')).first()
        if user:
            token = token_encode({'username': user.username, 'type': user.type})
            return return_msg_with_token(200, 'Validation Completed', token=token)
        return return_exception_code(401, "Validation fails")


######## 数据库操作


def exec_cypher(cypher_statement: str, return_type: list) -> dict:
    cursor = graph.run(cypher_statement)
    node_list = []
    edge_list = []
    # 取出节点对象和关系对象
    for record in cursor:
        for i, type in enumerate(return_type):
            if type == "N":
                node_list.append(record[i])
            if type == "R":
                edge_list.append(record[i])
    edge_list = list(set(edge_list))
    node_list = list(set(node_list))
    # 格式化节点和关系，以字典的列表存储
    nodes = list(map(serialize_node, node_list))
    edges = list(map(serialize_edge, edge_list))
    # 使节点和关系不重复
    node_id = []
    edge_id = []
    nodes_single = []
    edges_single = []
    for node in nodes:
        if node['<id>'] not in node_id:
            node_id.append(node['<id>'])
            nodes_single.append(node)
    for edge in edges:
        if edge['<id>'] not in edge_id:
            edge_id.append(edge['<id>'])
            edges_single.append(edge)
    return {"nodes": nodes_single, "edges": edges_single}


def serialize_node(node):
    data = {
        "<id>": node.identity,
        "label": list(node.labels)[0],
        "attribute": dict(node)
    }
    return data


def serialize_edge(edge):
    # 关系属性值使用列表存储的，只取第一个值
    attribute = {}
    for key, value in dict(edge).items():
        if isinstance(value, list):
            attribute[key] = value[0]
        else:
            attribute[key] = value
    data = {
        "<id>": edge.identity,
        "source": edge.start_node.identity,
        "target": edge.end_node.identity,
        "type": type(edge).__name__,
        "attribute": attribute
    }
    return data




####### 返回格式化

def return_deleted_relationship(number: int):
    return jsonify({
        "code": 200,
        "msg": {
            "number": number
        }
    })


def return_exception_code(code: int, msg: str):
    return jsonify({
        "code": code,
        "msg": msg
    })


def return_msg_with_token(code: int, msg: str, token: str = None):
    return jsonify({
        "code": code,
        "msg": msg,
        "token": token
    })


#
# driver = GraphDatabase.driver(config.DATABASE_URL, auth=(config.DATABASE_USERNAME, config.DATABASE_PASSWORD))
#
#
# def get_db():
#     if not hasattr(g, 'neo4j_db'):
#         g.neo4j_db = driver.session()
#     return g.neo4j_db
#
#
# # 程序上下文销毁钩子,但实际上每次请求结束都会被调用
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'neo4j_db'):
#         print('--db close--')
#         g.neo4j_db.close()
#
#
# # 执行Cypher指令
# def exec_read(cypher_statement: str):
#     db = get_db()
#
#     def run_tx(tx):
#         return tx.run(cypher_statement)
#
#     return db.read_transaction(run_tx)
#
#
# def exec_write(cypher_statement: str):
#     db = get_db()


######## 注册api
api.add_resource(KnowledgeGraph, '/graph', '/')
api.add_resource(User, '/user')
api.add_resource(Session, '/session')
api.add_resource(NodeRoute, '/graph/node')
api.add_resource(RelationshipRoute, '/graph/edge')

if __name__ == '__main__':
    app.run()
