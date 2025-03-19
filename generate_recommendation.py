import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load dataset
data = pd.read_csv('movies.csv') 

# Step 2: Preprocess features
selectedFeatures = ['genres', 'keywords', 'overview', 'tagline', 'cast', 'director']
for feature in selectedFeatures:
    data[feature] = data[feature].fillna("")

# Step 3: Combine features into a single string
comFeatures = data['genres'] + ' ' + data['keywords'] + ' ' + data['overview'] + ' ' + data['tagline'] + ' ' + data['cast'] + ' ' + data['director']

# Step 4: Convert text to feature vectors
vectorizer = TfidfVectorizer()
featureVector = vectorizer.fit_transform(comFeatures)

# Step 5: Calculate similarity scores
similarity = cosine_similarity(featureVector)

# Step 6: Save everything
pickle.dump(similarity, open('similarity.pkl', 'wb'))
data.to_csv('movies.csv', index=False)