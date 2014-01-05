import json
from flask import Flask, render_template, g, jsonify, request
from kazoo.client import KazooClient
from werkzeug.exceptions import BadRequest
import urllib

app = Flask(__name__)
# app.debug = True

# Host string of the ZooKeeper servers to connect to
# ZK_HOSTS = 'elsaprtmq01.server.hulu.com:2181'

# Node metadata to view
ZNODESTAT_ATTR = [
    'aversion',
    'ctime',
    'czxid',
    'dataLength',
    'ephemeralOwner',
    'mtime',
    'mzxid',
    'numChildren',
    'version']

@app.template_filter('with_hosts')
def with_hosts_filter(path):
    return path + "?hosts=" + urllib.quote(g.hosts)

@app.before_request
def before_request():
    hosts = request.args.get('hosts')
    g.hosts = hosts
    if (request.path.startswith('/nodes') or request.path.startswith('/data') or request.path.startswith('/zk')) and not hosts:
      raise BadRequest('no hosts parameters')
    if request.path.startswith('/nodes/') or request.path.startswith('/data/'):
        g.zk = KazooClient(hosts=g.hosts, read_only=True)
        g.zk.start()

@app.teardown_request
def teardown_request(exception):
    if 'zk' in g:
        g.zk.stop()
        g.zk.close()

@app.route('/zk/', defaults={'path': ''})
@app.route('/zk/<path:path>')
def view(path):
    return render_template('zk.html', path=path, hosts=g.hosts)

@app.route('/nodes/', defaults={'path': ''})
@app.route('/nodes/<path:path>')
def nodes(path):
    ancestors = []
    full_path = ''
    ancestors.append({
        'name': '/',
        'full_path': '/'})
    for ancestor in path.split('/'):
        if ancestor != '':
            full_path += '/' + ancestor
            ancestors.append({
                'name': ancestor,
                'full_path': full_path})
    children = sorted(g.zk.get_children(path))
    return render_template('_nodes.html',
        path=full_path + '/',
        hosts=g.hosts,
        children=children,
        ancestors=ancestors)

@app.route('/data/', defaults={'path': ''})
@app.route('/data/<path:path>')
def data(path):
    node = g.zk.get(path)
    meta = {}
    for attr in ZNODESTAT_ATTR:
        meta[attr] = getattr(node[1], attr)
    if path.endswith('/'):
        path = path[:-1]
    data = parse_data(node[0])
    return render_template('_data.html',
        path='/' + path,
        data=data,
        hosts=g.hosts,
        is_dict=type(data) == dict,
        meta=meta);

@app.route('/')
def root():
  return render_template('index.html')
    

def parse_data(raw_data):
    try:
        data = json.loads(raw_data)
        return data
    except:
        return raw_data

if __name__ == '__main__':
    app.run()
