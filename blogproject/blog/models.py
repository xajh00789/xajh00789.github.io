#coding:utf8
import markdown
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import strip_tags

# Create your models here.

#类名就是一个数据库表格，类属性对应表格列，属性名对应列名，id列 自动创建
#类名是数据库表名，Django规定
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.TextField()
    body=models.TextField()
    created_time=models.DateTimeField()
    modified_time=models.DateTimeField()
    views=models.PositiveIntegerField(default=0)
    #新增views字段记录阅读量,该类型值仅允许0或正整数


    # 用户一旦访问increase_views方法自身views字段值+1
    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])
        #将数据库更新值存入数据库,update_fields值更新数据库中views字段

    #文章摘要
    excerpt=models.CharField(max_length=200,blank=True)
#CharField要求必须存入数据,blank=True就可以允许空值

    category=models.ForeignKey(Category)
    #一篇文章只能对应一个类别 ，一个类别下可以有多篇文章

    tags=models.ManyToManyField(Tag,blank=True)
    #一篇文章可以对应多个标签，一个标签可以对应多篇文章,且标签可以为空

    author=models.ForeignKey(User)
    #一篇文章的作者只能有一个,User从django.contrib.auth.models导入

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

#url.py中的app_name = 'blog' 告诉了 Django 这个 URL 模块是属于 blog 应用的，
# 因此 Django 能够顺利地找到 blog 应用下 name 为 detail 的视图函数，
# 于是 reverse 函数会去解析这个视图函数对应的 URL，

    def save(self,*args,**kwargs):
        if not self.excerpt: #如果没有填写摘要
            #实例化一个Markdown类，用于渲染body的文本
            md=markdown.Markdown(extensions=['markdown.extensions.extra','markdown.extensions.codehilite'])
            self.excerpt=strip_tags(md.convert(self.body))[:54]
            #将Markdown文本渲染成HTML标签
            #再从文本摘取前54个字符赋予excerpt

        super(Post,self).save(*args,**kwargs)
        #调用父类的save方法将数据保存到数据库中



    class Meta:
        ordering=['-created_time']
#指定Post内部类Meta类之后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序

