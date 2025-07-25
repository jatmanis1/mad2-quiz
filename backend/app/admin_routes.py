from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Subject, Chapter, Quiz, Question, User, Score, db
from datetime import datetime
import redis

admin_bp = Blueprint('admin', __name__)
redis_client = redis.Redis(decode_responses=True)

# def admin_required():
#     def decorator(f):
#         @jwt_required()
#         def decorated_function(*args, **kwargs):
#             claims = get_jwt()
#             if claims.get('role') != 'admin':
#                 return jsonify({'message': 'Admin access required'}), 403
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

# Subject Management
@admin_bp.route('/subjects', methods=['GET'])
# @admin_required()
def get_subjects():
    # Check cache first
    cached_subjects = redis_client.get('subjects_list')
    if cached_subjects:
        import json
        return jsonify(json.loads(cached_subjects)), 200
    
    subjects = Subject.query.filter_by(is_active=True).all()
    subjects_data = [subject.to_dict() for subject in subjects]
    
    # Cache for 5 minutes
    import json
    redis_client.setex('subjects_list', 300, json.dumps(subjects_data))
    
    return jsonify(subjects_data), 200

@admin_bp.route('/subjects', methods=['POST'])
# @admin_required()
def create_subject():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'message': 'Subject name is required'}), 400
    
    subject = Subject(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(subject)
    db.session.commit()
    
    # Clear cache
    redis_client.delete('subjects_list')
    
    return jsonify(subject.to_dict()), 201

@admin_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
# @admin_required()
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)
    
    db.session.commit()
    redis_client.delete('subjects_list')
    
    return jsonify(subject.to_dict()), 200

@admin_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
# @admin_required()
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    subject.is_active = False
    
    db.session.commit()
    redis_client.delete('subjects_list')
    
    return jsonify({'message': 'Subject deleted successfully'}), 200

# Chapter Management
@admin_bp.route('/subjects/<int:subject_id>/chapters', methods=['GET'])
# @admin_required()
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id, is_active=True).all()
    return jsonify([chapter.to_dict() for chapter in chapters]), 200

@admin_bp.route('/subjects/<int:subject_id>/chapters', methods=['POST'])
# @admin_required()
def create_chapter(subject_id):
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'message': 'Chapter name is required'}), 400
    
    chapter = Chapter(
        name=data['name'],
        description=data.get('description', ''),
        subject_id=subject_id
    )
    
    db.session.add(chapter)
    db.session.commit()
    
    return jsonify(chapter.to_dict()), 201

# Quiz Management
@admin_bp.route('/chapters/<int:chapter_id>/quizzes', methods=['POST'])
# @admin_required()
def create_quiz(chapter_id):
    data = request.get_json()
    
    required_fields = ['title', 'date_of_quiz', 'time_duration']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400
    
    quiz = Quiz(
        title=data['title'],
        description=data.get('description', ''),
        chapter_id=chapter_id,
        date_of_quiz=datetime.fromisoformat(data['date_of_quiz'].replace('Z', '+00:00')),
        time_duration=data['time_duration']
    )
    
    db.session.add(quiz)
    db.session.commit()
    
    return jsonify(quiz.to_dict()), 201

# Question Management
@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['POST'])
# @admin_required()
def add_question(quiz_id):
    data = request.get_json()
    
    required_fields = ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400
    
    question = Question(
        quiz_id=quiz_id,
        question_statement=data['question_statement'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option'],
        marks=data.get('marks', 1)
    )
    
    db.session.add(question)
    
    # Update quiz total marks
    quiz = Quiz.query.get(quiz_id)
    quiz.total_marks += question.marks
    
    db.session.commit()
    
    return jsonify(question.to_dict(include_answer=True)), 201

# Dashboard Analytics
@admin_bp.route('/dashboard/stats', methods=['GET'])
# @admin_required()
def get_dashboard_stats():
    stats = {
        'total_users': User.query.filter_by(role='user').count(),
        'total_subjects': Subject.query.filter_by(is_active=True).count(),
        'total_quizzes': Quiz.query.filter_by(is_active=True).count(),
        'total_attempts': Score.query.count(),
        'recent_scores': []
    }
    
    # Get recent quiz attempts
    recent_scores = Score.query.order_by(Score.timestamp_of_attempt.desc()).limit(10).all()
    stats['recent_scores'] = [score.to_dict() for score in recent_scores]
    
    return jsonify(stats), 200


# Add these to your admin_routes.py

@admin_bp.route('/chapters/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    
    db.session.commit()
    return jsonify(chapter.to_dict()), 200

@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter.is_active = False
    
    db.session.commit()
    return jsonify({'message': 'Chapter deleted successfully'}), 200

@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_quiz_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([question.to_dict(include_answer=True) for question in questions]), 200

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Update quiz total marks
    quiz = Quiz.query.get(question.quiz_id)
    quiz.total_marks -= question.marks
    
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({'message': 'Question deleted successfully'}), 200

@admin_bp.route('/chapters', methods=['GET'])
def get_all_chapters():
    chapters = Chapter.query.filter_by(is_active=True).all()
    return jsonify([chapter.to_dict() for chapter in chapters]), 200


# Add to admin_routes.py

@admin_bp.route('/quizzes', methods=['GET'])
def get_all_quizzes():
    quizzes = Quiz.query.filter_by(is_active=True).all()
    return jsonify([quiz.to_dict() for quiz in quizzes]), 200

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    quiz.title = data.get('title', quiz.title)
    quiz.description = data.get('description', quiz.description)
    quiz.date_of_quiz = datetime.fromisoformat(data['date_of_quiz'].replace('Z', '+00:00')) if data.get('date_of_quiz') else quiz.date_of_quiz
    quiz.time_duration = data.get('time_duration', quiz.time_duration)
    
    db.session.commit()
    return jsonify(quiz.to_dict()), 200

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.is_active = False
    
    db.session.commit()
    return jsonify({'message': 'Quiz deleted successfully'}), 200
