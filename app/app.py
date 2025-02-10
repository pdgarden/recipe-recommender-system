# -------------------------------------------------------------------------------------------------------------------- #
"""
Streamlit app implementing a recipe recommender system
"""
# -------------------------------------------------------------------------------------------------------------------- #
# Imports

import pandas as pd
import plotly.express as px
import streamlit as st

import constants
from utils.scoring import compute_recipe_affinity_score, labelize_recipes

# -------------------------------------------------------------------------------------------------------------------- #
# App

st.set_page_config(layout="wide")

st.header("Recipes recommendation")
st.sidebar.header("Informations about your taste")

# ------ #
# Sidebar

liked_ingredients = st.sidebar.multiselect("Select liked ingredients", constants.DEFAULT_ASKED_INGREDIENTS)
disliked_ingredients = st.sidebar.multiselect(
    "Select disliked ingredients",
    constants.DEFAULT_ASKED_INGREDIENTS,
)

launch_recipes_recommendation = st.sidebar.button("Get recipe recommendations")


# -------------------- #
# Recipe recommendation

if launch_recipes_recommendation:
    # Compute affinity score
    constants.DF_FEATURES["affinity_score_label"] = labelize_recipes(
        constants.DF_FEATURES["Ingredients"], liked_ingredients, disliked_ingredients
    )
    constants.DF_FEATURES["affinity_score_estimated"] = compute_recipe_affinity_score(constants.DF_FEATURES)

    # Select recipes with most affinity among labelized and estimated recipes
    constants.DF_FEATURES_AFFINITY_ESTIMATED = constants.DF_FEATURES.dropna(
        subset="affinity_score_estimated"
    ).sort_values("affinity_score_estimated")

    constants.DF_FEATURES_AFFINITY_LABELED = constants.DF_FEATURES.dropna(subset="affinity_score_label").sort_values(
        "affinity_score_label"
    )

    df_recommendation = pd.concat([constants.DF_FEATURES_AFFINITY_ESTIMATED, constants.DF_FEATURES_AFFINITY_LABELED])
    df_recommendation = df_recommendation[constants.AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS]

    # Recipes vizualisation
    fig_1 = px.scatter(
        constants.DF_FEATURES[constants.DF_FEATURES.affinity_score_label != 0],
        x="tsne_comp_0",
        y="tsne_comp_1",
        color="affinity_score_label",
        hover_data=constants.AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS,
        color_continuous_scale=px.colors.diverging.RdBu_r,
        color_continuous_midpoint=0,
        title="Liked ingredients - Labelized score",
    ).update_layout({"plot_bgcolor": "#E0E0E0"})

    fig_2 = px.scatter(
        constants.DF_FEATURES.dropna(subset="affinity_score_estimated"),
        x="tsne_comp_0",
        y="tsne_comp_1",
        color="affinity_score_estimated",
        hover_data=constants.AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS,
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
