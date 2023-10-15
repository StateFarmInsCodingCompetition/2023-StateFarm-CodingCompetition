from http.server import SimpleHTTPRequestHandler, HTTPServer
from simple_data_tool import SimpleDataTool
import inspect

host = 'localhost'
port = 8080

data = SimpleDataTool()

# Cache all get_ functions
data_functions = {func: getattr(data, func) for func in dir(data) if
                  callable(getattr(data, func)) and func.startswith('get_')}


class PythonServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        path = self.path[1:].split('/')  # Split path for easy directing
        last = len(path) - 1
        pSplit = None
        if '?' in path[last]:  # Contains path parameters
            pSplit = path[last].split('?')
            path[last] = pSplit[0]

        paramsSet = pSplit[1].split('&') if pSplit is not None else []  # Extract path parameters
        params = dict((x[0], x[1]) for x in [e.split('=') for e in paramsSet])

        response: tuple[str, int] = ('Unknown query', 400)  # Default response

        if path[0] == 'func':  # This is a function request
            if len(path) == 1:  # No function specified, so tell user all valid functions
                res = {}
                for n, f in data_functions.items():
                    res[n] = dict((n, p.annotation) for n, p in inspect.signature(f).parameters.items())

                response = (str(res), 200)
            else:  # Serve function responses
                func_name = path[1]
                if func_name not in data_functions:  # Unknown function
                    response = ('Operation does not exist', 400)

                func = data_functions.get(func_name)
                sig = inspect.signature(func)
                required_params = dict((n, p.annotation) for n, p in sig.parameters.items())  # Map param name to type
                signature_match = True

                for p in required_params:  # Verify that all needed arguments are present
                    if p not in params:
                        response = (f'One or more arguments are missing: {required_params}', 400)
                        signature_match = False
                        break
                    params[p] = required_params[p](params[p])  # Cast to proper types

                if signature_match:
                    response = (func(**params), 200)  # Execute function

        # Send and serve
        self.send_response(response[1], "OK")
        self.send_header("Content-length", str(len(str(response[0]))))
        self.end_headers()
        self.wfile.write(bytes(str(response[0]), "utf-8"))


if __name__ == '__main__':
    server = HTTPServer((host, port), PythonServer)
    print(f"Data server started at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server and driver stopped successfully")
    exit()
