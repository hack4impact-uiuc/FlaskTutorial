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

ROOT_URL = '/'
MIRROR_URL = '/mirror/<name>'
USERS_URL = '/users'
USERS_ID_URL = '/users/<int:user_id>'

@app.route(ROOT_URL)
def hello_world():
    return create_response('hello world!')

@app.route(MIRROR_URL)
def mirror(name):
    return create_response({'name' : name})

# TODO: Implement the rest of the API here!

# GET /user method, with query string for team parameter
@app.route(USERS_URL, methods = ['GET'])
def get_users():
    all_users = db.get('users')
    team = request.args.get('team')
    matched = all_users if team is None else [i for i in all_users if i['team'] == team]
    return create_response({'users' : matched}, message = 'I got you the users man')

# POST /user method, requires name, age, and team to work
# gives an error message back specifying which parameters are missing
@app.route(USERS_URL, methods = ['POST'])
def post_user():
    args = request.get_json()
    fields = ['name', 'age', 'team']
    user_info = [args.get(field) for field in fields]
    if None in user_info:
        message = 'Missing parameters ' + str([field for field in fields if args.get(field) == None])
        return create_response(args, 422, message)
    else:
        user = db.create('users', args)
        return create_response({'user' : user }, 201, 'Successfully added user!')

# GET /users/<user_id> method, returns error message if id not found
@app.route(USERS_ID_URL, methods = ['GET'])
def user(user_id):
    matched = db.getById('users', user_id)
    if matched is None:
        return create_response(matched, 404, 'You\'re a noob, gimme a real user')
    return create_response({'user' : matched}, message = 'Wow you\'re not a noob')

# PUT /users/<user_id> method, takes in as many or as little parameters
# 	for the user as desired.
# For more robust implementation may want to discard parameters that
# aren't defined for a user, or else will add random entry to user object
@app.route(USERS_ID_URL, methods = ['PUT'])
def put_user_by_id(user_id):
    matched = db.getById('users', user_id)
    if matched is None:
        return create_response(matched, 404, 'You\'re a noob, gimme a real user')
    args = request.get_json()
    updated_user = db.updateById('users', user_id, args)
    return create_response({'user' : updated_user}, message = 'Successfully updated user!')

# DELETE /users/<user_id> method and returns number of user in message
@app.route(USERS_ID_URL, methods = ['DELETE'])
def delete_user_by_id(user_id):
    matched = db.getById('users', user_id)
    if matched is None:
        return create_response(matched, 404, 'You\'re a noob, gimme a real user')
    deleted_user = db.deleteById('users', user_id)
    return create_response({'user' : deleted_user}, message = 'Deleted user ' + str(user_id))

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
