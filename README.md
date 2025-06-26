# Film Success Analysis Dashboard

The **Film Success Analysis Dashboard** is an interactive web analytics application built with Streamlit that explores what drives box office success across movies. By combining movie metadata with external APIs like World Bank, OMDb, and TMDB, the dashboard provides powerful visualizations and machine learning insights to analyze trends in budget, genre, seasonality, language, and global market potential.

This project demonstrates full-stack data integration, exploratory data analysis, machine learning for classification, and storytelling through visualization to surface insights about global film performance.

[Live Demo - Launch the Film Success Analysis Dashboard](https://film-success-analysis.streamlit.app/)

---

## Technology Stack

| Category            | Technology Used                          | Purpose                                                             |
|---------------------|------------------------------------------|---------------------------------------------------------------------|
| Programming         | Python                                   | Core development language                                           |
| Framework           | Streamlit                                | Web-based data dashboard                                            |
| Data Handling       | Pandas, NumPy                            | Data preprocessing, transformation, and manipulation                |
| Visualization       | Plotly, Altair                           | Interactive and high-quality charting                               |
| Machine Learning    | scikit-learn (Logistic Regression)       | Predicting hit potential based on budget and release month         |
| API Integration     | OMDb API, TMDB API, World Bank API       | Movie metadata, GDP, and population data                            |
| Country Intelligence| pycountry, REST Countries API            | Enriching language and country data                                 |
| Data Pipeline       | Custom ETL scripts                       | Modular ingestion and table population logic                        |

---

## Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/bgiatran/film-success-analysis.git
cd film-success-analysis
```

2. **Create a Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
```

3. **Install Required Packages**

```bash
pip install -r requirements.txt
```

4. **Run the Dashboard**

```bash
streamlit run streamlit_app\app.py
```

---

## Project Purpose & Significance

Understanding what makes a film successful is not just a creative question—it’s a strategic and financial challenge that impacts production decisions, marketing campaigns, and international distribution.

This project was built to explore the key factors that influence box office performance, including:

- What characteristics define a successful film—such as genre, budget, timing, and language.
- How global population, language reach, and economic strength affect market potential.
- Whether we can predict film success using a minimal set of quantifiable inputs.

As someone interested in both storytelling and data analytics, I wanted to examine how content, timing, and global audience dynamics come together to shape a film’s outcome. This dashboard was designed to combine:

- Data science and SQL-based insight generation
- Economic and language-driven market modeling
- Machine learning for early-stage outcome prediction

The result is a tool that simulates how real-world studios, producers, and analysts might evaluate project risk, audience strategy, and international opportunity before a film is released.

---

## Feature Walkthrough

<!-- 1. Revenue & Genre Analysis -->
<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Revenue & Genre Analysis</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>A scatterplot comparing film budget to global revenue</li>
      <li>A bar chart showing average revenue per film genre</li>
    </ul>
    <p><strong>Why it matters:</strong> These visualizations decode the classic risk vs. reward equation in filmmaking. The scatterplot helps detect outliers (e.g., low-budget high-revenue indie hits or expensive flops), while the genre chart reveals which genres consistently deliver strong financial performance.</p>
    <p><strong>Practical Use Cases:</strong></p>
    <ul>
      <li>Studios identifying high-ROI genres for upcoming slates</li>
      <li>Data-backed budgeting decisions for producers</li>
      <li>Strategic investment targeting for investors or financiers</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (101).png" alt="Revenue & Genre Analysis" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

---

<!-- 2. Seasonality & Language Revenue -->
<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Seasonality & Language Revenue</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Line chart of average revenue by release month</li>
      <li>Bar chart of top 10 languages by total box office revenue</li>
    </ul>
    <p><strong>Why it matters:</strong> The seasonality chart identifies revenue peaks (e.g., summer or holiday blockbusters), enabling optimized release strategies. The language chart highlights dominant linguistic markets, useful for distribution and dubbing prioritization.</p>
    <p><strong>Real-world use:</strong></p>
    <ul>
      <li>Release calendar planning for global markets</li>
      <li>Localization strategy for language-specific promotion</li>
      <li>Analyzing language-driven revenue disparities</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (102).png" alt="Seasonality & Language Revenue" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

---

<!-- 3. Hit Predictor + GDP-Population Context -->
<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Hit Predictor + Market Economics</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>An interactive ML model that predicts if a movie will be a “hit” based on budget and release timing</li>
      <li>GDP vs. population scatterplot by country</li>
    </ul>
    <p><strong>Why it matters:</strong> The hit predictor offers real-time decision support using basic features to estimate success probability — a powerful tool for producers during pre-greenlight stages. The GDP vs. population chart helps stakeholders target economically viable but under-tapped countries.</p>
    <p><strong>Practical Use Cases:</strong></p>
    <ul>
      <li>Greenlight gatekeeping with quick financial forecasting</li>
      <li>Market research for international expansion or first releases</li>
      <li>Feature importance analysis for model explainability</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (103).png" alt="Hit Predictor + GDP Population" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

---

<!-- 4. Language Deep Dive -->
<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Language Deep Dive</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Bar chart of top languages by speaker population</li>
      <li>Languages spoken across the most countries</li>
      <li>Language-to-country explorer table</li>
    </ul>
    <p><strong>Why it matters:</strong> This section provides a deeper understanding of linguistic reach and cultural targeting. Knowing which languages span across nations — and where they are most spoken — can unlock global viewership with minimal localization overhead.</p>
    <p><strong>Practical Use Cases:</strong></p>
    <ul>
      <li>Translating scripts for languages with global spread</li>
      <li>Finding multilingual growth regions for streaming platforms</li>
      <li>Boosting international content accessibility</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (104).png" alt="Language Deep Dive" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

---

<!-- 5. Global Language Monetization -->
<div style="display: flex; align-items: flex-start; gap: 20px; margin-bottom: 32px;">
  <div style="flex: 1;">
    <h3>Global Language Monetization</h3>
    <p><strong>What it shows:</strong></p>
    <ul>
      <li>Revenue-per-million-speakers bar chart for top global films</li>
      <li>Language GDP vs. speaker count bubble chart</li>
      <li>Choropleth map of world population distribution</li>
      <li>Bar chart comparing GDP and population per language</li>
    </ul>
    <p><strong>Why it matters:</strong> This set of visualizations uncovers untapped language markets with high revenue potential. By normalizing revenue by speaker count and layering GDP insights, studios can prioritize translations and releases where ROI is strongest.</p>
    <p><strong>Real-world use:</strong></p>
    <ul>
      <li>Pitching localization plans to producers and investors</li>
      <li>Choosing languages for subtitles and dubs based on economic potential</li>
      <li>Geopolitical insights for multi-market release campaigns</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <img src="./images/Screenshot (105).png" alt="Global Language Monetization" style="max-width: 100%; border-radius: 8px;" />
  </div>
</div>

---

## Key Contributions

- Built a modular ETL pipeline to aggregate and clean film metadata from OMDb, TMDB, and World Bank APIs.
- Designed multi-tab Streamlit dashboard with real-time interactivity and machine learning integration.
- Implemented logistic regression hit predictor with confidence score and feature importance display.
- Designed unique charts to highlight GDP/language/population patterns for international expansion.

---

## Future Improvements

- Expand the hit predictor with more features (genre, runtime, MPAA rating)
- Incorporate sentiment analysis of reviews
- Add real-time box office scraping for dynamic forecasting
- Introduce unsupervised clustering of films by performance profile

---

## Author

**Bria Tran**  
Data Analyst | Product Thinker | Film + Music Industry Enthusiast  
[GitHub](https://github.com/bgiatran) • [LinkedIn](https://linkedin.com/in/bria-tran)
