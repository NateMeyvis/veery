from bottle import route, run

@route("/")
def hello():
    return "Bottle says hello."

run(host="0.0.0.0", port=8000)
