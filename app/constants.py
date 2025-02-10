from pathlib import Path

import pandas as pd

# Constants for app

DEFAULT_NB_ASKED_INGREDIENTS = 500
NB_RECOMMENDED_RECIPES = 20
AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS = ["Name", "Ingredients", "Origin", "Link"]

DF_FEATURES = pd.read_parquet(Path("data") / "recipe_db.parquet")

INGREDIENTS_PER_RECIPE = DF_FEATURES["Ingredients"].str.split(", ")
INGREDIENTS = pd.Series([element for list_ in INGREDIENTS_PER_RECIPE for element in list_]).value_counts()
DEFAULT_ASKED_INGREDIENTS = INGREDIENTS.head(DEFAULT_NB_ASKED_INGREDIENTS).index.str.title()
