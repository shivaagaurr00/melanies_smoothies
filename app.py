# Import python packages
import streamlit as st

# NOTE:
# This app runs outside Snowflake, so Snowpark imports are NOT available

# ✅ App title and description
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# ✅ Temporary fruit list (replace with Snowflake later)
fruit_list = [
    "Apple", "Banana", "Blueberries", "Strawberries",
    "Mango", "Pineapple", "Dragon Fruit", "Lime"
]

# Name on smoothie
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Multiselect with max selection limit
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Build ingredients string
ingredients_string = ""

if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)
    st.write("Your smoothie will include:", ingredients_string)

# Submit button
submit_order = st.button("Submit Order")

if submit_order:
    if not name_on_order or not ingredients_list:
        st.error("❌ Please enter a name and choose at least one ingredient.")
    else:
        st.success("✅ Your smoothie order has been placed!", icon="🎉")
