from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from gfk_app.serializers import ViewCountSerializer, AddAlbumSerializer
from .models import *
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',  
    handlers=[
        logging.FileHandler("app.log"),  
        # logging.StreamHandler()          
    ]
)

class AddCommentView(APIView):
    def post(self, request, id):
        try:
            if request.data["comment_for"] == 1:
                post_obj = Post.objects.get(id=id)
                content_type = ContentType.objects.get_for_model(Post)
                CommentModel.objects.create(
                    content_type=content_type,
                    object_id=post_obj.id,
                    comment=request.data['comment'] 
                    )
            return Response({'data': None, 'message': 'done', 'status': 200})
        except Exception as err:
            return Response({'data':str(err), 'message': 'Something went wrong', 'status': 400})

class GetCommentsOfPost(APIView):
    def get(self, request, id):
        try:
            content_type = ContentType.objects.get_for_model(Post)
            comments = CommentModel.objects.filter(
                content_type=content_type,
                object_id=id,
            )
            # serializer = ViewCountSerializer(comments, many=True)
            return Response({'data': comments.values('comment'), 'message': 'done', 'status': 200})
        except Exception as err:
            logging.error(f"{err}")
            return Response({'data':str(err), 'message': 'Something went wrong', 'status': 400})

class GetAlbumsView(APIView):
    def get(self, request):
        try:
            albums = Album.objects.all()
            serializer = ViewCountSerializer(albums, many=True)
            return Response({'data': serializer.data, 'message': 'done', 'status': 200})
        except Exception as err:
            logging.error(f"{err}")
            return Response({'data':str(err), 'message': 'Something went wrong', 'status': 400})

class AddAlbumView(APIView):
    def post(self, request):
        try:
            serializer = AddAlbumSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'message': 'done', 'status': 200})
            return Response({'data': serializer.errors, 'message': 'Went wrong', 'status': 400})
        except Exception as err:
            logging.error(f"{err}")
            return Response({'data':str(err), 'message': 'Something went wrong', 'status': 400})
