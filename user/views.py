from django.http import HttpResponse
from projects.models import ProjectCategory
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .forms import SignUpForm, ReviewForm
from .review_functions import getReviews, averageRating, confirm_work_relationship

def index(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            print(form)
            user.profile.company = form.cleaned_data.get('company')

            user.is_active = False
            print(*form.cleaned_data['categories'])
            user.profile.categories.add(*form.cleaned_data['categories'])
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            from django.contrib import messages
            messages.success(request, 'Your account has been created and is awaiting verification.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

def review(request, reviewed_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user.profile
            review.reviewed = User.objects.get(id=reviewed_id)
            review_success = "False"
            if(confirm_work_relationship(review.reviewer, review.reviewed)):
                review.save()
                review_success = "True"
            return redirect('/?review_success=' + review_success)
    else:
        try:
            User.objects.get(id=reviewed_id)
            form = ReviewForm()
        except:
            return redirect('/')
    user = User.objects.get(id=reviewed_id)
    return render(request, 'user/review.html', {'form': form, 'user': user})


def user_page(request, user_id):
    user = User.objects.get(id=user_id)
    username = user.username
    avg_rating = averageRating(user_id)
    if (avg_rating == 0):
        avg_rating = "-"
    
    reviews = []
    ratings = []
    for review in getReviews(user_id): 
        splitted = str(review).split("-")
        ratings.append(splitted[0])
        reviews.append(splitted[1])

    return render(request, 'user/user_page.html', {'username': username, 'rating': avg_rating, 'reviews': zip(ratings, reviews)})

        

            