from flask import Flask, request, current_app, abort, jsonify
from flask_cors import CORS
import redis
import json
import os

app = Flask(__name__)
# TODO: restrict origins again later
cors = CORS(app, origins=['*'])

redis_host = os.environ.get("REDIS_HOST", default="localhost")
redis_port = int(os.environ.get("REDIS_PORT", default=6379))
redis_db = int(os.environ.get("REDIS_DB", default=0))
rd = redis.Redis(host=redis_host, port=redis_port, db=redis_db)


def _rd2str(data):
    """
    Shorthand helper to get a str from redis responses (bytes)
    """
    return data.decode("utf-8")


def _item_list(prefix):
    items = []
    for k in rd.scan_iter(prefix + '/*'):
        elem = json.loads(rd.get(k))
        # add id field with prefix and slash removed
        elem['id'] = _rd2str(k)[(len(prefix) + 1):]
        items.append(elem)
    return items


def _store_params(key, request_dict, entry_list, additional={}):
    to_store = {}
    for entry_key in entry_list:
        val = request_dict.get(entry_key)
        # require all entry keys and abort if not available
        if not val:
            return False
        to_store[entry_key] = val

    for akey in additional:
        to_store[akey] = additional[akey]

    rd.set(key, json.dumps(to_store))
    return True


def _load_bar(bar_id):
    item = rd.get('bar/' + bar_id)
    bar_dict = None
    if item:
        bar_dict = json.loads(item)
    return bar_dict


def _save_bar(bar_id, bar_dict):
    rd.set('bar/' + bar_id, json.dumps(bar_dict))


# duplicate read bars endpoint for plugins
@app.route('/bars')
@app.route('/plugins/bars')
def list_bars():
    bars = _item_list('bar')

    return jsonify(bars)

# duplicate read tables endpoint for plugins
@app.route('/bars/<bar_id>/tables')
@app.route('/plugins/bars/<bar_id>/tables')
def bar_tables(bar_id):
    tables = _item_list('tbl/' + bar_id)
    return jsonify(tables)


@app.route('/bars/<bar_id>/tables/<tbl_id>/join', methods=['POST'])
def join_table(bar_id, tbl_id):
    json_data = request.get_json(force=True)
    if 'user' not in json_data:
        abort(400)

    rd_key = 'tbl/' + bar_id + '/' + tbl_id
    table_state = rd.get(rd_key)
    if not table_state:
        return (jsonify({}), 404)

    table_users = json.loads(table_state)
    user = json_data.get('user')
    if user in table_users.get('guests'):
        return (jsonify({}), 304)

    table_users.get('guests').append(user)
    rd.set(rd_key, json.dumps(table_users))

    bar = _load_bar(bar_id)
    if not bar:
        return (jsonify({}), 404)
    bar['users'] = bar.get('users') + 1
    _save_bar(bar_id, bar)

    return jsonify({})


@app.route('/bars/<bar_id>/tables/<tbl_id>/leave', methods=['POST'])
def leave_table(bar_id, tbl_id):
    json_data = request.get_json(force=True)
    if 'user' not in json_data:
        abort(400)

    rd_key = 'tbl/' + bar_id + '/' + tbl_id
    table_state = rd.get(rd_key)
    if not table_state:
        return (jsonify({}), 404)

    table_users = json.loads(table_state)
    user = json_data.get('user')
    if user not in table_users.get('guests'):
        return (jsonify({}), 304)

    guests_new = set(table_users.get('guests'))
    guests_new.remove(user)
    table_users['guests'] = list(guests_new)
    rd.set(rd_key, json.dumps(table_users))

    bar = _load_bar(bar_id)
    if not bar:
        return (jsonify({}), 404)
    bar['users'] = max(bar.get('users') - 1, 0)
    _save_bar(bar_id, bar)

    return jsonify({})


@app.route('/bars/<bar_id>/music')
def music(bar_id):
    bar_music = rd.get('mus/' + bar_id)
    if bar_music:
        music_data = json.loads(bar_music)
        return jsonify(music_data)
    else:
        return (jsonify({}), 404)


@app.route('/bars/<bar_id>/drinks')
def drinks(bar_id):
    drink_list = _item_list('drink/' + bar_id)
    return jsonify(drink_list)


@app.route('/bars/<bar_id>/drinks/buy', methods=['POST'])
def buy_drink(bar_id):
    json_data = request.get_json(force=True)
    if 'user' not in json_data or 'drinkId' not in json_data:
        abort(400)

    # TODO: actually store something
    return jsonify({
        'token': 'abcde'
    })

# ---- management API ---
# TODO: auth

@app.route('/manage/bars/<bar_id>', methods=['PUT'])
def add_bar(bar_id):
    json_data = request.get_json(force=True)
    store_ok = _store_params('bar/' + bar_id, json_data, [
        'name', 'description', 'image'
    ], {'users': 0})

    if not store_ok:
        abort(400)

    return (jsonify({}), 201)


@app.route('/manage/bars/<bar_id>/tables/<tbl_id>', methods=['PUT'])
def add_table(bar_id, tbl_id):
    rd_key = 'tbl/' + bar_id + '/' + tbl_id
    if rd.get(rd_key):
        return (jsonify({}), 304)
    rd.set(rd_key, json.dumps({
        'guests': []
    }))

    return (jsonify({}), 201)


@app.route('/manage/bars/<bar_id>/drinks/<drink_id>', methods=['PUT', 'DELETE'])
def manage_drinks(bar_id, drink_id):
    item_key = 'drink/' + bar_id + '/' + drink_id
    if request.method == 'DELETE':
        rd.delete(item_key)
        return jsonify({})
    else:
        json_data = request.get_json(force=True)
        store_ok = _store_params(item_key, json_data, [
            'name', 'price'
        ])

        if not store_ok:
            abort(400)

        return (jsonify({}), 201)


@app.route('/manage/bars/<bar_id>/music', methods=['POST'])
def update_music(bar_id):
    json_data = request.get_json(force=True)
    store_ok = _store_params('mus/' + bar_id, json_data, [
        'url', 'playbackPosition'
    ])

    if not store_ok:
        abort(400)

    return (jsonify({}), 201)


# ---- Plugin API ----


# see above:
# /plugins/bars
# /plugins/bars/<bar_id>/tables


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
