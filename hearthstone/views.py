default_encoding = 'utf-8'
from django.shortcuts import render, get_object_or_404
from .models import Image, Voice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm, CommentForm
from haystack.query import SearchQuerySet
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def index(request, tag_slug=None):
    # 獲取圖片列表
    #image_list = Image.objects.all()

    # 產生分頁物件
    object_list = Image.objects.all().order_by('-publish')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 9) # 9 images in each page
    page = request.GET.get('page') # indicates the current page number
    try:
        image_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        image_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        image_list = paginator.page(paginator.num_pages)
    # 將image_list傳入模板逕行數據渲染，然後返回給瀏覽器

    return render(request, 'index.html', {'page':page ,'image_list': image_list, 'tag': tag})

@login_required
def index_detail(request, year, month, day, author_id, id):
    image = get_object_or_404(Image,author=author_id, id=id,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = image.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.image = image
            new_comment.name = request.user.first_name
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'detail.html',
                  {'image': image,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def image_search(request):
    form = SearchForm
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Image).filter(content=cd['query']).load_all()
            # 计算所有结果
            total_results = results.count()

    else:
        cd = {}
        results = {}
        total_results = {}
    return render(request, 'image/search.html',{'form': form, 'cd': cd, 'results': results, 'total_results': total_results})

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like_image.add(request.user)
            else:
                image.user_like_image.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})