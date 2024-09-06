"""Show HTMX counter with Button"""

from fasthtml.common import Titled, fast_app, serve, Div, Section, Button, H3

app, route = fast_app(live=True)

count = 0


@route("/")
def get():
	return Titled(
		"FastHTML app",
		Section(
			Button("Click me to count"),
			hx_get="/add1",
			hx_target="#counter",
		),
		Section(
			H3("Counter: "),
			H3("0", id="counter"),
		),
	)

@route("/add1")
def get():
	global count
	count += 1
	return H3(f"{count}")


serve()
