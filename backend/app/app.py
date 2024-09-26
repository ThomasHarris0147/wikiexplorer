from datetime import timedelta

from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from wiki_crawler import WikiCrawler

crawler = WikiCrawler()

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'your_pythongeeks_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'


# POST request example
@app.route('/crawl_link', methods=['POST'])
@cross_origin()
def crawl_link():
    """
    deprecated: was used as a proof of concept, takes a long time to load at once with big numbers
    """
    data = request.json
    link = data.get('link')
    limit = data.get('limit')
    first_n_sublinks = data.get('first_n_sublinks')

    if link:
        sub_links, links = crawler.walk_sub_links(link, limit, first_n_sublinks)
        d3_nodes, d3_links = crawler.convert_links_and_sub_links_to_d3_nodes_and_links(sub_links, links)
        return jsonify({"nodes": d3_nodes, "links": d3_links})
    else:
        return jsonify({"error": "Incorrect or no link provided"}), 400


# @app.route('/reset', methods=['GET'])
# @cross_origin()
# def reset():
#     session.__setitem__("collected_links",[])
#     return jsonify({"success": "true"})


@app.route('/post_link', methods=['POST', 'GET'])
@cross_origin()
def post_link():
    data = request.json
    link = data.get('link')
    first_n_sublinks = None
    last_n_sublinks = None
    if "first_n_sublinks" in data:
        first_n_sublinks = data.get('first_n_sublinks')
    if "last_n_sublinks" in data:
        last_n_sublinks = data.get('last_n_sublinks')
    crawled_links = set(data.get('crawled_links'))
    if first_n_sublinks is None and last_n_sublinks is None:
        return jsonify({"error": "limit for number of links not good"}), 400

    if link:
        sub_links = None
        if first_n_sublinks:
            sub_links = crawler.get_first_sub_links(link, crawled_links, first_n_sublinks)
        if last_n_sublinks:
            sub_links = crawler.get_last_sub_links(link, crawled_links, last_n_sublinks)
        d3_nodes = crawler.convert_links_to_d3_nodes(sub_links)
        return jsonify({"nodes": d3_nodes})
    else:
        return jsonify({"error": "Incorrect or no link provided"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=3000)
