# Designed for undergraduate graduation project

## 界面设计目标

仿照Neo4j Bloom设计一个能进行可视化展示和查询的界面，同时添加可视化编辑功能。

# interfaces between backend and frontend

## 1.请求首页

### 1）address

/graph

### 2) type

HTTP GET

### 3) description

默认页面，进入后先鉴权。验证通过后返回一个可视化页面。未登录时会被重定向到登录界面。

### 4） return

```json
{
  "code": 200,
  "msg": {
    "nodes": [node name],
    "edges": [relationship name]
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

### 4） request message formate

```json
{
  "Cypher-sentiment": Cypher sentiment,
  "Return-Type": Py2Neo object type list in Cypher sentiment by order
}
```

Explanation："Return-Type"字段以列表的形式按顺序列出Cypher查询中RETURN子句的返回值类型

返回值类型对应字段如下


| type         | keyword |
| -------------- | --------- |
| node         | N       |
| relationship | R       |
|              |         |

For example：有如下Cypher语句：`MATCH (n)-[r]-(m) RETURN n,r,m`,

则Return-Type字段为["N", "R", "N]

### 5） return

```json
{
  "code": 200,
  "msg": {
    "edges":[
      {
        "attribute": edge's attribute dict,
        "source": source node id,
        "target": target node id,
        "type": edge type
      }
    ],
    "nodes":[
      {
        "attribute": node's attribute dict,
        "id": node id,
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

### 4） request message formate(post)

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

# 数据库表

## 1. 用户表


| 字段     | 数据类型 | 描述           |
| ---------- | ---------- | ---------------- |
| uername  | TEXT     | 用户名         |
| password | TEXT     | 密码，密文储存 |
| email    | TEXT     | 用户电子邮件   |
| type     | INTEGER  | 用户类别       |
