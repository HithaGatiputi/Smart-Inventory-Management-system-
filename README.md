# Smart-Inventory-Management-system
kirana-demand-forecaster/
├── data/
│   ├── raw/                    # Kaggle data goes here
│   ├── processed/              # Cleaned + transformed
│   └── synthetic/              # Generated Indian patterns
├── backend/
│   ├── app.py                  # Flask entry point
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   ├── alerts.py
│   │   └── perishables.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── clustering.py       # K-Means
│   │   ├── classifier.py       # Decision Tree
│   │   ├── multiplier.py       # MultiplierEngine
│   │   └── pipeline.py         # Full ML pipeline
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── preprocessor.py
│   │   └── feature_engineer.py
│   └── utils/
│       ├── festival_calendar.json
│       ├── product_categories.json
│       └── area_profiles.json
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ContextPanel.jsx
│   │   │   ├── ForecastTable.jsx
│   │   │   └── AlertPanel.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
├── notebooks/
│   ├── 01_data_exploration.ipynb
…
