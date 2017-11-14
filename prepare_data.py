# to drop movies with less than 20 ratings and
# to create a rating file that is comma separated without timestamps
from __future__ import print_function

from collections import defaultdict
import json

movie_file = open('raw_data/movies.dat', 'r')  # data source: https://github.com/sidooms/MovieTweetings
movies = dict()
for line in movie_file.readlines():
    movie_id, name, genre_string = line.split('::')
    genre_string = genre_string.strip()
    genres = genre_string.split('|') if genre_string else list()
    movies[movie_id] = {'name': name, 'genres': genres}

rating_file = open('raw_data/ratings.dat', 'r')  # data source: https://github.com/sidooms/MovieTweetings
ratings_by_movie = defaultdict(list)
num_ratings_by_movie = defaultdict(int)
for line in rating_file.readlines():
    user_id, movie_id, rating, timestamp = line.split('::')
    ratings_by_movie[movie_id].append({'user_id': user_id, 'rating': int(rating)})
    num_ratings_by_movie[movie_id] += 1

for movie_id, num_ratings in num_ratings_by_movie.items():
    if num_ratings < 30:
        movies.pop(movie_id, None)
        ratings_by_movie.pop(movie_id)
        num_ratings_by_movie.pop(movie_id)

with open('movies.json', 'w') as file:
    json.dump(movies, file, indent=4)
with open('ratings.csv', 'w') as file:
    for movie_id, movie_ratings in ratings_by_movie.items():
        for movie_rating in movie_ratings:
            file.write('{},{},{}\n'.format(movie_rating['user_id'], movie_id, movie_rating['rating']))

# movies with most ratings
import operator    
most_rated_movie_ids = sorted(num_ratings_by_movie.items(), key=operator.itemgetter(1), reverse=True)[:10]
print('Movies with most ratings')
print('------------------------')
for movie_id, num_ratings in most_rated_movie_ids:
    print(movies[movie_id], num_ratings)

# movies with highest ratings
rating_aggs_by_movie = defaultdict(dict)
for movie_id in ratings_by_movie.keys():
    rating_aggs_by_movie[movie_id]['num'] = num_ratings_by_movie[movie_id]
    rating_aggs_by_movie[movie_id]['sum'] = sum([rating['rating'] for rating in ratings_by_movie[movie_id]])
    rating_aggs_by_movie[movie_id]['avg'] = round(float(rating_aggs_by_movie[movie_id]['sum']) / num_ratings_by_movie[movie_id], 2)

highest_rated_movie_ids = sorted(rating_aggs_by_movie.items(), key=lambda rating_agg: rating_agg[1]['avg'], reverse=True)[:10]
print('Movies with highest ratings')
print('---------------------------')
for movie_id, agg in highest_rated_movie_ids:
    print(movies[movie_id], agg)

# movies with lowest ratings
lowest_rated_movie_ids = sorted(rating_aggs_by_movie.items(), key=lambda rating_agg: rating_agg[1]['avg'],)[:10]
print('Movies with lowest ratings')
print('--------------------------')
for movie_id, agg in lowest_rated_movie_ids:
    print(movies[movie_id], agg)

'''
Movies with most ratings
------------------------
{'genres': ['Sci-Fi', 'Thriller'], 'name': 'Gravity (2013)'} 3013
{'genres': ['Biography', 'Comedy', 'Crime'], 'name': 'The Wolf of Wall Street (2013)'} 2654
{'genres': ['Action', 'Adventure', 'Fantasy'], 'name': 'Man of Steel (2013)'} 2592
{'genres': ['Adventure', 'Drama', 'Sci-Fi'], 'name': 'Interstellar (2014)'} 2493
{'genres': ['Action', 'Adventure', 'Horror'], 'name': 'World War Z (2013)'} 2379
{'genres': ['Crime', 'Mystery', 'Thriller'], 'name': 'Now You See Me (2013)'} 2335
{'genres': ['Action', 'Adventure', 'Sci-Fi'], 'name': 'Iron Man 3 (2013)'} 2268
{'genres': ['Biography', 'Drama', 'Thriller'], 'name': 'Captain Phillips (2013)'} 2065
{'genres': ['Crime', 'Drama', 'Mystery'], 'name': 'Gone Girl (2014)'} 2037
{'genres': ['Crime', 'Drama', 'Mystery'], 'name': 'Prisoners (2013)'} 1975

Movies with highest ratings
---------------------------
{'genres': ['Comedy', 'Drama', 'Fantasy'], 'name': 'MSG 2 the Messenger (2015)'} {'sum': 480, 'num': 48, 'avg': 10.0}
{'genres': ['Comedy', 'Drama'], 'name': 'Be Somebody (2016)'} {'sum': 3505, 'num': 351, 'avg': 9.99}
{'genres': ['Drama', 'War'], 'name': 'Dag II (2016)'} {'sum': 302, 'num': 32, 'avg': 9.44}
{'genres': ['Drama'], 'name': 'Nema-ye Nazdik (1990)'} {'sum': 292, 'num': 31, 'avg': 9.42}
{'genres': ['Crime', 'Drama'], 'name': 'The Shawshank Redemption (1994)'} {'sum': 8186, 'num': 870, 'avg': 9.41}
{'genres': ['Adventure', 'Drama', 'Fantasy'], 'name': 'The Lord of the Rings: The Return of the King (2003)'} {'sum': 2495, 'num': 267, 'avg': 9.34}
{'genres': ['Action', 'Crime', 'Drama'], 'name': 'The Dark Knight (2008)'} {'sum': 5064, 'num': 546, 'avg': 9.27}
{'genres': ['Drama', 'Family', 'Music'], 'name': 'Taare Zameen Par (2007)'} {'sum': 799, 'num': 87, 'avg': 9.18}
{'genres': ['Crime', 'Drama'], 'name': '12 Angry Men (1957)'} {'sum': 4591, 'num': 500, 'avg': 9.18}
{'genres': ['Crime', 'Drama'], 'name': 'The Godfather: Part II (1974)'} {'sum': 2501, 'num': 273, 'avg': 9.16}

Movies with lowest ratings
--------------------------
{'genres': ['Biography', 'Drama'], 'name': 'Reis (2016)'} {'sum': 80, 'num': 35, 'avg': 2.29}
{'genres': ['Drama', 'War'], 'name': 'The Thin Red Line (1998)'} {'sum': 741, 'num': 236, 'avg': 3.14}
{'genres': ['Action', 'Sci-Fi', 'Thriller'], 'name': 'Left Behind (2014)'} {'sum': 298, 'num': 88, 'avg': 3.39}
{'genres': ['Horror', 'Sci-Fi', 'Thriller'], 'name': 'Cell (2016)'} {'sum': 197, 'num': 56, 'avg': 3.52}
{'genres': ['Comedy', 'Horror'], 'name': 'Piranha 3DD (2012)'} {'sum': 144, 'num': 40, 'avg': 3.6}
{'genres': ['Action', 'Adventure', 'Sci-Fi'], 'name': 'Vice (2015)'} {'sum': 123, 'num': 34, 'avg': 3.62}
{'genres': ['Action', 'Sci-Fi'], 'name': 'Batman & Robin (1997)'} {'sum': 212, 'num': 56, 'avg': 3.79}
{'genres': ['Comedy'], 'name': 'Jack and Jill (2011)'} {'sum': 168, 'num': 44, 'avg': 3.82}
{'genres': ['Comedy'], 'name': 'Scary Movie 5 (2013)'} {'sum': 753, 'num': 197, 'avg': 3.82}
{'genres': ['Action', 'Adventure', 'History'], 'name': 'Hammer of the Gods (2013)'} {'sum': 128, 'num': 33, 'avg': 3.88}
'''