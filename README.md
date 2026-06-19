# Recco

A Streamlit-based movie recommendation app that uses content-based filtering over movie overviews to suggest similar movies.

## What it does

- Loads movie metadata from `movies_metadata.csv`
- Builds a TF-IDF matrix over movie overviews
- Computes cosine similarity to recommend similar movies
- Displays recommendations in a Streamlit app with poster images and hoverable movie cards

## Files

- `app.py` - Streamlit app entry point
- `recc.py` - Recommendation logic and poster fetching
- `movies_metadata.csv` - Movie dataset used for recommendations
- `recc.ipynb` - Notebook for development / exploration

## Install

```bash
pip install streamlit pandas scikit-learn requests
```

## Run the app

From the repository root:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal.

## Notes

- The app uses an API key inside `recc.py` to fetch posters from TMDB.
- Make sure `movies_metadata.csv` is present in the project root and included in the deployed repo.
- Streamlit Cloud must receive `movies_metadata.csv` as part of the app files; otherwise the app cannot load recommendations.
- If the app renders HTML as text, use `unsafe_allow_html=True` in `st.markdown` only for the card markup.
