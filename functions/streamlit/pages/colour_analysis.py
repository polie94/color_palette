import streamlit as st
import os
from functions.cv.seasonal_images import *

def colour_analysis():
    """ A function that render the first page of the web app
        Contains following elements:
        1. Upload of an image
        2. A call to a transformer model for img segmentation and further processing
        4. Display the seasonal and subseasonal output images
        Args:
            None
        Returns:
            None
    """
    st.title("Colour Analysis")

    img = st.file_uploader(
        label="Upload your picture!",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False)
    st.divider()

    if img:
        img = Image.open(img)
        st.image(image=img.resize((100, 100)),
                caption="Your Uploaded Image")
        
        st.divider()
        with st.spinner("Wait for it...", show_time=True):
            img_prep = ImagePrep(img=img)
            img_prep.prepare_output()

        col_winter, col_spring, col_summer, col_autumn = st.columns(4)

        season_cols = {
            "winter": col_winter,
            "spring": col_spring,
            "summer": col_summer,
            "autumn": col_autumn
            }

        for season, col in season_cols.items():
            with col:
                st.title(season.title())
                st.image(f"seasonales_output/{season}.jpg")

                with st.expander("See subseasons"):
                    imgs_subseason = [
                        file for file in os.listdir("subseasonales_output")
                        if season in file
                    ]                
                    for img_name in imgs_subseason:
                        img = Image.open(f"subseasonales_output/{img_name}")
                        img_caption = img_name.split(".")[0] \
                                                .replace("_", " ") \
                                                .title()
                        st.image(image=img,
                                caption=img_caption)
        
