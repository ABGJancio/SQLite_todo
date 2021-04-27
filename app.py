from flask import Flask, render_template, request
from forms import TodoForm
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    todos=todos.select_all()

    if request.method == "POST":
        if form.validate_on_submit():
            todos.add_todo(form.data)
        return redirect(url_for("todos_list"))

    return render_template("todos.html", form=form, todos=todos, error=error)


@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos.select_id(todo_id - 1)
    form = TodoForm(data=todo)

    if request.method == "POST":
        if form.validate_on_submit():
            todos.update(todos, todo_id - 1, form.data)
        return redirect(url_for("todos_list"))

    return render_template("todo.html", form=form, todo_id=todo_id)


if __name__ == '__main__':
    app.run(debug=True)
