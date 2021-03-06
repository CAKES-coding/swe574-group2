import json

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from wikodeApp.models import Author, Keyword, RegistrationApplication, Article, TagRelation, \
    FollowRelation, Activity,Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wikodeApp.forms import ApplicationRegistrationForm, GetArticleForm, TagForm, FilterForm
from wikodeApp.utils import followManager
from wikodeApp.utils.activityManager import ActivityManager
from wikodeApp.utils.fetchArticles import createArticles
from wikodeApp.utils.voteManager import VoteManager
from wikodeApp.utils.suggestionManager import SuggestionManager
import string
import random
from wikodeApp.utils.textSearch import Search
from dal import autocomplete
from wikodeApp.utils.wikiManager import getLabelSuggestion, WikiEntry, FreeTag
from wikodeApp.utils.feedDTO import Feed


@login_required
def homePage(request):
    if request.method == 'POST':
        search_terms = request.POST.get('searchTerms').split(",")
        search = Search(search_terms)

        filter_form = FilterForm(request.POST)
        if filter_form.is_valid():
            search.filterArticles(filter_form.cleaned_data)
        results_list = search.getSearchResults(filter_form.cleaned_data.get('order_by'))

        page = request.POST.get('page', 1)
        paginator = Paginator(results_list, 25)
        search_str = request.POST.get('searchTerms')
        filter_params = filter_form.cleaned_data

        filter_params_str = '&'.join([filter_key + '=' + str(filter_params.get(filter_key))
                                      for filter_key in filter_params
                                      if filter_params.get(filter_key)]
                                     )
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        if results_list:
            date_data = search.getYearlyArticleCounts()
        else:
            date_data = {}
        context = {"results_list": results,
                   "search_term": search_str,
                   "filter_params": filter_params_str,
                   "date_labels": date_data.keys(),
                   "data_values": date_data.values(),
                   "parent_template": "wikodeApp/searchResults.html",
                   "filter_form": filter_form,
                   "result_size": len(results_list)
                   }
    else:
        # todo: Look for a pagination without rerunning search query
        if request.GET.get('page', False):
            page = request.GET.get('page')
            search_terms = request.GET.get('term').split(",")

            search = Search(search_terms)
            filter_params = {
                "start_date": request.GET.get('start_date', None),
                "end_date": request.GET.get('end_date', None),
                "author_field": request.GET.get('author_field', None),
                "journal_field": request.GET.get(('journal_field', None)),
                "keywords_field": request.GET.get('keywords_field', None),
                "order_by": request.GET.get('order_by', None)
            }
            search.filterArticles(filter_params)
            results_list = search.getSearchResults(filter_params.get('order_by'))

            paginator = Paginator(results_list, 25)
            search_str = request.GET.get('term')

            filter_params_str = '&'.join([filter_key + '=' + str(filter_params.get(filter_key))
                                          for filter_key in filter_params
                                          if filter_params.get(filter_key)]
                                         )

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            context = {"results_list": results,
                       "search_term": search_str,
                       "filter_params": filter_params_str,
                       "parent_template": "wikodeApp/searchResults.html",
                       "filter_form": FilterForm(initial=filter_params),
                       "result_size": len(results_list)
                       }

        else:
            # In order to get recent activities we retrieve the last 50 activities entered to DB
            recent_activities = Activity.objects.exclude(user=request.user).order_by('-id')[:50]
            feed_list = Feed(recent_activities).getFeed()

            suggestion_manager = SuggestionManager(request.user.id)
            article_suggestionDTO_list = suggestion_manager.get_article_suggestionDTO_list()
            user_suggestionDTO_list = suggestion_manager.get_user_suggestionDTO_list()

            # Then here we show the send the activities frontend
            context = {"parent_template": "wikodeApp/homePage.html",
                       "feedList": feed_list,
                       "articleSuggestionDTOList": article_suggestionDTO_list,
                       "userSuggestionDTOList": user_suggestionDTO_list,
                       "filter_form": FilterForm(initial={'order_by': 'relevance'})}

    return render(request, 'wikodeApp/searchAndFilterBox.html', context=context)


@login_required
def articleDetail(request, pk):
    article = Article.objects.get(pk=pk)
    wiki_info = {}
    fragment_info = {}
    if request.method == 'GET':
        activity_manager = ActivityManager(user=request.user)
        activity_manager.saveViewActivity('3', article.id)
    if request.method == 'POST':
        print(request.POST)
        if 'get_tag' in request.POST:
            # brings tag from wikidata
            tag_form = TagForm(data=request.POST)
            tag_data = WikiEntry(tag_form.data['wikiLabel'])
            wiki_info['qid'] = tag_data.getID()
            wiki_info['label'] = tag_data.getLabel()
            wiki_info['description'] = tag_data.getDescription()
            fragment_info['fragment_text'] = request.POST.get('fragment_text')
            fragment_info['start_index'] = request.POST.get('fragment_start_index')
            fragment_info['end_index'] = request.POST.get('fragment_end_index')

        elif 'add_tag' in request.POST:
            # Tagging an article
            # end index of "-1" means tagging whole article, else is annotation
            if request.POST.get('qid'):
                tag_data = WikiEntry(request.POST['qid'])
                tag = tag_data.saveTag()
                tag_data.saveRelatedWikiItems()

            elif request.POST.get('label'):
                tag = FreeTag(request.POST['label'], request.POST['description']).save()

            else:
                tag = None

            if request.POST.get('fragment_text'):
                fragment_text = request.POST['fragment_text']
                fragment_start_index = request.POST['fragment_start_index']
                fragment_end_index = request.POST['fragment_end_index']
            else:
                fragment_text = ''
                fragment_start_index = 0
                fragment_end_index = -1

            user = User.objects.get(id=request.user.id)
            TagRelation.objects.get_or_create(article=article,
                                              tag=tag,
                                              fragment=fragment_text,
                                              start_index=fragment_start_index,
                                              end_index=fragment_end_index,
                                              tagger=user
                                              )
            activity_manager = ActivityManager(user=request.user)

            if fragment_end_index != "-1":
                activity_manager.saveAnnotationActivity(target_article_id=article.id,
                                                        tag_id=tag.id,
                                                        start_index=fragment_start_index,
                                                        end_index=fragment_end_index)
                activity_manager.saveTaggingActivityForArticle(target_id=article.id,
                                                               tag_id=tag.id)
            else:
                activity_manager.saveTaggingActivityForArticle(target_id=article.id,
                                                               tag_id=tag.id)

        elif 'tag_relation_id' in request.POST:
            # Delete tag from an article
            tag = TagRelation.objects.get(id=request.POST['tag_relation_id'])
            tag.delete()

    tag_form = TagForm()
    authors = Author.objects.filter(article=article)
    keywords = Keyword.objects.filter(article=article)
    keywords_list = ', '.join([item.KeywordText for item in keywords])
    tags = TagRelation.objects.filter(article=article).select_related('tag')

    article_dict = {"authors": authors,
                    "title": article.Title,
                    "abstract": article.Abstract,
                    "pmid": article.PMID,
                    "tag_form": tag_form,
                    "keywords": keywords_list,
                    "tags": tags
                    }

    article_dict.update(wiki_info)
    article_dict.update(fragment_info)

    return render(request, 'wikodeApp/articleDetail.html', context=article_dict)


class TagAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        taglist = getLabelSuggestion(self.q)
        return taglist


def registration(request):
    if request.method == 'POST':
        registration_form = ApplicationRegistrationForm(data=request.POST)
        if registration_form.is_valid():
            if RegistrationApplication.objects.filter(email=request.POST['email']).filter(
                    applicationStatus='1').exists():
                return render(request, 'wikodeApp/registration.html', {'form': registration_form,
                                                                       'under_review': 'An application with this email is currrently under review. Please try again with another email.',
                                                                       'registration_form': registration_form})
            elif User.objects.filter(email=request.POST['email']).filter(is_active='True').exists():
                return render(request, 'wikodeApp/registration.html', {'form': UserCreationForm(),
                                                                       'same_email': 'This email is used before. Please use another email.',
                                                                       'registration_form': registration_form})
            else:
                registration_form.save()
                return render(request, 'wikodeApp/login.html', {'form': UserCreationForm(),
                                                                'success': 'Thank you for your application. Your account will be activated after reviewed carefully.'})
        else:
            return render(request, 'wikodeApp/registration.html', {'registration_form': registration_form})
    else:
        registration_form = ApplicationRegistrationForm()

    return render(request, 'wikodeApp/registration.html', {'registration_form': registration_form})


@login_required
def registrationRequests(request):
    if request.method == 'POST':
        if 'approve' in request.POST:
            approved_request = RegistrationApplication.objects.get(pk=request.POST['approve'])
            approved_request.applicationStatus = '2'
            approved_request.save()
            random_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            user = User(username=approved_request.email,
                        first_name=approved_request.name,
                        last_name=approved_request.surname,
                        email=approved_request.email,
                        password=random_password)
            user.set_password(user.password)
            user.save()

            requests_list = RegistrationApplication.objects.filter(applicationStatus='1').order_by('applicationDate')
            requests_dict = {"registration_requests": requests_list, "password": random_password}
            return render(request, 'wikodeApp/registrationRequests.html', context=requests_dict)

        if 'reject' in request.POST:
            rejected_request = RegistrationApplication.objects.get(pk=request.POST['reject'])
            rejected_request.applicationStatus = '3'
            rejected_request.save()

    requests_list = RegistrationApplication.objects.filter(applicationStatus='1').order_by('applicationDate')
    requests_dict = {"registration_requests": requests_list}
    return render(request, 'wikodeApp/registrationRequests.html', context=requests_dict)


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('wikodeApp:homePage'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            return render(request, 'wikodeApp/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password did not match.'})

    else:
        return render(request, 'wikodeApp/login.html', {})


@login_required
def userList(request):
    if request.method == 'POST':
        if 'user_id' in request.POST:
            removed_user = User.objects.get(pk=request.POST['user_id'])
            removed_user.is_active = False
            removed_user.save()
        elif 'admin_status' in request.POST:
            admin_user = User.objects.get(pk=request.POST['admin_status'])
            admin_user.is_superuser = not admin_user.is_superuser
            admin_user.save()

    users = User.objects.filter(is_active=True)
    cur_username = request.user.username
    admin_status = User.objects.filter(username=cur_username).values_list('is_superuser')
    return render(request, 'wikodeApp/userList.html', {'user_list': users, 'admin': admin_status[0][0]})


@login_required
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('wikodeApp:userLogin'))


@login_required
def getArticles(request):
    if request.method == 'POST':
        form = GetArticleForm(request.POST)

        if form.is_valid():
            createArticles(form.cleaned_data['article_topic'], form.cleaned_data['volume'])
            saved_count = Article.objects.all().count()
            return render(request, 'wikodeApp/articlesSaved.html', {'saved_count': saved_count})
    else:
        form = GetArticleForm()

    return render(request, 'wikodeApp/fetchArticles.html', {'form': form})


## Renders the profilePage.html with the authenticated user's information
## Navigation item 'Profile'sent opens /myprofile url.
@login_required
def myProfilePage(request):
    user = request.user

    follower_list = json.dumps(followManager.getFollowerList(user))
    followee_list = json.dumps(followManager.getFolloweeList(user))

    # In order to get recent activities of a user we retrieve the activities of the current user
    recentActivities = Activity.objects.filter(user_id=user.id)
    feed_list = Feed(recentActivities).getFeed()

    # In order to get tagged articles of the user we filter the articles with user id
    taggedArticles = TagRelation.objects.filter(tagger_id = user.id)
    tagged_articlelist = []
    tagged_article_idlist =[]
    for tags in taggedArticles:
        tag_article_id=tags.article_id
        articleid_url=reverse('wikodeApp:articleDetail', args=(tag_article_id,))
        article=Article.objects.get(id=tag_article_id)
        if (tag_article_id in tagged_article_idlist):
            continue
        article_tags= TagRelation.objects.filter(article_id=tag_article_id)
        tagnames=""
        for taginArticles in article_tags:
            tagnames += taginArticles.tag.label + ", "
        tagnames = tagnames[:-2]
        tagged_articles={"articletitle": article.Title,
                         "PM_id": article.PMID,
                         "tagnames":tagnames,
                         "articleid_url": articleid_url
                         }

        tagged_article_idlist.append(tag_article_id)
        tagged_articlelist.append(tagged_articles)

    # Then here we show the send the activities frontend

    context = {
        'user': user,
        'follower_list': follower_list,
        'followee_list': followee_list,
        "parent_template": "wikodeApp/profilePage.html",
        "feedList": feed_list,
        "tag_list": tagged_articlelist,
    }

    return render(request, 'wikodeApp/profilePage.html', context)


## Renders the profilePage.html with the clicked user's id information as pk
## Navigates to /profile/# url.
@login_required
def getProfilePageOfOtherUser(request, pk):
    other_user = User.objects.get(id=pk)
    session_user = User.objects.get(id=request.user.id)

    if other_user == session_user:
        return redirect('wikodeApp:myProfilePage')

    is_followed = FollowRelation.objects.filter(followee_id=other_user.id, follower_id=session_user.id).exists()

    follower_list = json.dumps(followManager.getFollowerList(other_user))
    followee_list = json.dumps(followManager.getFolloweeList(other_user))

    # In order to get recent activities of a user we retrieve the activities of the current user
    recentActivities = Activity.objects.filter(user_id=other_user.id)
    feed_list = Feed(recentActivities).getFeed()

    # In order to get tagged articles of the user we filter the articles with user id
    taggedArticles = TagRelation.objects.filter(tagger_id=other_user.id)
    tagged_articlelist = []
    #we gather ids here
    tagged_article_idlist = []
    for tags in taggedArticles:
        tag_article_id = tags.article_id
        articleid_url = reverse('wikodeApp:articleDetail', args=(tag_article_id,))
        if (tag_article_id in tagged_article_idlist):
            continue
        article = Article.objects.get(id=tag_article_id)
        article_tags = TagRelation.objects.filter(article_id=tag_article_id)
        tagnames = ""
        for taginArticles in article_tags:
            tagnames += taginArticles.tag.label + ", "
        tagnames = tagnames[:-2]
        #create json for the html
        tagged_articles = {"articletitle": article.Title,
                           "PM_id": article.PMID,
                           "tagnames": tagnames,
                           "articleid_url": articleid_url
                           }
        tagged_article_idlist.append(tag_article_id)
        tagged_articlelist.append(tagged_articles)

    # Then here we show the send the activities frontend

    context = {
        'profile': other_user,
        'is_followed': is_followed,
        'follower_list': follower_list,
        'followee_list': followee_list,
        "parent_template": "wikodeApp/profilePage.html",
        "feedList": feed_list,
        "tag_list": tagged_articlelist,
    }

    return render(request, 'wikodeApp/profilePage.html', context)

## Adds the other_user to session user's followee list.
## If already following, unfollows it.
## 'Can follows Kenan'
## Can = Follower
## Kenan = Followee
@login_required
def followUser(request, pk):
    other_user = User.objects.get(id=pk)
    session_user = User.objects.get(id=request.user.id)
    activityManager = ActivityManager(session_user)

    ## is_followed is True when the session user is already following the other user.
    is_followed = FollowRelation.objects.filter(followee_id=other_user.id, follower_id=session_user.id).exists()

    if is_followed:
        activityManager.saveUnfollowActivity(other_user.id)
        following = FollowRelation.objects.get(follower_id=session_user.id, followee_id=other_user.id)
        following.delete()
    else:
        activityManager.saveFollowActivity(other_user.id)
        FollowRelation.objects.create(follower_id=session_user.id, followee_id=other_user.id)

    ## Return Follow/Unfollow button appearance is determined by is_followed value.
    ## If True don't show Follow button, show Unfollow instead.
    return redirect('wikodeApp:getProfilePageOfOtherUser', pk)


@login_required()
def vote(request):
    vote_manager = VoteManager(user_id=request.user.id)
    if request.method == 'POST':
        tag_relation_id = request.POST.get('tagRelationId')
        vote_type = request.POST.get('voteType')

        activity_manager = ActivityManager(user=request.user)
        tag_relation = TagRelation.objects.get(id=tag_relation_id)
        tag_id = tag_relation.tag_id
        article_id = tag_relation.article_id
        if vote_type == 'upVote':
            vote_manager.upVote(tag_relation_id)
            activity_manager.saveUpvoteActivity(tag_id, article_id)
        else:
            vote_manager.downVote(tag_relation_id)
            activity_manager.saveDownvoteActivity(tag_id, article_id)

        vote_sum = vote_manager.getVoteSum(tag_relation_id)
        TagRelation.objects.filter(id=tag_relation_id).update(vote_sum=vote_sum)
        user_vote = vote_manager.getUserVote(tag_relation_id)
        return JsonResponse({"voteSum": vote_sum, "userVote": user_vote}, status=200)
    else:
        tag_relation_ids = request.GET.get('tagRelationIds').split(',')
        user_vote_dict = vote_manager.getUserVoteDict(tag_relation_ids)
        return JsonResponse({"userVoteDict": user_vote_dict}, status=200)


def error(request, *args, **argv):
    return render(request, 'wikodeApp/error.html')
