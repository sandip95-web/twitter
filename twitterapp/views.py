from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Tweet
from django.contrib import messages
from . form import TweetForm,SignUpForm,ProfilePicForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        forms=TweetForm(request.POST or None)
        if request.method == "POST":
            if forms.is_valid():
                tweet=forms.save(commit=False)
                tweet.user=request.user
                tweet.save()
                messages.success(request,"Your Tweet Has Been Posted")
                return redirect("index")
        tweets=Tweet.objects.all().order_by("-created_at")
        return render(request,'index.html',{"tweets":tweets,"forms":forms})
    else:
        tweets=Tweet.objects.all().order_by("-created_at")
        return render(request,'index.html',{"tweets":tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles=Profile.objects.exclude(user=request.user)
        return render(request,'profile_list.html',{"profiles":profiles})
    else:
        messages.warning(request,"You Must be Logged in")
        return redirect("index")

def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:        
            profiles=Profile.objects.get(user_id=pk)
            return render(request,'followers.html',{"profiles":profiles})
        else:
            messages.warning(request,"That's not your Profile")
            return redirect("index")
    else:
        messages.warning(request,"You Must be Logged in")
        return redirect("index")

def following(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:        
            profiles=Profile.objects.get(user_id=pk)
            return render(request,'following.html',{"profiles":profiles})
        else:
            messages.warning(request,"That's not your Profile")
            return redirect("index")
    else:
        messages.warning(request,"You Must be Logged in")
        return redirect("index")


            
            

def unfollow(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request,f"You Have successfully unfollow {profile.user.username}")
        return redirect(request.META.get("HTTP_REFERER"))        
    else:
        messages.warning(request,"You Must Be logged in!")
        return redirect(request.META.get("HTTP_REFERER"))
        
def follow(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request,f"You Have successfully follow {profile.user.username}")
        return redirect(request.META.get("HTTP_REFERER"))        
    else:
        messages.warning(request,"You Must Be logged in!")
        return redirect(request.META.get("HTTP_REFERER"))

def profile(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        tweets=Tweet.objects.filter(user_id=pk)
        if request.method == 'POST':
            current_user_profile=request.user.profile
            action=request.POST.get('follow')   
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request,"profile.html",{"profile":profile,"tweets":tweets})
    else:
        messages.warning(request,"You must be logged in To view this Page");
        return redirect("index")
    
def login_user(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been successfully logged in!")
            return redirect("index")
        else:
            messages.success(request,"Something went wrong!")
            return redirect("login")
    else:
        return render(request,"login.html");

def logout_user(request):
    logout(request)
    messages.success(request,"Successfully Logged out!")
    return redirect("login")

def register_user(request):
    form=SignUpForm()
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You have been successfully logged in")
            return redirect("index")    
    return render(request,"register.html",{"form":form})

def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        profile_user=Profile.objects.get(user__id=request.user.id)
        form=SignUpForm(request.POST or None,instance=current_user)
        profile_form=ProfilePicForm(request.POST or None,request.FILES or None,instance=profile_user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            login(request,current_user)
            messages.success(request,"Your profile has been updated!")
            return redirect("index")
        return render(request,"update_user.html",{"form":form,"profile_form":profile_form})
    else:
        messages.success(request,"You must be logged in to view this page!")
        return redirect("index")
        
def tweet_likes(request,pk):
    if request.user.is_authenticated:
        tweet=get_object_or_404(Tweet,id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,"You must be logged in to view this page!")
        return redirect("index")



def tweet_share(request,pk):
    tweet=get_object_or_404(Tweet,id=pk)
    if tweet:
        return render(request,"tweet_share.html",{"tweet":tweet})
    else:
        messages.success(request,"Tweet doesn't Exist!")
        return redirect("index")

                
def delete(request,pk):
    if request.user.is_authenticated:
        tweet=get_object_or_404(Tweet,id=pk)
        if tweet:
            tweet.delete()
            messages.success(request,"Tweet Successfully Deleted!")
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,"You must be Login!")
        return redirect("index")


def edit(request,pk):
    if request.user.is_authenticated:
        tweet=get_object_or_404(Tweet,id=pk)
        if tweet:
            forms=TweetForm(request.POST or None,instance=tweet)
            if request.method == "POST":
                if forms.is_valid():
                    tweet=forms.save(commit=False)
                    tweet.user=request.user
                    tweet.save()
                    messages.success(request,"Tweet Successfully updated!")
                    return redirect('index')
            else:
                return render(request,'edit.html',{'forms':forms,'tweet':tweet})
    else:
        messages.success(request,"You must be Login!")
        return redirect("index")
    
def search_tweet(request):
    if request.method == "POST":
        search=request.POST.get('search_tweet')
        tweets=Tweet.objects.filter(body__contains=search)
        return render(request,'search_tweet.html',{'search':search,'tweets':tweets})
    else:
     return render(request,'search_tweet.html')
 
def search_user(request):
    if request.method == "POST":
        search=request.POST.get('search_user')
        searched=User.objects.filter(username__contains=search)
        return render(request,'search_user.html',{'search':search,'searched':searched})
    else:
     return render(request,'search_user.html')