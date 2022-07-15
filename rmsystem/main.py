from rmsystem.packages import * 

from rmsystem.admin import admin

app = Flask(__name__, static_url_path = "/", static_folder = "")

app.register_blueprint(admin, url_prefix="/admin")  # admin related APIS goes here


app.config['SECRET_KEY'] = 'somesecretkey' 
def set_mongodb_name(db_name = 'default_db'):
    app.config['MONGO_DBNAME'] = db_name                                           #Configuring the MongoDB Database Name 
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/'+app.config['MONGO_DBNAME']                   #and URL of MongoDB
    ##mongo = PyMongo(app)
    mongo.init_app(app)


# ERROR HANDLER 
@app.errorhandler(404)                                                         
def not_found(error):
    """ error handler """
    #LOG.error(error)
    return make_response(jsonify({'result':'false','output':'Ohh Snap! Double Check Your URL'}), 404)

# HOME PAGE
@app.route('/', methods=['GET'])
def api_root():
    return 'Hola!! -- HOME PAGE'



if __name__ == '__main__':
    app.run( debug=True, threaded=True)