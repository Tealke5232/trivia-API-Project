import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

TRIVIA_PER_PAGE = 10

def get_paginated_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * TRIVIA_PER_PAGE
    end = start + TRIVIA_PER_PAGE

    questions = [question.format() for question in questions]
    paginated_questions = questions[start:end]

    return paginated_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})  # setting Cors to allow all orgins

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_all_categories():
        try:
            categories = Category.query.all()
            data = {}
            for category in categories:
                data[category.id] = category.type
            return jsonify({
                'success': True,
                'categories': data
            }), 200
        except:
            abort(500)

    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()

        paginated_questions = get_paginated_questions(request, questions)

        if (len(paginated_questions) == 0):  # lets add a hint to add trivia if no trivia is present
            try:
                question = Question(question='There Seems to be no Trivia!', answer='Go and add some !', difficulty=1, category='delete me')
                question.insert()
            except:
                abort(404)

        categories_list = {}
        for category in categories:
            categories_list[category.id] = category.type

        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'categories': categories_list,
            'questions': paginated_questions
        }), 200

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.get(id)
            question.delete()
            return jsonify({
                'success': True,
                'message': "Trvia Question has been deleted"
            }), 200
        except:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def question_post():
        data = request.get_json()

        question = data.get('question', '')
        answer = data.get('answer', '')
        difficulty = data.get('difficulty', '')
        category = data.get('category', '')
        search_term = data.get('searchTerm', None)

        try:
            if search_term:
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
                current_questions = get_paginated_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions),
                    'current_category': None
                }), 200
            else:
                question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = get_paginated_questions(request, questions)
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all()),
                    'message' : 'successfuly added the trivia quesiton'
                }), 201
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            category_id = str(category_id)
            selection = Question.query.filter(Question.category == category_id).all()
            current_questions = get_paginated_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category_id
            }), 200

        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz_question():
        data = request.get_json()
        if not data:
            abort(400)
        previous_question = data['previous_questions']
        category_id = str(int(data['quiz_category']['id']))

        if category_id == 0:
            if previous_question is not None:
                questions = Question.query.filter(
                    Question.id.notin_(previous_question)).all()
            else:
                questions = Question.query.all()
        else:
            if previous_question is not None:
                questions = Question.query.filter(
                    Question.id.notin_(previous_question),
                    Question.category == category_id).all()
            else:
                questions = Question.query.filter(Question.category == category_id).all()

        next_question = random.choice(questions).format()
        if not next_question:
            abort(404)
        if next_question is None:
            next_question = False

        return jsonify({
            'success': True,
            'question': next_question
        }), 200
###############################################################################
#####                    Error handlers                                   #####
###############################################################################
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'The request could not be understood by the server due to incorrect syntax. The client SHOULD NOT repeat the request without modifications.'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'The server can not find the requested resource.'
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'The request HTTP method is known by the server but has been disabled and cannot be used for that resource.'
        }), 405

    @app.errorhandler(410)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 410,
            'message': 'The requested resource is no longer available at the server.'
        }), 410

    @app.errorhandler(422)
    def unprocesable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'The server understands the content type and syntax of the request entity, but still server is unable to process the request for some reason.'
        }), 422
    return app

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'The server encountered an unexpected condition which prevented it from fulfilling the request.'
        }), 500

    @app.errorhandler(505)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 505,
            'message': 'The HTTP version used in the request is not supported by the server.'
        }), 505
