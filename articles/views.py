from rest_framework import serializers
from .serializers import ArticleSerializer, CommentSerializer,ContactSerializer
from .models import Articles,ViewArticleHistory,SavedArticles
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from .models import Contact,Comment
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
import random

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'All_Articles':'aritcles-list/',
        'One_Article':'article/<str:id>/',
        'Articles_With_Cetgory':'articles-list/cetagory/',
        'User_Login_Token':'token/',
        'Refresh_User_Token':'token/refresh/',
        'Create_User':'create-user/',
        'Search':'search/<str:query>/',
        'Save_Viewed_Articles_Or_As_History_(Login_Required)':'saveArticlesOrHistory/',
        'Get_Saved_Articles_Or_History_(Login_Required)':'getSavedArticlesOrHistory/',
        'Contact_(Login_Required)':'contact/',
        'Notification_(Login_Required)':'notification/',
        'Save_Comments_(Login_Required)':'save-comments/',
        'Get_Comments':'get-comments/',
        'Delete_Comments_(Login_Required)':'delete-comments/'
    }
    return Response(api_urls)

@api_view(['GET'])
def articlesList(request):
    cetagory = request.GET.get('cetagory')
    quantity = request.GET.get('articlesQty')
    fromNext = request.GET.get('fromNext')
    if(cetagory=='all'):
        if(quantity=='all'):
            articles = Articles.objects.all().order_by('-pub_date')
            articles.update(total_articles_length=len(articles))
            serializer = ArticleSerializer(articles,many=True)
            return Response(serializer.data)
        else:
            articles = Articles.objects.all().order_by('-pub_date')
            articles.update(total_articles_length=len(articles))
            articles = articles[int(fromNext):(int(quantity)+int(fromNext))]
            serializer = ArticleSerializer(articles,many=True)
            return Response(serializer.data)
    else:
        if(quantity=='all'):
            articles = Articles.objects.filter(cetagory=cetagory).order_by('-pub_date')
            articles.update(total_articles_length=len(articles))
            serializer = ArticleSerializer(articles,many=True)
            return Response(serializer.data)
        else:
            articles = Articles.objects.filter(cetagory=cetagory).order_by('-pub_date')[int(fromNext):(int(quantity)+int(fromNext))]
            print(articles)
            articles.update(total_articles_length=len(articles))
            serializer = ArticleSerializer(articles,many=True)
            return Response(serializer.data)

@api_view(['GET'])
def articlesWithCetagory(request):
    catQunatity = request.GET.get('cetagoriesQty')
    articlesQuantity = request.GET.get('articlesQty')
    fromNext = request.GET.get('fromNext')
    articlesOfCet = request.GET.get('cetagoryIs')
    allArticles = Articles.objects.all()
    articlesCet = allArticles.values('cetagory')
    totalCet = [items['cetagory'] for items in articlesCet]
    totalCet = list(set(totalCet))

    if articlesOfCet:
        newArticles = allArticles.filter(cetagory=articlesOfCet)
        totalArticles = len(newArticles)
        newArticles.update(total_articles_length=totalArticles)
        finalArticles = newArticles[int(fromNext):int(articlesQuantity)]

    else:
        if catQunatity == 'all':
            finalArticles = Articles.objects.none()
            for item in totalCet:
                newArticles = allArticles.filter(cetagory=item)
                # newArticles = allArticles.update()
                totalArticles = len(newArticles)
                newArticles.update(total_articles_length=totalArticles)
                newArticles = newArticles[int(fromNext):int(articlesQuantity)]
                finalArticles = newArticles|finalArticles
        else:
            if len(totalCet) >= 3:
                cetToGet = random.sample(totalCet,2)
                finalArticles = Articles.objects.none()
                for item in cetToGet:
                    newArticles = allArticles.filter(cetagory=item)
                    totalArticles = len(newArticles)
                    newArticles.update(total_articles_length=totalArticles)
                    newArticles = newArticles[int(fromNext):int(articlesQuantity)]
                    finalArticles = newArticles|finalArticles
            else:
                cetToGet = random.sample(totalCet,len(totalCet))
                finalArticles = Articles.objects.none()
                for item in cetToGet:
                    newArticles = allArticles.filter(cetagory=item)
                    totalArticles = len(newArticles)
                    newArticles.update(total_articles_length=totalArticles)
                    newArticles = newArticles[int(fromNext):int(articlesQuantity)]
                    finalArticles = newArticles|finalArticles
    serializer = ArticleSerializer(finalArticles,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def article(request,pk):
    article = Articles.objects.get(id=pk)
    serializer = ArticleSerializer(article,many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    loginDetails = ''
    if(not len(request.data['password']) < 8):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = 201
            detail = 'User created successfully!'
            loginDetails = {'email':request.data['email'],'password':request.data['password']}
        else:
            detail = 'User already exist'
            response = 406
    else:
        response = 405
        detail = 'Password is too short.'
    return Response({'response':response,'details':detail,'loginDetails':loginDetails})

@api_view(['POST'])
def saveArticleOrHistory(request):
    article = request.data['article']
    user = request.data['user']
    saveIn = request.data['saveIn']
    article = Articles.objects.get(id=int(article))
    user = User.objects.get(id=int(user))
    if(saveIn == 'History'):
        checkInList = ViewArticleHistory.objects.filter(User=user,Article=article)
        if len(checkInList)>0:
            checkInList.update(date=timezone.now())
        else:
            if ViewArticleHistory.objects.filter(User=user).count()>3:
                ViewArticleHistory.objects.filter(id__in=list(ViewArticleHistory.objects.values_list('pk', flat=True)[:1])).delete()
            ViewArticleHistory.objects.update_or_create(User=user,Article=article)
        detail = 'Article successfully saved in history'
        
    else:
        checkInList = SavedArticles.objects.filter(User=user,Article=article)
        if len(checkInList)>0:
            checkInList.delete()
            detail = 'Article is removed form saved Articles'
        else:
            SavedArticles.objects.update_or_create(User=user,Article=article)
            detail = 'Article successfully saved in Saved Articles'
    return Response({'details':detail})

@api_view(['POST'])
def getSavedArticlesOrHistory(request):
    user = request.data['user']
    getFrom = request.data['getFrom']
    user = User.objects.get(id=int(user))
    allArticles = Articles.objects.all()
    if getFrom == 'History':
        userItems = ViewArticleHistory.objects.filter(User=user).order_by('-date')
        query = Articles.objects.none()
        for items in userItems:
            query = query|allArticles.filter(id=items.Article.id)
        query = query.order_by("-viewarticlehistory__date")
        serializer = ArticleSerializer(query,many=True)

    elif getFrom == 'oneArticle':
        article = request.data['article']
        userItems = SavedArticles.objects.filter(User=user)
        query = Articles.objects.none()
        for items in userItems:
            if items.Article.id == int(article):
                query = allArticles.filter(id=article)
        serializer = ArticleSerializer(query,many=True)

    else:
        userItems = SavedArticles.objects.filter(User=user)
        query = Articles.objects.none()
        for items in userItems:
            query = query|allArticles.filter(id=items.Article.id)
        serializer = ArticleSerializer(query,many=True)

    return Response(serializer.data)





@api_view(['GET'])
def search(request,pk):
    allArticles = Articles.objects.all()
    searchTitle = allArticles.filter(title__icontains=pk)
    searchDesc = allArticles.filter(description__icontains=pk)
    searchCategory = allArticles.filter(cetagory__icontains=pk)
    searchSub_Category = allArticles.filter(sub_cetagory__icontains=pk)
    searchAuthor = allArticles.filter(author__icontains=pk)
    searches = searchTitle|searchDesc|searchCategory|searchSub_Category|searchAuthor
    searches.update(total_articles_length=len(searches))
    serializer = ArticleSerializer(searches,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def contact(request):
    user = request.data['user']
    user = User.objects.get(id=user)
    title = request.data['title']
    desc = request.data['description']
    checkForUser = Contact.objects.filter(User=user).order_by('-date')
    if len(checkForUser)>0:
        nowTime = timezone.now()
        date = (str(checkForUser.first().date)[:19])
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        first = datetime(date.year, date.month, date.day)
        second = datetime(nowTime.year, nowTime.month, nowTime.day)
        if (first-second).days <= -1:
            Contact.objects.update_or_create(User=user,title=title,description=desc,date=timezone.now())
            detail = "Contact request has been created."
        else:
            detail = "Contact request is also pending."
    else:
        Contact.objects.update_or_create(User=user,title=title,description=desc,date=timezone.now())
        detail = "Contact request has been created."
    return Response({'detail':detail})


@api_view(['POST'])
def notification(request):
    user = request.data['user']
    user = User.objects.get(id=user)
    if request.data['work'] == 'fetch':
        userItems = Contact.objects.filter(User=user,seen_by_manager=True).order_by('-date')
        serializer = ContactSerializer(userItems,many=True)
        return Response(serializer.data)
    elif request.data['work'] == 'unseenQuantity':
        userItems = Contact.objects.filter(User=user,seen_by_manager=True,seen_by_user=False)
        userItems = len(userItems)
        return Response({'unseenQuantity':userItems})
    else:
        updateItems = request.data['updateItems']
        userItems = Contact.objects.filter(User=user)
        for items in updateItems:
            userItems.filter(id=int(items)).update(seen_by_user=True)
        return Response('')


@api_view(['POST'])
def saveComments(request):
    user = request.data['user']
    user = User.objects.get(id=user)
    if request.data['work'] == 'comments':
        # save as a comment
        article = request.data['article']
        article = Articles.objects.get(id=article)
        Comment.objects.update_or_create(User=user,Article=article,comment=request.data['commentData'],replay_comment_text=[])
        # send updated list of comments
        allComments = Comment.objects.all().order_by('-create_date')
        comment = allComments.filter(Article=article)
        serializer = CommentSerializer(comment,many=True)
        return Response(serializer.data)
    else:
        mainComment = request.data['main-comment']
        allComments = Comment.objects.all().order_by('-create_date')
        mainComment = allComments.filter(id=mainComment)
        # Saving Replies as A json format
        # getting all existing replies and appendin new replay init.
        allReplies = mainComment[0].replay_comment_text
        for item in allReplies:
            if item['User_id'] == user.id:
                if item['replay_comment_text'] == request.data['commentData']:
                    break
        else:
            allReplies.insert(0,
                {
                    "User_first_name":user.first_name,
                    "User_last_name":user.last_name,
                    "User_id":user.id,
                    "replay_comment_text":request.data['commentData'],
                    "create_date":str(timezone.now())
                }
            )
        mainComment.update(replay_comment_text=allReplies)
        # Sending Return Updated Informartion
        article = request.data['article']
        article = Articles.objects.get(id=article)
        comment = allComments.filter(Article=article)
        serializer = CommentSerializer(comment,many=True)

        return Response(serializer.data)

@api_view(['POST'])
def getComments(request):
    if request.data['work'] == 'comments':
        article = request.data['article']
        article = Articles.objects.get(id=article)
        allComments = Comment.objects.all().order_by('-create_date')
        comment = allComments.filter(Article=article)
            
        serializer = CommentSerializer(comment,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def delComment(request):
    user = request.data['user']
    user = User.objects.get(id=user)
    if request.data['work'] == 'del_comment':
        commentToDel = request.data['commentToDel']
        commentOfUser = Comment.objects.filter(User=user)
        commentOfUser.filter(id=commentToDel).delete()


    else:
        mainComment = request.data['main-comment']
        allComments = Comment.objects.all().order_by('-create_date')
        mainComment = allComments.filter(id=mainComment)
        allReplies = mainComment[0].replay_comment_text
        for item in allReplies:
            if item['User_id'] == user.id:
                if item['replay_comment_text']==request.data['replayToDel']:
                    allReplies.remove(item)
        mainComment.update(replay_comment_text=allReplies)

        
    article = request.data['article']
    article = Articles.objects.get(id=article)
    allComments = Comment.objects.all().order_by('-create_date')
    comment = allComments.filter(Article=article)
    serializer = CommentSerializer(comment,many=True)
        

    return Response(serializer.data)
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['id'] = user.id
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer