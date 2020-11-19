import sentry_sdk
import env
import os

from bottle import Bottle, request
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    # в модуле env.py присвойте SENTRY_DSN свои значения, для инициализации в sentry-sdk
    dsn=env.SENTRY_DSN,
    integrations=[BottleIntegration()]
)

app = Bottle()

@app.route('/')
def main_page():
    return '''
        <h3>Click on links:</h3>
        <a href="https://whispering-chamber-02388.herokuapp.com/success">success</a><br>
        <a href="https://whispering-chamber-02388.herokuapp.com/fail">fail</a>
    '''

@app.route('/fail')  
def fail():  
    raise RuntimeError("There is an error! You tryed to open 'fail' page")

@app.route('/success')  
def success():  
    return '''
        <p>status 200 OK</p><br>
        <a href="https://whispering-chamber-02388.herokuapp.com/">Back to main page</a>
    '''


if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8080, debug=True)
