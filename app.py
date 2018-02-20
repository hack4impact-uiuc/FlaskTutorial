from flask import Flask, jsonify, request
import mockdb.mockdb_interface as db

app = Flask(__name__)

def create_response(data={}, status=200, message=''):
    """
    Wraps response in a consistent format throughout the API
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response

    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    """
    response = {
        'success': 200 <= status < 300,
        'code': status,
        'message': message,
        'result': data
    }
    return jsonify(response), status

"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

@app.route('/')
def hello_world():
    return create_response('hello world!')

@app.route('/mirror/<name>')
def mirror(name):
    data = {
        'name': name
    }
    return create_response(data)

# TODO: Implement the rest of the API here!

@app.route('/users')
def users():
    if 'team' in request.args:
        data = db.getByTeam('users', request.args.get('team'))
        if data is None:
            return create_response({})
        return create_response(data)
    else:
        return create_response(db.get('users'))

@app.route('/users', methods=['POST'])
def createUser():
    if not 'name' in request.json or not 'age' in request.json or not 'team' in request.json:
        return create_response({}, 422, "Missing parameters in body. Must contain name, age, and team.")
    else:
        data = db.create('users', request.json)
        return create_response(data, 201)

@app.route('/users/<user_id>')
def users_id(user_id):
	data = db.getById('users', int(user_id))

	if data is None:
		return create_response({}, 404, "There is no user with the specified ID")
	return create_response(data)

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
