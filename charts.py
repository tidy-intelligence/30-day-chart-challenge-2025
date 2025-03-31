import altair as alt

from data import circular_data, fractions_data, slope_data


# NOTE: this approach only works on altair==5.4.1 (which is the pyodide version)
def custom_theme():
    font = "Open Sans"
    return {
        "config": {
            "title": {"font": font, "anchor": "start"},
            "axis": {"labelFont": font, "titleFont": font},
            "header": {"labelFont": font, "titleFont": font},
            "legend": {
                "labelFont": font,
                "titleFont": font,
            },
        }
    }


alt.themes.register("custom_theme", custom_theme)
alt.themes.enable("custom_theme")


def fractions_chart():
    income_order = [
        "Low income",
        "Lower middle income",
        "Upper middle income",
        "High income",
    ]

    region_selection = alt.selection_point(
        fields=["region_name"], bind="legend", name="Region"
    )
    income_selection = alt.selection_point(
        fields=["income_level_name"], bind="legend", name="Income"
    )
    combined_condition = region_selection & income_selection

    chart = (
        (
            alt.Chart(fractions_data)
            .mark_point(filled=True)
            .encode(
                x=alt.X("male", title="Male", axis=alt.Axis(format=".0%")),
                y=alt.Y("female", title="Female", axis=alt.Axis(format=".0%")),
                color=alt.Color("region_name", title="Region"),
                size=alt.Size(
                    "income_level_name",
                    title="Income level",
                    sort=income_order,
                    scale=alt.Scale(range=[100, 500]),
                ),
                tooltip=[
                    alt.Tooltip("entity_name", title="Country"),
                    alt.Tooltip("region_name", title="Region"),
                    alt.Tooltip("male", title="Male", format=".1%"),
                    alt.Tooltip("female", title="Female", format=".1%"),
                    alt.Tooltip("income_level_name", title="Income level"),
                    alt.Tooltip(
                        "gdp_per_capita", title="GDP per Capita", format=",.0f"
                    ),
                ],
                opacity=alt.condition(
                    combined_condition, alt.value(0.5), alt.value(0.05)
                ),
            )
        )
        .properties(
            title=alt.TitleParams(
                "Alcohol-attributable fraction of mortality, 2019",
            )
        )
        .add_params(region_selection, income_selection)
        .interactive()
    )

    return chart


fractions_chart()


def slope_chart():
    base_chart = (
        (
            alt.Chart(slope_data).encode(
                x=alt.X("year:O", title=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y("value", title=None, axis=alt.Axis(format=".0%")),
                color=alt.Color("name", legend=None),
                tooltip=[
                    alt.Tooltip("name", title="Country"),
                    alt.Tooltip("year", title="Year"),
                    alt.Tooltip("value", title="Proportion", format=".1%"),
                ],
            )
        )
        .properties(
            title=alt.TitleParams(
                "Proportion of women participating in the labor force, 2014 to 2023",
            )
        )
        .interactive()
    )

    line_chart = base_chart.mark_line()
    point_chart = base_chart.mark_point(filled=True)
    labels = (
        alt.Chart(slope_data)
        .transform_filter(alt.datum.year == 2023)
        .mark_text(align="left", dx=5)
        .encode(
            x=alt.X("year:O"),
            y=alt.Y("value"),
            text="name",
            color="name",
        )
    )

    chart = line_chart + point_chart + labels

    return chart


def circular_chart():
    chart = (
        alt.Chart(circular_data)
        .mark_bar()
        .encode(
            x=alt.X("value", title=None, axis=alt.Axis(format=".0%")),
            y=alt.Y("name", sort="-x", title=None),
            color=alt.condition(
                alt.datum.name == "EU", alt.value("darkblue"), alt.value("#61c0bf")
            ),
            tooltip=[
                alt.Tooltip("name", title="Country"),
                alt.Tooltip("value", title="Rate", format=".1%"),
            ],
        )
        .properties(
            title=alt.TitleParams(
                "Circular material use rate, 2023",
            )
        )
        .interactive()
    )
    return chart
