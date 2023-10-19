from PIL import Image
import numpy as np

# Import necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


#setup logo at top
#image_path = Image.open('logo.jpg')
#st.image(image_path)
st.title("AI Powered Retention & Success")

# read prediction data that we saved as a csv file while working on the ai_accelerator_modelInsights_streamlit_v1.ipynb notebook
predictions = pd.read_csv("./prediction_output_students.csv", index_col=False)

max_rows = predictions.shape[0]  # calculates the number of rows in predictions dataset

# --------setting page config -------------------------------------------------------
im = Image.open("./logo.jpg")

col1, col2 = st.columns([8, 1])

with col1:
    st.header(":blue[Attrition Analysis - Kutztown University]")  # edit this for your usecase
    st.markdown(
        "Allows career advisors & faculty to understand student attrition risk and \
                gain insights into how to best support student success long term!"
    )
#with col2:
#    st.image("./logo.jpg", width=50)  # Image for logo
#    st.caption("**_Powered by Datarobot_**")


# -----Code to hide index when displaying dataframes--------
# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
# --------------------------------------------------------------------
# ------------Specify columns to display from prediction dataset
# This should be edited based on your usecase
columns = [
    [
        "Customer_ID_x",
        "Transfer Student",
        "Number_of_Advisor_Meetings",
        "Tenure_in_Days",
        "Internet_Type",
        "Internet_Service",
        "Degree Type",
        "Paperless_Billing",
        "Payment_Method",
        "Time_Spent_On_App",
        "Zip_Code",
        "Churn_Value_1_PREDICTION",
    ]
]
# ------------------------------------------------------------

# ----------------------------------Code to show different visualizations in the app
with st.container():
    with st.expander("Make your criteria selections"):
        threshold = st.slider(
            "Select churn interval", min_value=0.00, max_value=1.00, value=(0.0, 1.00)
        )
        max_rows = predictions[
            (predictions["Churn_Value_1_PREDICTION"] >= threshold[0])
            & (predictions["Churn_Value_1_PREDICTION"] <= threshold[-1])
        ].shape[
            0
        ]  # calculates the number of rows in predictions dataset based on churn threshold criteria
        display_rows = st.slider(
            "Select how many students you want to see within the interval ",
            min_value=1,
            max_value=max_rows,
            value=max_rows,
        )
    
    # columns to display in churn scores table
    columns_to_display = ["Customer_ID_x", "Churn_Value_1_PREDICTION"]
    # code to create dynamic dataframe based on user selection in the slider
    predictions_subset = (
        predictions[
            (predictions["Churn_Value_1_PREDICTION"] >= threshold[0])
            & (predictions["Churn_Value_1_PREDICTION"] <= threshold[-1])
        ]
        .sort_values(by="Churn_Value_1_PREDICTION", ascending=False)
        .reset_index(drop=True)
        .head(display_rows)
    )
    # Plot to show top churn reason
    plot_df = (
        predictions_subset["EXPLANATION_1_FEATURE_NAME"]
        .value_counts()
        .reset_index()
        .rename(
            columns={"index": "Feature_name", "EXPLANATION_1_FEATURE_NAME": "customers"}
        )
        .sort_values(by="customers")
    )
    fig = px.bar(
        plot_df,
        x="customers",
        y="Feature_name",
        orientation="h",
        title="Important Reasons Relating To Student Attrition",
        labels={'x': 'Students', 'y':'Reason'},
    )

with st.container():
    st.subheader(":blue[Attrition Risk Score And Key Insights]")

    col1, col2 = st.columns([1.5, 1])
    with col1:
        # st.markdown("**Top churn reasons**")
        tab1, tab2 = st.tabs(["View plot", "View data"])
        # Plot to show top reason for churn (prediction explanation ) by #customers
        tab1.plotly_chart(fig)
        # code to display the information in above plot as table
        tab2.markdown("")  # To skip a line in the UI
        tab2.markdown(":blue[**Top reason by #students**]")
        tab2.table(plot_df.sort_values(by="customers", ascending=False))
    with col2:
        st.markdown("")  # To skip a line in the UI
        st.markdown("")  # To skip a line in the UI
        st.markdown("")  # To skip a line in the UI
        st.markdown("")  # To skip a line in the UI
        st.markdown("")  # To skip a line in the UI

        # code to show dataframe in the app
        st.markdown("**Risk scores for students**")
        # st.write('Churn risk score')

        st.dataframe(
            predictions_subset[columns_to_display].rename(
                columns={
                    "Customer_ID_x": "Student_ID",
                    "Churn_Value_1_PREDICTION": "Attrition Risk Score",
                }
            )
        )
        # st.markdown('**Note**: _Churn label in the table above is based on the defualt churn threshold set for the deployment_')

if st.button('Send a personalized email notification to students at risk!'):
    st.write('Generating custom respsones for the 32 students and emailing them ...')
