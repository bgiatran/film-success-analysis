# app.py – Film Success Analysis Dashboard
# Author: Bria Tran
# Description: Streamlit dashboard that visualizes and predicts film success using SQL, machine learning, and API-enriched data.
# This version includes detailed in-code comments explaining key sections for portfolio and academic demonstration.

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

# Import custom visualization functions from visuals.py
from visuals import (
    budget_vs_revenue_scatter,
    genre_bar_chart,
    release_seasonality_chart,
    language_revenue_chart
)

# Sidebar Trigger: Full Pipeline Reset
# This button allows the user to reset the entire database and rerun all scripts,
# including schema creation, API fetching, data transformation, and ML model training.
if st.sidebar.button("Reset DB and Rerun Pipeline"):
    st.sidebar.warning("Rebuilding the database... This may take a few seconds.")
    with st.spinner("Reinitializing and rerunning full pipeline..."):
        base = os.path.dirname(os.path.dirname(__file__))
        # List of all scripts needed to fully refresh the pipeline
        scripts_to_run = [
            os.path.join(base, "database", "init_db.py"),
            os.path.join(base, "api_modules", "country_api.py"),
            os.path.join(base, "api_modules", "world_bank_api.py"),
            os.path.join(base, "scripts", "fetch_gdp_data.py"),
            os.path.join(base, "scripts", "populate_missing_tables.py"),
            os.path.join(base, "scripts", "data_pipeline.py"),
            os.path.join(base, "scripts", "train_model.py"),
        ]
        # Sequentially execute each script
        for script in scripts_to_run:
            subprocess.run(["python", script])
    st.sidebar.success("Database successfully rebuilt and repopulated.")

# App Layout Configuration
st.set_page_config(page_title="Film Success Analysis", layout="wide")
st.title("Film Success Analysis Dashboard")

# Database Connection Setup
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "film.db")
conn = sqlite3.connect(DB_PATH)

# Load Core Tables into DataFrames
df = pd.read_sql("SELECT * FROM movies", conn)  # Main movie dataset
gdp_df = pd.read_sql("SELECT * FROM world_bank_data", conn)  # GDP & population data
lang_market_df = pd.read_sql("SELECT * FROM language_market", conn)  # Language reach and country mapping

# Streamlit Tab Layout
# Consolidates content into four thematic tabs for improved UX
# 1. Revenue vs. Genre  2. Seasonality & Language  3. Prediction & Market Data  4. Language Deep Dive

# Create four distinct tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Revenue & Genres",
    "Season & Language",
    "Hit Predictor & Markets",
    "Language Deep Dive"
])

# TAB 1: Revenue & Genre Trends
# Analyzes how film budgets relate to success and highlights genre-level performance.
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue vs. Budget")
        fig = budget_vs_revenue_scatter(df)  # Scatter plot using Plotly
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Average Revenue by Genre")
        genre_df = pd.read_sql("""
            SELECT genre, AVG(revenue) as avg_revenue
            FROM genres JOIN movies USING(movie_id)
            GROUP BY genre
        """, conn).set_index("genre")
        fig = genre_bar_chart(genre_df)
        st.plotly_chart(fig, use_container_width=True)

    # Independent chart for population by language to set context for later sections
    st.subheader("Top Languages by Population")
    lang_group = lang_market_df.groupby("language")["population"].sum().sort_values(ascending=False).head(15)
    fig_lang = px.bar(lang_group, x=lang_group.values, y=lang_group.index, orientation="h", title="Most Spoken Languages")
    st.plotly_chart(fig_lang, use_container_width=True)

# TAB 2: Seasonal Release Behavior + Language Earnings
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Seasonality of Releases")
        fig = release_seasonality_chart(df)  # Monthly distribution
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenue by Language")
        fig = language_revenue_chart(df)
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: ML Prediction Tool + Global Market Chart
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hit Predictor")
        if os.path.exists("ml/hit_predictor.pkl"):
            bundle = joblib.load("ml/hit_predictor.pkl")
            model = bundle["model"]
            scaler = bundle["scaler"]
            feature_names = bundle["feature_names"]

            # User input for prediction features
            budget = st.slider("Budget ($)", 1_000_000, 300_000_000, 50_000_000, step=1_000_000)
            release_month = st.selectbox("Release Month", list(range(1, 13)))

            # Scale and predict
            X_input = pd.DataFrame({
                feature_names[0]: [float(budget)],
                feature_names[1]: [float(release_month)]
            })
            scaled_input = pd.DataFrame(scaler.transform(X_input), columns=feature_names)
            prediction = model.predict(scaled_input)[0]
            prob = model.predict_proba(scaled_input)[0][1]
            st.metric("Prediction", "HIT" if prediction else "FLOP", f"{prob*100:.1f}% confidence")

            # Show feature weights for interpretability
            weights = model.coef_[0]
            st.markdown("**Feature Importance**")
            st.write({feature_names[0]: round(weights[0], 3), feature_names[1]: round(weights[1], 3)})
        else:
            st.error("Model not found. Please train it and place it at `ml/hit_predictor.pkl`.")

    with col2:
        st.subheader("GDP vs Population")
        gdp_filtered = gdp_df.dropna()
        gdp_filtered["log_gdp"] = gdp_filtered["gdp"].apply(lambda x: np.log10(x) if x > 0 else 0)
        fig_gdp = px.scatter(gdp_filtered, x="log_gdp", y="population_gdp", title="GDP vs Population", hover_data=["iso_code"])
        st.plotly_chart(fig_gdp, use_container_width=True)

# TAB 4: Language Market Breakdown and Potential
with tab4:
    st.subheader("Language Deep Dive")

    # Comparative visuals on language population vs global reach
    col1, col2 = st.columns(2)
    with col1:
        lang_pop = lang_market_df.groupby("language")[["population"]].sum().sort_values(by="population", ascending=False).head(15)
        fig_lang_pop = px.bar(lang_pop, x="population", y=lang_pop.index, orientation="h", title="Top Languages by Population")
        st.plotly_chart(fig_lang_pop, use_container_width=True)

    with col2:
        lang_country_count = lang_market_df.groupby("language")["country"].nunique().sort_values(ascending=False).head(15)
        fig_lang_count = px.bar(lang_country_count, x=lang_country_count.values, y=lang_country_count.index, orientation="h", title="Languages Spoken in Most Countries")
        st.plotly_chart(fig_lang_count, use_container_width=True)

    # Interactive filter for exploring countries by language
    st.markdown("**Explore Countries for Selected Language**")
    selected_lang = st.selectbox("Choose a language", sorted(lang_market_df["language"].unique()))
    lang_country_df = lang_market_df[lang_market_df["language"] == selected_lang].sort_values(by="population", ascending=False)
    st.dataframe(lang_country_df.reset_index(drop=True))

    st.subheader("Language Impact on Revenue & GDP")

    # Merge language metadata with country GDP for deeper analysis
    def get_iso(country_name):
        try:
            country = pycountry.countries.lookup(country_name)
            return getattr(country, "alpha_3", None)
        except LookupError:
            return None

    if "iso_code" not in lang_market_df.columns:
        lang_market_df["iso_code"] = lang_market_df["country"].apply(get_iso)

    merged_df = pd.merge(
        df[["title", "language", "revenue"]],
        lang_market_df[["language_code", "language", "country", "population"]],
        how="left",
        left_on="language",
        right_on="language_code"
    )

    # Compute revenue per million speakers to assess market ROI
    reach_df = merged_df.groupby(["title", "language_x", "revenue"]).agg({"population": "sum"}).reset_index()
    reach_df["revenue_per_million"] = reach_df.apply(
        lambda row: row["revenue"] / (row["population"] / 1_000_000) if row["population"] > 0 else 0, axis=1
    )

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Revenue per Million Speakers")
        top_ratio = reach_df[reach_df["population"] > 0].sort_values(by="revenue_per_million", ascending=False).head(10)
        fig_ratio = go.Figure(go.Bar(x=top_ratio["revenue_per_million"], y=top_ratio["title"], orientation="h"))
        fig_ratio.update_layout(title="Revenue per Million Global Speakers", xaxis_title="Revenue per Million ($)")
        st.plotly_chart(fig_ratio, use_container_width=True)

    with col4:
        lang_gdp_raw = pd.merge(lang_market_df, gdp_df[["iso_code", "gdp"]], on="iso_code", how="inner").dropna()
        summary = lang_gdp_raw.groupby("language").agg(
            total_population=("population", "sum"), avg_gdp=("gdp", "mean"), countries=("iso_code", "nunique")
        ).sort_values(by="total_population", ascending=False).head(20)

        fig_lang_gdp = px.scatter(
            summary, x="avg_gdp", y="total_population", size="countries", text=summary.index,
            labels={"avg_gdp": "Avg GDP", "total_population": "Total Speakers"},
            title="Language Market Potential"
        )
        fig_lang_gdp.update_traces(textposition="top center")
        st.plotly_chart(fig_lang_gdp, use_container_width=True)

    # Final multi-metric comparison: GDP vs Population by Language + Choropleth map
    col5, col6 = st.columns(2)
    with col5:
        bar_data = lang_gdp_raw.groupby("language").agg({"gdp": "mean", "population": "sum"}).reset_index()
        bar_long = bar_data.melt(id_vars="language", value_vars=["gdp", "population"], var_name="Metric", value_name="Value")
        fig_bar = px.bar(bar_long, x="language", y="Value", color="Metric", barmode="group", title="GDP vs Population by Language")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col6:
        lang_map = lang_market_df.groupby("country")[["population"]].sum().reset_index()
        fig_map = px.choropleth(lang_map, locations="country", locationmode="country names", color="population", color_continuous_scale="Viridis", title="Global Population by Country")
        st.plotly_chart(fig_map, use_container_width=True)

# Footer & Download
st.markdown("Made by Bria Tran · Powered by Streamlit, SQL, Plotly & ML")
st.download_button("Download Movie Dataset", data=df.to_csv(index=False), file_name="movies.csv", mime="text/csv")
conn.close()