from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template("index.html")


def fork_users(url):
    fork_data = requests.get(url).json()
    users_list = []
    count = 0
    for data in fork_data:
        if 'owner' in data.keys():
            users_list.append(data['owner']['login'])
            count += 1
            if count == 3:
                break
    return users_list


@app.route('/search', methods=['POST', 'GET'])
def search():
    username = request.form['username']
    url = f"https://api.github.com/users/{username}/gists"
    user_data = requests.get(url).json()
    gists_list = []
    for data in user_data:
        if 'url' in data.keys():
            tags = []
            gist = dict()
            gist['url'] = data['url']
            for key in data["files"]:
                tags.append(data["files"][key]["language"])
            gist['files'] = tags
            fork_url = data["forks_url"]
            gist['fork_users'] = fork_users(fork_url)
            gists_list.append(gist)
    return render_template('index.html', data=gists_list)


@app.route('/file', methods=['POST'])
def get_file_content():
    url = request.form['url']
    user_data = requests.get(url).json()
    for key in user_data['files']:
        content = user_data['files'][key]['content']
    return jsonify(content)


if __name__ == '__main__':
    app.run()
