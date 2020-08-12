from .models import Folder, File
from rest_framework import serializers


class FolderSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """レコードの作成時に、フォルダも作成
        """
        folder = Folder.objects.create(**validated_data)
        folder.create_folder()

        return folder

    class Meta:
        model = Folder
        fields = '__all__'


class FolderBreadcrumbsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ['id', 'name', 'level']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class FileListSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id',
                  'belong_folder',
                  'name',
                  'file_url']

    def get_file_url(self, file):
        request = self.context.get('request')
        file_url = file.file.url
        return request.build_absolute_uri(file_url)
