import rmsystem.main as main
from rmsystem.main import app

DB_NAME = "rmsystem_db"
main.set_mongodb_name(db_name = DB_NAME)
app.run(debug=True, threaded=True)
