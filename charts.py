import altair as alt

from data import (
    big_or_small_data,
    circular_data,
    fractions_data,
    ranking_data,
    slope_data,
)


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
                        "gdp_per_capita", title="GDP per capita", format=",.0f"
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


def slope_chart(
    countries=[
        "Bolivia",
        "Malta",
        "Guatemala",
        "Bosnia and Herzegovina",
        "Saudi Arabia",
    ],
):
    slope_data_sub = slope_data[slope_data["name"].isin(countries)]

    base_chart = (
        (
            alt.Chart(slope_data_sub).encode(
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
        alt.Chart(slope_data_sub)
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


def big_or_small_chart():
    chart = (
        alt.Chart(big_or_small_data)
        .encode(
            alt.Theta("area").stack(True),
            alt.Radius("area").scale(type="sqrt"),
            color=alt.Color("size_group:N", legend=None),
            tooltip=[
                alt.Tooltip("size_group", title="Farm size"),
                alt.Tooltip("area", title="Share of agricultural area", format=".1%"),
                alt.Tooltip("farms", title="Number of farms", format=","),
            ],
        )
        .properties(
            title=alt.TitleParams(
                "Distribution of global agricultural area by farm size",
            )
        )
        .interactive()
    )

    arc = chart.mark_arc(innerRadius=20, stroke="#fff")
    text = chart.mark_text(radiusOffset=50).encode(text="size_group")

    chart = arc + text
    return chart


def ranking_chart():
    hover = alt.selection_single(on="mouseover")

    base_chart = alt.Chart(ranking_data).encode(
        x=alt.X("year", axis=alt.Axis(format="d", title=None)),
        y=alt.Y("rank", axis=alt.Axis(title=None)),
        color=alt.Color("name:N", legend=None),
        opacity=alt.condition(hover, alt.value(1), alt.value(0.2)),
        strokeWidth=alt.condition(hover, alt.value(3), alt.value(1)),
    )

    lines = base_chart.mark_line(point=True)

    labels = (
        alt.Chart(ranking_data)
        .transform_filter(alt.datum.year == 2022)
        .mark_text(align="left", dx=5)
        .encode(
            x=alt.X("year", axis=alt.Axis(format="d", title=None)),
            y=alt.Y("rank", axis=alt.Axis(title=None)),
            text="name",
            color="name",
        )
    )

    chart = (
        (lines + labels)
        .add_params(hover)
        .properties(title="Rank in the Economic Complexity Index")
    )

    return chart
