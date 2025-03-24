from shiny import App, render, ui
from shinywidgets import output_widget, render_altair

from charts import fractions_chart
from utils import placeholder_text

app_ui = ui.page_navbar(
    ui.head_content(ui.include_css("styles.css")),
    ui.nav_panel(
        "Comparisons",
        ui.card(
            ui.card_header("Fractions"),
            ui.card_body(output_widget("fractions")),
        ),
        ui.card(ui.card_header("Slope")),
        ui.card(ui.card_header("Circular")),
        ui.card(ui.card_header("Big or Small")),
        ui.card(ui.card_header("Ranking")),
        ui.card(ui.card_header("Florence Nightingal")),
    ),
    ui.nav_panel("Distributions", ui.markdown(placeholder_text())),
    title="30 Day Chart Challenge",
)


def server(input, output, session):
    @output()
    @render_altair
    def fractions():
        return fractions_chart()


app = App(app_ui, server)
