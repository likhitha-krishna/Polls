from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
#from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Question,Choice, Vote
from .serializers import QuestionSerializer , ChoiceSerializer, VoteSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination


def home(request):
    response_data = """
    <h1><b> Welcome to my POLLS project</b></h1>
    <h2>Please register here to access specified options :</h2>
    <a href="/register/">Register here</a><br>
    <h2>Please select an options below to continue :</h2>
    <a href="/questions-list/">List of Questions</a><br>
    <a href="/view-question/<str:code>/">View Question</a><br>
    <a href="/vote/">Do Vote</a><br>
    <a href="/results/">Show result</a><br>
    <h2>Filter based URLs:</h2>
    <a href="/questions/">Get required Question</a><br>
    <a href="/choice/">Get required Choice</a><br>
    <a href="/voters/">Get voters history</a><br>

    """
    return HttpResponse(response_data)


class QuestionList(APIView):
    """
    List of all question
    """
    # serializer_class = QuestionSerializer
    # permission_classes=[IsAdminOrReadOnly]

    # def get(self,request):

    #     questions = Question.objects.all()
    #     serializer = QuestionSerializer(questions,many=True)
    #     return Response(serializer.data)   

    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request):
        questions = Question.objects.all()
        
        #add pagination

        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(questions,request)
        serializer = QuestionSerializer(result_page,many=True)

        return paginator.get_paginated_response(serializer.data)


class QuestionDetail(APIView):
    """
    Retrieve, update or delete a question by it's unique code along with choices.
    """

    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Allow all authenticated users to view
        return [IsAdminUser()]  # Only admin users can update or delete
    
    def get(self,request,code):
        
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code",status=status.HTTP_404_NOT_FOUND)
            # NotFound(detail="No such question with provided code")

        # choices = question.choice_set.all()

        # question_data = {
        #     "question_text" : question.question_text,
        #     "published_date" : question.published_date,
        #     "choices" : ChoiceSerializer(choices,many=True).data    #.data gives you the final Python list of dictionaries
        # }

        # return Response(question_data)

        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    def patch(self,request,code):
        
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code")
        
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,code):
        
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code")
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class QuestionCreate(APIView):
    """
    Create a new question with a unique code.
    """
    serializer_class = QuestionSerializer

    permission_classes =[IsAdminUser]
    def post (self, request):
        serializer = QuestionSerializer(data=request.data) #request.data is user filled data

        if Question.objects.filter(question_text=request.data.get("question_text")).exists():
            return Response("This question already exists",status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data,status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteAPIView(APIView):
    """
    Allow users to vote for choice
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer


    def post(self,request):
        #choice_id = request.data.get("choice_id")
        choice_text = request.data.get("choice_text")
        #if not choice_id:
        if not choice_text:
            return Response({"error":"Invalid choice_text"}, status=status.HTTP_400_BAD_REQUEST)
        
        #case insensitive match
        choice = get_object_or_404(Choice,choice_text__iexact=choice_text)

        # Check if the user has already voted for this choice
        user = request.user  # Get the authenticated user
        if Vote.objects.filter(user=user, choice=choice).exists():
            return Response({"error": "You have already voted for this choice."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new Vote instance
        vote = Vote.objects.create(user=user, choice=choice)


        choice.votes += 1
        choice.save()

        question_text = choice.question.question_text
        return Response({
        
            "question_text": question_text,
            "choice_text" : choice_text,
            "message":"Vote successfull",
            "updated_votes" : choice.votes,      

        }, status=status.HTTP_200_OK)
    
class ResultsView(APIView):
    """
    Return a list of all choices sorted by vote count
    """
    def get(self,request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions,many=True)
        return Response(serializer.data)

'''
class CodeBasedResultView(APIView):

    """
    Retrieving result of  list of all choices sorted by vote count using unique code
    """
    serializer_class = ChoiceSerializer
    def get(self,request,code):
        try:
            unique_code=Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code",status=status.HTTP_404_NOT_FOUND)
        
        choices=unique_code.choice_set.all().order_by("votes")
        serializer = ChoiceSerializer(choices,many=True)
        return Response(serializer.data)


class QuestionIdAPIView(APIView):
    def get(self, request):
        question_id = request.query_params.get('question')
        queryset = Choice.objects.all()
        if question_id:
            queryset = queryset.filter(question__id=question_id)
        serializer = ChoiceSerializer(queryset, many=True)
        return Response(serializer.data)

'''


class QuestionFilter(APIView):
    def get(self,request):
        question_text = request.query_params.get("question_text")
        queryset = Question.objects.all()
        if question_text:
            queryset=queryset.filter(question_text__icontains=question_text)
        serializer = QuestionSerializer(queryset,many=True)
        return Response(serializer.data)
    
class ChoiceFilter(APIView):
    def get(self,request):
        choice = request.query_params.get("choice_text")
        queryset = Choice.objects.all()
        if choice:
            queryset=queryset.filter(choice_text__icontains=choice)
        serializer = ChoiceSerializer(queryset,many=True)
        return Response (serializer.data)

class VoteFilter(APIView):
    def get(self,request):
        username = request.query_params.get("username")
        queryset = Vote.objects.all()

        if username:
            queryset=queryset.filter(user__username=username)        
        serializer = VoteSerializer(queryset,many=True)
        return Response(serializer.data)

