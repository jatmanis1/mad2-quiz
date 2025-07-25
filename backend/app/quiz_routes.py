from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Quiz, Question, Score, User, db
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/<int:quiz_id>/start', methods=['GET'])
@jwt_required()
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    quiz_data = {
        'quiz': quiz.to_dict(),
        'questions': [question.to_dict(include_answer=False) for question in questions],
        'start_time': datetime.utcnow().isoformat()
    }
    
    return jsonify(quiz_data), 200

@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    user_answers = data.get('answers', {})
    time_taken = data.get('time_taken', 0)
    
    # Calculate score
    total_scored = 0
    for question in questions:
        user_answer = user_answers.get(str(question.id))
        if user_answer and int(user_answer) == question.correct_option:
            total_scored += question.marks
    
    # Save score
    score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        total_scored=total_scored,
        total_marks=quiz.total_marks,
        time_taken=time_taken,
        answers=user_answers
    )
    
    db.session.add(score)
    db.session.commit()
    
    return jsonify({
        'score': score.to_dict(),
        'correct_answers': {str(q.id): q.correct_option for q in questions}
    }), 200

@quiz_bp.route('/results/<int:score_id>', methods=['GET'])
# @jwt_required()
def get_quiz_results( score_id):
    # user_id = get_jwt_identity()
    score = Score.query.filter_by(id=score_id).first_or_404()
    s1 = score.to_dict()
    quiz_id = score.quiz_id
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    results = {
        'score': score.to_dict(),
        'quiz': quiz.to_dict(),
        'detailed_results': []
    }
    
    # Add detailed question-wise results
    for question in questions:
        user_answer = score.answers.get(str(question.id)) if score.answers else None
        is_correct = user_answer and int(user_answer) == question.correct_option
        
        results['detailed_results'].append({
            'question': question.to_dict(include_answer=True),
            'user_answer': user_answer,
            'is_correct': is_correct
        })
    
    return jsonify(results), 200
