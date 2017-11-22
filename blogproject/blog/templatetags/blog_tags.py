from ..models import Post,Category
#这是一个文档模板标签
from  django import template

register=template.Library()
#实例化template.Library这个类

#将函数get_recent_post装饰为register.simple_tag
#在模板中使用语法 {% get_recent_posts %} 调用这个函数
#最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


#归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')

#分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.all()

