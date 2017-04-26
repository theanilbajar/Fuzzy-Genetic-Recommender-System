import numpy as np

i_cols = ['unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
#Gim for active users:
gr1 = np.zeros(19)
gf1 = np.zeros(19)
rgr1 = np.zeros(19)
rgf1 = np.zeros(19)
mrgf1 = np.zeros(19)
gim1 = np.zeros(21)
def tr(i):
    total=0
    for k in count['rating']:
        total = total + k 
    return total
#Genre rating of Genre Gj for user ui.
def gr(movies):
    
    temp = 0
    for i in range(0,19):
        gr1[i] = np.dot(movies['rating'],movies[i_cols[i]])
    return gr1

def gf(movies):
    
    for i in range(0,19):
        gf1[i] = movies[i_cols[i]].sum()
    return gf1
    
def rgr(movies, gr1, tr):
    for i in range(0,19):
        rgr1[i] = gr1[i]/tr
    return rgr1

def rgf(movies, gf1, tf):
    for i in range(0, 19):
        rgf1[i] = gf1[i]/tf
    return rgf1
def add_for_mrgf(movies):
    total = np.zeros(19)
    for i in range(0, 19):
        m_t = movies.loc[movies[i_cols[i]]==1]
        for j in m_t['rating']:
            total[i] = total[i] + (j-2)
    return total

def mrgf(movies, tf):
    added = add_for_mrgf(movies)
    for i in range(0, 19):
        mrgf1[i] = (added[i])/(3.0*tf)
    return mrgf1

def gim_final(m, i):
    tf = m.shape[0]
    #print tf
    tr = 0
    for k in m['rating']:
        tr = tr + k
    movies = m.loc[m['rating'] >= 3.0]
    #print 'Movies shape :', movies.shape
    gr1 = gr(movies)
    gf1 = gf(movies)
    rgr1 = rgr(movies, gr1, tr)
    rgf1 = rgf(movies, gf1, tf)
    mrgf1 = mrgf(movies,tf)
    #print mrgf1
    nf = 5.0
    for i in range(0,19):        
        gim1[i] = (2*nf*mrgf1[i]*rgr1[i])/(rgr1[i]+mrgf1[i]) 
    gim = np.nan_to_num(gim1)
    return gim