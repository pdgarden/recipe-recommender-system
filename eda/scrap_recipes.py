# -------------------------------------------------------------------------------------------------------------------- #
"""
Scrap recipes from db recipe, available here: https://cosylab.iiitd.edu.in/recipedb/
"""
# -------------------------------------------------------------------------------------------------------------------- #
# Imports

import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------------------------------------------------------- #
# Constants

BASE_URL = "https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/"
MIN_ITEM_ID = 0
MAX_ITEM_ID = 150_000
DISPLAYED_PROGRESSION_BATCH = 500
HTTP_REQUEST_TIMEOUT = 10


# -------------------------------------------------------------------------------------------------------------------- #
# Functions


@dataclass
class Recipe:
    id: int
    name: str
    ingredients: List[str]
    origin: str


def get_recipe_ingredients(soup: BeautifulSoup) -> List[str]:

    list_ingredients = []

    for tag in soup.find_all(id="ingredient_nutri")[0].find_all("td"):

        extract = tag.find("a")

        if extract is not None:
            list_ingredients.append(extract.contents[0])

    return list_ingredients


def get_recipe_name(soup: BeautifulSoup) -> str:

    return soup.find_all("h3")[0].text


def get_recipe_origin(soup: BeautifulSoup) -> str:

    return soup.find(id="recipe_info").find("p").contents[0]


def get_soup(recipe_id: int) -> BeautifulSoup:

    url = BASE_URL + str(recipe_id)

    r = requests.post(url, timeout=HTTP_REQUEST_TIMEOUT)

    if r.status_code != 200:
        error_msg = f"Invalid request status_code ({r.status_code}) for url {url} "
        raise requests.exceptions.HTTPError(error_msg)

    return BeautifulSoup(r.text, "html.parser")


# -------------------------------------------------------------------------------------------------------------------- #
# Main

if __name__ == "__main__":

    list_recipes = []

    for curr_id in range(MIN_ITEM_ID, MAX_ITEM_ID):

        try:

            time.sleep(0.2)

            curr_soup = get_soup(curr_id)

            recipe = Recipe(
                id=curr_id,
                name=get_recipe_name(curr_soup),
                ingredients=get_recipe_ingredients(curr_soup),
                origin=get_recipe_origin(curr_soup),
            )

            list_recipes.append(recipe)

        except Exception as exc:
            print(f"Error while processing item {curr_id}: {exc}")

        if curr_id % DISPLAYED_PROGRESSION_BATCH == 0:
            print(f"Items: {curr_id}")
            pd.DataFrame(
                {
                    "id": [e.id for e in list_recipes],
                    "name": [e.name for e in list_recipes],
                    "ingredients": [" | ".join(e.ingredients) for e in list_recipes],
                    "origin": [e.origin for e in list_recipes],
                }
            ).to_csv(Path("data") / "big_db_recipes_raw.csv", index=False)

    df_recipes = pd.DataFrame(
        {
            "id": [e.id for e in list_recipes],
            "name": [e.name for e in list_recipes],
            "ingredients": [" | ".join(e.ingredients) for e in list_recipes],
            "origin": [e.origin for e in list_recipes],
        }
    )

    df_recipes.to_csv(Path.cwd().parent / "data" / "recipe_db_raw.zip", index=False)

    print(
        "Done",
        f"nb_recipes: {len(df_recipes)}",
        f"first recipes: {df_recipes.head()}",
        sep="\n\n---\n",
    )
