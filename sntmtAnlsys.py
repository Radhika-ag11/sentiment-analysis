from flask import Flask, render_template, request


from textblob import TextBlob

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('Article.html')

@app.route('/', methods=['POST'] )
def getdata():
    text=request.form['text']
    
    blob=TextBlob(text)
    
    return render_template('art.html', p=blob.sentiment)
    


if __name__ == '__main__':
    app.run()