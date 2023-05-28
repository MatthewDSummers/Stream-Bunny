from django.urls import path
from . import views

urlpatterns = [
    path('',views.favorite_movies_main_page),
    path('movie_info_discussion_page/<int:movie_id>',views.movie_info_discussion_page),
    path('user_favorite_movies_page/<int:member_id>',views.user_favorite_movies_page),
    path('user_info_page',views.user_info_page), 
    path('user_info_page_edit',views.user_info_page_edit),
    path('user_info_edit_save',views.user_info_edit_save),
    path('user_info_update_successful',views.user_info_update_successful),
    path('members_list_page',views.members_list_page), 
    # path('comment',views.comment),
    path('response',views.response), 
    path('like/<int:movie_id>/<str:origin_page>',views.ue_like), 

    # MATTHEW'S DISCUSSION WORK (for "movie_discussion.html")
    path('movie_discussion/<int:movie_id>',views.movie_discussion_page),
    path('discuss/<int:movie_id>',views.discuss), 
    # path('comment/<int:movie_id>/<int:discussion_id>',views.comment), 
    path('comment/<int:movie_id>/<int:msg_id>',views.comment), 
    path('delete_discussions',views.delete_discussions), 

# TEST
    path('user_info_page_test',views.user_info_page_test), 

]
