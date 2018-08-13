from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, ImageForm, Voiceform, VoiceUpdateform
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.contrib import messages
Image = apps.get_model('hearthstone', 'Image')
Voice = apps.get_model('hearthstone', 'Voice')

default_encoding = 'utf-8'
# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render (request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):

    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

@login_required
def model_form_upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)  # commit=False tells Django that "Don't send this to database yet, I have more things I want to do with it."
            image.author = request.user      # use your own profile here
            form.save()
            return HttpResponseRedirect('/account/')
    else:
        form = ImageForm()
    return render(request, 'account/model_form_upload_image.html', {
        'form': form
    })


@login_required
def model_form_upload_voice(request):

    if request.method == 'POST':

        form = Voiceform(request, request.POST, request.FILES)

        if form.is_valid():
            voice = form.save(commit=False)  # commit=False tells Django that "Don't send this to database yet, I have more things I want to do with it."
            voice.author = request.user  # use your own profile here
            form.save()
            return render(request, 'account/upload_done.html')
    else:
        form = Voiceform(request)
    return render(request, 'account/model_form_upload_voice.html', {
        'form': form
    })

@login_required
def profile_data(request):

    # 產生分頁物件
    object_list = Image.objects.all().filter(author=request.user).order_by('-publish')
    paginator = Paginator(object_list, 10) # 9 images in each page
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

    return render(request, 'account/profile_data.html', {'page':page ,'image_list': image_list})

@login_required
def edit_profile_image(request, id):

    if request.method == 'POST':
        img = Image.objects.get(pk=id)
        form = ImageForm(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/profile/')

    else:
        img = Image.objects.get(pk=id)
        form = ImageForm(instance=img)

    return render(request, 'account/editimg.html', { 'form':form })

@login_required
def edit_profile_voice_detail(request, id):

    if request.method == 'POST':
        voice = Voice.objects.get(pk=id)
        form = VoiceUpdateform(request.POST, request.FILES, instance=voice)

        if form.is_valid():
            '''obj = form.save(commit=False)                  #update_fields is an argument to a model's save() method, not to the form's save() method.
            obj.save(update_fields=['audio_file'])'''
            form.save()
            return HttpResponseRedirect('/account/profile/edit_voice/' + str(id))
    else:
        voice = Voice.objects.get(pk=id)
        form = VoiceUpdateform(instance=voice)
    return render(request, 'account/editvoice_detail.html', {
        'form': form, 'voice': voice
    })

@login_required
def edit_profile_voice_list(request, id):
    image_list = Image.objects.all().filter(id=id)
    # 產生分頁物件
    voice_list = Voice.objects.all().filter(image_id=id)

    return render(request, 'account/editvoice.html', {'voice_list': voice_list, 'image_list': image_list})


@login_required
def image_delete(request, id):
    instance = get_object_or_404(Image, id=id)
    if request.user == instance.author:
        instance.delete() # or save edits
        messages.success(request, "已成功刪除")
        return HttpResponseRedirect('/account/profile/')
    else:
        raise PermissionDenied # import it from django.core.exceptions
        return HttpResponseRedirect('/account/profile/')