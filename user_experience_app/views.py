from django.shortcuts import render,redirect,HttpResponse
from .models import *
from login_app.models import User, Image
from django.contrib import messages
# from stream_bunny_v0_2_app.models import Movie
from stream_bunny_v0_2_app.models import Movie, Discussion, Comment
# from user_experience_app.models import Discussion, Comment

def favorite_movies_main_page(request):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        "name_of_page" : "favorite_movies_main_page",
        "user" : user,
        "movies" : Movie.objects.all()
    }
    return render(request,'favorite_movies_main_page.html',context)

def members_list_page(request):
    user = User.objects.get(id=request.session['user_id'])
    members = User.objects.all()
    context = {
        "name_of_page" : "members_list_page",
        "user" : user,
        "members" : members
    }
    return render(request,'members_list_page.html',context)
    
def member_profile(request, member_id):
    user = User.objects.get(id=request.session['user_id'])
    member = User.objects.get(id=member_id)
    member_likes = member.liked_by.all()
    # user_likes = user.liked_by.all()
    context ={
        "name_of_page" : "member_profile_page",
        "member" : member,
        "member_likes" : member_likes,
        "movies" : member.liked_by.all(),
        # "user_liked" : user_likes,
    }
    return render(request, 'member_profile.html', context)

def movie_info_discussion_page(request,movie_id):
    user = User.objects.get(id=request.session['user_id'])
    movie = Movie.objects.get(id=movie_id)

    context = {
        "name_of_page" : "movie_info_discussion_page",
        "user" : user,
        "movie" : movie,
    }
    return render(request,'movie_info_discussion_page.html',context)

    
def user_favorite_movies_page(request,member_id):
    member = User.objects.get(id=member_id)

    context = {
        "name_of_page" : "user_favorite_movies_page",
        "member" : member,
        "movies" : member.liked_by.all(),
        "user" : User.objects.get(id=request.session['user_id']),

    }
    return render(request,'user_favorite_movies_page.html',context)
    
def user_info_page(request):
    user = User.objects.get(id=request.session['user_id'])
    # my_likes = user.liked_by.all()

    context = {
        "name_of_page" : "user_info_page",
        "user" : user,
        "movies" : user.liked_by.all(),
        'images':Image.objects.filter(user=user.id),
    }
    return render(request,'user_info_page.html',context)
    
def user_info_page_edit(request):
    user = User.objects.get(id=request.session['user_id'])
    birthday=user.birthday.strftime("%Y-%m-%d")
    print(birthday)
    print(type(birthday))
    context = {
        "user" : user,
        "birthday" : birthday
    }
    return render(request,'user_info_page_edit.html',context)

def user_info_edit_save(request):
    errors = User.objects.registerValidator(request.POST)
    request.session['errors'] = errors
    # first_name = request.POST['first_name']
    # last_name = request.POST['last_name']
    # birthday = request.POST['birthday']
    # email = request.POST['email']
    # password = request.POST['password']
    # confirm_password = request.POST['confirm_password']
    # request.session['first_name'] = first_name
    # request.session['last_name'] = last_name
    # request.session['birthday'] = birthday
    # request.session['email'] = email
    # request.session['password'] = password
    # request.session['confirm_password'] = confirm_password
    if len(errors) > 0:
        # for key, value in errors.items():
        #     messages.error(request,value)
        return redirect('/xxxxxxxxxxxxx')
    else:
        # request.session.flush()
        # password_bcrypt = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        # request.session['user_id'] = user.id
        user = User.objects.get(id=request.session['user_id'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.birthday = request.POST['birthday']
        user.email = request.POST['email']
        user.about_me = request.POST['about_me']
        # user.confirm_password = request.POST['confirm_password']
        user.save()
        context = {

        }
    return render(request,'user_info_update_successful.html',context)
        # return redirect('/stream-bunny/user_experience/user_info_update_successful')

def user_info_update_successful(request):
    context ={
        
    }

    return render(request,'user_info_update_successful.html',context)


def comment(request):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        "user" : user,
        "name_of_page" : "comment_partial (use ajax)",
    }
    return render(request,'comment_partial.html',context)
    
def response(request):
    user = User.objects.get(id=request.session['user_id'])

    context = {
        "user" : user,
        "name_of_page" : "response_partial (use ajax)",
    }
    return render(request,'response_partial.html',context)

def ue_like(request,movie_id,origin_page):
    if request.session['user_id']:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        movie = Movie.objects.get(id=movie_id)
        if movie in user.liked_by.all():
            user.liked_by.remove(movie) 
        else:
            user.liked_by.add(movie)
        return HttpResponse(movie.liked_by.all().count())
    return redirect('/stream-bunny')

def like(request, movie_id):
    user = User.objects.get(id=request.session["user_id"])

    Movie.objects.create(imdb_id = movie_id)

    movie = Movie.objects.get(id=movie_id)
    movie.liked_by.add(user)

    return render(request,"user_info_page.html")



# MATTHEW'S DISCUSSION WORK (for "movie_discussion.html")
def movie_discussion_page(request,movie_id):
    user = User.objects.get(id=request.session['user_id'])
    movie = Movie.objects.get(id=movie_id)
    # discussion = Discussion.objects.filter(id=movie_id)
    discussions = Discussion.objects.filter(movie=movie_id)
    genres_2 = ''
    if movie.genres:
        genres = movie.genres
        genre_list = genres.split("'")
        for i in range(1,len(genre_list),2):
            genres_2 += genre_list[i] + ' - '
        genres_2 = genres_2[:-3]

    context = {
        "name_of_page" : "movie_info_discussion_page",
        "user" : user,
        "movie" : movie,
        "genres" : genres_2, 
        "discussions" : discussions,
    }
    return render(request,'movie_discussion.html',context)

def discuss(request, movie_id):
    if len(request.POST['discuss']) > 1:
        Discussion.objects.create(
            user = User.objects.get(id=request.session['user_id']),
            movie = Movie.objects.get(id=movie_id),
            content = request.POST['discuss'],
        )
    discussions = Discussion.objects.filter(movie=movie_id)
    context = {
        "discussions" : discussions,
        "movie" : Movie.objects.get(id=movie_id),
    }
    return render(request,'response_partial.html',context)

def comment(request,movie_id,msg_id):
    if len(request.POST['comment']) > 1:
        Comment.objects.create(
            user = User.objects.get(id=request.session['user_id']),
            discussion = Discussion.objects.get(id=msg_id),
            comment = request.POST['comment']
        )
    discussions = Discussion.objects.filter(movie=movie_id)
    context = {
        "discussions" : discussions,
        "movie" : Movie.objects.get(id=movie_id),
    }
    return render(request,'response_partial.html',context)

    # msg = Discussion.objects.get(id=msg_id)
    # context = {
    #     "msg" : msg,
    # }
    # return render(request,'comment_partial.html',context)

def delete_discussions(request):
    Discussion.objects.all().delete()
    return redirect('/stream-bunny/user_experience')



# TEST

# it works 
def user_info_page_test(request):
    user = User.objects.get(id=request.session['user_id'])
    # my_likes = user.liked_by.all()

    context = {
        "name_of_page" : "user_info_page",
        "user" : user,
        "movies" : user.liked_by.all(),
        'images':Image.objects.filter(user=user.id),
    }
    return render(request,'user_info_page_test.html',context)