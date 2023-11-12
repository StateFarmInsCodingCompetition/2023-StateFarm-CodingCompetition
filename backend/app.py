import inspect

from flask import request, Flask, Response, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from simple_data_tool import SimpleDataTool

app = Flask(__name__)
app.config.from_pyfile('secrets.properties', silent=False)

CORS(app)

print('Initializing...')
client = MongoClient(app.config['DB_URI'])  # Connect to db
data = SimpleDataTool(client)  # Init tool
print('Done!')

# Cache all get_ functions
data_functions = {func: getattr(data, func) for func in dir(data) if
                  callable(getattr(data, func)) and func.startswith('get_')}

# Used to convert text responses into a json body
def json_wrap(text):
    return {'response': text}


@app.route('/<path:path>', methods=['GET', 'POST'])
def endpoint(path):  # Generified endpoint for all data access
    if path not in data_functions:
        return Response('Invalid API Endpoint', 400)

    func = data_functions[path]  # Find associated data function
    args = request.args  # Get request arguments
    missing = {}
    print('Got', args)
    cast_args = {}
    for n, p in inspect.signature(func).parameters.items():  # Match signature
        if n not in args:
            missing[str(n)] = str(p.annotation)
            print('missing')
        else:
            cast_args[n] = p.annotation(args[n])  # Cast to proper data type

    print('Converted to', args)

    if len(missing) != 0:  # User has not sent all required request arguments
        response = jsonify(missing)
        response.status = 422
        return response

    return jsonify(json_wrap(func(**cast_args)))
