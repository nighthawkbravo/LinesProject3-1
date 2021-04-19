import os
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

PUBLIC_FILE_DIR = 'public/'
app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
	"lucas": generate_password_hash("wh40k"),
}

def make_tree(path):
	tree = dict(name=os.path.basename(path), children=[])
	try: lst = os.listdir(path)
	except OSError:
		pass #ignore errors
	else:
		for name in lst:
			fn = os.path.join(path, name)
			if os.path.isdir(fn):
				tree['children'].append(make_tree(fn))
			else:
				tree['children'].append(dict(name=name))
	return tree

@auth.verify_password
def verify_password(username, password):
	if username in users and \
			check_password_hash(users.get(username), password):
		return username

@app.route('/files', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['untrusted_file']
		f.save(os.path.join(PUBLIC_FILE_DIR, secure_filename(f.filename)))
		return redirect('/', code=302)

	return render_template('upload.html')


@app.route('/public/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory=PUBLIC_FILE_DIR, filename=filename)


@app.route('/')
def index():
	return render_template('dirtree.html', tree=make_tree(PUBLIC_FILE_DIR))

if __name__ == '__main__':
	app.run()
