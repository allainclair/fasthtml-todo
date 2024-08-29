"""Show HTMX Button that shows a Card"""

from fasthtml.common import Titled, fast_app, serve, Button, H3, Section

app, route = fast_app(live=True)

count = 0


@route("/")
def get():
	return Titled(
		"FastHTML app",
		Section(
			Button(
				"Click me to count",
				hx_get="/add1",
				hx_target="#counter",
			),
		),
		Section(
			H3("Counter: 0", id="counter"),
		),
	)

@route("/add1")
def get():
	global count
	count += 1
	return f"Counter: {count}"


serve()
