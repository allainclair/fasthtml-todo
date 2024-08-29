"""Show HTMX requests with a counter"""

from fasthtml.common import Titled, fast_app, serve, Div

app, route = fast_app(live=True)


@route("/")
def get():
	return Titled(
		"FastHTML app",
		Div("Click me to count"),
	)


serve()
