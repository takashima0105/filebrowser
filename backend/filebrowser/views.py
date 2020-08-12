from django.db import transaction
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from user.models import User
from .models import Folder, File
from .serializers import FolderSerializer, FileSerializer, FileListSerializer
from .serializers import FolderBreadcrumbsSerializer
from itertools import chain


class FolderCreateAPIView(generics.CreateAPIView):
    """新規フォルダの作成API
    POST /folder_create/<slug:parentid>
    """

    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = (IsAuthenticated, )

    @action(detail=True, method=['post'])
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():

                user = User.objects.get(id=self.request.user.id)
                if(kwargs.get('parentid') == 'home'):
                    root_folder = Folder.objects.get(
                        user=user, level=0, tree_id=1)
                    data = {'user': user.id, 'name': request.data.get(
                        'name'), 'parent': root_folder.id}
                else:
                    parent = Folder.objects.get(
                        pk=kwargs.get('parentid'))
                    data = {'user': user.id, 'name': request.data.get(
                        'name'), 'parent': parent.id}

                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                result = serializer.save()

                response = self.serializer_class(result)
                return Response(response.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            result = {
                'message': 'フォルダが存在しません。'
            }
            return Response(status=status.HTTP_404_NOT_FOUND)
        except FileExistsError:
            result = {
                'message': '既に同名のフォルダが存在します。'
            }
            return Response(data=result, status=status.HTTP_409_CONFLICT)
        except (NameError, ValidationError):
            result = {
                'message': '要求されたリクエストが正しくありません。'
            }
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)


class FolderBreadcrumbsAPIView(generics.ListAPIView):
    """フォルダのパンくずリストの取得API
    GET /breadcrumbs/<slug:folderid>/
    """

    pagination_class = None
    serializer_class = FolderBreadcrumbsSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        try:
            user = User.objects.get(id=self.request.user.id)
            folderid = self.kwargs.get('folderid', None)
            if(folderid == 'home'):
                queryset = Folder.objects.none()
            else:
                queryset = Folder.objects.get(
                    pk=folderid,
                    user=user).get_ancestors(include_self=True)[1:]

            return queryset
        except ObjectDoesNotExist:
            return Folder.objects.none()


class FileCreateAPIView(generics.CreateAPIView):
    """新規ファイルの登録API
    POST /file_upload/<slug:folderid>/
    """

    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated, )

    @action(detail=True, method=['post'])
    def create(self, request, *args, **kwargs):

        try:
            with transaction.atomic():
                user = User.objects.get(id=self.request.user.id)
                folderid = self.kwargs.get('folderid')

                _file = request.FILES.get('file')

                if(folderid == 'home'):
                    root_folder = Folder.objects.get(
                        user=user, level=0, tree_id=1)
                    data = {'belong_folder': root_folder.id,
                            'file': _file,
                            'name': _file.name,
                            'register_user': user.id}
                else:
                    folder = Folder.objects.get(
                        user=user, pk=folderid)
                    data = {'belong_folder': folder.id,
                            'file': _file,
                            'name': _file.name,
                            'register_user': user.id}

                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)

                result = serializer.save()

                response = self.serializer_class(result)
                return Response(response.data, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            result = {
                'message': '又はフォルダが存在しません。'
            }
            return Response(data=result, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            result = {
                'message': 'アップロードされたファイルが不正です。'
            }
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)


class ListAPIView(generics.ListAPIView):
    """図面リストの取得API

    Request:
        [GET] /item/<slug:folderid>/
    """

    permission_classes = (IsAuthenticated, )

    def get_folder_queryset(self):
        user = User.objects.get(id=self.request.user.id)

        folderid = self.kwargs.get('folderid', None)
        if(folderid == 'home'):
            queryset = Folder.objects.filter(
                level=1, user=user)
        else:
            queryset = Folder.objects.get(
                pk=folderid, user=user).get_children()
        return queryset

    def get_file_queryset(self):
        user = User.objects.get(id=self.request.user.id)

        folder_id = self.kwargs.get('folderid', None)
        if(folder_id == 'home'):
            root_folder = Folder.objects.get(
                user=user, level=0, tree_id=1)
            queryset = File.objects.filter(
                belong_folder=root_folder)
        else:
            folder = Folder.objects.get(
                user=user, pk=folder_id)
            queryset = File.objects.filter(
                belong_folder=folder)

        return queryset

    def get_queryset(self, request):

        folder_queryset = self.get_folder_queryset()
        file_queryset = self.get_file_queryset()

        items = list(chain(folder_queryset, file_queryset))
        results = list()
        for item in items:
            item_type = item.__class__.__name__.lower()
            if isinstance(item, Folder):
                serializer = FolderSerializer(item)
            if isinstance(item, File):
                serializer = FileListSerializer(
                    item, context={"request": request})
            results.append({'type': item_type, 'data': serializer.data})

        return results

    @action(detail=True, method=['get'])
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset(request)

            data = self.paginate_queryset(queryset)
            if data is not None:
                return self.get_paginated_response(data)

            return Response(data)
        except ObjectDoesNotExist:
            result = {
                'message': 'フォルダが存在しません。'
            }
            return Response(data=result, status=status.HTTP_404_NOT_FOUND)
