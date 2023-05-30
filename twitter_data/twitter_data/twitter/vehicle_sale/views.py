import nltk
from django.shortcuts import render
from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Product,Review_added
from .forms import RateForm
from django.http import HttpResponseRedirect,response
from django.http import HttpResponse,FileResponse
import csv
import pandas as pd
import sys
from textblob import TextBlob
import tweepy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from IPython.display import display
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix,roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn import naive_bayes


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(request, "There was error logging in try again....")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html');
def login_admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user.is_superuser:
            login(request, user)
            return redirect('home')

        else:
            messages.success(request, "There was error logging in try again....")
            return redirect('admin-login')
    else:
        return render(request, 'authenticate/admin-login.html');
def logout_user(request):
    logout(request)
    messages.success(request,"You Are Logged Out!")
    return redirect('login')
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password= password)
            login(request,user)
            messages.success(request, "Registered Successfully")
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request,'authenticate/register_user.html',{'form':form})
def home(request):

    return render(request,'home.html',{})
def all_product(request):
    product_list = Product.objects.all()
    return render(request, 'product_list.html',
                  {'product_list':product_list})
def show_product(request,product_id):
    product=Product.objects.get(pk=product_id)
    return render(request,'show_product.html',{'product':product})
def rate(request):
    product = Product.objects.all()
    submitted = False
    # form = VenueForm
    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            form.save()
            # submitted = True
            return HttpResponseRedirect('/rate?submitted=True')
    else:
        form = RateForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'rate.html', {'form': form, 'submitted': submitted, 'product':product})

def review_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachement; filename = rate.csv'
    #create a csv writer
    writer = csv.writer(response)
    writer.writerow(['Product Name','Review'])

    review = Review_added.objects.all()
    print(review)

    for rate in review:
        writer.writerow([rate.product_selected,rate.review])

    return response
def classification(request):
    submitted = False
    # form = VenueForm
    product = Product.objects.all()
    if request.method == "POST":
        status = ' '
        val1 = request.POST["Product_name"]
        row = pd.read_csv("C:/Users/V G Varghese/Downloads/rate.csv", usecols=['Product Name', 'Review'])
        row.set_index("Product Name", inplace=True)
        rows = row.loc[[val1],
                           ["Review"]]
        n= len(rows.index)
        print(n)
        pol = rows['polarity'] = rows.apply(lambda x: TextBlob(x['Review']).sentiment.polarity, axis=1)
        sub =rows['subjectivity'] = rows.apply(lambda x: TextBlob(x['Review']).sentiment.subjectivity, axis=1)
        avg = rows['polarity'].mean()
        avg = avg/n
        print(avg)
        review = Review_added.objects.all().filter(product_selected=val1)
        if avg <0:
            status = 'negative-Reviews'
        elif avg >0:
            status = 'positive'
        else:
            status = 'neutral'
        print(rows)
        print(avg)
        submitted=True
        return render(request, 'classify.html', {'val1':val1,'avg':avg,'review':review,'rows': rows, 'submitted':submitted,'product': product,'status':status})
    else:
        return render(request, 'classify.html',{'submitted':submitted,'product': product})

def classifytweets(request):
    submitted = False
    positive =False
    neutral = False
    negetive =False
    if request.method == "POST":
        api_key = "NLDxY7Jj92Ryc2c7QWr4i93pD"
        api_key_s = "vikXgk4Kl1BGZX9S6maSI1BJtehOj6JbZ4Kj8B2oSKGSfmhZyp"
        access_token = "1462785832083886080-ezNwLx1xaN0KGYPjus5VRSOjoFW6rb"
        acces_token_secret = "609Qy62vaxvarwTX7ZDFZ4aiP6pJP4igCFJqVkcQbAReP"
        token = "AAAAAAAAAAAAAAAAAAAAAPJFWAEAAAAA348RxFdpTkN%2Bowzxhi32kzFu9Rk%3DOyGr4sj0DqxGMN8HmYCviEC9xbKfWPeRmN0Mb2WxzrFB5xxboy"
        auth_handeler = tweepy.OAuthHandler(consumer_key=api_key,consumer_secret=api_key_s)
        auth_handeler.set_access_token(access_token,acces_token_secret)

        api = tweepy.API(auth_handeler)
        search_item = request.POST["product"]
        tweets_amount = 200
        tweets =tweepy.Cursor(api.search_tweets, q=search_item,lang = 'en').items(tweets_amount)

        #processing data and cleaning data set
        pol = 0
        for tweet in tweets:
            final_text = tweet.text.replace('RT','')
            if final_text.startswith(' @'):
                position = final_text.index(':')
                final_text = final_text[position+2:]
            if final_text.startswith('@'):
                position = final_text.index(' ')
                final_text = final_text[position+2:]
            analysis = TextBlob(final_text)
            print(tweets)
            pol += analysis.polarity
            pol = pol/200
        submitted = True
        if pol < 0:
           negetive = True
        elif pol > 0:
            positive = True
        else:
            neutral = True


        return render(request, 'tweets.html',{'positive':positive,'negetive':negetive,'neutral':neutral,'submitted':submitted,'pol':pol})
    else:
        return render(request,'tweets.html',{'submitted':submitted})

def naivebayes(request):
   data = pd.read_csv("C:/Users/V G Varghese/Downloads/twitter/carreviews.csv",encoding='cp1252', names=['liked','txt'])
   # nltk.download('stopwords')
   stopset = set(stopwords.words('english'))
   vectorizer = TfidfVectorizer(use_idf=True, lowercase=True, strip_accents='ascii', stop_words=stopset)
   y=data.liked
   X = vectorizer.fit_transform((data.txt).apply(lambda x: np.str_(x)))


   print(y.shape,X.shape)
   X_train, X_test,y_train,y_test = train_test_split(X,y,random_state=42)
   clf = naive_bayes.MultinomialNB()
   clf.fit(X_train,y_train)
   print(roc_auc_score(y_test, clf.predict_proba(X_test)[:,1]))
   submitted = False

   val1 = 'Hyundai-Verna'
   status = ' '

   row = pd.read_csv("C:/Users/V G Varghese/Downloads/rate.csv", usecols=['Product Name', 'Review'])
   row.set_index("Product Name", inplace=True)
   rows = row.loc[[val1],
                      ["Review"]]
   print(rows)
   k= rows.loc[:,"Review"]

   sum=0
   a = []
   for rev in k:
       a.append(rev)
   print(a)
   r = np.array(a)
   r=[r]
   for x in r:
       y = vectorizer.transform(x)
       score = clf.predict(y)
   print(score)
   lis = score.tolist()
   n = len(lis)
   for s in lis:
       sum = sum+s
   print(sum/n)

   return render(request,'home.html',{})