from projects.models import get_taskOffer
from .models import Profile, Review
from django.contrib.auth.models import User

def getReviews(reviewed_id):
    return Review.objects.filter(
        reviewed = User.objects.get(id=reviewed_id))

def averageRating(user_id):
    sum = 0
    reviews = getReviews(user_id)
    for review in reviews:
        sum += review.rating
    if(len(reviews) > 0):
        return round(sum/len(reviews), 2)
    else:   
        return 0

def confirm_work_relationship(reviewer, reviewed):
    reviewer_profile = reviewer
    # Convert from User to profile, Reviewed is stored as a User
    reviewed_profile = Profile.objects.get(user=reviewed)
    relationship = False
    finished_statuses= ['ps', 'dd']

    for offer in get_taskOffer(reviewed_profile):
        if((offer.task.project.user == reviewer_profile) and offer.task.status in finished_statuses):
            relationship = True

    for offer in get_taskOffer(reviewer_profile):
        if((offer.task.project.user == reviewed_profile) and (offer.task.status in finished_statuses)):
            relationship = True
            

    return relationship

def confirm_duplicate_review(reviewer, reviewed):
    duplicate = False
    for review in Review.objects.filter(reviewer = reviewer):
        if review.reviewed == reviewed:
            duplicate = True
    
    return duplicate


def getAvgRating(self):
    return averageRating(self.id)


User.add_to_class("getAvgRating", getAvgRating)