# Import python packages
import streamlit as st
import pandas as pd
import requests

# ----------------------------
# App Title
# ----------------------------
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# ----------------------------
# Fruit data (UI label vs API search value)
# This replaces the Snowflake FRUIT_OPTIONS table
# ----------------------------
fruit_data = [
    {"FRUIT_NAME": "Apples", "SEARCH_ON": "Apple"},
    {"FRUIT_NAME": "Blueberries", "SEARCH_ON": "Blueberry"},
    {"FRUIT_NAME": "Strawberries", "SEARCH_ON": "Strawberry"},
    {"FRUIT_NAME": "Raspberries", "SEARCH_ON": "Raspberry"},
    {"FRUIT_NAME": "Jack Fruit", "SEARCH_ON": "Jackfruit"},
    {"FRUIT_NAME": "Banana", "SEARCH_ON": "Banana"},
    {"FRUIT_NAME": "Watermelon", "SEARCH_ON": "Watermelon"},
]

# Convert to Pandas DataFrame
pd_df = pd.DataFrame(fruit_data)

# ----------------------------
# Name input
# ----------------------------
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# ----------------------------
# Multiselect (max 5)
# ----------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

# ----------------------------
# Show ingredients + nutrition
# ----------------------------
if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

        # ✅ Pandas LOC to get SEARCH_ON value
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.write(
            "The search value for",
            fruit_chosen,
            "is",
            search_on,
            "."
        )

        st.subheader(fruit_chosen + " Nutrition Information")

        api_url = "https://my.smoothiefroot.com/api/fruit/" + search_on
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            st.dataframe(response.json(), use_container_width=True)
        else:
            st.warning("Nutrition data not found.")

    ingredients_string = ingredients_string.rstrip(", ")
    st.write("Your smoothie will include:", ingredients_string)

# ----------------------------
# Submit button
# ----------------------------
st.divider()
submit_order = st.button("Submit Order")

if submit_order:
    if not name_on_order or not ingredients_list:
        st.error("❌ Please enter a name and choose at least one ingredient.")
    else:
        st.success("✅ Your smoothie order has been placed!", icon="🎉")
