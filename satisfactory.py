from part import Part
import pandas as pd
import numpy as np
from copy import deepcopy

# load parts and recipes from spreadsheet
def parse_parts_and_recipes(filename):

    parts_df = pd.read_excel(filename, sheet_name="Parts")
    recipes_df = pd.read_excel(filename, sheet_name="Recipes")
    parts_list = {row["Name"]:Part(name=row["Name"], kind=row["Kind"]) for _, row in parts_df.iterrows()}
    # Process recipes:
    for _, row in recipes_df.iterrows():

        inputs = []
        cleaned_row = row.dropna()
        for i in [1, 2, 3, 4]:
            try:
                inputs.append([cleaned_row[f"Input {i}"], cleaned_row[f"Number {i}"]])
            except KeyError:
                continue

        parts_list[row["Output"]].add_recipe(inputs, row["Output rate"], row["Building"])

    return parts_list

def solve_supply_chain(outputs, integral=True):
    """Solved the logistics supply chain with the desired outputs.
    
    Parameters:
    -----------
    - outputs: dict
        A dictionary of the form {part: number}, specifying the desired outputs.
    
    Returns:
    --------
    - ingredients: dict
        A dictionary whose keys are all the parts of the supply chain. The value
        associated to each key is itself a dictionary containing the following
        items:
            - requirements: dict
                A dictionary of the form {part: number} which states that [number]
                of the current ingredient is needed to make [part]
            - required: int
                The total number of this item that is needed
            - multiplier: int
                The number of production facilities required for this item
            - supplied: int
                The total number of this item that is produced
    """

    ingredients = {}

    for part, number in outputs.items():
        ingredients[part] = {"requirements":{"output": number},
                             "required": number,
                             "supplied": 0}

    all_solved = False
    while not all_solved:
        new_ingredients = deepcopy(ingredients)
        
        for item, status in ingredients.items():
            
            recipe = parts_list[item].get_default_recipe()
            new_status = new_ingredients[item]

            if recipe is None:
                new_status["supplied"] = status["required"]
                continue

            inputs = recipe.inputs
            output = recipe.outputs[0][1]

            new_status["solved"] = (status["supplied"] >= status["required"])

            if not new_status["solved"]:

                if integral:
                    new_status["multiplier"] = np.ceil(status["required"] / output)
                else:
                    new_status["multiplier"] = float(status["required"]) / output
                    
                new_status["supplied"] = output * new_status["multiplier"]
                new_status["inputs"] = {}

                for part, number in inputs:
                    if part in ingredients.keys():
                        new_ingredients[part]["requirements"][item] = number * new_status["multiplier"]
                    else:
                        new_ingredients[part] = {"requirements": {item: number * new_status["multiplier"]},
                                                 "required": number * new_status["multiplier"],
                                                 "supplied": 0}

                    new_status["inputs"][part] = new_status["multiplier"] * number

            

        ingredients = deepcopy(new_ingredients)
        all_solved = True
        for item, status in ingredients.items():
            status["required"] = sum([num for _, num in status["requirements"].items()])
            status["leftover"] = status["supplied"] - status["required"]
            status["solved"] = status["leftover"] >= 0
            all_solved &= (status["solved"])

    return ingredients

parts_list = parse_parts_and_recipes("recipes.ods") 