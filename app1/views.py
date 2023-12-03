from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout 

from django.db.models import Q
from .models import News,Comment
from django.contrib.auth.models import User
from .forms import CommentForm


# Create your views here.
def index(request):
    newsdata = News.objects.all()

    return render(request,'index.html',{'newsdata':newsdata})

@login_required
def details(request,id):
    data = News.objects.get(id=id)   
    comments= Comment.objects.all()
    news = get_object_or_404(News, pk=id) 
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news

            # Ensure that the author is set to the current user
            if request.user.is_authenticated:
                new_comment.author = request.user
                new_comment.save()
                return redirect('details', id=id)
            else:
                # Handle the case when the user is not authenticated
                return redirect('signin')  # Redirect to the login page or handle as appropriate
    else:
        comment_form = CommentForm()

    return render(request,'details.html',{'data':data, 'comment_form':comment_form,'news':news,'comments':comments})


def news_filter(request):
    query = request.GET.get('q')
    #location_query = request.GET.get('location')
    #language__query = request.GET.get('language')

    # Initial queryset
    news = News.objects.all()


    if query:
        # Apply filters based on the query
        news = news.filter(
            Q(location__icontains=query) |
            Q(language__icontains=query)
        )  # Ensure you have model instances  
   
    return render(request,'news_filter.html',{'news': news, 'query':query})

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Your Password1  and password2 are not same.")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('signup')
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1= request.POST.get('password1')
        print(username,password1)
        user=authenticate(request,username=username,password=password1)
        
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            print(username,password1)
            return HttpResponse("Password is incorrect")
        
    return render(request,'signin.html')

def logoutpage(request):
    logout(request)
    return redirect('signin')
