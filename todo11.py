"""It uses by default uvicorn, picocss, HTMX"""

from fasthtml.common import Titled, fast_app, serve

app, route = fast_app(live=True)


@route("/")
def get():
	return Titled(
		"Todo List in FastHTML",
		# Form(
		# 	Fieldset(
		# 		Input(name="todo", placeholder="Add an item"),
		# 		Input(type="submit", value="Add", hx_post="/add", hx_target="#TODO-list"),  # Show: hx_swap="outerHTML",
		# 		role="group",
		# 	),
		# ),
		# Div(id="todo-list"),
	)


# @route('/add')
# def post():
# 	return P(
# 		"Todo List in FastHTML"
# 	)


serve()
