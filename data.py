from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
fractions_data = pd.read_csv(app_dir / "fractions.csv")
