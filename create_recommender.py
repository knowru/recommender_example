from surprise import (
    KNNBaseline, Reader, Dataset, dump
)

# First, train the algortihm to compute the similarities between items
data = Dataset.load_from_file('ratings.csv', reader=Reader(sep=',', rating_scale=(1, 10)))
trainset = data.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNBaseline(sim_options=sim_options)
algo.train(trainset)

'''
>>> algo.predict('425', '0338564')
Prediction(uid='425', iid='0338564', r_ui=None, est=8.8268148604314725, details={u'actual_k': 40, u'was_impossible': False})
>>> algo.predict('732', '1219827')
Prediction(uid='732', iid='1219827', r_ui=None, est=1.3944813261280586, details={u'actual_k': 8, u'was_impossible': False})
'''

dump.dump('knn.algo', algo=algo)