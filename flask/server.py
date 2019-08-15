from flask import Flask, redirect, url_for, request, render_template
from article_graphMaker import articleToGraph
from flair.models import SequenceTagger
app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

tagger = SequenceTagger.load('chunk')

@app.route('/')
def hello_world():
	return render_template('index.html')
# def my_fun():
# 	return 'My Function!'

@app.route('/image/<name>')
def image(name):
	name = 'images/'+name.strip()+'.png'
	return render_template('image.html', imgLink=name)


@app.route('/push_article', methods= ['POST'])
def push_article():
	if request.method == 'POST':
		article = request.form['article_text']
		imgLink = articleToGraph(article, tagger)[14:]
		return redirect(url_for('image', name = imgLink))



if __name__ == '__main__':
	app.run(debug=True)