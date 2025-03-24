import altair as alt

from data import fractions_data


def custom_theme():
    font = "Open Sans"
    return {
        "config": {
            "title": {"font": font},
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
    chart = (
        alt.Chart(fractions_data)
        .mark_bar(color="#007bc2", stroke="white")
        .encode(x=alt.X("bill_length_mm", bin=True, title=None), y="count()")
    )
    return chart
