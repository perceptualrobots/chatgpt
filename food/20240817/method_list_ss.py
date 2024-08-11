import pandas as pd

# Data to be included in the spreadsheet
data = {
    "Recipe": [
        "Vanilla Ice Cream with Xanthan Gum", "Vanilla Ice Cream with Xanthan Gum", "Vanilla Ice Cream with Xanthan Gum",
        "Vanilla Ice Cream with Xanthan Gum", "Vanilla Ice Cream with Xanthan Gum", "Vanilla Ice Cream with Xanthan Gum",
        "Vanilla Ice Cream with Xanthan Gum", "Vanilla Ice Cream with Xanthan Gum",
        "Chocolate Avocado Truffles", "Chocolate Avocado Truffles", "Chocolate Avocado Truffles",
        "Chocolate Avocado Truffles", "Chocolate Avocado Truffles",
        "Butternut Squash with Orange Oil and Burnt Honey", "Butternut Squash with Orange Oil and Burnt Honey",
        "Butternut Squash with Orange Oil and Burnt Honey", "Butternut Squash with Orange Oil and Burnt Honey",
        "Lentil Bread (Flourless)", "Lentil Bread (Flourless)", "Lentil Bread (Flourless)", "Lentil Bread (Flourless)",
        "Tomato Salad", "Tomato Salad", "Tomato Salad", "Tomato Salad",
        "Chicken Meatballs", "Chicken Meatballs", "Chicken Meatballs", "Chicken Meatballs",
        "Chorizo and Date Skewers", "Chorizo and Date Skewers", "Chorizo and Date Skewers",
        "Garlic Shrimp with Chili", "Garlic Shrimp with Chili", "Garlic Shrimp with Chili", "Garlic Shrimp with Chili",
        "Classic Margarita", "Classic Margarita", "Classic Margarita"
    ],
    "Steps": [
        "Measure 480ml heavy cream", "Measure 240ml whole milk", "Measure 150g granulated sugar",
        "Combine the cream, milk, and sugar in a saucepan", "Heat mixture over medium heat until hot but not boiling",
        "Add 1 tablespoon vanilla extract", "Whisk in 1/2 teaspoon xanthan gum until fully combined",
        "Chill the mixture in the refrigerator for several hours until cold",
        "Melt 300g dark chocolate in the microwave or over a double boiler", "Mash 1.5 ripe avocados (about 225g) until smooth",
        "Combine the melted chocolate with the mashed avocado", "Stir in 1.5 teaspoons vanilla extract",
        "Chill the mixture in the refrigerator until firm",
        "Preheat the oven to 220°C (430°F)", "Peel, deseed, and cut 1 medium butternut squash (about 1.2kg) into wedges",
        "Toss the squash with olive oil, salt, and pepper", "Place the squash on a baking tray",
        "Measure 200g red lentils and soak them in water for at least 4 hours", "Drain the soaked lentils and blend them in a food processor until smooth",
        "Add 2 large eggs to the lentil mixture", "Add 1 teaspoon baking powder and 1/2 teaspoon salt to the mixture",
        "Slice 800g of ripe tomatoes", "Thinly slice 1 small red onion", "Prepare 1/4 cup of fresh basil leaves",
        "Arrange the sliced tomatoes on a serving plate",
        "Preheat the oven to 190°C (375°F)", "Mix 450g ground chicken with 60g gluten-free breadcrumbs, 1 large egg, 1 teaspoon Italian seasoning, and 1 minced garlic clove",
        "Shape the chicken mixture into meatballs", "Place the meatballs on a baking sheet lined with parchment paper",
        "Preheat the oven to 200°C (400°F)", "Wrap each of 12 Medjool dates (pitted) with a slice of chorizo (200g total)",
        "Secure each with a toothpick", "Slice 4 garlic cloves thinly", "Finely chop 1 red chili", "Chop 2 tablespoons of fresh parsley", "Juice 1 lemon",
        "Measure 50ml tequila", "Measure 25ml triple sec", "Measure 25ml fresh lime juice"
    ],
    "Final Steps": [
        "Churn the ice cream mixture in an ice cream maker", "Transfer the ice cream to a container and freeze until firm", None, None, None, None, None, None,
        "Roll the mixture into small truffle-sized balls", "Roll each ball in cocoa powder to coat", None, None, None, None, None, None, None,
        "Pour the lentil mixture into a loaf tin lined with parchment paper", "Bake the lentil bread in the preheated oven for 35-40 minutes until a toothpick inserted into the center comes out clean",
        "Allow the bread to cool completely before slicing", None, None, None, None, None,
        "Bake the meatballs in the preheated oven for 20-25 minutes until cooked through", None, None, None, None, None,
        "Roast the skewers in the preheated oven for 10-15 minutes until the chorizo is crispy", None, None, None,
        "Add the tequila, triple sec, and lime juice to a cocktail shaker filled with ice cubes", "Shake well until chilled",
        "Strain into a prepared glass and serve immediately"
    ]
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
file_path_spreadsheet = "/mnt/data/Recipe_Steps_and_Final_Steps.xlsx"
df.to_excel(file_path_spreadsheet, index=False)

file_path_spreadsheet
