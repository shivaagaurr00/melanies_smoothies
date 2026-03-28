# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Create Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# App title and description
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# Get fruit data (display + search values)
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)

# Convert Snowpark DF → Pandas DF
pd_df = my_dataframe.to_pandas()

# Name on smoothie
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Multiselect (limit = 5)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

        # 🎯 Use SEARCH_ON instead of FRUIT_NAME
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

        # Nutrition section
        st.subheader(fruit_chosen + " Nutrition Information")

        fruityvice_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        if fruityvice_response.status_code == 200:
            st.dataframe(
                fruityvice_response.json(),
                use_container_width=True
            )
        else:
            st.warning("Nutrition data not found.")

    ingredients_string = ingredients_string.rstrip(", ")
``
