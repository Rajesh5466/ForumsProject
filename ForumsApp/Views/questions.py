from datetime import datetime

from django.contrib.auth.mixins import *
from django.shortcuts import *
from django.urls import reverse_lazy
from django.views.generic import *
from django.db.models import *
from ForumsApp.Forms import *
from ForumsApp.Views.auth import UpdateLoginTimeView
from ForumsApp.models import *


class QuestionListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Questions
    template_name = 'questions.html'

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['data'] = self.model.objects.all().values('id', 'title', 'username__username','tags').annotate(
            count=Count('answers__id'))
        context['datalen'] = len(context['data'])
        context.update({'user_permissions': self.request.user.get_all_permissions, })
        return context

class TagSearchView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Questions
    template_name = 'Tagform.html'
    form_class = TagForm

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context = super(TagSearchView, self).get_context_data(**kwargs)
        queryset=Questions.objects.values('tags')
        tagsList=[]
        for query in queryset:
            tagsList=tagsList+query['tags'].split("#")[1:]
        tagsSet=set(tagsList)
        context['tags']=[(y,tagsList.count(y)) for y in tagsSet ]
        context.update({'user_permissions': self.request.user.get_all_permissions, })
        return context


    def post(self, request, *args, **kwargs):
        T_form = TagForm(request.POST)
        return redirect('ForumsApp:tags',tag=T_form.data['tags'])

class QuestionTagsListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Questions
    template_name = 'questions.html'

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context = super(QuestionTagsListView, self).get_context_data(**kwargs)
        tag=self.kwargs.get('tag')
        context['data']=Questions.objects.filter(Q(tags__contains=tag+"#") | Q(tags__endswith=tag)).values('id', 'title', 'username__username','tags').annotate(count=Count('answers__id'))
        context['datalen']=len(context['data'])
        context.update({'user_permissions': self.request.user.get_all_permissions, })
        return context

class UnansweredListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model=Questions
    template_name = 'questions.html'

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context = super(UnansweredListView, self).get_context_data(**kwargs)
        context['data'] = self.model.objects.all().values('id', 'title', 'username__username','tags').annotate(
            count=Count('answers__id')).filter(count=0)
        context['datalen']=len(context['data'])
        # print(context['data'])
        context.update({'user_permissions': self.request.user.get_all_permissions, })
        return context

class CreateQuestionView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Questions
    template_name = 'questionform.html'
    form_class = QuestionForm
    success_url = reverse_lazy('ForumsApp:allQuestions')


    def get(self, request, *args, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        Q_form = QuestionForm(request.POST)
        if Q_form.is_valid():
            tags = Q_form.cleaned_data['tags']
            if not tags[0] == '#':
                tags='#'+tags
            Question = Q_form.save(commit=False)
            Question.username = user
            Question.tags=tags
            Question.save()
        return redirect('ForumsApp:allQuestions')


class EditQuestionView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Questions
    form_class = QuestionForm
    template_name = 'questionform.html'
    success_url = reverse_lazy('ForumsApp:allQuestions')

    def has_permission(self):
        Q_uid=Questions.objects.values('username__id').get(id=self.kwargs.get('pk'))
        request_uid=self.request.user.id
        if Q_uid['username__id']==request_uid:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context = super(EditQuestionView, self).get_context_data(**kwargs)
        context.update({
            'form':QuestionForm(instance=Questions.objects.get(id=self.kwargs.get('pk'))),
        })
        return context



def AboutView(request):
    UpdateLoginTimeView.updateTime(request)
    return render(request, 'about.html')
