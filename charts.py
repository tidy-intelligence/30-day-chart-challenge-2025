import altair as alt

from data import df


def fractions_chart():
    chart = (
        alt.Chart(df)
        .mark_bar(color="#007bc2", stroke="white")
        .encode(x=alt.X("bill_length_mm", bin=True, title=None), y="count()")
    )
    return chart
