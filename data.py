from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
fractions_data = pd.read_csv(app_dir / "data/fractions.csv")
slope_data = pd.read_csv(app_dir / "data/slope.csv")
circular_data = pd.read_csv(app_dir / "data/circular.csv")
