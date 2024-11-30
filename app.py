from flask import Flask, render_template, request, redirect, jsonify, abort
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import re
from datetime import datetime
from urllib.parse import quote_plus

app = Flask(__name__)
Base = declarative_base()

# Database Models
class GoLink(Base):
    __tablename__ = 'golinks'
    id = Column(Integer, primary_key=True)
    shortlink = Column(String, unique=True, nullable=False)
    destination = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

class LinkUsage(Base):
    __tablename__ = 'link_usage'
    id = Column(Integer, primary_key=True)
    shortlink = Column(String, nullable=False)
    accessed_at = Column(DateTime, default=func.now())
    args = Column(String, nullable=True)

# Database setup
def get_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'golinks.db')
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

@app.route('/')
def root():
    return redirect('/go/go')

@app.route('/go/<path:shortlink>')
def handle_go_link(shortlink):
    db = get_db()
    
    # Special case for go/go
    if shortlink == 'go':
        return render_template('index.html')
    
    # Find the link in database
    link = db.query(GoLink).filter_by(shortlink=shortlink).first()
    if not link:
        return redirect('/go/go')
    
    # Get any additional arguments
    args = request.args.get('q', '')
    
    # Record usage
    usage = LinkUsage(shortlink=shortlink, args=args)
    db.add(usage)
    db.commit()
    
    # Handle the destination URL
    destination = link.destination
    if '{query}' in destination and args:
        destination = destination.replace('{query}', quote_plus(args))
    elif args:
        if '?' in destination:
            destination += f'&q={quote_plus(args)}'
        else:
            destination += f'?q={quote_plus(args)}'
    
    return redirect(destination)

@app.route('/api/links', methods=['GET'])
def get_links():
    db = get_db()
    links = db.query(GoLink).all()
    return jsonify([{
        'id': link.id,
        'shortlink': link.shortlink,
        'destination': link.destination,
        'created_at': link.created_at.isoformat()
    } for link in links])

@app.route('/api/links', methods=['POST'])
def create_link():
    data = request.json
    shortlink = data.get('shortlink', '').strip()
    destination = data.get('destination', '').strip()
    
    if not shortlink or not destination:
        abort(400, description="Both shortlink and destination are required")
    
    if not re.match(r'^[a-zA-Z0-9-_]+$', shortlink):
        abort(400, description="Shortlink can only contain letters, numbers, hyphens, and underscores")
        
    if not destination.startswith(('http://', 'https://')):
        destination = 'https://' + destination
    
    db = get_db()
    existing = db.query(GoLink).filter_by(shortlink=shortlink).first()
    if existing:
        abort(409, description="Shortlink already exists")
    
    link = GoLink(shortlink=shortlink, destination=destination)
    db.add(link)
    db.commit()
    
    return jsonify({
        'id': link.id,
        'shortlink': link.shortlink,
        'destination': link.destination,
        'created_at': link.created_at.isoformat()
    })

@app.route('/api/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    db = get_db()
    link = db.query(GoLink).get(link_id)
    if not link:
        abort(404)
    
    db.delete(link)
    db.commit()
    return '', 204

@app.route('/api/analytics')
def get_analytics():
    db = get_db()
    analytics = db.query(
        LinkUsage.shortlink,
        func.count(LinkUsage.id).label('usage_count'),
        func.max(LinkUsage.accessed_at).label('last_used')
    ).group_by(LinkUsage.shortlink).all()
    
    return jsonify([{
        'shortlink': item[0],
        'usage_count': item[1],
        'last_used': item[2].isoformat() if item[2] else None
    } for item in analytics])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
