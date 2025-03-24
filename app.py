from shiny.express import input, render, ui
from shinywidgets import render_altair

from charts import fractions_chart
from utils import placeholder_text

ui.page_opts(title="30 Day Chart Challenge")

ui.nav_spacer()


with ui.nav_panel("Comparisons"):
    with ui.navset_card_underline(title="World Bank WDI"):
        with ui.nav_panel("Fractions"):

            @render_altair
            def fractions():
                return fractions_chart()

        with ui.nav_panel("Slope"):
            placeholder_text()


with ui.nav_panel("Distributions"):
    placeholder_text()
