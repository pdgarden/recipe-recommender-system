# -------------------------------------------------------------------------------------------------------------------- #
"""
Streamlit app implementing a recipe recommender system
"""
# -------------------------------------------------------------------------------------------------------------------- #
# Imports

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.scoring import compute_recipe_affinity_score, labelize_recipes

# -------------------------------------------------------------------------------------------------------------------- #
# Constants

DEFAULT_NB_ASKED_INGREDIENTS = 500
NB_RECOMMENDED_RECIPES = 20
PLOT_DISPLAYED_HOVER_COLUMNS = ["Name", "Ingredients", "Origin", "Link"]

df_features = pd.read_csv(Path("data") / "recipe_db.zip")

INGREDIENTS_PER_RECIPE = df_features["Ingredients"].str.split(", ")
INGREDIENTS = pd.Series([element for list_ in INGREDIENTS_PER_RECIPE for element in list_]).value_counts()
DEFAULT_ASKED_INGREDIENTS = INGREDIENTS.head(DEFAULT_NB_ASKED_INGREDIENTS).index.str.title()


# -------------------------------------------------------------------------------------------------------------------- #
# App

st.set_page_config(layout="wide")

st.header("Recipes recommendation")
st.sidebar.header("Informations about your taste")

# ------ #
# Sidebar

liked_ingredients = st.sidebar.multiselect("Select liked ingredients", DEFAULT_ASKED_INGREDIENTS)
disliked_ingredients = st.sidebar.multiselect(
    "Select disliked ingredients",
    DEFAULT_ASKED_INGREDIENTS,
)

launch_recipes_recommendation = st.sidebar.button("Get recipe recommendations")


# -------------------- #
# Recipe recommendation

if launch_recipes_recommendation:
    # Compute affinity score
    df_features["affinity_score_label"] = labelize_recipes(
        df_features["Ingredients"], liked_ingredients, disliked_ingredients
    )
    df_features["affinity_score_estimated"] = compute_recipe_affinity_score(df_features)

    # Select recipes with most affinity among labelized and estimated recipes
    df_features_affinity_estimated = (
        df_features.dropna(subset="affinity_score_estimated")
        .sort_values("affinity_score_estimated")
        .tail(int(NB_RECOMMENDED_RECIPES / 2))
    )

    df_features_affinity_labeled = (
        df_features.dropna(subset="affinity_score_label")
        .sort_values("affinity_score_label")
        .tail(int(NB_RECOMMENDED_RECIPES / 2))
    )

    df_recommendation = pd.concat([df_features_affinity_estimated, df_features_affinity_labeled])
    df_recommendation = df_recommendation[PLOT_DISPLAYED_HOVER_COLUMNS]

    # Recipes vizualisation
    fig_1 = px.scatter(
        df_features[df_features.affinity_score_label != 0],
        x="tsne_comp_0",
        y="tsne_comp_1",
        color="affinity_score_label",
        hover_data=PLOT_DISPLAYED_HOVER_COLUMNS,
        color_continuous_scale=px.colors.diverging.RdBu_r,
        color_continuous_midpoint=0,
        title="Liked ingredients - Labelized score",
    ).update_layout({"plot_bgcolor": "#E0E0E0"})

    fig_2 = px.scatter(
        df_features.dropna(subset="affinity_score_estimated"),
        x="tsne_comp_0",
        y="tsne_comp_1",
        color="affinity_score_estimated",
        hover_data=PLOT_DISPLAYED_HOVER_COLUMNS,
        color_continuous_scale=px.colors.diverging.RdBu_r,
        color_continuous_midpoint=0,
        title="Liked ingredients - Estimated score",
    ).update_layout({"plot_bgcolor": "#E0E0E0"})

    # App layouts
    tab_table, tab_plots = st.tabs(["🗃 Table vizualisation", "📈 Scatter plot visualization"])

    tab_table.text("Here are some recipes that have been identified as corresponding to your tastes")
    tab_table.dataframe(df_recommendation)

    tab_plots.text("Here is a low dimension representation of recipes. The color corresponds to the affinity score")
    tab_plots.plotly_chart(fig_1, use_container_width=True)
    tab_plots.plotly_chart(fig_2, use_container_width=True)
