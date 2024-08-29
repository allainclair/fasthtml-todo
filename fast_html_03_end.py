"""Show HTMX Button that shows a Card"""

from fasthtml.common import Titled, fast_app, serve, Button, Section, Card, Header, Footer, H4, Strong, Nav, Ul, Li

app, route = fast_app(live=True)

@route("/")
async def get():
	return Titled(
		"FastHTML app",
		Section(
			Nav(
				Ul(
					Li(
						Button(
						Strong("Show my important card"),
							hx_get="/cards",
							hx_target="#card-section",
							hx_swap="beforeend",
						),
					),
					Li(
						Button(
							Strong("Reset cards"),
							hx_delete="/cards",
							hx_target="#card-section",
						),
					),
				),
			),
		),
		Section(
			id="card-section"
		),
	)

@route("/cards")
async def get():
	return MyCard()


@route("/cards")
async def delete():
	return ""


def MyCard() -> Card:
	return Card(
		Header(H4("PicoCSS Card")),
		"This is the body of the card",
		Footer("Footer of the card"),
	)


serve()
