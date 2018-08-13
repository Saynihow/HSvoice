default_encoding = 'utf-8'
from django.shortcuts import render, get_object_or_404
from .models import Image, Voice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from haystack.query import SearchQuerySet


def index(request):
    # 獲取圖片列表
    #image_list = Image.objects.all()

    # 產生分頁物件
    object_list = Image.objects.all().order_by('-publish')
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

    return render(request, 'index.html', {'page':page ,'image_list': image_list})

def index_detail(request, year, month, day, title):
    image = get_object_or_404(Image, title=title,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'detail.html',
                  {'image': image})


def image_search(request):
    form = SearchForm
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Image).filter(content=cd['query']).load_all()
            # 計算所有結果
            total_results = results.count()

    else:
        cd = {}
        results = {}
        total_results = {}
    return render(request, 'image/search.html',{'form': form, 'cd': cd, 'results': results, 'total_results': total_results})