from flask import Flask
from forms import TodoForm
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    return todos.select_all()

if __name__ == '__main__':
    app.run(debug=True)


