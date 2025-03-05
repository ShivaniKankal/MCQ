from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Question, TestSession, UserResponse, Choice
from .serializers import QuestionSerializer, TestSessionSerializer
import uuid

@api_view(['POST'])
def start_test(request):
    """Start a test session and return 10 random MCQs."""
    session_id = str(uuid.uuid4())  # Unique session ID
    test_session = TestSession.objects.create(session_id=session_id)

    questions = Question.get_random_questions(10)
    serialized_questions = QuestionSerializer(questions, many=True).data

    return Response({
        "session_id": session_id,
        "questions": serialized_questions
    })

@api_view(['POST'])
def submit_answer(request):
    """Submit an answer for a question."""
    session_id = request.data.get('session_id')
    question_id = request.data.get('question_id')
    selected_choice_id = request.data.get('selected_choice_id')

    test_session = TestSession.objects.filter(session_id=session_id).first()
    if not test_session:
        return Response({"error": "Invalid session"}, status=400)

    question = Question.objects.get(id=question_id)
    selected_choice = Choice.objects.get(id=selected_choice_id)

    UserResponse.objects.create(
        test_session=test_session,
        question=question,
        selected_choice=selected_choice
    )

    return Response({"message": "Answer submitted successfully!"})

@api_view(['GET'])
def get_results(request, session_id):
    """Retrieve test results for a given session."""
    test_session = TestSession.objects.filter(session_id=session_id).first()
    if not test_session:
        return Response({"error": "Invalid session"}, status=400)

    responses = UserResponse.objects.filter(test_session=test_session)
    total_questions = responses.count()
    correct_answers = sum(1 for resp in responses if resp.is_correct())

    return Response({
        "session_id": session_id,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score_percentage": (correct_answers / total_questions) * 100 if total_questions else 0
    })
