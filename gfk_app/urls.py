from gfk_app.views import AddCommentView, GetCommentsOfPost, GetAlbumsView, AddAlbumView
from django.urls import path


urlpatterns = [
    path('add-comment/<int:id>/', AddCommentView.as_view()),
    path('comments/<int:id>/', GetCommentsOfPost.as_view()),
    path('albums/', GetAlbumsView.as_view()),
    path('album/', AddAlbumView.as_view()),
]
