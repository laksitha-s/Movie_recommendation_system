from flask import Flask, request, render_template
import pandas as pd
import pickle
import difflib
import os
import gdown

app = Flask(__name__)

# Google Drive File ID for similarity.pkl (Replace with your actual file ID)
FILE_ID = "1koUbcZbnTFHKQaLjNC6x-LGR-IbAZI5l"
FILE_PATH = "similarity.pkl"

# Download similarity.pkl if it doesn't exist
if not os.path.exists(FILE_PATH):
    print("Downloading similarity.pkl...")
    gdown.download(f"https://drive.google.com/uc?export=download&id={FILE_ID}", FILE_PATH, quiet=False)

# Load preprocessed data
movies = pd.read_csv('movies.csv')

# Load similarity matrix
with open(FILE_PATH, 'rb') as f:
    similarity = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    error_message = ''
    
    if request.method == 'POST':
        movie_name = request.form['movie'].strip().lower()
        
        listTitles = movies['title'].str.lower().tolist()
        findCloseMatch = difflib.get_close_matches(movie_name, listTitles)

        if not findCloseMatch:
            error_message = "Oops! Movie not found. Please try another."
        else:
            closeMatch = findCloseMatch[0]
            movieIndex = movies[movies['title'].str.lower() == closeMatch]['index'].values[0]

            similarityScore = list(enumerate(similarity[movieIndex]))
            SortedSimilarMovies = sorted(similarityScore, key=lambda x: x[1], reverse=True)

            recommendations = [
                movies.iloc[movie[0]]['title'] for movie in SortedSimilarMovies[:10]
            ]
    
    return render_template('index.html', recommendations=recommendations, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
