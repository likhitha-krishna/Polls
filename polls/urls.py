from django.urls import path
from .views import QuestionCreate,QuestionList,QuestionDetail,VoteAPIView, ResultsView, CodeBasedResultView
from . import views


app_name = "polls"
urlpatterns = [
    path("",views.home,name="home"),
    path("create-question/",QuestionCreate.as_view(),name="create_question"),
    path("questions-list/",QuestionList.as_view(),name="questions_list"),
    path("view-question/<str:code>/",QuestionDetail.as_view(),name="question_detail"),
    path("vote/",VoteAPIView.as_view(),name="vote"),
    path("results/",ResultsView.as_view(),name="view_results"),
    path("result/<str:code>/",CodeBasedResultView.as_view(),name="codebased_results"),
] 

