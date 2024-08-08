"""It uses by default uvicorn, picocss, HTMX"""

from dataclasses import dataclass

from fasthtml.common import (
	Div,
	Fieldset,
	Form,
	Input,
	P,
	Titled,
	fast_app,
	serve,
)

app, route = fast_app(live=True)


@dataclass
class Item:
	todo: str


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
		Div(id="todo-list"),
	)


@route("/add")
def post(item: Item):
	return P(item.todo)


serve()
