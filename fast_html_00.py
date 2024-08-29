"""It uses by default uvicorn, picocss, HTMX"""

from fasthtml.common import Titled, fast_app, serve, P

app, route = fast_app(live=True)


@route("/")
def get():
	return Titled("FastHTML App")



serve()
