from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Viewers


# Create your views here.


def index(request):
    Allpost = Post.objects.all()
    context = {'Allpost': Allpost}
    return render(request, 'FirstPage.html', context)


def post(request, slug):
    post = Post.objects.filter(slug=slug).first()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for is not None:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if Viewers.objects.filter(ipslug=ip).count() == 0:
        ipc = Viewers(ipslug=ip)
        ipc.save()
    else:
        ipc = Viewers.objects.filter(ipslug=ip).first()

    if ipc not in post.views.all():
        post.views.add(ipc)
    print("Views::",post.views.all().count())
    context = {'post': post}
    return render(request, 'Post.html', context)


def like(request):
    if request.method == 'POST':
        likeStatus = False
        post = get_object_or_404(Post, slug=request.POST.get('Pid'))
        if request.user in post.like.all():
            post.like.remove(request.user)
            likeStatus = False
        else:
            post.like.add(request.user)
            likeStatus = True
        count = post.like.all().count()
        # id = request.POST.get('Pid')
        # print(id)
        # if Post.objects.filter(slug=id).exists:
        #     like = Post.like.add(request.user)
        return JsonResponse({
            'status': True,
            'likeStatus': likeStatus,
            'likes': count
        })


def favourite(request):
    if request.method == 'POST':
        saveStatus = False
        post = get_object_or_404(Post, slug=request.POST.get('Pid'))

        if request.user in post.Favourite.all():
            post.Favourite.remove(request.user)
            saveStatus = False
        else:
            post.Favourite.add(request.user)
            saveStatus = True

        return JsonResponse({
            'status': True,
            'saveStatus': saveStatus,
        })


def signupHandle(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if (username or email or password) == "":
            return redirect('index')
        elif not username.isalnum():
            return HttpResponse("Only Charecter are allow.")
        elif User.objects.filter(username=username).exists():
            return HttpResponse("User name aready taken")

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("../")
        return redirect('../')
    return render(request, 'signup.html')


def logoutHandle(request):
    logout(request)
    return redirect("../")


def loginHandle(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('Story_App:index')
        else:
            return redirect('Story_App:index')
    return render(request, 'login.html')


def search(request):
    quary = request.GET['quary']
    if len(quary) == 70:
        Allpost = Post.objects.none()
    else:
        AllpostName = Post.objects.filter(name__icontains=quary)
        Allpostcontent = Post.objects.filter(content__icontains=quary)
        Allpost = AllpostName.union(Allpostcontent)
    if Allpost.count() == 0:
        y = "No Result Found"
        t = "t"
        params = {'y': y, 'true': t}
        return render(request, "search.html", params)
    params = {'Allpost': Allpost, 'quary': quary}
    return render(request, 'search.html', params)


def SavePost(request):
    post = Post.objects.filter(Favourite=request.user)
    if not Post.objects.filter(Favourite=request.user):

        text = 'Zero Stories in your Favourite List'
        context = {'Text': text}
        return render(request, 'Fvr.html', context)
    context = {'Allpost': post}

    return render(request, 'Fvr.html', context)
