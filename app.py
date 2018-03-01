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

# GET /user method, with query string for team parameter
def get_users():
	all_users = db.get('users')
	team = request.args.get('team')
	matched = all_users if team is None else [i for i in all_users if i['team'] == team]
	return create_response(matched, message = 'I got you the users man')

# POST /user method, requires name, age, and team to work
# gives an error message back specifying which parameters are missing
def post_user():
	args = request.get_json()
	fields = ['name', 'age', 'team']
	user_info = [args.get(field) for field in fields]
	if None in user_info:
		message = 'Missing parameters ' + str([field for field in fields if args.get(field) == None])
		return create_response(args, 422, message) 
	else:
		return create_response(db.create('users', args), 201, 'Successfully added user!')

# entrypoint for /users HTTP request
@app.route('/users', methods = ['GET', 'POST'])
def users():
	if request.method == 'GET':
		return get_users()
	elif request.method == 'POST':
		return post_user()

# PUT /users/<id> method, takes in as many or as little parameters
# 	for the user as desired.
# For more robust implementation may want to discard parameters that
# aren't defined for a user, or else will add random entry to user object
def put_user(id):
	args = request.get_json()
	return create_response(db.updateById('users', id, args), message = 'Successfully update user!')

# DELETE /users/<id> method and returns number of user in message
def delete_user(id):
	return create_response(db.deleteById('users', id), message = 'Deleted user ' + str(id))

# entrypoint for /users/<id> HTTP request
# regardless of request type, returns error message if id not found
@app.route('/users/<id>', methods = ['GET', 'PUT', 'DELETE'])
def user(id):
	matched = db.getById('users', int(id))
	if matched is None:
		return create_response(matched, 404, 'You\'re a noob, gimme a real user')
	elif request.method == 'GET':
		return create_response(matched, message = 'Wow you\'re not a noob')
	elif request.method == 'PUT':
		return put_user(int(id))
	elif request.method == 'DELETE':
		return delete_user(int(id))

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
