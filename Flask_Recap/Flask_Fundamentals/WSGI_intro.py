# WSGI -> Web Server Gateway Interface is a specification that tells our Python code on a client or a server how to communicate effectively over HTTP/HTTPS

# Werkzeug -> Is the WSGI library

from werkzeug.wrappers import Request, Response
@Request.application
def application(request):
    print(f"This web server is running at {request.remote_addr}")
    return Response("A WSGI generated this response!")

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple(
        hostname="localhost",
        port=5555,
        application=application
    )
