from flask import Flask, render_template, request
from flask.views import MethodView
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def form1():
    return render_template('form.html')


class HelloView(MethodView):
    def get(self):
        return jsonify({'hello': 'world'})

    def post(self):
        return request.data


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)


app.add_url_rule('/hello', view_func=HelloView.as_view('hello_view'), methods=['get', 'post'])
