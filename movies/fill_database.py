import requests
from . import config
from . models import Movie
from django.utils.dateparse import parse_date

my_api_key = config.API_KEY['api_key']
base_url = 'https://api.themoviedb.org/3/'


def fill_database():
    url = f'{base_url}movie/now_playing?api_key={my_api_key}&language=en-US&region=TR'
    popular = requests.get(url)
    result = popular.json()
    movie_title_list = []

    # for to see movies in API...
    # for movie in result['results']:
    #     print(movie)

    for movie in result['results']:
        movie_title_list.append(movie['title'])
        if Movie.objects.filter(name=movie['title']).first() is None and movie['poster_path'] is not None:
            Movie.objects.create(
                name=movie['title'],
                description=movie['overview'],
                image=movie['poster_path'],
                release_date=parse_date(movie['release_date'])
            )
            print(f'{ movie["title"] } is added.')

    not_playing = Movie.objects.exclude(name__in=movie_title_list)

    for movie in not_playing:
        movie.playing_now = False
        movie.save()


