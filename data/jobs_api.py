import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

























# @blueprint.route('/api/jobs')
# def get_news():
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).all()
#     return jsonify(
#         {
#             'jobs':
#                 [item.to_dict(only=('title', 'salary', 'content', 'user.name'))
#                  for item in jobs]
#         }
#     )
#
#
# @blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
# def get_one_news(jobs_id):
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).get(jobs_id)
#     if not jobs:
#         return jsonify({'error': 'Not found'})
#     return jsonify(
#         {
#             'jobs': jobs.to_dict(only=(
#                 'title', 'salary', 'content', 'user_id'))
#         }
#     )
#
#
# @blueprint.route('/api/jobs', methods=['POST'])
# def create_news():
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['title', 'content', 'user_id']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     news = Jobs(
#         title=request.json['title'],
#         salary=request.json['salary'],
#         content=request.json['content'],
#         user_id=request.json['user_id'], )
#     db_sess.add(news)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
#
#
# @blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
# def delete_jobs(jobs_id):
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).get(jobs_id)
#     if not jobs:
#         return jsonify({'error': 'Not found'})
#     db_sess.delete(jobs)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
