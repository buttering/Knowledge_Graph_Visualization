# Designed for undergraduate graduation project

# Run the project:

## Start the back-end.

1. Start neo4j(need java11+)

```powershell
cd [neo4j installation directory]\bin
./neo4j.bat console
```

2. Start flask

```powershell
cd [project directory]
set FLASK_APP=app.py
flask run
```

## Start the front-end.

```powershell
cd [porject directory]/client
npm run serve
```

# 界面设计目标

仿照Neo4j Bloom设计一个能进行可视化展示和查询的界面，同时添加可视化编辑功能。

# Interfaces between backend and frontend

## 1.请求图数据

### 1）address

/graph

### 2) type

HTTP GET

### 3) description

先鉴权，通过后返回所有节点和关系信息，并单独给出节点名和关系名列表

### 4） return

```json
{
  "code": 200,
  "msg": {
    "node_name_list": [node name],
    "edge_name_list": [relationship name],
    "nodes":[
      {
        "<id>": node's identity,
        "attribute": node's attribute dict,
        "label": node label
      }
    ],
    "edges":[
      {
        "<id>": edge's identity,
        "attribute": edge's attribute dict,
        "source": source node id,
        "target": target node id,
        "type": edge type
      }
    ]
}
```

### 5) return msg explanation

返回信息包含数据库中的节点和关系名，用于可视化检索。

## 2. Cypher查询

### 1）address

/graph

### 2) type

HTTP POST

### 3) description

对数据库进行查询，返回查询json结果。

### 4） request body format

```json
{
  "Cypher-Statement": Cypher statement,
  "Return-Type": Py2Neo object type list in Cypher statement by order
}
```

*Explanation：*"Return-Type"字段以列表的形式按顺序列出Cypher查询中RETURN子句的返回值类型

返回值类型对应字段如下


| type         | keyword |
| -------------- | --------- |
| node         | N       |
| relationship | R       |
|              |         |

*For example：*有如下Cypher语句：`MATCH (n)-[r]-(m) RETURN n,r,m`,

则Return-Type字段为["N", "R", "N]

### 5） return

```json
{
  "code": 200,
  "msg": {
    "edges":[
      {
        "<id>": edge's identity
        "attribute": edge's attribute dict,
        "source": source node id,
        "target": target node id,
        "type": edge type
      }
    ],
    "nodes":[
      {
        "<id>": node's identity,
        "attribute": node's attribute dict,
        "label": node label
      }
    ]
  
  }
}
```

## 3. 用户登录

### 1) address

/user/sign

### 2) type

HTTP GET/POST/DELETE

### 3) description

用户登录操作，GET用于请求登录界面，POST用于提交登录信息,DELETE用于登出用户。

### 4） return(post)

- success

```json
{
  "code": 200,
  "msg": "Validation Completed"
}
```

- failure

```json
{
  "code": 401,
  "msg": "Validation fails"
}
```

## 4.用户注册

### 1) address

/user/register

### 2) type

HTTP GET/POST

### 3) description

用户注册操作，GET用于请求注册页面，POST用于提交注册信息

### 4） request body format(post)

```json
{
  "username": user name,
  "password": password,
  "email": e-mail
}
```

### 5) retrun(post)

- success

```json
{
  "code": 500,
  "msg": "Registration Completed"
}
```

- failure

```json
{
  "code": 401,
  "msg": "Duplicate Username"
}
```

```json
{
  "code": 402,
  "msg": "Repeat email"
}
```

```json
{
  "code": 403,
  "msg": "Incorrect Password Format"
}
```

## 5. 节点操作

### 1）address

/graph/node

## 2) type

HTTP POST/PUT/DELETE

### 3) description

对节点进行增加（POST）、删除（DELETE）以及对节点属性进行修改（PUT）

### 4） request body format

- POST

```json
{
  "Node-Type": Node type， which will be the label of node,
  "Node-Attribute": Dict of node attributes
}
```

- PUT

```json
{
  "Node-Id" : Node ID,
  "Node-Attribute": Dict of node attributes
}
```

- DELETE

```json
{
  "Node-Id" : Node ID,
}
```

*Notation：* 对节点属性进行修改必须把节点所有的属性（包括已存在的和新增的）传入。

### 5) return

- success

```json
{
  "code": 200,
  "msg":{
    "number": Number of changed nodes
  }
}
```

- failure

```json
{
  "code": 411,
  "msg": "Can't find node by this ID!"
}
```

## 6. 关系操作

### 1) address

/graph/edge

### 2) type

HTTP POST/PUT/DELETE

### 3) description

对关系进行增加（POST）、删除（DELETE）以及对关系属性进行修改（PUT）。

### 4） request body format

- POST

```json
{
  "Edge-Type": Node type， which will be the label of node,
  "Edge-Attribute": Dict of Relationship attributes,
  "Source-Node": ID of source node,
  "Target-Node": ID of target node

}
```

- PUT

```json
{
  "Edge-Id" : Relationship ID,
  "Edge-Attribute": Dict of relationship attributes
}
```

- DELETE

```json
{
  "Edge-Id" : Relationship ID,
}
```

*Notation：* 对关系属性进行修改必须把节点所有的属性（包括已存在的和新增的）传入。

### 5) return

- success

```json
{
  "code": 200,
  "msg":{
    "number": Number of changed relationships
  }
}
```

- failure

```json
{
  "code": 410,
  "msg": "Can't find relationship by this ID!"
}
```

# 数据库表

## 1. 用户表


| 字段     | 数据类型 | 描述           |
| ---------- | ---------- | ---------------- |
| uername  | TEXT     | 用户名         |
| password | TEXT     | 密码，密文储存 |
| email    | TEXT     | 用户电子邮件   |
| type     | INTEGER  | 用户类别       |
