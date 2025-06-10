from api.api import app

# Entry point for Google Cloud Function
def flask_entry_point(request):

    with app.request_context(request.environ):
        return app.full_dispatch_request()

# # Local server for testing
# if __name__ == '__main__':
#     app.run(debug=True, port=8082, use_reloader=False)
