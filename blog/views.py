from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import Post, Category, ArticleStatistic, Comment,CommentReports
from .forms import PostForm, EditForm, CommentForm, EditCommentForm,ReportCommentForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Sum
from members.models import CustomUser
from django.http import HttpResponse,Http404



class HomeView(ListView):  
    model = Post  
    template_name = 'home.html'  
    paginate_by = 4
    ordering = ['-id']
    queryset = Post.objects.filter(published=True)

    def get_context_data(self, *args, **kwargs):
        top_list = get_top_articles_list()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["top_list"] = top_list
        return context

def category_view(request, input_cat):

    try:
        category_query = Category.objects.get(name=input_cat)
    except:
        return render(request, 'no_category.html', {'inputcat_as_title': input_cat.title(), })
    else:
        category_posts = Post.objects.filter(published=True,
            category=input_cat.replace('-', ' ')).order_by('-id')
        paginator = Paginator(category_posts, per_page=4)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'category_detail.html',
                      {'input_cat': input_cat, 'inputcat_as_title': input_cat.title().replace('-', ' '), 'posts': posts, })

def categories_view(request):
    existing_categories_for_other_views = Category.objects.all()
    if existing_categories_for_other_views:
        return render(request, 'categories.html', {'existing_categories_for_other_views': existing_categories_for_other_views, })
    else:
        return render(request, 'no_categories.html', {})

def top_list_view(request):
    popular = get_top_articles_list()
    return render(request, 'top_list.html', {'popular_list': popular})


class ArticleView(UpdateView):
    model = Post
    template_name = 'article.html'
    form_class = CommentForm
    

    def get(self, request, *args, **kwargs):

        article = get_object_or_404(Post, text_to_url=self.kwargs['text_to_url'])
        obj, created = ArticleStatistic.objects.get_or_create(
            defaults={
                "article": article,
                "date": timezone.now()
            },
            date=timezone.now(),
            article=article,
        )
        obj.views += 1
        obj.save(update_fields=['views'])

        object = Post.objects.get(text_to_url=self.kwargs['text_to_url'])

        comments = Comment.objects.filter(post=article.id)
        comments_amount = Comment.objects.filter(
                post=article.id).count()


        profile_info = CustomUser.objects.all()


            
        current_user = request.user

        context = {
            'current_user':current_user,
            'profile_info':profile_info,
            'object': object,
            'comments': comments,
            'comments_amount': comments_amount,
        }

        if current_user.is_superuser:
            return render(request, template_name=self.template_name, context=context)
        elif object.published == True:
            return render(request, template_name=self.template_name, context=context)
        else:
            raise Http404()


    def post(self, request, *args, **kwargs):
        article = Post.objects.get(text_to_url=self.kwargs['text_to_url'])
        current_user = request.user

        if request.POST.get('the_comment'):
            # add comment
            text_comment = request.POST.get('the_comment', False)
            new_comment = Comment.objects.create(
                body=text_comment,
                post=article,
                user=current_user
            )
            new_comment.save()

        # add reply to reply
        elif request.POST.get('the_reply_to_reply'):
            
            text_reply_to_reply = request.POST.get('the_reply_to_reply', False)

            # get id of response comment
            reply_id = request.POST['reply_parent']

            # get id of parent of response comment
            parent_id = Comment.objects.filter(id=reply_id).first().parent.id
            parent_instance = Comment.objects.filter(id=parent_id).first()

            # get user to response
            response_to_id = Comment.objects.filter(id=reply_id).get().user.id
            response_to_user = CustomUser.objects.get(id=response_to_id).nickname
            
            new_comment = Comment.objects.create(
                body=text_reply_to_reply,
                post=article,
                user=current_user,
                parent=parent_instance,
                reponse_to=response_to_user,
                reponse_to_id=response_to_id,
            )
            new_comment.save()

        # add reply
        elif request.POST.get('the_reply'):

            text_reply = request.POST.get('the_reply', False)

            parent_id = request.POST['comment_parent']
            parent_instance = Comment.objects.filter(id=parent_id).first()
            response_to_id = Comment.objects.filter(id=parent_id).get().user.id
            response_to_user = CustomUser.objects.get(id=response_to_id).nickname

            new_comment = Comment.objects.create(
                body=text_reply,
                post=article,
                user=current_user,
                parent=parent_instance,
                reponse_to=response_to_user,
                reponse_to_id=response_to_id,
            )

            new_comment.save()

        # comments info (after he add comment it will count them)
        comments = Comment.objects.filter(
            post=article.id)
        comments_amount = Comment.objects.filter(
            post=article.id).count()

        context = {
            'current_user':current_user,
            'object': article,
            'comments': comments,
            'comments_amount': comments_amount,
        }

        return render(request, template_name=self.template_name, context=context)

class EditComment(UpdateView):
    model = Comment
    template_name = 'edit_comment.html'
    form_class = EditCommentForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        comment_user = self.get_object().user

        if comment_user == current_user:
            return super().get(request, *args, **kwargs)
        elif comment_user != current_user:
            raise Http404()

class ReportView(CreateView):
    model = CommentReports
    template_name = 'report_comment.html'
    form_class = ReportCommentForm



    def post(self,request,*args,**kwargs):

        reported_comment = get_object_or_404(Comment, slug=self.kwargs['slug'])
        who_report = request.user
        report_body = request.POST['report_body']

        report = CommentReports.objects.create(
            report_body=report_body,
            reported_comment=reported_comment,
            who_report=who_report,

        )
     
        report.save()
        return redirect(reverse('home'))

class DeleteReport(DeleteView):
    model = CommentReports

    template_name = 'delete_report.html'  

    success_url = reverse_lazy('home')
 
class DeleteComment(DeleteView):
    model = Comment

    template_name = 'delete_comment.html'  

    success_url = reverse_lazy('home')


    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        current_user = self.request.user
        comment_user = comment.user

        if comment_user == current_user:
            return super().get(request, *args, **kwargs)
        elif comment_user != current_user:
            raise Http404()


class AddPost(CreateView):
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm

    def get(self,request,*args,**kwargs):
        categories_amount = len(Category.objects.all())

        
        if categories_amount == 0:
            return HttpResponse("Nie dodałeś jeszcze żadnych kategorii dla tego nie możesz dodać żadnego postu.")
        
        elif categories_amount != 0:
            return super().get(request, *args, **kwargs)

class EditPost(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = EditForm

        
    def get(self,request,*args,**kwargs):
        article = get_object_or_404(Post, slug=self.kwargs['slug'])
        article_author = article.author
        current_user = request.user

        if current_user == article_author:
            return super().get(request, *args, **kwargs)

        elif current_user != article_author:
            raise Http404() 
                
class DeletePost(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

    def get(self,request,*args,**kwargs):
        article = get_object_or_404(Post, slug=self.kwargs['slug'])
        article_author = article.author
        current_user = request.user

        if current_user == article_author:
            return super().get(request, *args, **kwargs)
            
        elif current_user != article_author:
            raise Http404("Strona nie istnieje") 


class AddCategory(CreateView):
    model = Category 
    template_name = 'add_category.html'
    fields = '__all__'

class EditCategory(UpdateView):
    model = Category
    template_name = 'edit_category.html'
    fields = "__all__"
    success_url = reverse_lazy('home')

class DeleteCategory(DeleteView):
    model = Category
    template_name = 'delete_category.html' 
    success_url = reverse_lazy('home')


class AdminPanel(DetailView):
    model = Post
    template_name = 'admin_view.html'

    def get(self,request,*args,**kwargs):

        

        current_user = request.user

        if current_user:

            unpublished_posts = Post.objects.filter(published=False)
            comment_reports = CommentReports.objects.all()
           

            context = {
                'current_user':current_user,
                'unpublished_posts':unpublished_posts,
                'comment_reports':comment_reports,
            }

            return render(request, template_name=self.template_name, context=context)
            

        else:
            raise Http404() 





def search_view(request, *args, **kwargs):
    if 'query' in request.GET:
        query = request.GET['query']
        post_titles = get_blog_queryset(query=query)
        return render(request, 'search.html', {'search_request': query, 'search_results': post_titles})
    else:
        return render(request, 'search.html', {})

def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)
    return(list(set(queryset)))

def get_top_articles_list():

    popular = ArticleStatistic.objects.filter(
        
        date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
    ).values(
        'article_id', 'article__title','article__published','article__text_to_url',
    ).annotate(
        views=Sum(
            'views'
        )
    ).order_by('-views')[:5]

    return popular
