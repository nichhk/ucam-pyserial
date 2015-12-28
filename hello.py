from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
	print 'got a request'
	return 'HELLLOOOOO tyler'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)

