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
from utils.llm import extract_clean_ingredients
from utils.scoring import compute_recipe_affinity_score, labelize_recipes

# -------------------------------------------------------------------------------------------------------------------- #
# App

st.set_page_config(layout="wide", page_title="Recipe recommender", page_icon="🍝")

st.header("Recipes recommendation")
st.sidebar.header("Information about your taste")

# -------------- #
# Sidebar - inputs

recipe_request = st.sidebar.text_area(
    label="Your request",
    placeholder="Could you recommend a recipe? I fancy potatoes, carrots, and peas, but hate onions and garlic",
)
launch_recipes_recommendation = st.sidebar.button("Get recipe recommendations")


# -------------------- #
# Recipe recommendation

if launch_recipes_recommendation:
    request_ingredients = extract_clean_ingredients(recipe_request)
    st.markdown(f"""
List of ingredients from the request associated with:
* A positive feeling: {", ".join(request_ingredients.positive_ingredients)}
* A negative feeling: {", ".join(request_ingredients.negative_ingredients)}
""")

    df_features = constants.DF_FEATURES.copy()

    # Compute affinity score
    df_features["affinity_score_label"] = labelize_recipes(
        df_features["Ingredients"],
        request_ingredients.positive_ingredients,
        request_ingredients.negative_ingredients,
    )
    df_features["affinity_score_estimated"] = compute_recipe_affinity_score(df_features)

    # Select recipes with most affinity among labelized and estimated recipes
    df_features_affinity_estimated = df_features.dropna(subset="affinity_score_estimated").sort_values(
        "affinity_score_estimated"
    )

    df_features_affinity_labeled = df_features.dropna(subset="affinity_score_label").sort_values("affinity_score_label")

    df_recommendation = pd.concat(
        [
            df_features_affinity_estimated,
            df_features_affinity_labeled,
        ]
    ).drop_duplicates(subset="Name")

    # Figures of scores
    fig_score_label = px.scatter(
        df_features[df_features.affinity_score_label != 0],
        x="umap_comp_0",
        y="umap_comp_1",
        color="affinity_score_label",
        hover_data=constants.AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS,
        color_continuous_scale=px.colors.diverging.RdBu_r,
        color_continuous_midpoint=0,
        title="Liked ingredients - Labelized score",
        width=600,
        height=600,
    ).update_layout({"plot_bgcolor": "#E0E0E0"})

    fig_score_estimated = px.scatter(
        df_features.dropna(subset="affinity_score_estimated"),
        x="umap_comp_0",
        y="umap_comp_1",
        color="affinity_score_estimated",
        hover_data=constants.AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS,
        color_continuous_scale=px.colors.diverging.RdBu_r,
        color_continuous_midpoint=0,
        title="Liked ingredients - Estimated score",
        width=600,
        height=600,
    ).update_layout({"plot_bgcolor": "#E0E0E0"})

    # --------- #
    # App layouts
    tab_rec, tab_table, tab_plots = st.tabs(
        ["Recommendations", "🗃 Table vizualisation", "📈 Scatter plot visualization"]
    )

    # Recommendations in plain text
    df_to_md = lambda df: "\n".join(  # noqa: E731
        ("* **" + df.Name + ":** " + df.Ingredients).str.replace("-", " ").head(5).tolist()
    )
    tab_rec.markdown("Here are some recipes that have been identified with corresponding ingredients:")
    tab_rec.markdown(df_to_md(df_recommendation.sort_values("affinity_score_label", ascending=False)))
    tab_rec.divider()
    tab_rec.markdown(
        "Here are some recipes that don't directly contain the ingredients that you mentioned, but similar ingredients:"
    )
    tab_rec.markdown(df_to_md(df_recommendation.sort_values("affinity_score_estimated", ascending=False)))

    # Recommendations in table
    tab_table.markdown("Table of recommended recipes, sorted by affinity score.")
    tab_table.dataframe(
        df_recommendation.sort_values("affinity_score_label")[constants.AFFINITY_PLOT_DISPLAYED_HOVER_COLUMNS]
    )

    # Recommendations in graph
    tab_plots.text("Here is a low dimension representation of recipes. The color corresponds to the affinity score")
    tab_plots.plotly_chart(fig_score_label, use_container_width=True)
    tab_plots.plotly_chart(fig_score_estimated, use_container_width=True)
