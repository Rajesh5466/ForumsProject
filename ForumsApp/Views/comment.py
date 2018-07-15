from django.contrib.auth.mixins import *
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from ForumsApp.Forms import *
from ForumsApp.Views.auth import UpdateLoginTimeView
from ForumsApp.models import *



class CommentListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    model=AnswersComments
    template_name = 'comments.html'

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        key=self.kwargs.get('pk1')
        context=super(CommentListView,self).get_context_data(**kwargs)
        context['data']=self.model.objects.values('id','description','username__username','username__id').filter(answer_id=key)
        context['datalen']=len(context['data'])
        context['answerinfo']=Answers.objects.values('id','description','question_id','username__username').get(pk=key)
        context.update({'user_permissions':self.request.user.get_all_permissions,})
        return context


class CreateCommentView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = AnswersComments
    template_name = 'answerform.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        user =self.request.user
        Comment_form = CommentForm(request.POST)
        if Comment_form.is_valid():
            Comment=Comment_form.save(commit=False)
            Comment.username=user
            Comment.answer=get_object_or_404(Answers,pk=self.kwargs.get('pk1'))
            Comment.save()
        return redirect('ForumsApp:answer',pk=self.kwargs.get('pk'))



class EditCommentView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    model=AnswersComments
    form_class = CommentForm
    template_name = 'answerform.html'
    success_url = reverse_lazy('ForumsApp:allQuestions')

    def has_permission(self):
        Comment_uid=AnswersComments.objects.values('username__id').get(id=self.kwargs.get('pk2'))
        request_uid=self.request.user.id
        if Comment_uid['username__id']==request_uid:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        UpdateLoginTimeView.updateTime(self.request)
        context = super(EditCommentView, self).get_context_data(**kwargs)
        context.update({
            'form':CommentForm(instance=AnswersComments.objects.get(id=self.kwargs.get('pk2'))),
        })

        return context

    def post(self, request, *args, **kwargs):
        user =self.request.user
        Comment_form = CommentForm(request.POST,instance=AnswersComments.objects.get(id=self.kwargs.get('pk2')))
        if Comment_form.is_valid():
            Comment=Comment_form.save(commit=False)
            Comment.username=user
            Comment.answer=get_object_or_404(Answers,pk=self.kwargs.get('pk1'))
            Comment.save()
        return redirect('ForumsApp:getComment',pk=self.kwargs.get('pk'),pk1=self.kwargs.get('pk1'))
