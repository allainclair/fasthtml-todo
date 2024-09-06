"""Show HTMX requests with a counter"""

from fasthtml.common import Titled, fast_app, serve, Div, P

app, route = fast_app(live=True)

count = 0
count_2 = 0


@route("/")
async def get():
	return Titled(
		"FastHTML app",
		Div(
			"Click me to count: 0",
			hx_get="/add1",  # HTMX
		),

	)

@route("/add1")
async def get():
	global count
	global count_2
	count += 1
	count_2 += 2
	return f"Click me to count: {count}"


serve()
