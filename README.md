# Film Success Analysis Dashboard

A fully interactive data science dashboard to uncover **what makes a movie a hit or a flop**, using real-world film, economic, and language data. Built with Streamlit, SQL, Plotly, and Machine Learning, this project showcases my ability to combine **data engineering**, **EDA**, **feature engineering**, **ML modeling**, and **visual storytelling** to deliver business insights that could benefit companies like **Netflix, Sony Pictures, Universal Music Group, or Spotify**.

> _"Can we predict which movies will succeed at the box office based on budget, language, timing, and global markets?"_

---

## Dashboard Preview

<!-- Replace the placeholder image links with actual screenshots -->
| Tab | Description | Preview |
|-----|-------------|---------|
| Revenue vs. Budget | Compares film budgets and box office performance | ![Revenue vs Budget](screenshots/revenue_vs_budget.png) |
| Genre Analysis | Shows average revenue by genre | ![Genre Analysis](screenshots/genre_analysis.png) |
| Seasonality | Analyzes film success by release month | ![Seasonality](screenshots/seasonality.png) |
| Language Revenue | Reveals top-earning languages in film | ![Language Revenue](screenshots/language_revenue.png) |
| Hit Predictor | ML-based prediction of movie success | ![Hit Predictor](screenshots/hit_predictor.png) |
| Global Insights | Plots GDP vs population of film markets | ![Global Insights](screenshots/global_insights.png) |
| Language Market | Examines language population and reach | ![Language Market](screenshots/language_market.png) |
| Language Impact | Connects audience reach with revenue | ![Language Impact](screenshots/language_impact.png) |

---

## Project Highlights

-  **Built an end-to-end ML pipeline** to predict film success using logistic regression
-  **ETL + SQL analysis** across multiple sources: TMDb, OMDb, World Bank, and GeoNames
-  **Global market analysis** by language, GDP, population, and region
-  **Trained predictive model** using `sklearn` and deployed with `joblib`
-  **Custom interactive visualizations** using Plotly and Streamlit Tabs
-  **Modular architecture** with pipeline scripts, model training, and dashboard separation
-  **Scalable design** to integrate new predictors or charts with minimal refactoring

---

## What I Learned

- How to clean and structure data for ML using `pandas`, `sqlite3`, and SQL joins
- How to engineer features (e.g., release month, revenue ratios) from raw text and date columns
- How to build and interpret **logistic regression models**
- How to measure success metrics like **revenue per million speakers**
- How to deploy scalable dashboards for storytelling using **Streamlit**
- How to **merge economic indicators** like GDP and language markets with entertainment data

---

## Tech Stack

| Area | Technologies |
|------|--------------|
| Dashboard | Streamlit, Plotly |
| Machine Learning | Scikit-Learn (`LogisticRegression`, `StandardScaler`), joblib |
| Data Cleaning | Pandas, SQLite, SQL |
| Data Sources | TMDb, OMDb, World Bank API, GeoNames, pycountry |
| Packaging | Python 3.11+, virtualenv |
| ️ Structure | Modular: `app.py`, `train_model.py`, `scripts/init_db.py`, `scripts/data_pipeline.py` |
| Pipeline | Bash + Python scripts to refresh database and retrain model |

---

## Machine Learning Model: `Hit Predictor`

- **Model**: Logistic Regression
- **Input Features**: Budget, Release Month
- **Target Variable**: `is_hit` (based on revenue vs. budget ratio)
- **Preprocessing**: Scaled with `StandardScaler`
- **Training Pipeline**: `train_model.py`
- **Model Storage**: `ml/hit_predictor.pkl`
- **Deployed in Dashboard**: Tab 5 - “Hit Predictor”

---

## Database Schema

- `movies`: Core table with budget, revenue, language, release date
- `genres`: Linked by movie ID, contains genres
- `world_bank_data`: GDP and population by country (from API)
- `language_market`: Country-level speaker population by language

> Database is built using a combination of cleaned CSVs and live API ingestion.

---

## Challenges & Problem-Solving

This project pushed me to grow as both a data scientist and an engineer. Some of the most interesting and difficult challenges I faced included:

### Integrating Data from Disparate Sources
Merging data from APIs (TMDb, OMDb, World Bank) and CSVs required:
- Handling missing values, inconsistent country/language names
- Mapping countries to ISO codes using `pycountry` with fallback logic
- Designing ETL logic to clean, transform, and merge multi-source data

### Building a Predictive Model with Minimal Features
Predicting film success using only **budget** and **release month** presented two problems:
- Severe class imbalance (too many flops)
- Limited predictive power
I solved this by engineering a **dynamic threshold system** to define hits and tuning the logistic regression model with scaled inputs.

###  Making Scikit-Learn & Streamlit Work Together
Streamlit and Scikit-learn integration produced:
- `UserWarning: X does not have valid feature names`
- Type mismatches between user input and trained model format  
The fix was to **standardize feature inputs as named Pandas DataFrames**, matching the scaler and model expectations exactly.

### Analyzing Language Markets Across Countries
Aggregating film success by **language** (not country) meant:
- Accounting for languages spoken across many nations (e.g. Spanish, Arabic)
- Calculating total population and GDP by language, not just by geography
- Resolving ambiguous mappings like "Korea" → "South Korea"

> These challenges taught me to build robust data pipelines, debug complex integration issues, and deliver real-world insights at scale — skills directly transferable to roles at companies like Netflix, Sony, or Universal Music Group.

---

## Chart-by-Chart Explanation

### 1. Revenue vs. Budget
- **What it shows**: Outliers and clusters of hit vs. flop movies
- **Insight**: Some low-budget films outperform big blockbusters

### 2. Genre Analysis
- **What it shows**: Which genres have the highest average revenue
- **Insight**: Action, Adventure, and Animation consistently outperform

### 3. Seasonality
- **What it shows**: Distribution of box office revenue by release month
- **Insight**: Summer and holiday months dominate

### 4.️ Language Revenue
- **What it shows**: Total revenue by language of the film
- **Insight**: English is dominant, but other markets are rising

### 5. Hit Predictor
- **What it does**: Predicts "HIT" or "FLOP" using ML model
- **Insight**: Helps studios evaluate financial potential pre-release

### 6. Global Insights (GDP vs Population)
- **What it shows**: Size and wealth of potential film markets
- **Insight**: High-GDP countries don't always have large populations

### 7. Language Market
- **What it shows**: Total number of speakers and countries per language
- **Insight**: Languages like Spanish, Hindi, and Arabic are globally distributed

### 8. Language Impact
- **What it shows**: Revenue per million speakers
- **Insight**: Helps identify under-leveraged language markets with high potential ROI

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/film-success-analysis.git
cd film-success-analysis

# 2. Create virtual environment and activate
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database and model
python scripts/init_db.py
python scripts/data_pipeline.py
python train_model.py

# 5. Run the Dashboard
streamlit run app.py

# OR Run all steps in one command

# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/film-success-analysis.git
cd film-success-analysis

# 2. Run the setup and dashboard launcher
python run_all.py