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
# Fruit data: UI display vs API search values
# ----------------------------
fruit_data = [
    {"FRUIT_NAME": "Apples", "SEARCH_ON": "Apple"},
    {"FRUIT_NAME": "Lime", "SEARCH_ON": "Lime"},
    {"FRUIT_NAME": "Ximenia", "SEARCH_ON": "Ximenia"},
    {"FRUIT_NAME": "Dragon Fruit", "SEARCH_ON": "Dragonfruit"},
    {"FRUIT_NAME": "Guava", "SEARCH_ON": "Guava"},
    {"FRUIT_NAME": "Figs", "SEARCH_ON": "Fig"},
    {"FRUIT_NAME": "Jack Fruit", "SEARCH_ON": "Jackfruit"},
    {"FRUIT_NAME": "Blueberries", "SEARCH_ON": "Blueberry"},
    {"FRUIT_NAME": "Vanilla Fruit", "SEARCH_ON": "Vanilla"},
    {"FRUIT_NAME": "Nectarine", "SEARCH_ON": "Nectarine"},
]

pd_df = pd.DataFrame(fruit_data)

# ----------------------------
# Name input
# ----------------------------
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# ----------------------------
# Ingredients (limit 5)
# ----------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

# ----------------------------
# Order filled status (✅ THIS IS THE KEY PART)
# ----------------------------
order_filled = st.checkbox("Mark this order as filled")

# ----------------------------
# Show nutrition information
# ----------------------------
if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

        # Look up API search value
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.write(
            "The search value for",
            fruit_chosen,
            "is",
            search_on
        )

        st.subheader(fruit_chosen + " Nutrition Information")

        api_url = "https://my.smoothiefroot.com/api/fruit/" + search_on
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            st.dataframe(
                response.json(),
                use_container_width=True
            )
        else:
            st.warning("Nutrition data not found.")

    ingredients_string = ingredients_string.rstrip(", ")
    st.write("Your smoothie will include:", ingredients_string)

# ----------------------------
# Submit order
# ----------------------------
st.divider()
submit_order = st.button("Submit Order")

if submit_order:
    if not name_on_order or not ingredients_list:
        st.error("❌ Please enter a name and select at least one ingredient.")
    else:
        st.success("✅ Order Submitted!", icon="🎉")
        st.write("👤 Name:", name_on_order)
        st.write("🥗 Ingredients:", ingredients_string)
        st.write("📦 Order Filled:", order_filled)
