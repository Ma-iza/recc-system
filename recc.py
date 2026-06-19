import pandas as pd
import requests
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

ROOT_DIR = Path(__file__).resolve().parent
METADATA_PATH = ROOT_DIR / "movies_metadata.csv"

if not METADATA_PATH.exists():
    raise FileNotFoundError(
        f"Required data file not found: {METADATA_PATH}. "
        "Make sure movies_metadata.csv is present in the repo root."
    )

metadata = pd.read_csv(METADATA_PATH)
metadata = metadata.reset_index(drop=True)
metadata = metadata[
    metadata["overview"].notna()
]
metadata = metadata.head(10000)

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(
    metadata["overview"]
)


metadata = metadata[
    metadata["id"].notna()
]
metadata = metadata[
    metadata["id"].astype(str).str.isnumeric()
]
metadata["id"] = metadata["id"].astype(int)

indices = pd.Series(
    metadata.index,
    index=metadata["title"].str.strip()
).drop_duplicates()

def recommend(title, top_n=5):

    idx = indices[title]

    sim_scores = linear_kernel(
        tfidf_matrix[idx:idx+1],
        tfidf_matrix
    ).flatten()

    movie_indices = sim_scores.argsort()[
        -(top_n+1):
    ][::-1]

    movie_indices = movie_indices[1:]

    return metadata[
        ["title", "id"]
    ].iloc[movie_indices]


API_KEY = "693efc985281c060e807d38aa436dab0"


def fetch_poster(movie_id):

    try:

        url = (
            f"https://api.themoviedb.org/3/movie/"
            f"{movie_id}?api_key={API_KEY}"
        )

        data = requests.get(url).json()

        poster_path = data.get(
            "poster_path"
        )

        if poster_path:

            return (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

    except:
        pass

    return None
