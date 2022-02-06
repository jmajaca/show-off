from flask import Blueprint

doc_endpoint = Blueprint('doc_endpoint', __name__, static_folder='../doc')


@doc_endpoint.route('/doc')
def doc():
    return doc_endpoint.send_static_file('index.html')
