from flask import Flask, redirect, url_for, g, request, jsonify
from neo4j import GraphDatabase
from flask_restful_swagger_2 import Api, Resource
from py2neo import Graph, Node, NodeMatcher, Subgraph, Relationship, RelationshipMatcher

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

        return return_deleted_relationship(1)

    def put(self):
        request_data = request.get_json()
        node_attributes = request_data.get('Node-Attribute')
        node_id = request_data.get('Node-Id')

        node_matcher = NodeMatcher(graph)
        try:
            changed_node = node_matcher[node_id]
        except KeyError:
            return return_exception_code(411, "Can,t find node by this ID")
        changed_node.clear()  # 清楚所有属性
        changed_node.update(node_attributes)

        tx = graph.begin()
        tx.push(changed_node)
        tx.commit()

        return return_deleted_relationship(1)

    def delete(self):
        request_data = request.get_json()
        node_id = request_data.get('Node-Id')

        node_matcher = NodeMatcher(graph)
        try:
            deleted_node = node_matcher[node_id]
        except KeyError:
            return return_exception_code(411, "Can,t find node by this ID")
        graph.delete(deleted_node)

        return return_deleted_relationship(1)


class RelationshipRoute(Resource):
    def post(self):
        request_data = request.get_json()
        relationship_type = request_data.get('Edge-Type')
        relationship_attribute = request_data.get('Edge-Attribute')
        relationship_source_node_ID = request_data.get('Source-Node')
        relationship_target_node_ID = request_data.get('Target-Node')

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

    def put(self):
        request_data = request.get_json()
        relationship_ID = request_data.get('Edge-Id')
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

    def delete(self):
        request_data = request.get_json()
        relationship_ID = request_data.get('Edge-Id')

        relationship_matcher = RelationshipMatcher(graph)
        try:
            deleted_relationship = relationship_matcher[relationship_ID]
        except KeyError as e:
            return return_exception_code(410, "Can't find relationship by this ID!")

        graph.separate(deleted_relationship)

        return return_deleted_relationship(1)


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
api.add_resource(RelationshipRoute, '/graph/edge')


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
