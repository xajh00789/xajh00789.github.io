#coding:utf8
from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request,post_pk):
    post=get_object_or_404(Post,pk=post_pk)
    #获取被评论的文章，get_object_or_404获取的文章Post存在是，则获取，否则返回404）

    if request.method=='POST':
        form = CommentForm(request.POST)
        #提交的数据存在request.POST中，利用其构造CommentForm实例，生成表单

        if form.is_valid():
            comment=form.save(commit=False)
            #利用表单的数据生成Comment模型类的实例

            comment.post=post
            #将评论和被评论的文章关联起来

            comment.save()
            #最终将评论数据保存进数据库

            return redirect(post)
            #重定向到post的详情页

        else:
            #检查到数据不合格，重新渲染详情页，并且渲染表单的错误
            comment_list=post.comment_set.all()
            #获取post对应的全部评论,等价于Post.objects.filter(category=cate)

            context={'post':post,'form':form,'comment_list':comment_list}

            return render(request,'blog/detail.html',context=context)



    return redirect(post)
    #不是post请求，重定向到文章详情页
