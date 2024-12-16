from pathlib import Path
from django.db import models
import uuid #高い確率で他の識別子とは被らない識別子を生成する


class Page(models.Model):      
    #verbose_name :そのデータについての説明             
    #uuidを指定し自動でuuidを生成　editable=Falseで変更不可にする
    
    id =  models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    
    #文字列のフィールド100文字まで
    title = models.CharField(max_length=100, verbose_name="タイトル")

    body = models.TextField(max_length=2000, verbose_name="本文")

    page_date = models.DateField(verbose_name="日付")
    
    picture = models.ImageField(
        upload_to="diary/picture/",blank =True, null =True, verbose_name="写真")

    #auto_now_add：このデータが初めて生成されたその時の日時を保存
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    #auto_now:このデータが保存更新されるたびその時の日時を保存
    updated_at = models.DateTimeField(auto_now =True, verbose_name="更新日時")

    #return self.どのデータかを判断するときに分かりやすいもの
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        picture = self.picture
        super().delete(*args,**kwargs)
        if picture:
            Path(picture.path).unlink(missing_ok=True)          