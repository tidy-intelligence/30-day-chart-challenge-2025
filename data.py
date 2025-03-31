from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
fractions_data = pd.read_csv(app_dir / "data/fractions.csv")
slope_data = pd.read_csv(app_dir / "data/slope.csv")
circular_data = pd.read_csv(app_dir / "data/circular.csv")
big_or_small_data = pd.read_csv(app_dir / "data/big_or_small.csv")
ranking_data = pd.read_csv(app_dir / "data/ranking.csv")


def group_farm_size(name):
    if name == "< 1 ha":
        return "Small"
    elif name in ["1–2 ha", "2–5 ha", "5–10 ha", "10–20 ha", "20–50 ha", "50–100 ha"]:
        return "Medium"
    elif name in ["100–200 ha", "200–500 ha", "500–1 000 ha"]:
        return "Big"
    else:
        return "Very Big"


big_or_small_data["size_group"] = big_or_small_data["name"].apply(group_farm_size)
big_or_small_data = big_or_small_data.groupby("size_group", as_index=False).agg(
    {"area": "sum", "farms": "sum"}
)
group_order = ["Small", "Medium", "Big", "Very Big"]
big_or_small_data["size_group"] = pd.Categorical(
    big_or_small_data["size_group"], categories=group_order, ordered=True
)
