import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load datasets
movies = pd.read_csv('movies.csv')
credits = pd.read_csv('credits.csv')

# merge datasets on id
movies = movies.merge(credits, on='title')

# keep important columns
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# remove missing values
movies.dropna(inplace=True)

# convert to string
movies['overview'] = movies['overview'].astype(str)
movies['genres'] = movies['genres'].astype(str)
movies['keywords'] = movies['keywords'].astype(str)

# create tags
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# similarity
similarity = cosine_similarity(vectors)

# save files
pickle.dump(movies.to_dict(), open('movie_dict.pkl','wb'))
pickle.dump(similarity, open('similarity.pkl','wb'))

print("✅ Model created successfully!")