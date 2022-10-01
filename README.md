# Recipe recommender system

The following repo implements a content based recipe recommendation system. It's studied using a notebbok, and served
using streamlit.


## Dataset:

* The dataset used is a sample of +6000 recipes extracted from the [recipeDB](https://cosylab.iiitd.edu.in/recipedb/),
* See [scrap_recipes.py](eda/scrap_recipes.py) for extraction script.
* For each recipe, the name, ingredients and origin is provided.


## Exploratory data analysis:

The EDA os led through the [eda_recipe_recommendations.ipynb](eda/eda_recipe_recommendations.ipynb) notebooks and 
explore the use of word embeddings and KNN algoithm to define an affinity score for the user.

## Implementation

The studied recommendation system is implemented using streamlit.

### Requirements

The requirements file only contains dependencies necessary to run the streamlit app. 
Some additionnal dependencies are required for the scrapping script and the notebook eda.

```sh
pip install -r requirements.txt
```

### Launch local web server

```sh
streamlit run app.py
```
