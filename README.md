# Sleemo: AWS AppSync Lambda Application Framework

A Simple yet powerful GraphQL framework powered by AWS AppSync Direct Lambda Resolver.

## Caution

**`Sleemo`** is still in the development phase. It aims to release its first version in November, 2020.

## Features
- No need to manually import other resolver functions and manage the tedious if-else based router from the gateway Lambda handler.
- The arguments of AppSync operations(queries and mutations) being parsed and passed to each resolver functions automatically.
- A utility functions provided to easily convert from and to AppSync scalar types such as AWSDateTime or AWSJSON

## Installation
```sh
pip install sleemo
```

## Usage

### Project Structure
An example of the **`Sleemo`** project could be structured like below:
```
/
|-- gatewayLambda.py
|-- resolvers/
|----- getTodo.py
|----- listTodo.py
|----- createTodo.py
|----- updateTodo.py
|----- deleteTodo.py
|-- requirements.txt
```

An example code with this project structure is given in the next section.

### An Example GraphQL Schema
```graphql
type Todo {
  id: ID!
  author: String!
  title: String!
  content: String
  done: Boolean!
  createdAt: AWSDateTime!
}

input CreateTodoInput {
  author: String!
  title: String!
  content: String
  done: Boolean
}

input UpdateTodoInput {
  author: String
  title: String
  content: String
  done: Boolean
}

type Query {
  getTodo(id: ID!): Todo
  listTodo: [Todo!]!
}

type Mutation {
  createTodo(input: CreateTodoInput!): Todo
  updateTodo(input: UpdateTodoInput!): Todo
  deleteTodo(id: ID!): Todo
}
```

### An Example Python Code

`gatewayLambda.py` is the default gateway of the AppSync resolver. It receives the event and route this event to appropriate functions.

```python
from sleemo.framework import get_appsync_framework

sleemo = get_appsync_framework(resolver_path='resolvers')

@sleemo.default_gateway()
def handler(event, context):
    return sleemo.resolve(event)

```

`resolver_path` represents where your resolver files are located. 

Now, let's take a look at how each resolver file lookes like. **`Sleemo`** doesn't care of how each resolver function should be implemented. You can use any libraries you prefer to implement your resolvers. **`Sleemo`** just passes the operation argument `input: CreateTodoInput` to `createTodo()` function with the original `event` variable.

```python
from sleemo.utils import get_appsync_type_utils

def createTodo(input, event):

    ## Your business logic here. 
    ## Below is an example of return data

    utils = get_appsync_type_utils()

    todo = {
        'id': utils.createID(),
        'author': input['author'],
        'title': input['title'],
        'content': input['content'],
        'done': False,
        'createdAt': utils.createAWSDateTime(),
    }

    return todo
```

Let's take another example of the resolver function `getTodo()`.

```python
from sleemo.utils import get_appsync_type_utils

def getTodo(id, event):

    ## Your business logic here. 
    ## Below is an example of return data

    utils = get_appsync_type_utils()

    todo = {
        'id': utils.createID(),
        'author': 'Taewoo Kim',
        'title': 'Sleemo Usage Example',
        'content': 'Simple yet powerful serverless GraphQL framework',
        'done': False,
        'createdAt': utils.createAWSDateTime(),
    }

    return todo
```

## LICENSE

[MIT LICENSE](./LICENSE)