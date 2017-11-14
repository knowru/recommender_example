import json
from surprise import dump

_, algo = dump.load('knn.algo')
with open('movies.json') as file:
    movies = json.load(file)
movie_name_to_raw_ids = dict()
for movie_id, movie_info in movies.items():
    movie_name_to_raw_ids[movie_info['name']] = movie_id

def parse_data(data):
    movie_name = data.get('movie_name', None)
    if not movie_name:
        raise ValueError('movie_name should be given')
    if movie_name not in movie_name_to_raw_ids:
        raise ValueError('unrecognized movie_name')
    k = data.get('k', 5)
    if not isinstance(k, int):
        raise ValueError('k should be an integer')
    if k < 1:
        raise ValueError('k should be a positive integer')
    return movie_name, k

def run(data):
    movie_name, k = parse_data(data)
    movie_raw_id = movie_name_to_raw_ids[movie_name]
    movie_inner_id = algo.trainset.to_inner_iid(movie_raw_id)
    neighbor_inner_ids = algo.get_neighbors(movie_inner_id, k=k)
    neighbor_raw_ids = [algo.trainset.to_raw_iid(inner_id) for inner_id in neighbor_inner_ids]
    neighbor_movies = [movies[neighbor_raw_id] for neighbor_raw_id in neighbor_raw_ids]
    return neighbor_movies

'''
>>> import knowledge
>>> from pprint import pprint
>>> pprint(knowledge.run(data={'movie_name': 'Dunkirk (2017)', 'k': 10}), indent=4)
[   {   u'genres': [], u'name': u'Blade Runner 2049 (2017)'},
    {   u'genres': [u'Adventure', u'Drama', u'Thriller'],
        u'name': u'The Revenant (2015)'},
    {   u'genres': [u'Comedy', u'Mystery'], u'name': u'Hail, Caesar! (2016)'},
    {   u'genres': [u'Drama'], u'name': u'Blue Jasmine (2013)'},
    {   u'genres': [u'Comedy', u'Drama', u'Musical'],
        u'name': u'La La Land (2016)'},
    {   u'genres': [u'Action', u'Adventure', u'Sci-Fi'],
        u'name': u'Mad Max: Fury Road (2015)'},
    {   u'genres': [u'Comedy', u'Drama'], u'name': u'Birdman (2014)'},
    {   u'genres': [u'Action', u'Crime', u'Drama'], u'name': u'Sicario (2015)'},
    {   u'genres': [u'Sci-Fi', u'Thriller'], u'name': u'Gravity (2013)'},
    {   u'genres': [u'Drama', u'Mystery', u'Sci-Fi'], u'name': u'Arrival (2016)'}]
>>> pprint(knowledge.run(data={'movie_name': 'Toy Story (1995)', 'k': 10}), indent=4)
[   {   u'genres': [u'Animation', u'Adventure', u'Comedy'],
        u'name': u'Toy Story 3 (2010)'},
    {   u'genres': [u'Animation', u'Adventure', u'Comedy'],
        u'name': u'Monsters University (2013)'},
    {   u'genres': [u'Animation', u'Adventure', u'Comedy'],
        u'name': u'Monsters, Inc. (2001)'},
    {   u'genres': [u'Action', u'Adventure', u'Fantasy'],
        u'name': u'Star Wars: Episode V - The Empire Strikes Back (1980)'},
    {   u'genres': [u'Adventure', u'Comedy', u'Sci-Fi'],
        u'name': u'Back to the Future (1985)'},
    {   u'genres': [u'Animation', u'Adventure', u'Comedy'],
        u'name': u'Up (2009)'},
    {   u'genres': [u'Animation', u'Adventure', u'Family'],
        u'name': u'Rise of the Guardians (2012)'},
    {   u'genres': [u'Animation', u'Adventure', u'Comedy'],
        u'name': u'Wreck-It Ralph (2012)'},
    {   u'genres': [u'Adventure', u'Drama', u'Fantasy'],
        u'name': u'Life of Pi (2012)'},
    {   u'genres': [u'Action', u'Crime', u'Thriller'],
        u'name': u'John Wick: Chapter 2 (2017)'}]
'''
