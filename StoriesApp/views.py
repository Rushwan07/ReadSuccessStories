from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post


# Create your views here.


def index(request):
    Allpost = Post.objects.all()
    context = {'Allpost': Allpost}
    return render(request, 'FirstPage.html', context)


def post(request, slug):
    post = Post.objects.filter(slug=slug).first()
    print(request.user)
    context = {'post': post}
    return render(request, 'Post.html', context)


def like(request):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=request.POST.get('Pid'))
        likes = post.like.add(request.user)
        count = post.like.all().count()
        print(count)
        # id = request.POST.get('Pid')
        # print(id)
        # if Post.objects.filter(slug=id).exists:
        #     like = Post.like.add(request.user)
        return JsonResponse({
            'status': True,
            'likes': count
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
        y = "Result Not Found"
        t = "t"
        params = {'y': y, 'true': t}
        return render(request, "search.html", params)
    params = {'Allpost': Allpost, 'quary': quary}
    return render(request, 'search.html', params)
