# Import python packages
import streamlit as st
import pandas as pd
import requests

# -------------------------------------------------
# Try to connect to Snowflake (only works in Snowflake)
# -------------------------------------------------
session = None
try:
    cnx = st.connection("snowflake")
    session = cnx.session()
    snowflake_available = True
except Exception:
    snowflake_available = False

# ----------------------------
# App Title
# ----------------------------
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# ----------------------------
# Fruit data (UI label vs API search value)
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
# Name on smoothie
# ----------------------------
name_on_order = st.text_input("Name on Smoothie:")

# ----------------------------
# Ingredient selection (max 5)
# ----------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

# ----------------------------
# Order filled status
# ----------------------------
order_filled = st.checkbox("Mark this order as filled")

# ----------------------------
# Nutrition info
# ----------------------------
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.subheader(fruit_chosen + " Nutrition Information")

        response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on,
            timeout=10
        )

        if response.status_code == 200:
            st.dataframe(response.json(), width="stretch")
        else:
            st.warning("Nutrition data not found.")

    st.write("Your smoothie will include:", ingredients_string)

# ----------------------------
# Submit Order
# ----------------------------
st.divider()
submit_order = st.button("Submit Order")

if submit_order:
    if not name_on_order or not ingredients_list:
        st.error("❌ Please enter a name and choose at least one ingredient.")
    else:
        if snowflake_available:
            insert_sql = """
                INSERT INTO smoothies.public.orders
                (name_on_order, ingredients, order_filled)
                VALUES (%s, %s, %s)
            """
            session.cursor().execute(
                insert_sql,
                (name_on_order, ingredients_string, order_filled)
            )
            st.success("✅ Order saved to Snowflake!", icon="🎉")
        else:
            st.warning(
                "⚠️ Snowflake is not available in this environment. "
                "The order was NOT saved."
            )

        st.write("Name:", name_on_order)
        st.write("Ingredients:", ingredients_string)
        st.write("Order Filled:", order_filled)
