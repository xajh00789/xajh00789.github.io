from django.db import models

# Create your models here.

#设计评论的数据库模型
class Comment(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=255)
    url=models.URLField(blank=True)
    text=models.TextField()
    #用户发表的内容
    created_time=models.DateTimeField(auto_now_add=True)
    #评论数据保存到数据库是，自动将created_time指定为当前时间

    post=models.ForeignKey('blog.Post')
    #一个评论只能属于一篇文章，一篇文章可以有多条评论，外键

    def __str__(self):
        return self.text[:20]
