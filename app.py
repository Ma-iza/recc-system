import streamlit as st

st.set_page_config(
    page_title="Recco",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}
.movie-card {
    position: relative;
    width: 180px;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 10px;
    transition: transform 0.3s ease;
    cursor: pointer;
}
.movie-card:hover {
    transform: scale(1.08);
}
.movie-card img {
    width: 100%;
    display: block;
}
.movie-card .title-overlay {
    position: absolute;
    bottom: 0;
    width: 100%;
    background: rgba(0, 0, 0, 0.75);
    color: white;
    padding: 6px;
    font-size: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

from recc import metadata, recommend, fetch_poster

st.markdown("""
# 🎬 Recco

Discover movies similar to your favorites using
content-based machine learning recommendations.
""")

def movie_card(title, poster_url):
    return f"""
    <div class="movie-card">
        <img src="{poster_url}" alt="{title}" />
        <div class="title-overlay">{title}</div>
    </div>
    """

selected_movie = st.selectbox(
    "Choose a movie",
    metadata["title"].values
)

# show selected movie poster
selected_row = metadata[
    metadata["title"] == selected_movie
].iloc[0]

poster = fetch_poster(selected_row["id"])

left, center, right = st.columns([1, 2, 1])

with center:
    st.image(poster, width=300)
    st.markdown(f"## {selected_movie}")
if st.button("Recommend"):

    recommendations = recommend(selected_movie)

    if recommendations is None or recommendations.empty:
        st.warning("No recommendations found")

    else:
        st.subheader("Recommended Movies")

        cols = st.columns(5)

        for col, (_, movie) in zip(cols, recommendations.iterrows()):

            poster_url = fetch_poster(movie["id"])

            with col:
                st.markdown(
                    movie_card(movie["title"], poster_url),
                    unsafe_allow_html=True
                )