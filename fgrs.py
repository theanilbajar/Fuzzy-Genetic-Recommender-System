""""""

# Import pandas and numpy
import pandas as pd
import numpy as np
import operator

from settings import NO_OF_GENRES, NO_OF_FEATURES
import load_data
import fuzzy_sets
import gim

# Create objects for Age and GIM to use for fuzzy sets
age = fuzzy_sets.Age()
gim_obj = fuzzy_sets.GIM()


def euclidean_dist(list_a, list_b):
    """Return the Euclidean distance between two array elements."""
    return np.linalg.norm(np.array(list_a) - np.array(list_b))


def fuzzy_dist(first_point, second_point, fuzzy_set_first_point, fuzzy_set_second_point):
    """Returns fuzzy distance between two values and their fuzzy sets."""
    return abs(first_point - second_point) * euclidean_dist(fuzzy_set_first_point, fuzzy_set_second_point)


def fuzzy_distance(ui, uj):
    """Returns fuzzy distance between given points."""

    fuzzy_dis = [0] * NO_OF_FEATURES

    # Get fuzzy set values for movie genres
    for i in range(0, NO_OF_GENRES):
        ui_gim = gim_obj.get_fuzzy_set(ui[i])
        uj_gim = gim_obj.get_fuzzy_set(uj[i])
        fuzzy_dis[i] = fuzzy_dist(ui[i], uj[i], ui_gim, uj_gim)

    # Get fuzzy set values for age
    ui_gim = age.get_fuzzy_set(ui[i])
    uj_gim = age.get_fuzzy_set(uj[i])
    fuzzy_dis[i] = fuzzy_dist(ui[i], uj[i], ui_gim, uj_gim)
    return fuzzy_dis


def model_for_users(users_data):
    """Create model for given users data i.e. merged movies, items, and users

    Args:
        users_data: DataFrame of merged movies, items, and users based on movie_id
    """

    i = 0
    model_data_for_users = pd.DataFrame(columns=m_cols)

    for key, value in users_data.iterrows():
        # Get user movies based on user
        user_movies = items_merged.loc[items_merged['user_id'] == value['user_id']]

        # Get feature list for all movies of one user
        feature_array = gim.gim_final(user_movies, value['user_id'])
        feature_array[NO_OF_GENRES] = value['age']
        feature_array[NO_OF_GENRES + 1] = value['user_id']

        # Save current feature values in model data
        model_data_for_users.loc[i] = feature_array
        i = i + 1
    return model_data_for_users


def recommend(nearest_neighbours, test_examples):
    """Recommend rating for given movies i.e. test_examples based on nearest neighbours.

    Also return average absolute error for each fold.
    """
    ms = 0
    for key, item in test_examples.iterrows():
        actual_rating, m_id = item['rating'], item['movie_id']
        n_ratings = []
        for i in nearest_neighbours:
            temp = items_merged.loc[items_merged['user_id'] == i].loc[items_merged['movie_id'] == m_id]
            for k, it in temp.iterrows():
                n_ratings.append(it['rating'])
        predicated_rating = float(sum(n_ratings)) / len(n_ratings) if len(n_ratings) else 0
        ms += abs(predicated_rating-actual_rating)
    return ms/test_examples.shape[0]

m_cols = ['unknown', 'Action', 'Adventure',
          'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
          'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', 'age',
          'user_id']

items_merged = load_data.items_merged

model_data_active_users = pd.DataFrame(columns=m_cols)
model_data_passive_users = pd.DataFrame(columns=m_cols)

# Users who has rated movies at least 60 movies
top_users = load_data.items_merged.groupby('user_id').size().sort_values(ascending=False)[:497]

for i in range(0, 5):

    # Get 10% of the top_users as active users and remaining are passive users
    active_users = top_users.sample(frac=0.10)

    # passive_users will be used as training examples
    passive_users = top_users.drop(active_users.index)

    # 34% of active users will be used for training and 66% users for testing purpose.
    training_active_users = active_users.sample(frac=0.34)
    testing_active_users = active_users.drop(training_active_users.index)

    # Get active and passive users' data from merged movies, items, and users
    active_users_data = items_merged.loc[items_merged['user_id'].isin(training_active_users)][:10]
    passive_users_data = items_merged.loc[items_merged['user_id'].isin(passive_users)][:10]

    # Get model for active users
    model_data_active_users = model_for_users(active_users_data)

    # Get model for passive users
    model_data_passive_users = model_for_users(passive_users_data)

    fuzzy_vec = []
    error = []
    for key, value in model_data_active_users.iterrows():
        i = 0
        for key_p, value_p in model_data_passive_users.iterrows():

            fuzzy_vec.append(fuzzy_distance(value, value_p))

            fuzzy_vec[i] = [(sum(x for x in fuzzy_vec[i][:-1]))**0.5, fuzzy_vec[i][-1]]
            i = i + 1

        neighbours = [n[1] for n in sorted(fuzzy_vec, key=operator.itemgetter(0), reverse=True)][:30]

        testing_user = items_merged.loc[items_merged['user_id'] == value['user_id']].sample(frac=0.66)

        # Recommend users based on neighbours
        error.append(recommend(neighbours, testing_user))

    MAE = (sum(error)/len(error))*100
    print("Mean Absolute Error is: ", MAE)