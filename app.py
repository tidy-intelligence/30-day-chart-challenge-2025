from pathlib import Path

from shiny import App, render, ui
from shinywidgets import output_widget, render_altair

from charts import fractions_chart
from utils import placeholder_text

css_file = Path(__file__).parent / "css" / "styles.css"

app_ui = ui.page_navbar(
    ui.head_content(ui.include_css(css_file)),
    ui.nav_panel(
        "Comparisons",
        ui.layout_column_wrap(
            ui.card(
                ui.card_header("Fractions"),
                ui.card_body(
                    ui.markdown(
                        "The figure shows the **alcohol-attributable fraction of mortality** "
                        "for the year 2019. denotes the proportion of a health outcome which "
                        "is caused by alcohol (i.e. that proportion which would disappear if "
                        "alcohol consumption was removed."
                    ),
                    output_widget("fractions"),
                    ui.markdown(
                        "Data Sources: Alcohol-attributable fractions are from the World Health Organization's  [Global Health Observatory (2024)](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-attributable-fractions-all-cause-deaths-(-)). "
                        "Region and income classifications are based on the World Bank's [Worl Development Indicators](https://databank.worldbank.org/source/world-development-indicators)."
                    ),
                ),
            ),
            ui.card(ui.card_header("Slope")),
            ui.card(ui.card_header("Circular")),
            ui.card(ui.card_header("Big or Small")),
            ui.card(ui.card_header("Ranking")),
            ui.card(ui.card_header("Florence Nightingal")),
            width=1 / 2,
        ),
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
