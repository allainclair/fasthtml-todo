"""It uses by default uvicorn, picocss, HTMX"""

from dataclasses import dataclass

from fasthtml.common import (
	A,
	Div,
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
				# Swap "before end", it inserts after the last element of the "hx_target".
				Input(
					type="submit",
					value="Add",
					hx_post="/add",
					hx_target="#todo-list",
					hx_swap="beforeend",
				),
				role="group",
			),
		),
		Div(id="todo-list"),
	)


@route("/add")
def post(item: Item):
	# Save states.
	global todo_counter
	todo_counter += 1
	todos[todo_counter] = item

	# Check if there is non-empty string.
	if item.todo:
		# Create a horizontal list of elements: delete, update, checkbox, text, mark.
		return Nav(
			Ul(
				A(
					Li(
						"❌",
						hx_delete=f"/todo/{todo_counter}",
						hx_target=f"#todo-{todo_counter}",
					)
				),  # Delete button.
				A(Li("🔄")),  # Update button.
				Li(  # When clicking on the checkbox, it requests /mark/{todo_id}.
					Input(
						type="checkbox",
						hx_post=f"/todo/{todo_counter}",
						hx_target=f"#todo-mark-{todo_counter}",
						hx_swap="outerHTML",
					),
				),
				Li("🔴", id=f"todo-mark-{todo_counter}"),  # Emoji mark.
				Li(item.todo),  # Text.
			),
			id=f"todo-{todo_counter}",
		)
	return None


@route("/todo/{todo_id}")
def delete(todo_id: int):
	del todos[todo_id]
	# Return the Li element.


@route("/todo/{todo_id}")
def post(todo_id: int):
	# get the last state.
	todo = todos[todo_id]
	# reverse it.
	todo.done = not todo.done
	# reverse the Emoji mark.
	mark = "✅" if todo.done else "🔴"
	# Return the Li element.
	return Li(mark, id=f"todo-mark-{todo_id}")


serve()
