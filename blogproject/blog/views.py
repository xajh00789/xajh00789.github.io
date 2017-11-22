#coding:utf8
from .models import Post,Category
from django.shortcuts import render,get_object_or_404
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView



def index(request):
    post_list=Post.objects.all()
    #使用 all() 方法从数据库里获取了全部的文章，存在了 post_list 变量里
    #- 号表示逆序,排序依据的字段是 created_time
    return render(request,'blog/index.html',context={'post_list':post_list})

class IndexView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'
    paginate_by=3

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()
#详情页视图函数，对 post 的 body 的值做一下渲染，把 Markdown 文本转为 HTML 文本再传递给模板
    post.body = markdown.markdown(post.body,
                                  extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite',
                                              'markdown.extensions.toc', ])

    form = CommentForm()
    comment_list = post.comment_set.all()  # 获取这篇post下的全部评论
    context = {'post': post, 'form': form, 'comment_list': comment_list}
    # 将文章，表单，文章下的评论列表作为模板变量传给detail.html模板，异便渲染数据

    return render(request, 'blog/detail.html', context=context)

    # 视图函数从 URL 捕获的文章 id 传递给模板
    # 当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，
    # 如果不存在，就给用户返回一个 404 错误


class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context





#归档页面
def archives(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month
                                  )
    return render(request,'blog/index.html',context={'post_list':post_list})
 #使用模型管理器（objects）的 filter 函数来过滤文章


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

    '''
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={'post_list':post_list})
#根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类
#通过 filter 函数过滤出了该分类下的全部文章
'''
