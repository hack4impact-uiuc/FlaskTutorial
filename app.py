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

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method=='GET':
        all_users = db.get('users')
        team = request.args.get('team') #asking for teams from query params
        team_users = []
        for user in all_users:
            if user['team'] == team:
                team_users.append(user)
        return create_response(team_users)
    elif request.method=='POST':
        json_input = request.get_json()
        name = json_input.get('name')
        age = json_input.get('age')
        team = json_input.get('team')
        try:
            new_user_data = {
                'name': name,
                'age': age,
                'team': team
            }
            create_user = db.create('users', new_user_data)
        except KeyError:
            fail_message = 'You are missing on or more of the body params required to create a new user. Please specify name, age, and team.'
            return create_response({}, 422, fail_message)
        return create_response(create_user, 201, 'You\'ve successfully crested a new user!')

# args = request.get_json()
#     fields = ['name', 'age', 'team']
#     user_info = [args.get(field) for field in fields]
#     if None in user_info:
#         message = 'Missing parameters ' + str([field for field in fields if args.get(field) == None])
#         return create_response(args, 422, message) 
#     else:
#         return create_response(db.create('users', args), 201, 'Successfully added user!')
 
##STEPS
#1. get json from request body
#2. check if name, age, and team exist in json
#3. if not, create_response with 422 status code with message
#4. if yes, create_response with given data and 201 status code


@app.route('/users/<id>', methods=['GET'])
def user_id(id):
    all_users = db.get('users')
    intId = int(id)
    if ((intId > 0) or (intId < len(all_users))):
        user = all_users[intId - 1]
        return create_response(user)
    else:
        return create_reponse({}, 404, "no such user")

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)