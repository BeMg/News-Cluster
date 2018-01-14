from flask import render_template, Flask, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
import pickle
import datetime
from utils import get_content, preprocess, get_by_cluster

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        url = request.form.get("newsurl")
        n_cluster = request.form.get("n_cluster")
        target = get_content(url)
        if target == None:
            items = []
            items.append(dict(title="這是一個無效的連結", url="https://this_is_not_workable_url"))
            return render_template('main.html', items=items)
        else:
            url, title, text = target
            cluster = preprocess(text, n_cluster)
            items = []
            sdata = get_by_cluster(n_cluster, cluster, 100)
            for url_, title_, cluster_ in sdata:
                items.append(dict(title=title_, url=url_))
            return render_template('main.html', items=items, target=[dict(url=url, title=title)])
    else:
        return render_template('main.html', items=[], target=[])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)