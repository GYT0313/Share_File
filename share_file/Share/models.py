from django.db import models
from datetime import datetime #导入时间

# Create your models here.

class Upload(models.Model):
    DownloadDocount = models.IntegerField(verbose_name="访问次数", default=0)
    #访问该页面的次数
    code = models.CharField(max_length=8, verbose_name='code')
    #唯一标识一个文件
    Datatime = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    #文件上传时间
    path = models.CharField(max_length=32, verbose_name='下载路径')
    #文件存储路径
    name = models.CharField(max_length=32, verbose_name='文件名', default='')
    #文件名
    Filesize = models.CharField(max_length=10, verbose_name='文件大小')
    PCIP = models.CharField(max_length=32, verbose_name='IP地址', default='')
    #上传文件的地址
    
    class Meta(): #用于定义数据表名, 排序方式
        verbose_name='download' #指明易理解的名字
        db_table = 'download' #表名

    def __str__(self):
        return self.name