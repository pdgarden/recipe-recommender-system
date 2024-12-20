# Recipe recommender system

The following repo implements a content based recipe recommendation system. It's studied using a notebook, and served
using streamlit.



## Dataset

* The dataset used is a sample of +6000 recipes extracted from the [recipeDB](https://cosylab.iiitd.edu.in/recipedb/),
* See [scrap_recipes.py](eda/scrap_recipes.py) for extraction script.
* For each recipe, the name, ingredients and origin is provided.



## Exploratory data analysis

The EDA os led through the [eda_recipe_recommendations.ipynb](eda/eda_recipe_recommendations.ipynb) notebooks and 
explore the use of word embeddings and KNN algorithm to define an affinity score for the user.



## Quickstart

The studied recommendation system is implemented using streamlit.

### Set up

1. Install uv (v0.5.10):
   1. For macOS / Linux `curl -LsSf https://astral.sh/uv/0.5.10/install.sh | sh`
   2. For windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.5.10/install.ps1 | iex"`
2. Create virtual environment: `uv sync`

The lock file only contains dependencies necessary to run the streamlit app. 
Some additional dependencies are required for the scrapping script and the notebook eda.

### Launch local web server

```sh
uv run streamlit run app.py
```

### Cloud access

Application hosted by streamlit accessible [here](https://pdgarden-recipe-recommender-system-app-xlq89n.streamlitapp.com/).
