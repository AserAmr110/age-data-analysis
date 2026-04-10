import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Age Insights Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('cleaned_df.csv')

df_main = load_data()

st.title("Global Longevity Insights")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Data Explorer", "Geographical Insights", "Distribution Analysis"])

with tab1:
    st.header("Search and Raw Data")

    search_query = st.text_input("Search records (e.g. name or country):", "")

    if search_query:
        mask = df_main.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        df_display = df_main[mask]
    else:
        df_display = df_main

    st.info(f"Total records found: {len(df_display)}")
    st.dataframe(df_display.head(100), use_container_width=True)

with tab2:
    st.header("Country-wise Comparison")

    col_c, col_d = st.columns([1, 4])

    with col_c:
        option = st.selectbox(
            "Ranking Type:",
            ("Top 10", "Bottom 10"),
            key="geo_select"
        )

    is_ascending = True if option == "Bottom 10" else False

    max_age_by_country = df_main.groupby('country')['age_of_death'].max().sort_values(ascending=is_ascending).head(10)
    max_age_df = max_age_by_country.reset_index()
    max_age_df.columns = ['country', 'max_age']

    with col_d:
        fig2 = px.bar(
            max_age_df,
            x='country',
            y='max_age',
            color='max_age',
            title=f"{option} Countries by Maximum Age at Death",
            color_continuous_scale=px.colors.sequential.Viridis,
            template="plotly_dark"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Insights")

    avg_age = df_main['age_of_death'].mean()
    max_age = df_main['age_of_death'].max()
    min_age = df_main['age_of_death'].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Age", f"{avg_age:.1f}")
    col2.metric("Max Age", f"{max_age}")
    col3.metric("Min Age", f"{min_age}")

    st.write("Observation Summary:")
    st.write("- There is a clear difference between the countries with the highest and lowest life expectancy.")
    st.write("- Some countries experience very high life expectancies, often linked to healthcare quality.")
    st.write("- The distribution may be influenced by factors such as health, lifestyle, and socio-economic conditions.")

with tab3:
    st.header("Age Distribution and Occupation Analysis")

    col_a, col_b = st.columns([1, 3])

    with col_a:
        st.subheader("Filters")
        min_val = int(df_main['age_of_death'].min())
        max_val = int(df_main['age_of_death'].max())

        age_range = st.slider(
            "Select Age Range:",
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val),
            key="dist_slider"
        )


    filtered_df = df_main[(df_main['age_of_death'] >= age_range[0]) & (df_main['age_of_death'] <= age_range[1])]

    with col_b:
        fig1 = px.histogram(
            filtered_df,
            x='age_of_death',
            nbins=30,
            title=f'Distribution of Age at Death ({age_range[0]} - {age_range[1]})',
            template="plotly_dark",
            color_discrete_sequence=['#00CC96']
        )
        st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    st.subheader("Occupational Analysis")

    avg_age_by_occ = df_main.groupby("occupation")["age_of_death"].mean().sort_values(ascending=False).head(10)
    avg_age_df = avg_age_by_occ.reset_index()
    avg_age_df.columns = ['occupation', 'Average Age by occ']

    fig4 = px.bar(
        avg_age_df, 
        x='occupation', 
        y='Average Age by occ',
        title='Top 10 Occupations with Highest Average Age at Death',
        color='Average Age by occ',
        template='plotly_dark'
    )
    fig4.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)
