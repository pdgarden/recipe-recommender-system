from pathlib import Path

import pandas as pd

# Constants for app

DEFAULT_NB_ASKED_INGREDIENTS = 500
NB_RECOMMENDED_RECIPES = 20
AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS = ["Name", "Ingredients", "Origin", "Link"]

DF_FEATURES = pd.read_parquet(Path("data") / "recipe_db.parquet").drop_duplicates(subset=["Name"])

INGREDIENTS_PER_RECIPE = DF_FEATURES["Ingredients"].str.split(", ")
INGREDIENTS_OCCURRENCE = pd.Series([element for list_ in INGREDIENTS_PER_RECIPE for element in list_]).value_counts()

# List of ingredients sorted by occurrence, in "title format" e.g. 'Flour', 'Olive Oil'
AVAILABLE_INGREDIENTS = INGREDIENTS_OCCURRENCE.head(DEFAULT_NB_ASKED_INGREDIENTS).index.str.title()
