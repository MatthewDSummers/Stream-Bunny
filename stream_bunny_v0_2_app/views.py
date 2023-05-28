import json
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from imdb import IMDb
from django.template.defaulttags import register
from .methods import *
from stream_bunny_v0_2_app.api import get_stream
from .models import *
from user_experience_app.models import *
from login_app.models import *

@csrf_exempt
def movie_search(request):
    if 'user_id' in request.session.keys():
        user = User.objects.get(id=request.session['user_id'])

        context = {
            "name_of_page" : "Stream Bunny Search Page",
            "user" : user,
            "search_page" : True,
        }
        return render(request, 'movie_search.html',context)
    context = {
        "name_of_page" : "Stream Bunny Search Page",
        "search_page" : True,
    }
    return render(request, 'movie_search.html',context)

def search(request, query):
    ia = IMDb()
    curr_movies = ia.search_movie_advanced(query, adult=False)
    if curr_movies:
        movie_array = get_movie_info(curr_movies)
        curr_movies = sorted(movie_array, key=lambda d: d['votes'], reverse=True)
        for i in curr_movies:
            print(i['cast'])
        return HttpResponse(json.dumps(movie_array[:8]), content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"no movie": "Can't find movie"}),
            content_type="application/json"
        )

def get_movie(request, movie_id):
    ia = IMDb()
    movie_detail = ia.get_movie(movie_id)
    streaming_on = get_stream(movie_id)
    movie_dict = {
        'title': movie_detail.get('title'),
        'year' : movie_detail.get('year'),
    }
    if streaming_on:
        movie_dict['streams'] = streaming_on
    else:
        movie_dict['streams'] = []

    if movie_detail.get('cover url'):
        movie_dict['poster_link'] = movie_detail.get('cover url')
    if movie_detail.get('plot'):
        plot_snipped = movie_detail.get('plot')[0].split('::')[0]   #"snipped" version removes some extraneous text from
        movie_dict['plot'] = plot_snipped                           #the end of the plot data that database often attaches
    if movie_detail.get('rating'):
        movie_dict['rating'] = movie_detail.get('rating')
    if movie_detail.get('genres'):
        movie_dict['genres'] = movie_detail.get('genres')
    if movie_detail.get('director'):
        director_list = ''
        for i in range(len(movie_detail.get('director'))):
            director_list += movie_detail.get('director')[i]['name'] 
            director_list += ", "
        director_list = director_list[:-2]
        movie_dict['director'] = director_list
    return HttpResponse(json.dumps(movie_dict), content_type="application/json")

def like(request, movie_id):
    if 'user_id' in request.session.keys():

        user = User.objects.get(id=request.session['user_id'])
        movie_list = Movie.objects.filter(imdb_id = movie_id)
        if len(movie_list) > 0:
            movie = movie_list[0]
            movie.liked_by.add(user)

        else:
            ia = IMDb()
            movie = ia.get_movie(movie_id)

            this_movie = Movie.objects.create(
                imdb_id = movie_id,
                title = movie['title'],
            )
            if "rating" in movie.keys():
                this_movie.imdb_rating = movie['rating']
            if "cover url" in movie.keys():
                this_movie.poster_link = movie['cover url']
            if "plot" in movie.keys():
                this_movie.plot = movie['plot'][0]
            if "year" in movie.keys():
                this_movie.year = movie['year']
            if "genres" in movie.keys():
                this_movie.genres = movie['genres']
            if "director" in movie.keys():
                director_list = ''
                for director in movie['director']:
                    director_list = director_list + str(director) + ", "
                director_list = director_list[:-2]
                this_movie.director = director_list
            if "cast" in movie.keys():
                actor_list = ''
                for i in range(3):
                    actor_list = actor_list + str(movie['cast'][i]) + ", "
                actor_list = actor_list[:-2]
                this_movie.cast = actor_list
            user.liked_by.add(this_movie)
            movie.liked_by.add(user)

            this_movie.save()
        return redirect("/stream-bunny/user_experience")
    else:
        return redirect("/stream-bunny/login")
