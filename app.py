from flask import Flask, redirect, url_for, g, request, jsonify
from neo4j import GraphDatabase
from flask_restful_swagger_2 import Api, Resource
from py2neo import Graph, Node, NodeMatcher, Subgraph

import config

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 避免json中文乱码
api = Api(app, title='Knowledge Graph')

graph = Graph(config.DATABASE_URL, auth=(config.DATABASE_USERNAME, config.DATABASE_PASSWORD))


######## 路由操作

@app.route('/')
def hello_world():
    return redirect(url_for('graph'))


class KnowledgeGraph(Resource):
    def get(self):
        GET_ALL_NODES = 'MATCH (n) RETURN labels(n)'
        GET_ALL_RELATIONS = 'MATCH(n)-[r]-(m) RETURN type(r)'
        results1 = graph.run(GET_ALL_NODES)
        results2 = graph.run(GET_ALL_RELATIONS)
        node_names = set()
        relation_names = set()
        for item in results1.data():
            node_names = node_names.union(set(item['labels(n)']))
        for item in results2.data():
            relation_names = relation_names.union({item['type(r)']})
        json_dic = {
            "code": 200,
            "msg": {
                "nodes": list(node_names),
                "edges": list(relation_names)
            }
        }
        # 自动将congtent-type改成application/json
        return jsonify(json_dic)

    def post(self):
        # TODO: 检验是否是查询语句
        request_data = request.get_json()
        cypher_sentiment = request_data.get('Cypher-Sentiment')
        return_type = request_data.get('Return-Type')
        result = exec_cypher(cypher_sentiment, return_type)
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
    def post(self):
        request_data = request.get_json()
        node_label = request_data.get('Node-Type')
        node_attributes = request_data.get('Node-Attribute')

        new_node = Node()
        new_node.add_label(node_label)
        new_node.update(node_attributes)

        # 不考虑重复节点
        graph.create(new_node)
        graph.commit(graph.begin())

        return jsonify({
            "code": 200,
            "msg": {
                "number": 1
            }
        })

    def put(self):
        request_data = request.get_json()
        node_attributes = request_data.get('Node-Attribute')
        node_id = request_data.get('Node-Id')

        node_matcher = NodeMatcher(graph)
        changed_node = node_matcher[node_id]
        changed_node.clear()  # 清楚所有属性
        changed_node.update(node_attributes)

        tx = graph.begin()
        tx.push(changed_node)
        tx.commit()

        return jsonify({
            "code": 200,
            "msg": {
                "number": 1
            }
        })

    def delete(self):
        request_data = request.get_json()
        node_id = request_data.get('Node-Id')

        node_macher = NodeMatcher(graph)
        deleted_node = node_macher[node_id]

        graph.delete(deleted_node)

        return jsonify({
            "code": 200,
            "msg": {
                "number": 1
            }
        })


class User(Resource):
    def get(self):
        return ''

    def post(self):
        return ''

    def delete(self):
        return ''


class Register(Resource):
    def get(self):
        return ''

    def post(self):
        return ''


class Test(Resource):
    def get(self):
        return test()


######## 数据库操作


def exec_cypher(cypher_sentiment: str, return_type: list) -> dict:
    cursor = graph.run(cypher_sentiment)
    node_list = []
    edge_list = []
    # 取出节点对象和关系对象
    for record in cursor:
        for i, type in enumerate(return_type):
            if type == "N":
                node_list.append(record[i])
            if type == "R":
                edge_list.append(record[i])

        node_list = list(set(node_list))
    # 格式化节点和对象，以字典的列表存储
    nodes = list(map(serialize_node, node_list))
    edges = list(map(serialize_edge, edge_list))
    return {"nodes": nodes, "edges:": edges}


def serialize_node(node):
    data = {
        "<id>": node.identity,
        "label": list(node.labels)[0],
        "attribute": dict(node)
    }
    return data


def serialize_edge(edge):
    data = {
        "<id>": edge.identity,
        "source": edge.start_node.identity,
        "target": edge.end_node.identity,
        "type": type(edge).__name__,
        "attribute": dict(edge)
    }
    return data


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
# def exec_read(cypher_sentiment: str):
#     db = get_db()
#
#     def run_tx(tx):
#         return tx.run(cypher_sentiment)
#
#     return db.read_transaction(run_tx)
#
#
# def exec_write(cypher_sentiment: str):
#     db = get_db()


######## 注册api
api.add_resource(KnowledgeGraph, '/graph')
api.add_resource(User, '/user')
api.add_resource(Register, '/register')
api.add_resource(Test, '/t')
api.add_resource(NodeRoute, '/graph/node')


def test():
    def test1():
        pass
        # cypher_snetiment = 'match (movie:Movie) return movie'
        # result = exec_cypher(cypher_snetiment)
        # print(type(result))
        # # while result.forward():
        # #     print(result.current)
        # return result.data()  # 此方法返回字典

    return test1()


if __name__ == '__main__':
    app.run()
