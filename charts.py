import altair as alt

from data import df


@alt.theme.register("custom_theme", enable=True)
def custom_theme() -> alt.theme.ThemeConfig:
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


def fractions_chart():
    chart = (
        alt.Chart(df)
        .mark_bar(color="#007bc2", stroke="white")
        .encode(x=alt.X("bill_length_mm", bin=True, title=None), y="count()")
    )
    return chart
