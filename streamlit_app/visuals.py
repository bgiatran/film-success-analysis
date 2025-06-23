# streamlit_app\visuals.py

# imports
import plotly.express as px
import pandas as pd

def budget_vs_revenue_scatter(df):
    """
    Creates an interactive scatter plot showing the relationship between movie budgets and revenues.
    Useful for spotting outliers and checking whether bigger budgets tend to lead to higher revenue.
    """
    fig = px.scatter(
        df,
        x="budget",
        y="revenue",
        hover_data=["title", "release_date", "language"],  # Show these on hover
        title="Budget vs Revenue",
        labels={"budget": "Budget ($)", "revenue": "Revenue ($)"}
    )
    # Style the markers for better visibility
    fig.update_traces(marker=dict(size=12, color='royalblue', opacity=0.7))
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    return fig

def genre_bar_chart(genre_df):
    """
    Creates a bar chart showing average revenue per genre.
    Expects a DataFrame with genre as the index and a column called 'avg_revenue'.
    """
    fig = px.bar(
        genre_df,
        x=genre_df.index,  # Genres as categories
        y="avg_revenue",
        title="Average Revenue by Genre",
        labels={"genre": "Genre", "avg_revenue": "Avg Revenue"}
    )
    return fig

def release_seasonality_chart(df):
    """
    Line chart showing average movie revenue by release month.
    Helps visualize seasonal trends — for example, summer or holiday blockbusters.
    """
    # Extract release month from the full release date
    df["month"] = pd.to_datetime(df["release_date"]).dt.month

    # Group by month and calculate the mean revenue for each
    month_avg = df.groupby("month")["revenue"].mean().reset_index()

    fig = px.line(
        month_avg,
        x="month",
        y="revenue",
        title="Seasonality of Movie Releases",
        labels={"month": "Month", "revenue": "Avg Revenue"}
    )
    return fig

def language_revenue_chart(df):
    """
    Bar chart showing the top 10 languages by total revenue across all movies.
    Useful for understanding which language markets are most profitable.
    """
    # Aggregate revenue by language and sort descending
    lang_rev = df.groupby("language")["revenue"].sum().sort_values(ascending=False).head(10)

    fig = px.bar(
        lang_rev,
        x=lang_rev.index,    # Language codes or names
        y=lang_rev.values,   # Total revenue per language
        title="Top 10 Languages by Revenue",
        labels={"x": "Language", "y": "Total Revenue"}
    )
    return fig