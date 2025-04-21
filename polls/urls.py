from django.urls import path
from .views import QuestionCreate,QuestionList,QuestionDetail,VoteAPIView, ResultsView

app_name = "polls"
urlpatterns = [
    path("create-question/",QuestionCreate.as_view(),name="create_question"),
    path("questions/",QuestionList.as_view(),name="questions_list"),
    path("question/<str:code>/",QuestionDetail.as_view(),name="question_detail"),
    path("vote/",VoteAPIView.as_view(),name="vote"),
    path("results/<str:code>/",ResultsView.as_view(),name="view_results"),
] 

