from flask import Flask, render_template, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import parser as dateparser


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.db'
db = SQLAlchemy(app)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(250), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def todict(self):
        return {'id': self.id, 'name': self.name, 'entrances': [e.todict() for e  in self.entrances], 'capacity':self.capacity}

    def __repr__(self):
        return '<Store %r>' % self.name

class Entrance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(250), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'),
                        nullable=False)
    store = db.relationship('Store',
                            backref=db.backref('entrances', lazy=True))

    def __repr__(self):
        return '<Entrance %r>' % self.name

    def todict(self):
        return {'id': self.id, 'store_id': self.store_id, 'name': self.name}

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    entrance_id = db.Column(db.Integer, db.ForeignKey('entrance.id'),
                        nullable=False)
    entrance = db.relationship('Entrance',
                               backref=db.backref('records', lazy='dynamic', order_by='-Record.id'))
    inside = db.Column(db.Integer, nullable=False)
    change = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Record %r>' % self.id

    def todict(self):
        return {'id': self.id, 'entrance_id': self.entrance_id, 'timestamp': self.timestamp.isoformat(), 'inside': self.inside, 'change': self.change}



@app.route('/api/record/<store_id>/<entrance_id>', methods=['POST'])
def create_record(store_id, entrance_id):
    data = request.json
    if not data:
        abort(400)
    try:
        timestamp = dateparser.isoparse(data['timestamp'])
        inside = data['inside']
        change = data['change']
        # TODO: check if existing?
        newrec = Record(timestamp=timestamp, inside=inside, change=change, entrance_id=entrance_id)
        db.session.add(newrec)
        db.session.commit()
    except KeyError:
        abort(400)
    return 'ok'

@app.route('/api/store/<store_id>/<entrance_id>/records/<limit>')
@app.route('/api/store/<store_id>/<entrance_id>/records')
def get_records(store_id, entrance_id, limit=-1):
    entrance = Entrance.query.filter_by(store_id=store_id, id=entrance_id).one()
    if not entrance:
        abort(404)
    return jsonify([r.todict() for r in entrance.records.limit(limit)])

# @app.route('/api/store/<store_id>/<entrance_id>/records')
# def get_records(store_id, entrance_id):
#     entrance = Entrance.query.filter_by(store_id=store_id, id=entrance_id).one()
#     if not entrance:
#         abort(404)
#     return jsonify([r.todict() for r in entrance.records])

@app.route('/api/store/<store_id>/entrances')
def get_entrances(store_id):
    store = Store.query.filter_by(id=store_id).one()
    if not store:
        abort(404)
    return jsonify([e.todict() for e in store.entrances])

@app.route('/api/store/<store_id>')
def get_store(store_id):
    store = Store.query.filter_by(id=store_id).one()
    if not store:
        abort(404)
    return jsonify(store.todict())
    

@app.route('/dashboard/<store_id>')
def dashboard(store_id):
    store = Store.query.filter_by(id=store_id).one()
    if not store:
        abort(404)
    return render_template('dashboard.html', store_name = store.name)

@app.route('/traffic/<store_id>')
def trafficlight(store_id):
    store = Store.query.filter_by(id=store_id).one()
    if not store:
        abort(404)
    return render_template('trafficlight.html', store_name = store.name, store_id=store.id)

# static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    
