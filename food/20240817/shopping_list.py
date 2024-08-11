import pandas as pd
from collections import defaultdict

# Aggregating all ingredients into a shopping list
shopping_list = defaultdict(float)

# Extracted ingredients from all recipes
ingredients = [
    "450g large shrimp, peeled and deveined", 
    "4 garlic cloves, thinly sliced", 
    "1 red chili, finely chopped", 
    "2 tbsp fresh parsley, chopped", 
    "Juice of 1 lemon", 
    "2 tbsp olive oil", 
    "Salt and pepper to taste", 
    "12 slices of chorizo (200g)", 
    "12 Medjool dates, pitted", 
    "1 tbsp olive oil", 
    "1 tsp fresh thyme leaves", 
    "480ml heavy cream", 
    "240ml whole milk", 
    "150g granulated sugar", 
    "1 tbsp pure vanilla extract", 
    "1/2 tsp xanthan gum", 
    "Pinch of salt", 
    "1 medium butternut squash (approx. 1.2kg)", 
    "3 tbsp honey", 
    "2 tbsp orange juice", 
    "Olive oil", 
    "Salt and pepper", 
    "800g variety of ripe tomatoes, sliced", 
    "1 small red onion, thinly sliced", 
    "1/4 cup fresh basil leaves", 
    "2 tbsp red wine vinegar", 
    "3 tbsp olive oil", 
    "Salt and pepper to taste", 
    "1.5 ripe avocados (about 225g)", 
    "300g dark chocolate, melted", 
    "1.5 tbsp cocoa powder (for rolling)", 
    "1.5 tsp vanilla extract", 
    "200g red lentils, soaked for at least 4 hours", 
    "2 large eggs", 
    "1 tsp baking powder", 
    "Optional seasonings: herbs, spices, seeds", 
    "450g ground chicken", 
    "60g gluten-free breadcrumbs", 
    "1 large egg", 
    "1 tsp Italian seasoning", 
    "1 garlic clove, minced", 
    "Salt and pepper to taste", 
    "50ml tequila", 
    "25ml triple sec", 
    "25ml fresh lime juice", 
    "Salt for rimming the glass", 
    "Ice cubes"
]

# # Aggregating ingredients into the shopping list
for item in ingredients:
    item_split = item.split("^ ")
    for i in item_split:
        shopping_list[i] += 1


# Removing commas in the shopping list text
shopping_list_no_commas = {ingredient.replace(",", ""): quantity for ingredient, quantity in shopping_list.items()}

# Creating a DataFrame for the shopping list without commas
shopping_list_df_no_commas = pd.DataFrame(list(shopping_list_no_commas.items()), columns=["Ingredient", "Quantity"])

# Saving the shopping list to a document file
file_path_shopping_list = "/tmp/food/Recipe_Shopping_List.xlsx"
shopping_list_df_no_commas.to_excel(file_path_shopping_list, index=False)

file_path_shopping_list
