"""It uses by default uvicorn, picocss, HTMX"""

from dataclasses import dataclass

from fasthtml.common import (
	Fieldset,
	Form,
	Input,
	Li,
	Nav,
	Titled,
	Ul,
	fast_app,
	serve,
)

app, route = fast_app(live=True)

todo_counter = 0
todos = {}


@dataclass
class Item:
	todo: str
	done: bool = False


@route("/")
def get():
	return Titled(
		"Todo List in FastHTML",
		Form(
			Fieldset(
				Input(name="todo", placeholder="Add an item"),
				Input(
					type="submit",
					value="Add",
					hx_post="/add",
					hx_target="#todo-list",
				),
				role="group",
			),
		),
		Nav(id="todo-list"),
	)


@route("/add")
def post(item: Item):
	# Save states.
	global todo_counter
	todo_counter += 1
	todos[todo_counter] = item

	# Check if there is non-empty string.
	if item.todo:
		# Create a horizontal list of elements: checkbox, text, mark.
		return (
			Ul(
				Li(  # When clicking on the checkbox, it requests /mark/{todo_id}.
					Input(
						type="checkbox",
						hx_post=f"/mark/{todo_counter}",
						hx_target=f"#todo-mark-{todo_counter}",
						hx_swap="outerHTML",
					),
				),
				Li("🔴", id=f"todo-mark-{todo_counter}"),  # Emoji mark.
				Li(item.todo),  # TODO text.
			),
		)
	return None


@route("/mark/{todo_id}")
def post(todo_id: int):
	# get the last state.
	todo = todos[todo_id]
	# reverse it.
	todo.done = not todo.done
	# reverse the Emoji mark.
	mark = "✅" if todo.done else "🔴"
	# Return the Li element.
	return (Li(mark, id=f"todo-mark-{todo_id}"),)


serve()
