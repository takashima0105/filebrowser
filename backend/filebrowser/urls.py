from .views import FileCreateAPIView, FolderCreateAPIView
from .views import FolderBreadcrumbsAPIView, ListAPIView
from django.urls import path

# drawingfile_list = DrawingFileViewset.as_view({
#     'get': 'list',
#     'post': 'create'
# })

urlpatterns = [
    path('folder_create/<slug:parentid>/',
         FolderCreateAPIView.as_view()),
    path('breadcrumbs/<slug:folderid>/',
         FolderBreadcrumbsAPIView.as_view()),
    path('file_upload/<slug:folderid>/',
         FileCreateAPIView.as_view()),
    path('item/<slug:folderid>/',
         ListAPIView.as_view())
]
