# Import required libraries
import streamlit as st
import sqlite3
import pandas as pd
import joblib
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import pycountry

# Import custom chart functions from visuals.py
from visuals import (
    budget_vs_revenue_scatter,
    genre_bar_chart,
    release_seasonality_chart,
    language_revenue_chart
)

# Button in sidebar to fully reset and rerun the data pipeline
if st.sidebar.button("Reset DB and Rerun Pipeline"):
    st.sidebar.warning("Rebuilding the database... This may take a few seconds.")
    with st.spinner("Reinitializing and rerunning pipeline..."):
        base = os.path.dirname(os.path.dirname(__file__))
        init_script = os.path.join(base, "scripts", "init_db.py")
        pipeline_script = os.path.join(base, "scripts", "data_pipeline.py")

        # Recreate the database and reimport all data
        subprocess.run(["python", init_script])
        subprocess.run(["python", pipeline_script])

    st.sidebar.success("Database rebuilt and repopulated.")

# Set the dashboard page configuration
st.set_page_config(page_title="Film Success Analysis", layout="wide")

# Page title and short description
st.title("Film Success Analysis Dashboard")
st.markdown("""
A data-driven dashboard that explores what makes a movie a **hit** or a **flop**, based on real-world data.

- Data from: TMDb, OMDb, GeoNames, World Bank  
- Analysis: SQL + Pandas + ML  
- Prediction Model: Logistic Regression
""")

# Connect to the SQLite database
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "film.db")
conn = sqlite3.connect(DB_PATH)

# Load key datasets from the database
df = pd.read_sql("SELECT * FROM movies", conn)
gdp_df = pd.read_sql("SELECT * FROM world_bank_data", conn)
lang_market_df = pd.read_sql("SELECT * FROM language_market", conn)

# Create multiple tabs for different parts of the analysis
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Revenue vs. Budget",
    "Genres",
    "Seasonality",
    "Languages",
    "Hit Predictor",
    "Global Insights",
    "Language Market",
    "Language Impact"
])

with tab1:
    st.subheader("Revenue vs. Budget")
    fig = budget_vs_revenue_scatter(df)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Average Revenue by Genre")
    genre_df = pd.read_sql("""
        SELECT genre, AVG(revenue) as avg_revenue
        FROM genres JOIN movies USING(movie_id)
        GROUP BY genre
    """, conn).set_index("genre")
    fig = genre_bar_chart(genre_df)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Seasonality of Releases")
    fig = release_seasonality_chart(df)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Revenue by Language")
    fig = language_revenue_chart(df)
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("Hit Predictor")

    # Check if the ML model file exists
    if os.path.exists("ml/hit_predictor.pkl"):
        bundle = joblib.load("ml/hit_predictor.pkl")
        model = bundle["model"]
        scaler = bundle["scaler"]
        feature_names = bundle["feature_names"]

        # User input
        budget = st.slider("Budget ($)", 1_000_000, 300_000_000, 50_000_000, step=1_000_000)
        release_month = st.selectbox("Release Month", list(range(1, 13)))

        # Format input as a DataFrame with proper feature names
        X_input = pd.DataFrame({
            feature_names[0]: [float(budget)],
            feature_names[1]: [float(release_month)]
        })

        # Scale and preserve feature names
        scaled_input = pd.DataFrame(
            scaler.transform(X_input),
            columns=feature_names
        )

        # Predict
        prediction = model.predict(scaled_input)[0]
        prob = model.predict_proba(scaled_input)[0][1]

        st.metric("Prediction", "HIT" if prediction else "FLOP", f"{prob*100:.1f}% confidence")

        st.markdown("**Feature Importance**")
        weights = model.coef_[0]
        st.write({
            feature_names[0]: round(weights[0], 3),
            feature_names[1]: round(weights[1], 3)
        })
    else:
        st.error("Model not found. Please train it and place it at `ml/hit_predictor.pkl`.")

with tab6:
    st.subheader("Global Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**GDP vs Population**")
        gdp_filtered = gdp_df.dropna()
        gdp_filtered["log_gdp"] = gdp_filtered["gdp"].apply(lambda x: np.log10(x) if x > 0 else 0)

        fig_gdp = px.scatter(
            gdp_filtered, x="log_gdp", y="population_gdp",
            title="GDP vs Population",
            labels={"log_gdp": "Log(GDP $)", "population_gdp": "Population"},
            hover_data=["iso_code"]
        )
        st.plotly_chart(fig_gdp, use_container_width=True)

    with col2:
        st.markdown("**Top Languages by Population**")
        lang_group = lang_market_df.groupby("language")["population"].sum().sort_values(ascending=False).head(15)

        fig_lang = px.bar(
            lang_group,
            x=lang_group.values,
            y=lang_group.index,
            orientation="h",
            title="Most Spoken Languages"
        )
        st.plotly_chart(fig_lang, use_container_width=True)

with tab7:
    st.subheader("Language Market Overview")

    col1, col2 = st.columns(2)

    with col1:
        lang_pop = lang_market_df.groupby("language")[["population"]].sum().sort_values(by="population", ascending=False).head(15)
        fig_lang_pop = px.bar(lang_pop, x="population", y=lang_pop.index, orientation="h",
                              title="Top Languages by Population")
        st.plotly_chart(fig_lang_pop, use_container_width=True)

    with col2:
        lang_country_count = lang_market_df.groupby("language")["country"].nunique().sort_values(ascending=False).head(15)
        fig_lang_count = px.bar(lang_country_count, x=lang_country_count.values, y=lang_country_count.index,
                                orientation="h", title="Languages Spoken in Most Countries")
        st.plotly_chart(fig_lang_count, use_container_width=True)

    st.markdown("**Explore Countries for Selected Language**")
    selected_lang = st.selectbox("Choose a language", sorted(lang_market_df["language"].unique()))
    lang_country_df = lang_market_df[lang_market_df["language"] == selected_lang].sort_values(by="population", ascending=False)
    st.dataframe(lang_country_df.reset_index(drop=True))

with tab8:
    st.subheader("Language Impact on Revenue & Audience")

    def get_iso(country_name):
        try:
            country = pycountry.countries.lookup(country_name)
            return getattr(country, "alpha_3", None)
        except LookupError:
            return None

    merged_df = pd.merge(
        df[["title", "language", "revenue"]],
        lang_market_df[["language_code", "language", "country", "population"]],
        how="left",
        left_on="language",
        right_on="language_code"
    )

    reach_df = merged_df.groupby(["title", "language_x", "revenue"]).agg({"population": "sum"}).reset_index()
    reach_df["revenue_per_million"] = reach_df.apply(
        lambda row: row["revenue"] / (row["population"] / 1_000_000) if row["population"] > 0 else 0,
        axis=1
    )

    st.markdown("### Top Audience Reach")
    st.dataframe(
        reach_df.sort_values(by="population", ascending=False).head(10)
        .rename(columns={"language_x": "language", "population": "Global Language Population"})
    )

    st.markdown("### Revenue per Million Speakers")
    top_ratio = reach_df[reach_df["population"] > 0].sort_values(by="revenue_per_million", ascending=False).head(10)
    fig_ratio = go.Figure(go.Bar(
        x=top_ratio["revenue_per_million"],
        y=top_ratio["title"],
        orientation="h",
        marker=dict(color="green")
    ))
    fig_ratio.update_layout(title="Revenue per Million Global Speakers", xaxis_title="Revenue per Million ($)")
    st.plotly_chart(fig_ratio, use_container_width=True)

    if "iso_code" not in lang_market_df.columns:
        lang_market_df["iso_code"] = lang_market_df["country"].apply(get_iso)

    lang_gdp_raw = pd.merge(
        lang_market_df,
        gdp_df[["iso_code", "gdp"]],
        on="iso_code",
        how="inner"
    ).dropna(subset=["population", "gdp"])

    summary = (
        lang_gdp_raw
        .groupby("language")
        .agg(total_population=("population", "sum"),
             avg_gdp=("gdp", "mean"),
             countries=("iso_code", "nunique"))
        .sort_values(by="total_population", ascending=False)
        .head(20)
    )

    fig_lang_gdp = px.scatter(
        summary,
        x="avg_gdp",
        y="total_population",
        size="countries",
        text=summary.index,
        labels={"avg_gdp": "Average GDP of Speaker Countries (US$)", "total_population": "Total Speaker Population"},
        title="Language Market Potential — Population vs Economic Strength"
    )
    fig_lang_gdp.update_traces(textposition="top center")
    st.plotly_chart(fig_lang_gdp, use_container_width=True)

    st.markdown("### Comparison: GDP vs Population by Language")
    top_langs = lang_gdp_raw["language"].value_counts().head(10).index.tolist()
    bar_data = lang_gdp_raw[lang_gdp_raw["language"].isin(top_langs)].groupby("language").agg({
        "gdp": "mean",
        "population": "sum"
    }).reset_index()

    bar_long = bar_data.melt(id_vars="language", value_vars=["gdp", "population"],
                             var_name="Metric", value_name="Value")

    fig_bar = px.bar(
        bar_long,
        x="language",
        y="Value",
        color="Metric",
        barmode="group",
        title="Top Languages: Avg GDP vs Total Speaker Population"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### Global Population by Country")
    lang_map = lang_market_df.groupby("country")[["population"]].sum().reset_index()
    fig_map = px.choropleth(
        lang_map,
        locations="country",
        locationmode="country names",
        color="population",
        color_continuous_scale="Viridis",
        title="Global Population by Country (Language Market)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("Made by Bria Tran · Powered by Streamlit, SQL, Plotly & ML")

# Download button to export the movie dataset
st.download_button("Download Movie Dataset", data=df.to_csv(index=False), file_name="movies.csv", mime="text/csv")

# Close the database connection
conn.close()