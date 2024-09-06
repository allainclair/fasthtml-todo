"""It uses by default uvicorn, picocss, HTMX"""

from fasthtml.common import Titled, fast_app, serve

app, route = fast_app(live=True)


@route("/")
async def get():
	return Titled("FastHTML App 1")



serve()
