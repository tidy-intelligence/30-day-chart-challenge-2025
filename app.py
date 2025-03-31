from pathlib import Path

from shiny import App, render, ui
from shinywidgets import output_widget, render_altair

from charts import (
    big_or_small_chart,
    circular_chart,
    fractions_chart,
    ranking_chart,
    slope_chart,
)
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
                        "*Data Sources*: Alcohol-attributable fractions are from the World Health Organization's  [Global Health Observatory (2024)](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-attributable-fractions-all-cause-deaths-(-)). "
                        "Region and income classifications are based on the World Bank's [Worl Development Indicators](https://databank.worldbank.org/source/world-development-indicators)."
                    ),
                ),
            ),
            ui.card(
                ui.card_header("Slope"),
                ui.card_body(
                    ui.markdown(
                        "The figure shows a **slope chart** of changes in female labor force participation rate between 2014 and 2023 for the 5 countries with the largest percentage point increase in this period."
                    ),
                    output_widget("slope"),
                    ui.markdown(
                        "*Data Source*: International Labour Organization as provided through [Our World in Data](https://ourworldindata.org/grapher/female-labor-force-participation-rates-slopes). "
                    ),
                ),
            ),
            ui.card(
                ui.card_header("Circular"),
                ui.markdown(
                    "The figure shows the **circular material use rate**. It measures the share of material recycled and fed back into the economy - thus saving extraction of primary raw materials - in overall material use."
                ),
                output_widget("circular"),
                ui.markdown(
                    "*Data Source*: [Eurostat](https://ec.europa.eu/eurostat/cache/metadata/en/cei_srm030_esmsip2.htm)."
                ),
            ),
            ui.card(
                ui.card_header("Big or Small"),
                ui.markdown(
                    "The figure shows the global farmland distribution by **farm size**, with farms under 1 ha labeled Small, with those from 1-100 ha as Medium, 100-1,000 ha as Big, and anything larger as Very Big."
                ),
                output_widget("big_or_small"),
                ui.markdown(
                    "*Data Source*: [Lowder, Sanchez & Bertini (2021)](https://www.sciencedirect.com/science/article/pii/S0305750X2100067X#m0065)."
                ),
            ),
            ui.card(
                ui.card_header("Ranking"),
                ui.markdown(
                    "The figure shows the the **Economic Complexity Index ranking**, "
                    "which is a measure of the amount of capabilities and knowhow of a "
                    "given country determined by the diversity, ubiquity, and complexity "
                    "of the products it exports. It shows the trajectories of the top 10 countries "
                    "in 2022."
                ),
                output_widget("ranking"),
                ui.markdown(
                    "*Data Source*: [The Atlas of Economic Complexity](https://dataverse.harvard.edu/dataverse/atlas) by The Growth Lab at Harvard University."
                ),
            ),
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

    @output()
    @render_altair
    def slope():
        return slope_chart()

    @output()
    @render_altair
    def circular():
        return circular_chart()

    @output()
    @render_altair
    def big_or_small():
        return big_or_small_chart()

    @output()
    @render_altair
    def ranking():
        return ranking_chart()


app = App(app_ui, server)
