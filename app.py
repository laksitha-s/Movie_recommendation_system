from flask import Flask, request, render_template
import pandas as pd
import pickle
import difflib

app = Flask(__name__)

# Load preprocessed data
movies = pd.read_csv('movies.csv')
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    error_message = ''
    
    if request.method == 'POST':
        movie_name = request.form['movie']
        movie_name = movie_name.strip().lower()
        
        listTitles = movies['title'].str.lower().tolist()
        
        findCloseMatch = difflib.get_close_matches(movie_name, listTitles)
        
        if not findCloseMatch:
            error_message = "Oops! Movie not found. Please try another."
        else:
            closeMatch = findCloseMatch[0]
            movieIndex = movies[movies['title'].str.lower() == closeMatch]['index'].values[0]

            similarityScore = list(enumerate(similarity[movieIndex]))

            SortedSimilarMovies = sorted(similarityScore, key=lambda x: x[1], reverse=True)

            i = 0
            for movie in SortedSimilarMovies:
                index = movie[0]
                titleFromIndex = movies.iloc[index]['title']
                if i < 10:
                    recommendations.append(titleFromIndex)
                    i += 1
    
    return render_template('index.html', recommendations=recommendations, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
