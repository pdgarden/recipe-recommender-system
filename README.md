<img src="https://img.shields.io/badge/python-3.11-blue" alt="Supported Python version"> <img src="https://img.shields.io/static/v1?logo=uv&label=uv&message=0.5.10&color=blue"> <img src="https://img.shields.io/static/v1?logo=Streamlit&label=Streamlit&message=1.22.0&color=blue">


# Recipe recommender system

The following repo implements a content based recipe recommendation system. It's studied using a notebook, and served
using Streamlit.

The approach is explained [here](https://pdgarden.github.io/recipe-recommender-system/).



## Dataset

The recipe recommendation system suggests recipes based on an affinity scor computed with every recipes of a dataset.

* The dataset used is a sample of +6000 recipes extracted from the [recipeDB](https://cosylab.iiitd.edu.in/recipedb/)
* See `scrap_recipes.py` for extraction script.
* For each recipe, the name, ingredients and origin is provided.



## Exploratory data analysis

The EDA are done trough the notebooks in the `eda` folder. The current notebook are:
- `eda_recipe_recommendations.ipynb`: explore the use of word embeddings and KNN algorithm to define an affinity score for the user.
- `eda_ingredients_extraction.ipynb`: explore the extraction of ingredients a user requests by using small LLMs.


The corresponding EDA are deployed online using Quarto and are accessible [here](https://pdgarden.github.io/recipe-recommender-system/).


## Quickstart

The studied recommendation system is implemented using Streamlit.

### Set up

1. Install uv (v0.5.10):
   1. For macOS / Linux `curl -LsSf https://astral.sh/uv/0.5.10/install.sh | sh`
   2. For windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.5.10/install.ps1 | iex"`
2. Create virtual environment: `uv sync --all-groups`
3. To develop (Optional):
   1. `uv run pre-commit install -t commit-msg -t pre-commit` (Setup pre-commit)
   2. `uv run quarto preview --execute` (Display the EDA locally)


The lock file only contains dependencies necessary to run the Streamlit app. 

### Launch local web server

```sh
uv run Streamlit run app.py
```

### Cloud access

Application hosted by Streamlit accessible [here](https://pdgarden-recipe-recommender-system-app-xlq89n.Streamlitapp.com/).
