# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# ✅ Create Snowflake connection (UPDATED METHOD)
cnx = st.connection("snowflake")
session = cnx.session()

# App title and description
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# Get list of fruits from Snowflake
fruit_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").to_pandas()

# Name on smoothie
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Multiselect with max selection limit
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"],
    max_selections=5
)

# Build ingredients string
ingredients_string = ""

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

    ingredients_string = ingredients_string.rstrip(", ")
    st.write("Your smoothie will include:", ingredients_string)

# Submit button
submit_order = st.button("Submit Order")

# Insert order into Snowflake
if submit_order:

    if not name_on_order or not ingredients_list:
        st.error("❌ Please enter a name and choose at least one ingredient.")
    else:
        insert_stmt = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
            VALUES
                ('{name_on_order}', '{ingredients_string}', FALSE)
        """

        session.sql(insert_stmt).collect()

        st.success("✅ Your smoothie order has been placed!", icon="🎉")
