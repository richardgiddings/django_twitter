from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django_twitter_search.twitter_code.tweets import *
from .models import Tweet
from dateutil import parser

# Number of tweets to return.
# May move this out to enable user to change at some point
TWEETS = 20

def index(request):
    """
    Shows the search box and search button
    """
    return render(request, 'django_twitter_search/index.html')

def archive(request):

    archived_tweets = Tweet.objects.all()

    return render(request, 'django_twitter_search/archive.html', 
                            context={"tweets": archived_tweets})

def search(request):
    """
    Retrieves tweets
    """
    search_term = request.GET.get('search_term')
    results = search_twitter(search_term, TWEETS)

    return render(request, 'django_twitter_search/index.html', 
                            context={"results": results})

def save(request):

    if request.POST:
        tweet = Tweet()
        tweet.name = request.POST.get('name', '')
        tweet.screen_name = request.POST.get('screen_name', '')
        tweet.profile_image_url = request.POST.get('profile_image_url', '')
        tweet.text = request.POST.get('text', '')
        tweet.retweets = request.POST.get('retweet_count', '')
        tweet.favourites = request.POST.get('favorite_count', '')
        tweet.date = parser.parse(request.POST.get('created_at', ''))

        tweet.save()

    return redirect(reverse('django_twitter_search:archive'))

def delete(request, tweet_id=None):

    if request.POST:
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        tweet.delete()

    archived_tweets = Tweet.objects.all()

    return render(request, 'django_twitter_search/archive.html', 
                            context={"tweets": archived_tweets})