import pandas as pd

# Creating a tabulated timetable for the preparation and cooking schedule

# Data for the timetable
timetable_data = {
    "Time": [
        "9:00 AM - 9:15 AM",
        "9:15 AM - 9:20 AM",
        "9:20 AM - 9:30 AM",
        "9:30 AM - 9:35 AM",
        "9:35 AM - 9:50 AM",
        "10:00 AM - 10:15 AM",
        "10:15 AM - 10:55 AM",
        "10:15 AM - 10:25 AM",
        "10:25 AM - 11:05 AM",
        "10:25 AM - 10:35 AM",
        "11:00 AM - 11:10 AM",
        "11:10 AM - 11:35 AM",
        "11:35 AM - 11:45 AM",
        "11:45 AM - 12:00 PM",
        "1:00 PM - 1:10 PM",
        "2:00 PM - 2:10 PM",
        "2:30 PM - 2:45 PM",
        "4:00 PM - 4:10 PM",
        "4:10 PM - 4:25 PM",
        "4:45 PM - 4:55 PM",
        "5:00 PM - 5:30 PM"
    ],
    "Task": [
        "Prepare Vanilla Ice Cream base",
        "Chill Ice Cream mixture",
        "Melt chocolate, mash avocado for truffles",
        "Chill truffle mixture",
        "Slice tomatoes, onion, prepare basil",
        "Peel, cut, season butternut squash",
        "Roast butternut squash",
        "Blend and prepare lentil bread batter",
        "Bake lentil bread",
        "Prepare marinated olives (optional)",
        "Mix chicken meatballs ingredients",
        "Bake chicken meatballs",
        "Assemble chorizo and date skewers",
        "Roast chorizo skewers",
        "Prepare margarita mix and chill",
        "Churn ice cream",
        "Roll and coat chocolate avocado truffles",
        "Slice garlic, chop chili, prepare parsley",
        "Cook garlic shrimp with chili",
        "Assemble and dress tomato salad",
        "Reheat dishes as needed, serve margaritas"
    ],
    "Recipe": [
        "Vanilla Ice Cream with Xanthan Gum",
        "Vanilla Ice Cream with Xanthan Gum",
        "Chocolate Avocado Truffles",
        "Chocolate Avocado Truffles",
        "Tomato Salad",
        "Butternut Squash with Orange Oil and Burnt Honey",
        "Butternut Squash with Orange Oil and Burnt Honey",
        "Lentil Bread",
        "Lentil Bread",
        "Marinated Olives (Optional)",
        "Chicken Meatballs",
        "Chicken Meatballs",
        "Chorizo and Date Skewers",
        "Chorizo and Date Skewers",
        "Classic Margarita",
        "Vanilla Ice Cream with Xanthan Gum",
        "Chocolate Avocado Truffles",
        "Garlic Shrimp with Chili",
        "Garlic Shrimp with Chili",
        "Tomato Salad",
        "Final Reheat and Serve"
    ]
}

# Creating a DataFrame for the timetable
timetable_df = pd.DataFrame(timetable_data)

# Saving the timetable to a document file
file_path_timetable = "/tmp/food/Recipe_Preparation_Timetable.xlsx"
timetable_df.to_excel(file_path_timetable, index=False)

file_path_timetable
