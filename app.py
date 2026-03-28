# Import python packages
import streamlit as st
import requests

# ✅ App title and description
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# ✅ Temporary fruit list (simple names for users)
fruit_list = [
    "Apple",
    "Banana",
    "Blueberries",
    "Strawberries",
    "Mango",
    "Pineapple",
    "Watermelon",
    "Lime"
]

# Name on smoothie
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# ✅ Multiselect with max selection limit
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

# ✅ Nutrition section (API call)
st.divider()
st.subheader("🍎 Nutrition Information (SmoothieFroot API)")

# Use the **first selected fruit** for the API call
if ingredients_list:
    selected_fruit = ingredients_list[0].lower()

    try:
        api_url = f"https://my.smoothiefroot.com/api/fruit/{selected_fruit}"
        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            st.dataframe(
                data=response.json(),
                use_container_width=True
            )
        else:
            st.warning(
                f"⚠️ Nutrition data not available for {ingredients_list[0]}"
            )

    except Exception as e:
        st.error("❌ Unable to reach the SmoothieFroot API.")
        st.caption(str(e))

else:
    st.info("Select at least one fruit to see nutrition information.")

# Submit button
st.divider()
submit_order = st.button("Submit Order")

if submit_order:
    if not name_on_order or not ingredients_list:
        st.error("❌ Please enter a name and choose at least one ingredient.")
    else:
        st.success("✅ Your smoothie order has been placed!", icon="🎉")
