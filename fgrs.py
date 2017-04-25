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
#All in one DataFrame
df1 = pd.merge(users, ratings, on='user_id')
df = pd.merge(df1, items, on='movie_id')
#Users who has rated movies atleast 60 movies
top_users = df.groupby('user_id').size().sort_values(ascending=False)[:497]

#active_users and training_users - pd.Series()
active_users = top_users.sample(frac=(50/497.0))
training_users = top_users.drop(active_users.index)
#Make feature vectors for training users 
#tu_data - DataFrame(), Get deyails of the users which are in training_users
tu_data = df.loc[df['user_id'].isin(training_users)]
#Get age of all users which are in  tu_data
tu_age = tu_data['age']
tu_ages = tu_age.drop_duplicates()
#Apply fuzzy logic to age feature.
#Implementing fuzzy sets
#Use young(), middle(), old() of Age class
#Use very_bad(), bad(), average(), good(), very_good(), excellent() of GIM class
age_columns = ['age', 'age_young', 'age_middle', 'age_old']
tu_fuzzy_ages = pd.DataFrame(columns=age_columns)
a = Age()
j=0
for i in tu_ages:
    x =  [i, a.young(i), a.middle(i), a.old(i)]
    tu_fuzzy_ages.loc[j] = x
    j = j+1
g = GIM()
print 'GIM Example for value gim = 3.5:', g.very_bad(3.5), g.bad(3.5), g.average(3.5), g.good(3.5), g.very_good(3.5), g.excellent(3.5) 
#Example of fuzzy distance between two age 18 and 23 and their fuzzy
x = [g.very_bad(3.5), g.bad(3.5), g.average(3.5), g.good(3.5), g.very_good(3.5), g.excellent(3.5)]
y = [g.very_bad(2.5), g.bad(2.5), g.average(2.5), g.good(2.5), g.very_good(2.5), g.excellent(2.5)]
print x, y
print "Fuzzy distance between gim 3.5 and 2.5: ", fuzzy_dist(2.5, 3.5, np.array(x), np.array(y))

#Gim for active users:
def tr(i):
    count = df.loc[df['user_id']==i]
    total=0
    for k in count['rating']:
        total = total + k 
    return total
#Genre rating of Genre Gj for user ui.
def gr(j):
    gr1 = 0
    for i in range(0,19):
        print j['Action']

def gim_final(i,j):
    #get movies rated by user ui
    user_ui_movies = df.loc[df['user_id']==i]
    tf = user_ui_movies.shape[0]
    print tf
    tr = 0
    for k in user_ui_movies['rating']:
        tr = tr + k
    
    gr_array = np.zeros((tf, 19))
    k=0
    for movie in user_ui_movies['movie_id']:
        gr_array[k] = gr(movie)
        k = k+1
    
print gim_final(11, 1)
