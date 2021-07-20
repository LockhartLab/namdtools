"""

"""

# TODO 1. store df in session to make loading easier
# https://flask-session.readthedocs.io/en/latest/
# TODO 2. interactive plot
# TODO 3. allow for data download
# TODO 4. Display other details

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from glob import iglob
from hashlib import md5
from namdtools.io import read_log
import os
import pandas as pd
import uplot as u
from werkzeug.utils import secure_filename

# Some variables for uploading files
ALLOWED_EXTENSIONS = {'txt', 'out', 'log'}

# Create initial connection to Flask
app = Flask(__name__)
# app.config['SESSION_TYPE'] = 'filesystem'

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'3\x8eYn\x94\xe5\xdb\xba\xa5\xd6\x910\xe6fv\xab'


# Check that the file we upload is allowed
def allowed_file(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Index
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save the file securely
        file = request.files.get('namdlog', None)
        if file is None or not allowed_file(file.filename):
            return redirect(request.url)
        fname = os.path.join('static', secure_filename(file.filename))
        file.save(fname)

        # Get arguments
        quantity = request.form.get('quantity', 'potential')
        skip = request.form.get('skip', 0, type=int)
        print(skip)

        # Read NAMD log if necessary
        df = read_log(fname)
        # if fname not in session.keys():
        #     df = read_log(fname)
        #     session[fname] = df.to_json()
        # else:
        #     df = pd.DataFrame(session[fname])

        # Get the quantity
        y_title = quantity
        if quantity == 'temperature':
            quantity = 'temp'

        # Produce x and y
        x = df.index.values[skip:].astype(float)
        y = df[quantity].values[skip:].astype(float)
        print(x)
        print(y)

        # Create a temporary file for the plot
        # noinspection PyTypeChecker
        fname = md5(f'{fname}_{quantity}'.encode()).hexdigest() + '.svg'
        fpath = os.path.join('static', fname)

        # Save plot to temporary location
        fig = u.figure(style={
            'x_title': r'# $steps$',
            'y_title': r'$%s$' % y_title,
            # 'x_min': skip
        })
        fig += u.line(x, y)
        fig.to_mpl(save_as=fpath)

        # Return
        return jsonify({'plot': url_for('static', filename=fname)[1:]})

    # noinspection PyUnresolvedReferences
    return render_template('index.html')


# Run the app
if __name__ == '__main__':
    # Clean out static
    for fname in iglob('static/*.*'):
        print(fname)
        os.remove(fname)

    # Run
    app.run()
