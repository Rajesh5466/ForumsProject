
from django.urls import path
from ForumsApp.Views.auth import *
from ForumsApp.Views.comment import *
from ForumsApp.Views.questions import *
from ForumsApp.Views.answers import *
from ForumsApp.Views.users import *

app_name='ForumsApp'

urlpatterns=[
    path('forums/userlastSeen/',UpdateLoginTimeView.as_view(),name='lastseen'),
    path('forums/',LoginView.as_view(),name='login'),
    path('forums/signup/',SignupView.as_view(),name='signup'),
    path('forums/logout/', logout_user, name='logout'),

    path('forums/about/',AboutView),

    path('forums/users/',UsersListView.as_view(),name='getUsers'),
    path('forums/users/<int:pk>/user/',UserDetailsView.as_view(),name='getaUser'),
    path('forums/users/<int:pk>/userquestions/',UserQuestionsListView.as_view(),name='getUserQuestions'),
    path('forums/users/<int:pk>/useranswers/',UserAnswersListView.as_view(),name='getUserAnswers'),


    path('forums/questions/',QuestionListView.as_view(),name='allQuestions'),
    path('forums/questions/ask/',CreateQuestionView.as_view(),name='askQuestion'),
    path('forums/questions/<int:pk>/questionedit/', EditQuestionView.as_view(), name='editQuestion'),
    path('forums/questions/SearchbyTags/',TagSearchView.as_view(),name='TagSearch'),
    path('forums/questions/<str:tag>/alltags/',QuestionTagsListView.as_view(),name="tags"),


    path('forums/questions/<int:pk>/answers/',AnswerListView.as_view(),name='answer'),
    path('forums/questions/<int:pk>/answers/post/',CreateAnswerView.as_view(),name='postAnswer'),
    path('forums/questions/<int:pk1>/answer/<int:pk>/edit/',EditAnswerView.as_view(),name="editAnswer"),
    path('forums/unanswered/',UnansweredListView.as_view(),name='unanswered'),
    path('forums/questions/<int:pk>/answers/<int:pk1>/user/<int:pk2>/vote/<str:pk3>/',AnswerVotesView.as_view(),name='votes'),


    path('forums/questions/<int:pk>/answers/<int:pk1>/commentsView/',CommentListView.as_view(),name='getComment'),
    path('forums/questions/<int:pk>/answers/<int:pk1>/commentForm/', CreateCommentView.as_view(), name='postComment'),
    path('forums/questions/<int:pk>/answers/<int:pk1>/comments/<int:pk2>/commentedit/',EditCommentView.as_view(),name='editComment'),

]