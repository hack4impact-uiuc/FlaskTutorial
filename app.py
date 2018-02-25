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

# USERS_ROUTE = '/users'
# USERS_ID_ROUTE = '/users/<id>'

@app.route('/users')
def users():
    data = {
        'users': db.get('users')
    }
    return create_response(data)

@app.route('/users/<id>')
def user_by_id(id):
    data = {
        'user': db.getById('users', int(id))
    }
    if db.getById('users', int(id)) is None:
        return create_response('404 Error. ID was not found in the database.')
    else:
        return create_response(data)

#Added in the db.getByTeam command; see "mockdb_interface.py"
@app.route('/users/teams')
def team():
    team = request.args['team']
    data = {
        'users': db.getByTeam('users', team)
    }
    return create_response(data)

@app.route('/users', methods=['POST'])
def add_user():
    payload = request.get_json()
    name = request.get_json().get('name')
    age = request.get_json().get('age')
    team = request.get_json().get('team')

    if ((name is None) or (age is None) or (team is None)):
        return create_response('422 Error: Check if you posted name, age, and team parameters.')
    elif (type(age) is not int):
        return create_response('Age should be an integer')
    else:
        return create_response(db.create('users', payload))

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    update_values = request.get_json()
    name = request.get_json().get('name')
    age = request.get_json().get('age')
    team = request.get_json().get('team')

    if db.getById('users', int(id)) is None:
        return create_response('404 Error: The provided ID could not be found in the database')
    elif ((name is None) or (age is None) or (team is None)):
        return create_response('422 Error: Check if you posted name, age, and team parameters.')
    else:
        db.updateById('users', int(id), update_values)
        return create_response("Successfully updated.")

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    if db.getById('users', int(id)) is None:
        return create_response('404 Error: The provided ID could not be found in the database')
    else:
        db.deleteById('users', int(id))
        return create_response('Successfully deleted.')

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
