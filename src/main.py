""" Main module """

from routes import APP

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=3000, debug=True)
