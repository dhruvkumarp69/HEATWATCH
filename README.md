# HEATWATCH — Climate Intelligence Dashboard

A Streamlit dashboard for the NIErnaya 2026 Phase 2 climate / extreme-heat EDA project.

## Run locally (Mac / Windows / Linux)

```bash
cd HEATWATCH
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501. All five supplied CSV files are already included in `data/`.

## Deploy online with Streamlit Community Cloud

1. Create a GitHub repository and upload the contents of this folder.
2. Visit https://share.streamlit.io/ and connect GitHub.
3. Choose the repository, branch, and `app.py` as the main file.
4. Deploy. Keep the `data/` folder in the repository so the app can load the included datasets.

## Included datasets
- `temp_clean.csv`
- `temp_anomalies.csv`
- `heatwave_per_year.csv`
- `features_merged_1975_2019.csv`
- `IMD_Heat_Cold_Deaths_Cleaned.csv`

## Notes
Five-year block values in the heat/cold-wave series are annualised and flagged. Mortality comparisons are descriptive and should not be interpreted as causal attribution. Verify the source table and definitions before formal publication.
