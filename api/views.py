from rest_framework.views import APIView
from pytube import YouTube
import string, random
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core.cache import cache
global characters
global channel

characters = string.ascii_letters + string.digits
channel = get_channel_layer()

class FetchLinkAndGiveOptionsView(APIView):
    def post(self, request):
        link = request.data["link"]
        link_data = request.session.get("link")
        if link_data and link_data["link"] == link:
            return Response({"data": link_data, "message": "Select your choice and click on download"}, status=200)

        data = {"title":"", "only_audio":[], "only_video":[], "both":[], "uuid":""}

        yt = YouTube(
            link,
            use_oauth=False,
            allow_oauth_cache=True
            )
        data["title"] = yt.title

        only_audio = yt.streams.filter(only_audio = True)
        data["only_audio"] = [{"id": index, "filesize": "{:.1f}KB".format(((audio.filesize)/1000))} for index, audio in enumerate(only_audio)]

        only_video = yt.streams.filter(only_video = True, mime_type = "video/mp4")
        data["only_video"] = [{"id": index, "resolution": video.resolution, "filesize": "{:.2f}MB".format(((video.filesize)/1000000))} for index, video in enumerate(only_video)]

        both = yt.streams.filter(progressive = True)
        data["both"] = [{"id": index, "resolution": obj.resolution, "filesize": "{:.2f}MB".format(((obj.filesize)/1000000))} for index, obj in enumerate(both)]

        random_char = "".join([random.choice(characters) for i in range(10)])
        data["uuid"] = random_char

        if not link_data or link_data["link"] != link:
            request.session["link"] = {"link": link, "data" :data}

        return Response({"data": data, "message": "Select your choice and click on download"}, status=200)


class DownloadFileView(APIView):
    def post(self, request):
        try:
            link = request.data["link"]
            selected_type = request.data["selected_type"]
            selected_option = request.data["selected_option"]
            file_path = request.data["file_path"]
            self.uuid = request.data["uuid"]
            
            yt = YouTube(
                link,
                on_progress_callback = self.progress_func,
                on_complete_callback = self.complete_func,
                use_oauth=False,
                allow_oauth_cache=True
                )
            if selected_type == "only_audio":
                files = yt.streams.filter(only_audio = True)
            elif selected_type == "only_video":
                files = yt.streams.filter(only_video = True, mime_type = "video/mp4")
            elif selected_type == "both":
                files = yt.streams.filter(progressive = True)
            files[selected_option].download(output_path = file_path)
            return Response({"file": files[selected_option].title, "message": f"File successfully downloaded to {file_path}"}, status = 200)    
        except Exception as error:
            return Response({"error": str(error), "error_type": str(type(error)), "message": "Something went wrong"}, status = 400)    


    def progress_func(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        downloaded_size = round((bytes_downloaded)/1000000, 2)
        percent_completed = round((bytes_downloaded/total_size)*100, 2)
        data = {
                    "status": 1, 
                    "status_description": "In Progress",
                    "downloaded_size": f"{downloaded_size}MB", 
                    "percent_completed": percent_completed
                }
        # send to socket
        async_to_sync(channel.group_send)(
            self.uuid,
            {
                "type": "update_type",
                "msg": json.dumps(data)
            }
        )

    def complete_func(self, stream, file_path):
        data = {
                    "status": 2,
                    "status_description": "Completed", 
                    "file_path": file_path
                }
        async_to_sync(channel.group_send)(
            self.uuid,
            {
                "type": "update_type",
                "msg": json.dumps(data)
            }
        )

