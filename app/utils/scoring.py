from typing import List

import faiss
import numpy as np
import pandas as pd


def labelize_recipes(
    recipes: pd.Series,
    liked_ingredients: List[str],
    disliked_ingredients: List[str],
    thresh_affinity_score: bool = False,
) -> pd.Series:
    affinity_score = pd.Series(np.zeros(len(recipes)))

    # add special char to differentiate match between composed ingredients e.g. milk / coconut milk
    ingredients = "," + recipes.str.replace(", ", ",") + ","
    ingredients = ingredients.str.lower()

    for ingredient in liked_ingredients:
        affinity_score += ingredients.str.contains("," + ingredient.lower() + ",", regex=False).astype("int")

    for ingredient in disliked_ingredients:
        affinity_score -= ingredients.str.contains("," + ingredient.lower() + ",", regex=False).astype("int")

    if thresh_affinity_score:
        affinity_score = affinity_score / affinity_score.abs().replace(0, 1)

    return affinity_score


def compute_recipe_affinity_score(df: pd.DataFrame) -> pd.DataFrame:
    NB_NEIGHBORS = 5

    embedding_cols = [c for c in df.columns if "embedding_" in c]
    embedding_matrix = df[embedding_cols].astype("float32").to_numpy()

    # get label and unlabeled embeddings
    labeled_embeddings = embedding_matrix[df.affinity_score_label != 0, :]
    unlabeled_embeddings = embedding_matrix[df.affinity_score_label == 0, :]

    # create faiss index
    vector_dimension = labeled_embeddings.shape[1]
    index = faiss.IndexFlatIP(vector_dimension)

    # normalize and add labeled_embeddings
    faiss.normalize_L2(labeled_embeddings)
    index.add(labeled_embeddings)

    # normalize and query unlabeled_embeddings
    faiss.normalize_L2(unlabeled_embeddings)

    _, r_indexes = index.search(unlabeled_embeddings, k=NB_NEIGHBORS)

    df_labeled = df[df.affinity_score_label != 0].reset_index(drop=True)
    df_unlabeled = df[df.affinity_score_label == 0].reset_index(drop=True)

    neighbors_id_columns = [f"neighbor_{i}_id" for i in range(NB_NEIGHBORS)]
    neighbors_liked_columns = [f"neighbor_{i}_liked_bool_value" for i in range(NB_NEIGHBORS)]

    df_neighbors = pd.DataFrame(r_indexes, index=df_unlabeled.id, columns=neighbors_id_columns)

    for i in range(NB_NEIGHBORS):
        df_neighbors[f"neighbor_{i}_liked_bool_value"] = df_neighbors[f"neighbor_{i}_id"].map(
            df_labeled.affinity_score_label
        )

    df_neighbors["liked_estimated_score"] = df_neighbors[neighbors_liked_columns].mean(axis=1)

    return df["id"].map(df_neighbors.liked_estimated_score)
