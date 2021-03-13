from flask import Flask, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)  # init, migrate, upgrade


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/api/todos', methods=['GET', 'POST'])
@app.route('/api/todos/<int:id>', methods=['GET', 'DELETE'])
def todos(id=None):
    if request.method == 'POST':
        done = request.json.get('done')
        label = request.json.get('label')

        if not done:
            return jsonify({"msg": "Done es requerido"}), 400
        if not label:
            return jsonify({"msg": "Label es requerido"}), 400

        todo = Todo()
        todo.done = done
        todo.label = label
        todo.save()
        return jsonify(todo.serialize()), 201

    if request.method == 'GET':
        if id is not None:
            todos = Todo.query.get(id)
            if not todos:
                return jsonify({"msg": "Todo no encontrado"}), 404
            return jsonify(todos.serialize()), 200
        else:
            todos = Todo.query.all()
            todos = list(map(lambda todo: todo.serialize(), todos))
            return jsonify(todos), 200

    if request.method == 'DELETE':
        todos = Todo.query.get(id)
        if not todos: return jsonify({"msg": "Todo no encontrado"}), 404
        todos.delete()
        return jsonify({"msg": "Todo Borrado con exito"}), 200

if __name__ == '__main__':
    manager.run()
