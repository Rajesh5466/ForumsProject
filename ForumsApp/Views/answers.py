from django.contrib.auth.mixins import *
from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from ForumsApp.Forms import AnswerForm
from ForumsApp.Views.auth import UpdateLoginTimeView
from ForumsApp.models import *
from django.db.models import *



class AnswerListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    model=Answers
    template_name = 'answers.html'

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        key=self.kwargs.get('pk')
        context=super(AnswerListView,self).get_context_data(**kwargs)
        context['data']=self.model.objects.values('id','description','username__username','username__id','likes','dislikes').filter(question_id=key)
        context['questionid']=key
        context['questionuser']=Questions.objects.values('username__username').get(pk=key)
        context['question']=Questions.objects.values('title','description').get(pk=key)
        context['datalen']=len(context['data'])
        context.update({'user_permissions':self.request.user.get_all_permissions,})
        return context

class UserAnswersListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model=Answers
    template_name = 'userAnswers.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        key=self.kwargs.get('pk')
        context = super(UserAnswersListView, self).get_context_data(**kwargs)
        context['data']=Answers.objects.values('question_id__title','question_id','username__username').filter(username_id=key)
        context.update({'user_permissions':self.request.user.get_all_permissions,})
        return context

class CreateAnswerView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Answers
    template_name = 'answerform.html'
    form_class = AnswerForm

    def post(self, request, *args, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        user =self.request.user
        Answer_form = AnswerForm(request.POST)
        if Answer_form.is_valid():
            Answer=Answer_form.save(commit=False)
            Answer.username=user
            Answer.question=get_object_or_404(Questions,pk=self.kwargs.get('pk'))
            Answer.save()
        return redirect('ForumsApp:answer',pk=self.kwargs.get('pk'))


class EditAnswerView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    model=Answers
    form_class = AnswerForm
    template_name = 'answerform.html'
    success_url = reverse_lazy('ForumsApp:allQuestions')

    def has_permission(self):
        Answer_uid=Answers.objects.values('username__id').get(id=self.kwargs.get('pk'))
        request_uid=self.request.user.id
        if Answer_uid['username__id']==request_uid:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context = super(EditAnswerView, self).get_context_data(**kwargs)
        context.update({
            'form':AnswerForm(instance=Answers.objects.get(id=self.kwargs.get('pk'))),
        })
        return context



class AnswerVotesView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model=AnswerVotes

    def get(self, request, *args, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        answerId=self.kwargs.get('pk1')
        userId=self.kwargs.get('pk2')
        vote_Value=int(self.kwargs.get('pk3'))
        Record=[]
        try:
            Record = get_object_or_404(AnswerVotes,Q(answer_id=answerId) & Q(username_id=userId))
        except:
            pass
        answerRecord=Answers.objects.get(id=answerId)
        if Record:
            if not vote_Value==Record.vote:
                Record.vote=vote_Value
                Record.save()
                if vote_Value == 1:
                    answerRecord.likes=answerRecord.likes+1
                    answerRecord.dislikes = answerRecord.dislikes - 1
                elif vote_Value == -1:
                    answerRecord.likes=answerRecord.likes-1
                    answerRecord.dislikes = answerRecord.dislikes + 1
            else:
                Record.delete()
                if vote_Value==1:
                    answerRecord.likes = answerRecord.likes - 1
                elif vote_Value == -1:
                    answerRecord.dislikes = answerRecord.dislikes - 1
        else:
            obj = AnswerVotes()
            obj.answer=get_object_or_404(Answers,pk=answerId)
            obj.username=get_object_or_404(User,pk=userId)
            obj.vote=vote_Value
            obj.save()
            if vote_Value==1:
                answerRecord.likes = answerRecord.likes + 1
            elif vote_Value==-1:
                answerRecord.dislikes = answerRecord.dislikes + 1

        answerRecord.save()
        return redirect('ForumsApp:answer', pk=self.kwargs.get('pk'))