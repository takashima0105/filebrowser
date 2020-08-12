from django.db import models
from core.base_model import BaseModel
from mptt.models import MPTTModel
from django.conf import settings
import uuid
import os


class Folder(MPTTModel, BaseModel):
    """フォルダ情報テーブル
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'folder'

    # フォルダの作成
    def create_folder(self):
        # フォルダ情報の取得
        folder_path = self.get_folder_path()
        os.mkdir(folder_path)
        return folder_path

    def get_folder_path(self):
        """フォルダのパス情報を返す

        Returns:
            String: フォルダパス(絶対パス)
        """
        # 親フォルダの取得
        ancestors = self.get_ancestors(ascending=False, include_self=True)

        folder_path = settings.MEDIA_ROOT
        for ancestor in ancestors:
            folder_path = os.path.join(folder_path, ancestor.name)

        return folder_path

    def get_file_path(self):
        """ファイル保存用のパスを返す

        Returns:
            String: フォルダパス(相対パス)
        """

        # 親フォルダの取得
        ancestors = self.get_ancestors(ascending=False, include_self=True)

        folder_path = str(self.user.id)
        for ancestor in ancestors:
            folder_path = os.path.join(folder_path, ancestor.name)

        return folder_path


def get_upload_to(instance, filename):
    """保存先のフォルダを取得する

    Returns:
        String: フォルダパス
    """
    folder = Folder.objects.get(id=instance.belong_folder.id)
    folder_path = folder.get_file_path()
    return os.path.join(folder_path, filename)


class File(BaseModel):
    """図面情報テーブル
    """

    belong_folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)
    file = models.FileField(upload_to=get_upload_to,
                            blank=False, null=False, max_length=500)
    register_user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'file'
