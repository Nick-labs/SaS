from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.jobs import Jobs


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('title', 'content', 'contacts', 'user_id', 'salary'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('title', 'content', 'salary', 'contacts', 'user.name')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            salary=args['salary'],
            contacts=args['contacts']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('salary', required=True, type=int)
parser.add_argument('contacts', required=True)
parser.add_argument('user_id', required=True, type=int)
