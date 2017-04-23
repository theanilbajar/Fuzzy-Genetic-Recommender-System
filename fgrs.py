import pandas as pd
import numpy as np
#Load data form MovieLens data
#Load users
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols, encoding='latin-1')
#load ratings
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols, encoding='latin-1')
#load genres
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
items = pd.read_csv('ml-100k/u.item', sep='|', names=i_cols,
 encoding='latin-1')

#Most rated movies
most_rated = ratings.groupby('movie_id').size().sort_values(ascending=False)
#Print top 50 movies sorted by number of ratings movies have.
#print most_rated[:50]
from fuzzy_sets import Age, GIM
#Use young(), middle(), old() of Age class
#Use very_bad(), bad(), average(), good(), very_good(), excellent() of GIM class

def eucledian(A,B):
    return np.linalg.norm(A-B)

def fuzzy_dist(a, b, A, B):
    return abs(a-b)*eucledian(A,B)
print fuzzy_dist(35, 40, np.array([3, 4 ,5]), np.array([4, 5, 6]))
