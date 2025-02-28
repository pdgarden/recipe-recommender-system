from openai import OpenAI
from pydantic import BaseModel

import constants
from configuration import config


class IngredientsPosNeg(BaseModel):
    """Lists of ingredients associated to positive and negative feelings"""

    positive_ingredients: list[str]
    negative_ingredients: list[str]


class Ingredients(BaseModel):
    """A simple list of string in wich each string represent an ingredient"""

    ingredients: list[str]


def extract_raw_ingredients(
    recipe_request: str,
    llm_model: str,
    llm_client: OpenAI,
) -> IngredientsPosNeg:
    """Get the list of positive and negative ingredients for a given recipe request."""

    try:
        completion = llm_client.beta.chat.completions.parse(
            temperature=0,
            model=llm_model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Provide the list of positive and negative ingredients for the following recipe "
                        f"request in lowercase: {recipe_request}"
                    ),
                }
            ],
            response_format=IngredientsPosNeg,
        )

        recipe_response = completion.choices[0].message
        if recipe_response.parsed:  # noqa: SIM108
            ingredients_pos_neg = recipe_response.parsed
        else:
            ingredients_pos_neg = IngredientsPosNeg(positive_ingredients=[], negative_ingredients=[])
    except Exception as e:
        print(e)
        ingredients_pos_neg = IngredientsPosNeg(positive_ingredients=[], negative_ingredients=[])

    return ingredients_pos_neg


def make_ingredients_singular(
    ingredients: Ingredients,
    llm_model: str,
    llm_client: OpenAI,
) -> Ingredients:
    """Convert the ingredients in plural to ingredients in singular."""

    try:
        completion = llm_client.beta.chat.completions.parse(
            temperature=0,
            model=llm_model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Rewrite the list of items by making them singular: \n"
                        "Example: carrots -> carrot, onions -> onion, \n"
                        f"{ingredients}"
                    ),
                }
            ],
            response_format=Ingredients,
        )

        recipe_response = completion.choices[0].message
        if recipe_response.parsed:  # noqa: SIM108
            ingredients = recipe_response.parsed
        else:
            ingredients = Ingredients(ingredients=[])
    except Exception as e:
        print(e)
        ingredients = Ingredients(ingredients=[])

    return ingredients


def extract_clean_ingredients(recipe_request: str) -> IngredientsPosNeg:
    """Take a recipe request and return the associated positive and negative ingredients in clean format."""
    llm_args = {
        "llm_client": OpenAI(base_url=config.llm_base_url, api_key=config.llm_api_key),
        "llm_model": config.llm_model,
    }

    ingredients_pos_neg = extract_raw_ingredients(recipe_request=recipe_request, **llm_args)

    ingredients_singular_pos = make_ingredients_singular(
        ingredients=ingredients_pos_neg.positive_ingredients, **llm_args
    )
    ingredients_singular_neg = make_ingredients_singular(
        ingredients=ingredients_pos_neg.negative_ingredients, **llm_args
    )

    ingredients_pos_neg_singular = IngredientsPosNeg(
        positive_ingredients=ingredients_singular_pos.ingredients,
        negative_ingredients=ingredients_singular_neg.ingredients,
    )

    ingredients_pos_neg_in_db = IngredientsPosNeg(
        positive_ingredients=[
            ingredient.title()
            for ingredient in ingredients_pos_neg_singular.positive_ingredients
            if ingredient.title() in constants.AVAILABLE_INGREDIENTS
        ],
        negative_ingredients=[
            ingredient.title()
            for ingredient in ingredients_pos_neg_singular.negative_ingredients
            if ingredient.title() in constants.AVAILABLE_INGREDIENTS
        ],
    )
    return ingredients_pos_neg_in_db
