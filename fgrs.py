import pandas as pd
import numpy as np
a = Age()
g = GIM()
def eucledian(A,B):
    return np.linalg.norm(A-B)

def fuzzy_dist(a, b, A, B):
    return abs(a-b)*eucledian(A,B)

def fuzzy_distance(ui, uj):
    fuzzy_dis = []
    for i in range(0,19):
        ui_gim = np.array([g.very_bad(ui[i]), g.bad(ui[i]), g.average(ui[i]), g.good(ui[i]), g.very_good(ui[i]), g.excellent(ui[i])])
        uj_gim = np.array([g.very_bad(uj[i]), g.bad(uj[i]), g.average(uj[i]), g.good(uj[i]), g.very_good(uj[i]), g.excellent(uj[i])])
        fuzzy_dis.append(fuzzy_dist(ui[i], uj[i], ui_gim, uj_gim))
    
    ui_gim = np.array([a.young(ui[i]), a.middle(ui[i]), a.old(ui[i])])
    uj_gim = np.array([a.young(uj[i]), a.middle(uj[i]), a.old(uj[i])])
    fuzzy_dis.append(fuzzy_dist(ui[i], uj[i], ui_gim, uj_gim))
    print fuzzy_dis

#print fuzzy_dist(35, 40, np.array([3, 4 ,5]), np.array([4, 5, 6]))
#Data Details
#users_cols ='user_id', 'age', 'sex', 'occupation', 'zip_code'
#ratings_cols = 'user_id', 'movie_id', 'rating', 'unix_timestamp'
#i_cols = ['movie_id', 'movie_title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
# 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
# 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
#All in one DataFrame
mr_ur = pd.merge(load_data.users, load_data.ratings, on='user_id')
df = pd.merge(mr_ur, load_data.items, on='movie_id')
m_cols = ['unknown', 'Action', 'Adventure',
     'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
     'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'age', 'user_id']
model_data_au = pd.DataFrame(columns=m_cols)
feature_row = pd.DataFrame(columns=m_cols)
model_data_pu = pd.DataFrame(columns=m_cols)
#Users who has rated movies atleast 60 movies
top_users = load_data.df.groupby('user_id').size().sort_values(ascending=False)[:497]
    
for i in range(0,5):
    #active_users and passive_users - pd.Series()
    active_users = top_users.sample(frac=0.10)
    training_active_users = active_users.sample(frac=0.34)
    testing_active_users = active_users.drop(training_active_users.index)
    passive_users = top_users.drop(active_users.index)
    
    tau_data = df.loc[df['user_id'].isin(training_active_users)][:10]
    index = np.arange(0,tau_data.shape[0])
    i=0
    print index
    for key, value in tau_data.iterrows():
        user_ui_movies = df.loc[df['user_id']==value['user_id']]
        feature_array = []
        feature_array = gim.gim_final(user_ui_movies, value['user_id'])
        #print 'GIM array', feature_array
        feature_array[19], feature_array[20] = value['age'], value['user_id']
        #print feature_array.shape
        feature_row = pd.DataFrame(feature_array)
        model_data_au = model_data_au.append(feature_row)
    #print model_data_au
    #print model_data_au
    #Working with passive users
    i=0
    pu_data = df.loc[df['user_id'].isin(passive_users)][:10]
    
    for key, value in pu_data.iterrows():
        user_ui_movies = df.loc[df['user_id']==value['user_id']]
        feature_array_p = gim.gim_final(user_ui_movies, value['user_id'])
        #print 'GIM array', feature_array
        feature_array_p[19], feature_array_p[20] = value['age'], value['user_id']
        #print feature_array.shape
        feature_row = pd.DataFrame(feature_array_p)
        model_data_pu = model_data_pu.append(feature_row)
    print feature_array, feature_array_p
    fuzzy_distance(feature_array, feature_array_p)
    #print model_data_pu
