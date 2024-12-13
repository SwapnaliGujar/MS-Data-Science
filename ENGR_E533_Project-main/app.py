# -*- coding: utf-8 -*-
"""
Deep Learning Systems - Semester Project Demo Application:
Authors: Swapnali Gujar, Joshua Jones, Siddhesh Pande
"""

import os
import base64
import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_extras.app_logo import add_logo
from functools import cache
import matplotlib.pyplot as plt


@cache
def display_logo(asset_path):
    """Display the application logo."""
    try:
        logo_path = os.path.join(asset_path, "MyProducePal_Logo.PNG")

        # Encode the logo as Base64 for embedding in HTML
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode()

    except FileNotFoundError:
        st.error("Logo file not found. Please check the path.")
        print(f"\n{logo_path=}\n")


    # st.image(logo_path, use_container_width=True, width=1200)
    # Apply CSS for padding
    st.markdown(
        """
        <style>
        .main {
            padding-left: 10%;
            padding-right: 10%;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .logo-container img {
            max-width: 1200px;
            width: 100%;
            height: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the logo with the HTML-based approach
    st.markdown(
        f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="MyProducePal Logo">
        </div>
        """,
        unsafe_allow_html=True
    )


@cache
def load_data(asset_path):
    """Load required data into DataFrames."""
    demo_results_path = os.path.join(asset_path, "demo_results_with_prices.csv")
    live_testing_path = os.path.join(asset_path, "live_testing.csv")

    demo_results = pd.read_csv(demo_results_path)
    live_testing = pd.read_csv(live_testing_path)

    image_options = {True: demo_results.Image, False: demo_results.Image}

    return demo_results, live_testing


def setup_page():
    """Set up the Streamlit page and configuration."""
    st.set_page_config(layout="centered")


def display_live_image(image_filename, caption=None):
    """Displays an image given image_filename"""

    try:
        # Load the image
        image_path = os.path.join(os.getcwd(), image_filename)
        image = Image.open(image_path)

        with st.container():
            st.markdown(
                """
                <style>
                .stContainer > div {
                    width: 60%;
                    margin: auto;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.image(image, 
                     use_container_width=False, 
                     width=400,
                     caption=caption)

    except FileNotFoundError:
        st.error("Image file not found. Please check the path.")
        print(f"\n{image_path=}\n")


def show_confidence_level_with_table(df, column='Probability'):
    confidence_filter = st.slider('Minimum Confidence Level (%)', 0, 100, 50)
    filtered_df = df[df[column] >= confidence_filter]
    sorted_df = filtered_df.sort_values(by=column, ascending=False)

    columns_to_drop = ["Price_per_unit_usd", "Unit"]
    sorted_df.drop(columns_to_drop, axis=1, inplace=True)
    sorted_df = sorted_df.set_index("Image")
    st.dataframe(sorted_df)


def plot_prediction_confidence(predictions, confidences):
    fig, ax = plt.subplots()
    ax.barh(predictions, confidences, color='skyblue')
    ax.set_xlabel('Confidence (%)')
    ax.set_title('Prediction Confidence')
    st.pyplot(fig)


def display_confidence(selected_row, font_size=20):
    if   selected_row['Probability'] >= 90:
        confidence_color = 'green'
    elif selected_row['Probability'] >= 70:
        confidence_color = 'orange'
    else:
        confidence_color = 'red'
    st.markdown(f"<span style='color:{confidence_color}; font-size:{font_size}px;'>Match Confidence: {selected_row['Probability']}%</span>", unsafe_allow_html=True)


def styled_write(label="", value="", font_size=20):
    st.markdown(
        f"<p style='font-size:{font_size}px;'><strong>{label}:</strong> {value}</p>",
        unsafe_allow_html=True
    )


def get_item_price(row, weight):
    try:
        total_price = round(float(row['Price_per_unit_usd']) * float(weight), 2)
    except ValueError:
        st.warning("Please enter a valid weight/count.")
    return total_price


def main():
    """Main function to control the app's flow."""
    non_header_font_size = 18
    
    asset_path = os.path.join(os.getcwd(), "app_assets")

    # Configure Page Options
    setup_page()

    # Load Image Data
    demo_results, live_testing = load_data(asset_path)

    # Setup Logo
    display_logo(asset_path)


    # Mode Selection
    mode_switch = st.toggle("Mode: Live Check-Out", True, key="data_source")
    
    if mode_switch:
        # Live Checkout Mode

        

        # df = live_testing
        df = demo_results
        df["Probability"] *= 100
        df = df.round(decimals=2)

        # Get the row corresponding to the selected image
        selected_image = st.selectbox("Select an image:", df["Image"])
        selected_row = df[df["Image"] == selected_image].iloc[0]


        # Display the weight and unit entered by the user
        # Create a text input for weight and a dropdown select for unit
        measure_unit = None
        match selected_row["Unit"]:
            case "Lb":
                measure_unit = "Weight"
            case "Oz":
                measure_unit = "Weight"
            case "Count":
                measure_unit = "Count"
            case _:
                measure_unit = "Count"

        weight = st.text_input(f'Enter Quantity in {measure_unit}:', '1')
        


        st.header("**Top Matches**")
        st.subheader(f"{selected_row['Prediction']}")
        # st.subheader(f"{selected_row['Prediction']} ({selected_row['Probability']:.0f}%)")
        col1, col2 = st.columns([2,3],gap='large', vertical_alignment='top')
        with col1:
            display_live_image(selected_row["Image_Path"])
        with col2:
            st.write("") # spacing
        #     styled_write("MyProducePal", selected_row["Prediction"], font_size=non_header_font_size)
        #     display_confidence(selected_row, font_size=non_header_font_size)
        # with col3:
        #     st.write("") # spacing
            styled_write("Unit", selected_row["Unit"], font_size=non_header_font_size)
            styled_write("Unit Price: $", f'{float(selected_row["Price_per_unit_usd"]):.2f}', font_size=non_header_font_size)
            styled_write("Total Price: $", f'{get_item_price(selected_row, weight):.2f}', font_size=non_header_font_size)
     
        # Add a button to show alternatives
        show_alternatives = st.button("Not seeing your produce item? Show alternatives")

        if show_alternatives:
            df = df[df["Prediction"] == selected_row['Prediction']]
            df = df.sort_values(by="Probability", ascending=False)
            df.drop_duplicates(subset="Label",inplace=True, keep='first')
            
            df = df[df["Label"] != selected_row['Prediction']]
            # print(df.head(15))

            # Exclude the top match (already shown above)
            alternatives = df.head(2)

            # Display 2nd and 3rd highest predictions
            st.header("**Alternatives**")
            for _, alt_row in alternatives.iterrows():
                st.subheader(f"{alt_row['Label']}")
                # st.subheader(f"{alt_row['Label']} ({alt_row['Probability']:.0f}%)")
                col1, col2 = st.columns([2,3],gap='large', vertical_alignment='top')
                # col1, col2, col3 = st.columns([3,3,3],gap='large', vertical_alignment='top')
                with col1:
                    display_live_image(alt_row["Image_Path"])
                with col2:
                    # st.write("") # spacing
                    # styled_write("MyProducePal", alt_row["Prediction"], font_size=non_header_font_size)
                    # display_confidence(alt_row, font_size=non_header_font_size)
                # with col3:
                    st.write("") # spacing
                    styled_write("Unit", alt_row["Unit"], font_size=non_header_font_size)
                    styled_write("Unit Price: $", f'{float(alt_row["Price_per_unit_usd"]):.2f}', font_size=non_header_font_size)
                    styled_write("Total Price: $", f'{get_item_price(alt_row, weight):.2f}', font_size=non_header_font_size)
            if alternatives.empty:
                styled_write(value="No Alternatives Found", font_size=non_header_font_size)

    else:
        # Historical Mode
        df = demo_results
        df["Probability"] *= 100
        df = df.round(decimals=2)

        # Get the row corresponding to the selected image
        selected_image = st.selectbox("Select an image:", df["Image"])
        selected_row = df[df["Image"] == selected_image].iloc[0]

        st.header("**Top Matches**")
        col1, col2 = st.columns([2, 3],gap='large', vertical_alignment='top')
        with col1:
            display_live_image(selected_row["Image_Path"])
        with col2:
            st.write("") # spacing
            styled_write("Actual Label", selected_row["Label"], font_size=non_header_font_size)
            styled_write("MyProducePal Label", selected_row["Prediction"], font_size=non_header_font_size)
            display_confidence(selected_row, font_size=non_header_font_size)


        show_confidence_level_with_table(df)

        # predictions = ['Apple', 'Banana', 'Orange']  
        # confidences = [85, 90, 75] 
        # plot_prediction_confidence(predictions, confidences)


# Run the app
if __name__ == "__main__":
    main()
