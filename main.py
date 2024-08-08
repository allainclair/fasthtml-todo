"""FastHTML TODO list.
It uses by default uvicorn, picocss, HTMX
"""

from dataclasses import dataclass

from fasthtml.common import (
	Button,
	Div,
	Fieldset,
	Form,
	Input,
	Li,
	Link,
	Nav,
	Titled,
	Ul,
	fast_app,
	serve,
)

TODO_FIELDSET_ID = "todo-fieldset"
FORM_ID = "todo-form"

app, route = fast_app(
	hdrs=(
		Link(
			rel="stylesheet",
			href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.colors.min.css",
		),
		Link(rel="stylesheet", href="/main.css"),
	),
	live=True,
)

todo_counter = 0
todos = {}


@dataclass
class Item:
	todo: str
	done: bool = False


def fieldset() -> Fieldset:
	return Fieldset(
		Input(id="todo", placeholder="Add an item"),
		# Swap "before end":
		# It inserts after the last element of the "hx_target".
		Input(
			type="submit",
			value="Add",
			hx_post="/todos",
			hx_target="#todo-list",
			hx_swap="beforeend",
		),
		id=TODO_FIELDSET_ID,
		role="group",
		hx_swap_oob="true",
	)


def nav_todo_item(todo_id: int, todo_text: str) -> Nav:
	# Create a horizontal list of elements:
	# delete, update, checkbox, text, check emoji.
	return Nav(
		Ul(
			Li(
				Button(  # Delete button.
					"delete",
					hx_delete=f"/todos/{todo_id}",
					# Target this nav to be totally deleted.
					hx_target=f"#todo-{todo_id}",
					hx_swap="outerHTML",
					cls="pico-background-red-500",
				)
			),
			Li(
				Button(  # Edit button.
					"edit",
					hx_post=f"/todo-edit/{todo_id}",
					hx_target=f"#{FORM_ID}",
				)
			),
			Li(
				Input(
					type="checkbox",
					hx_post=f"/todo-check/{todo_id}",
					hx_target=f"#todo-check-{todo_id}",
					hx_swap="outerHTML",
				),
			),
			Li(todo_text, id=f"todo-text-{todo_id}"),  # Text
			Li("", id=f"todo-check-{todo_id}"),
		),
		id=f"todo-{todo_id}",
	)


def reset_and_build_some_todos() -> list[Nav]:
	# Save states.
	global todo_counter  # noqa: PLW0603
	global todos

	todo_counter = 0
	todos = {}
	nav_todos = []
	for i in range(1, 4):
		todo_counter += 1
		todo_text = f"Todo {i}"
		todos[todo_counter] = Item(todo=todo_text)
		nav_todos.append(nav_todo_item(i, todo_text))
	return nav_todos


@route("/")
async def get():  # noqa: ANN201
	return Titled(
		"Todo List in FastHTML",
		Form(
			fieldset(),
			id=FORM_ID,
		),
		Div(id="todo-list", *reset_and_build_some_todos()),
	)


@route("/todos")
async def post(item: Item):  # noqa: ANN201
	# Save states.
	global todo_counter  # noqa: PLW0603
	todo_counter += 1
	todos[todo_counter] = item

	# Check if there is non-empty string.
	if item.todo:
		return (
			nav_todo_item(todo_counter, item.todo),
			fieldset(),
		)
	return None


@route("/todos/{todo_id}")
async def delete(todo_id: int):  # noqa: ANN201
	del todos[todo_id]
	return None


@route("/todo-check/{todo_id}")
async def post(todo_id: int):  # noqa: ANN201 F811
	# Get the last state and reverse it.
	todos[todo_id].done = not todos[todo_id].done
	# Emoji mark.
	check = "✅" if todos[todo_id].done else ""
	# Return the Li element.
	return Li(check, id=f"todo-check-{todo_id}")


@route("/todos/{todo_id}")
async def put(todo_id: int, item: Item):  # noqa: ANN201
	# Check if there is non-empty string.
	if item.todo:
		item.done = todos[todo_id].done  # Keep the previous value.
		todos[todo_id] = item
		return Li(item.todo, id=f"todo-text-{todo_id}"), fieldset()

	# If empty, keep the old value.
	return Li(todos[todo_id].todo, id=f"todo-text-{todo_id}"), fieldset()


@route("/todo-edit/{todo_id}")
async def post(todo_id: int):  # noqa: ANN201
	todo = todos[todo_id]
	return (
		Fieldset(
			Input(id="todo", value=todo.todo),
			Input(
				type="submit",
				value="Edit",
				hx_put=f"/todos/{todo_id}",
				hx_target=f"#todo-text-{todo_id}",
				hx_swap="outerHTML",
				autofocus=True,
			),
			id=TODO_FIELDSET_ID,
			role="group",
		),
	)


serve()
