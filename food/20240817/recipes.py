import pandas as pd
import os



# Data for the table with full detailed methods and full ingredients list

# Adjusted data with formatted ingredients list as numbered lists with line feeds
data = {
    "Recipe Name": [
        "Garlic Shrimp with Chili", 
        "Chorizo and Date Skewers", 
        "Vanilla Ice Cream with Xanthan Gum", 
        "Butternut Squash with Orange Oil and Burnt Honey", 
        "Not Your Average Tomato Salad", 
        "4-Ingredient Chocolate Avocado Truffles", 
        "Healthy Lentil Bread (Flourless)", 
        "Healthy Baked Chicken Meatballs", 
        "Classic Margarita"
    ],
    "Servings": [
        "4", 
        "4-6", 
        "6-8", 
        "4", 
        "4", 
        "18 truffles", 
        "8 slices", 
        "4", 
        "1"
    ],
    "Ingredients (Full List)": [
        "1. 450g large shrimp, peeled and deveined\n2. 4 garlic cloves, thinly sliced\n3. 1 red chili, finely chopped\n4. 2 tbsp fresh parsley, chopped\n5. Juice of 1 lemon\n6. 2 tbsp olive oil\n7. Salt and pepper to taste", 
        "1. 12 slices of chorizo (200g)\n2. 12 Medjool dates, pitted\n3. 1 tbsp olive oil\n4. 1 tsp fresh thyme leaves", 
        "1. 480ml heavy cream\n2. 240ml whole milk\n3. 150g granulated sugar\n4. 1 tbsp pure vanilla extract\n5. 1/2 tsp xanthan gum\n6. Pinch of salt", 
        "1. 1 medium butternut squash (approx. 1.2kg)\n2. 3 tbsp honey\n3. 2 tbsp orange juice\n4. Olive oil\n5. Salt and pepper", 
        "1. 800g variety of ripe tomatoes, sliced\n2. 1 small red onion, thinly sliced\n3. 1/4 cup fresh basil leaves\n4. 2 tbsp red wine vinegar\n5. 3 tbsp olive oil\n6. Salt and pepper to taste", 
        "1. 1.5 ripe avocados (about 225g)\n2. 300g dark chocolate, melted\n3. 1.5 tbsp cocoa powder (for rolling)\n4. 1.5 tsp vanilla extract", 
        "1. 200g red lentils, soaked for at least 4 hours\n2. 2 large eggs\n3. 1 tsp baking powder\n4. 1/2 tsp salt\n5. Optional seasonings: herbs, spices, seeds", 
        "1. 450g ground chicken\n2. 60g gluten-free breadcrumbs\n3. 1 large egg\n4. 1 tsp Italian seasoning\n5. 1 garlic clove, minced\n6. Salt and pepper to taste", 
        "1. 50ml tequila\n2. 25ml triple sec\n3. 25ml fresh lime juice\n4. Salt for rimming the glass\n5. Ice cubes"
    ],
    "Method (Detailed)": [
        "1. Heat olive oil in a large pan over medium heat.\n2. Add garlic and chili, cook until fragrant.\n3. Add shrimp and cook until pink and cooked through, about 3-4 minutes.\n4. Stir in parsley and lemon juice, season with salt and pepper.\n5. Serve hot.", 
        "1. Preheat oven to 200°C.\n2. Wrap each date with a chorizo slice and secure with a toothpick.\n3. Arrange on a baking sheet, drizzle with olive oil, and sprinkle with thyme.\n4. Roast for 10-15 minutes until chorizo is crisp.", 
        "1. Heat cream, milk, and sugar until hot. Add vanilla.\n2. Mix xanthan gum with some cream mixture, then add back.\n3. Chill, churn in an ice cream maker, and freeze.", 
        "1. Preheat oven to 220°C.\n2. Cut butternut squash into wedges and toss with olive oil, salt, and pepper.\n3. Roast for 40 minutes until tender and caramelized.\n4. Meanwhile, in a small saucepan, heat honey until it starts to darken, then add orange juice and swirl to combine.\n5. Drizzle the burnt honey mixture over the roasted squash and serve.", 
        "1. Arrange the sliced tomatoes on a platter.\n2. Scatter the red onion slices and basil leaves over the tomatoes.\n3. Drizzle with red wine vinegar and olive oil.\n4. Season with salt and pepper, and serve immediately.", 
        "1. Melt the dark chocolate in a microwave or double boiler.\n2. In a bowl, mash the avocado until smooth, then mix in the melted chocolate and vanilla extract.\n3. Chill the mixture in the fridge until firm enough to scoop.\n4. Roll the mixture into balls and coat with cocoa powder.\n5. Store in the fridge until ready to serve.", 
        "1. Preheat oven to 180°C and line a loaf tin with parchment paper.\n2. Drain the soaked lentils and blend in a food processor until smooth.\n3. Add eggs, baking powder, salt, and any optional seasonings, and blend again until well combined.\n4. Pour the batter into the prepared loaf tin.\n5. Bake for 35-40 minutes, or until a toothpick inserted into the center comes out clean.\n6. Let cool completely before slicing.", 
        "1. Preheat the oven to 190°C and line a baking sheet with parchment paper.\n2. In a large bowl, combine the ground chicken, breadcrumbs, egg, Italian seasoning, garlic, salt, and pepper.\n3. Mix until well combined, then shape the mixture into meatballs.\n4. Place the meatballs on the prepared baking sheet and bake for 20-25 minutes, or until cooked through.\n5. Serve with your choice of sauce or sides.", 
        "1. Rub a lime wedge around the rim of a glass and dip it in salt to coat.\n2. Fill a cocktail shaker with ice cubes, then add the tequila, triple sec, and lime juice.\n3. Shake well until chilled.\n4. Strain into the prepared glass and serve immediately."
    ],
    "URL": [
        "N/A", 
        "N/A", 
        "N/A", 
        "https://ottolenghi.co.uk/pages/recipes/butternut-squash-orange-oil-burnt-honey", 
        "https://lorriegrahamblog.com/not-your-average-tomato-salad-ottolenghi/", 
        "https://www.eatingbirdfood.com/4-ingredient-chocolate-avocado-truffles/", 
        "https://www.ramonascuisine.com/healthy-lentil-bread-flourless/", 
        "https://feedthesoulblog.com/healthy-baked-chicken-meatballs/", 
        "https://www.bbc.co.uk/food/recipes/classicmargarita_84327"
    ]
}


# Creating a DataFrame
df = pd.DataFrame(data)

# Saving the DataFrame to a document file
file_path = "/tmp/food/Recipe_Summary_List_Full_Details.xlsx"
directory = os.path.dirname(file_path)

if not os.path.exists(directory):
    os.makedirs(directory)

df.to_excel(file_path, index=False)

# Displaying the table to the user
#import ace_tools as tools; tools.display_dataframe_to_user(name="Recipe Summary with Full Details", dataframe=df)

file_path
