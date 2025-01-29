import os

from flask import Flask, send_from_directory, Response
from flask_cors import CORS
from communityenergylabsserver.cache import cache, preload_cache, preload_test_cache
from communityenergylabsserver.routes import events
from communityenergylabsserver.models.EventSchema import load_events_data

class JSONResponse(Response):
        default_mimetype = 'application/json'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='../../client/events-app/dist')
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # Serve the frontend
    @app.route('/')
    def index():
        # Print current working directory
        print(app.root_path)
        return send_from_directory(os.path.join(app.root_path, '../../dist'), 'index.html')
    
    # Server static files
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(os.path.join(app.root_path, '../../dist'), path)
    
    # Register event routes
    app.register_blueprint(events.event_routes)

    # Default response type to json
    app.response_class = JSONResponse
    CORS(app, resources={r'/*': {'origins': '*'}})    
    cache.init_app(app)

    # Preload cache with data
    with app.app_context():
        # If not testing load cache data
        if test_config is None:
            preload_cache()


    return app
