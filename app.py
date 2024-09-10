import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load Data
df_fuel_consumption = pd.read_pickle(r"dataframe.pkl")

# Set up the Streamlit app layout
st.set_page_config(page_title="Fuel Consumption Analysis", page_icon="⛽", layout="wide")
st.title("Fuel Consumption and CO2 Emissions Analysis")

# Add GitHub icon with a button link to the top right
st.markdown(
    """
    <style>
    .github-link {
        position: absolute;
        right: 20px;
        top: 10px;
        text-decoration: none;
    }
    .github-link:hover {
        opacity: 0.8;
    }
    .github-link img {
        width: 32px;
    }
    .github-button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: #fff;
        background-color: #24292e;
        border-radius: 5px;
        text-decoration: none;
        margin-top: 10px;
        margin-right: 10px;
    }
    .github-button:hover {
        background-color: #444;
    }
    </style>

    <a href="https://github.com/shubham9760/CO2-Emission" class="github-link" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Link">
    </a>

    <a href="https://github.com/shubham9760/CO2-Emission" class="github-button" target="_blank">
        View on GitHub
    </a>
    """,
    unsafe_allow_html=True
)


# Sidebar options
st.sidebar.header("Navigation")
option = st.sidebar.selectbox(
    "Choose a view",
    [
        "CO2 Emission by Make",
        "CO2 Emission for MiniCompact Cars",
        "Fuel Consumption vs CO2 Emission",
        "CO2 Emission by Number of Cylinders",
        "CO2 Emission by Fuel Type",
        "Maximum and Minimum CO2 Emission",
        "Fuel Consumption by Make (City vs Highway)",
        "Top 5 Models with Highest CO2 Emission"
    ]
)

# Helper function for bar plot labels
def add_bar_labels(ax):
    """Add labels on top of bars in a plot."""
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10, color='black')

# Display content based on the sidebar selection
if option == "CO2 Emission by Make":
    st.header("CO2 Emission by Make")
    df_consumption_by_make = df_fuel_consumption.groupby("MAKE")["CO2EMISSIONS"].mean().sort_values(ascending=False).head(5)
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    ax1.bar(df_consumption_by_make.index, df_consumption_by_make.values, color='teal')
    ax1.set_xlabel("Make")
    ax1.set_ylabel("CO2 Emission")
    ax1.set_title("Top 5 Makes by CO2 Emission", fontsize=14, fontweight='bold')
    add_bar_labels(ax1)
    st.pyplot(fig1)

elif option == "CO2 Emission for MiniCompact Cars":
    st.header("CO2 Emission for MiniCompact Cars")
    df_make_model_emission = df_fuel_consumption.groupby(["MAKE", "VEHICLECLASS"])["CO2EMISSIONS"].mean().reset_index()
    minicompact_df = df_make_model_emission[df_make_model_emission["VEHICLECLASS"] == "MINICOMPACT"].sort_values(by="CO2EMISSIONS", ascending=False)
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    minicompact_df.plot(kind="bar", x="MAKE", y="CO2EMISSIONS", ax=ax2, color='lightcoral')
    ax2.set_xlabel("Make")
    ax2.set_ylabel("CO2 Emission")
    ax2.set_title("CO2 Emission for MiniCompact Cars", fontsize=14, fontweight='bold')
    add_bar_labels(ax2)
    st.pyplot(fig2)

elif option == "Fuel Consumption vs CO2 Emission":
    st.header("Fuel Consumption vs CO2 Emission")
    fig3 = px.scatter(df_fuel_consumption, x="FUELCONSUMPTION_COMB_MPG", y="CO2EMISSIONS",
                      title="Fuel Consumption vs CO2 Emission", labels={"FUELCONSUMPTION_COMB_MPG": "Fuel Consumption (MPG)", "CO2EMISSIONS": "CO2 Emission"},
                      color="CO2EMISSIONS", color_continuous_scale="Viridis")
    st.plotly_chart(fig3)

elif option == "CO2 Emission by Number of Cylinders":
    st.header("CO2 Emission by Number of Cylinders")
    df_cylinders = df_fuel_consumption.groupby("CYLINDERS")["CO2EMISSIONS"].mean().reset_index()
    fig4, ax4 = plt.subplots(figsize=(6, 3))
    ax4.scatter(df_cylinders["CYLINDERS"], df_cylinders["CO2EMISSIONS"], color='royalblue', marker='o')
    ax4.set_xlabel("Number of Cylinders")
    ax4.set_ylabel("CO2 Emission")
    ax4.set_title("CO2 Emission by Number of Cylinders", fontsize=14, fontweight='bold')
    st.pyplot(fig4)

elif option == "CO2 Emission by Fuel Type":
    st.header("CO2 Emission by Fuel Type")
    df_fueltype = df_fuel_consumption.groupby("FUELTYPE")["CO2EMISSIONS"].mean().reset_index()
    fig5 = px.bar(df_fueltype, x="FUELTYPE", y="CO2EMISSIONS", title="CO2 Emission by Fuel Type",
                  labels={"FUELTYPE": "Fuel Type", "CO2EMISSIONS": "CO2 Emission"}, color="CO2EMISSIONS", color_continuous_scale="Plasma")
    st.plotly_chart(fig5)

elif option == "Maximum and Minimum CO2 Emission":
    st.header("Maximum and Minimum CO2 Emission")
    max_co2 = df_fuel_consumption[df_fuel_consumption['CO2EMISSIONS'] == df_fuel_consumption['CO2EMISSIONS'].max()]
    min_co2 = df_fuel_consumption[df_fuel_consumption['CO2EMISSIONS'] == df_fuel_consumption['CO2EMISSIONS'].min()]
    st.subheader("Car with Maximum CO2 Emission")
    st.write(max_co2[['MAKE', 'MODEL', 'CO2EMISSIONS']])
    st.subheader("Car with Minimum CO2 Emission")
    st.write(min_co2[['MAKE', 'MODEL', 'CO2EMISSIONS']])

elif option == "Fuel Consumption by Make (City vs Highway)":
    st.header("Fuel Consumption by Make (City vs Highway)")
    df_fuel_by_make = df_fuel_consumption.groupby("MAKE")[["FUELCONSUMPTION_CITY", "FUELCONSUMPTION_HWY"]].mean().sort_values(by="FUELCONSUMPTION_HWY", ascending=False).head(5)
    fig6, ax6 = plt.subplots(figsize=(6, 3))
    df_fuel_by_make.plot(kind="line", marker='o', ax=ax6)
    ax6.set_xlabel("Make")
    ax6.set_ylabel("Fuel Consumption (MPG)")
    ax6.set_title("Fuel Consumption (City vs Highway)", fontsize=14, fontweight='bold')
    st.pyplot(fig6)

elif option == "Top 5 Models with Highest CO2 Emission":
    st.header("Top 5 Models with Highest CO2 Emission")
    top5_models = df_fuel_consumption.groupby("MODEL")["CO2EMISSIONS"].mean().sort_values(ascending=False).head(5)
    st.write(top5_models.reset_index())