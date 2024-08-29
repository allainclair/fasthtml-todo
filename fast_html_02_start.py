"""Show HTMX counter with Button"""

from fasthtml.common import Titled, fast_app, serve, Div

app, route = fast_app(live=True)

count = 0


@route("/")
def get():
	return Titled(
		"FastHTML app",
		Div(
			"Click me to count: 0",
			hx_get="/add1",
		),
	)

@route("/add1")
def get():
	global count
	count += 1
	return f"Click me to count: {count}"


serve()
