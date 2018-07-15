from django.contrib.auth.mixins import *
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import *

from ForumsApp.Views.auth import UpdateLoginTimeView
from ForumsApp.models import *


class UsersListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model=User
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context=super(UsersListView,self).get_context_data(**kwargs)
        context['users']=User.objects.all()
        context.update({'user_permissions':self.request.user.get_all_permissions,})
        return context

class UserDetailsView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model=User
    template_name = 'Userinfo.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        key=self.kwargs.get('pk')
        context = super(UserDetailsView, self).get_context_data(**kwargs)
        context['questionsCount']=len(Questions.objects.values().filter(username_id=key))
        context['answersCount']=len(Answers.objects.values().filter(username_id=key))
        context['commentsCount']=len(AnswersComments.objects.values().filter(username_id=key))
        context['userid']=key
        context.update({'user_permissions':self.request.user.get_all_permissions,})
        return context


class UserQuestionsListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model=User
    template_name = 'userQuestions.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        key=self.kwargs.get('pk')
        context = super(UserQuestionsListView, self).get_context_data(**kwargs)
        context['questions']=Questions.objects.all().values('id','title','username__username').filter(username_id=key).annotate(count=Count('answers__id'))
        context.update({'user_permissions':self.request.user.get_all_permissions,})
        return context