from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Quiz, Subject, Chapter, Score, Question, db
from datetime import datetime

user_bp = Blueprint('user', __name__)




@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_user_dashboard():
    user_id = get_jwt_identity()
    print(user_id,"sdfjklskjf")
    # Get user's quiz attempts
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
    
    # Calculate statistics
    total_attempts = len(scores)
    avg_score = sum(score.total_scored / score.total_marks * 100 for score in scores) / total_attempts if total_attempts > 0 else 0
    
    dashboard_data = {
        'total_attempts': total_attempts,
        'average_score': round(avg_score, 2),
        'recent_attempts': [score.to_dict() for score in scores[:10]],
        'available_quizzes': Quiz.query.filter_by(is_active=True).count()
    }
    
    return jsonify(dashboard_data), 200



@user_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_available_subjects():
    subjects = Subject.query.filter_by(is_active=True).all()
    return jsonify([subject.to_dict() for subject in subjects]), 200

@user_bp.route('/chapters', methods=['GET'])
@jwt_required()
def get_subject_chapters():
    chapters = Chapter.query.filter_by( is_active=True).all()
    return jsonify([chapter.to_dict() for chapter in chapters]), 200

@user_bp.route('/quizzes', methods=['GET'])
@jwt_required()
def get_chapter_quizzes():
    quizzes = Quiz.query.filter_by( is_active=True).all()
    return jsonify([quiz.to_dict() for quiz in quizzes]), 200


@user_bp.route('/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
    return jsonify([score.to_dict() for score in scores]), 200
