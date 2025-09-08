from flask import request
from flask_restful import Resource
from models import TodoModel, db


class TodoList(Resource):
    def get(self):
        todos = TodoModel.query.all()
        return [todo.to_dict() for todo in todos]

    def post(self):
        data = request.get_json()
        new_todo = TodoModel(task=data["task"])
        db.session.add(new_todo)
        db.session.commit()
        return new_todo.to_dict(), 201


class Todo(Resource):
    def get(self, todo_id):
        todo = TodoModel.query.get(todo_id)
        if not todo:
            return {"message": "Todo not found"}, 404
        return todo.to_dict()

    def put(self, todo_id):
        data = request.get_json()
        todo = TodoModel.query.get(todo_id)
        if not todo:
            return {"message": "Todo not found"}, 404
        todo.task = data["task"]
        db.session.commit()
        return todo.to_dict()

    def delete(self, todo_id):
        todo = TodoModel.query.get(todo_id)
        if not todo:
            return {"message": "Todo not found"}, 404
        db.session.delete(todo)
        db.session.commit()
        return {"message": "Deleted successfully"}, 200
