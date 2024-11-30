import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from urllib.parse import quote_plus
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from config import Config

# Initialize Sentry if DSN is provided
if dsn := os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Initialize SQLAlchemy with app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class GoLink(db.Model):
    __tablename__ = 'golinks'
    id = db.Column(db.Integer, primary_key=True)
    shortlink = db.Column(db.String(255), unique=True, nullable=False, index=True)
    destination = db.Column(db.String(2048), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'shortlink': self.shortlink,
            'destination': self.destination,
            'created_at': self.created_at.isoformat()
        }

class LinkUsage(db.Model):
    __tablename__ = 'link_usage'
    id = db.Column(db.Integer, primary_key=True)
    shortlink = db.Column(db.String(255), nullable=False, index=True)
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    args = db.Column(db.String(1024), nullable=True)
    user_agent = db.Column(db.String(1024), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return redirect('/')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('error.html'), 500

# Routes
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<path:shortlink>')
def handle_go_link(shortlink):
    try:
        # Find the link in database
        link = GoLink.query.filter_by(shortlink=shortlink).first()
        if not link:
            app.logger.info(f'Shortlink not found: {shortlink}')
            return render_template('not_found.html', shortlink=shortlink), 404
        
        # Get any additional arguments
        args = request.args.get('q', '')
        
        # Record usage with additional metadata
        usage = LinkUsage(
            shortlink=shortlink,
            args=args,
            user_agent=request.user_agent.string,
            ip_address=request.remote_addr
        )
        db.session.add(usage)
        db.session.commit()
        
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
    
    except Exception as e:
        app.logger.error(f'Error handling go link: {str(e)}')
        db.session.rollback()
        return redirect('/')

@app.route('/api/links', methods=['GET'])
def get_links():
    try:
        search_query = request.args.get('q', '').strip().lower()
        query = GoLink.query.order_by(GoLink.created_at.desc())
        
        if search_query:
            search_filter = db.or_(
                GoLink.shortlink.ilike(f'%{search_query}%'),
                GoLink.destination.ilike(f'%{search_query}%')
            )
            query = query.filter(search_filter)
        
        links = query.all()
        return jsonify([link.to_dict() for link in links])
    except Exception as e:
        app.logger.error(f'Error getting links: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/links', methods=['POST'])
def create_link():
    try:
        data = request.get_json()
        shortlink = data.get('shortlink', '').strip()
        destination = data.get('destination', '').strip()
        
        if not shortlink or not destination:
            return jsonify({'error': 'Both shortlink and destination are required'}), 400
        
        if not shortlink.isalnum() and not all(c in '-_' for c in shortlink if not c.isalnum()):
            return jsonify({'error': 'Shortlink can only contain letters, numbers, hyphens, and underscores'}), 400
            
        if not destination.startswith(('http://', 'https://')):
            destination = 'https://' + destination
        
        existing = GoLink.query.filter_by(shortlink=shortlink).first()
        if existing:
            return jsonify({'error': 'Shortlink already exists'}), 409
        
        link = GoLink(shortlink=shortlink, destination=destination)
        db.session.add(link)
        db.session.commit()
        
        return jsonify(link.to_dict()), 201
    
    except Exception as e:
        app.logger.error(f'Error creating link: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    try:
        link = GoLink.query.get(link_id)
        if not link:
            return '', 404
        
        db.session.delete(link)
        db.session.commit()
        return '', 204
    
    except Exception as e:
        app.logger.error(f'Error deleting link: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/links/<int:link_id>', methods=['PUT'])
def update_link(link_id):
    try:
        link = GoLink.query.get(link_id)
        if not link:
            return '', 404
        
        data = request.get_json()
        shortlink = data.get('shortlink', '').strip()
        destination = data.get('destination', '').strip()
        
        if not shortlink or not destination:
            return jsonify({'error': 'Both shortlink and destination are required'}), 400
        
        if not shortlink.isalnum() and not all(c in '-_' for c in shortlink if not c.isalnum()):
            return jsonify({'error': 'Shortlink can only contain letters, numbers, hyphens, and underscores'}), 400
            
        if not destination.startswith(('http://', 'https://')):
            destination = 'https://' + destination
        
        # Check if the new shortlink already exists (excluding the current link)
        existing = GoLink.query.filter(GoLink.shortlink == shortlink, GoLink.id != link_id).first()
        if existing:
            return jsonify({'error': 'Shortlink already exists'}), 409
        
        link.shortlink = shortlink
        link.destination = destination
        db.session.commit()
        
        return jsonify(link.to_dict()), 200
    
    except Exception as e:
        app.logger.error(f'Error updating link: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/links/<string:shortlink>/stats')
def get_link_stats(shortlink):
    try:
        stats = db.session.query(
            db.func.count(LinkUsage.id).label('usage_count'),
            db.func.max(LinkUsage.accessed_at).label('last_used')
        ).filter(LinkUsage.shortlink == shortlink).first()
        
        return jsonify({
            'usage_count': stats[0] if stats else 0,
            'last_used': stats[1].isoformat() if stats and stats[1] else None
        })
    except Exception as e:
        app.logger.error(f'Error getting link stats: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analytics')
def get_analytics():
    try:
        analytics = db.session.query(
            LinkUsage.shortlink,
            db.func.count(LinkUsage.id).label('usage_count'),
            db.func.max(LinkUsage.accessed_at).label('last_used')
        ).group_by(LinkUsage.shortlink).all()
        
        return jsonify([{
            'shortlink': item[0],
            'usage_count': item[1],
            'last_used': item[2].isoformat() if item[2] else None
        } for item in analytics])
    
    except Exception as e:
        app.logger.error(f'Error getting analytics: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

def setup_logging(app):
    if not app.debug:
        file_handler = RotatingFileHandler(
            Config.LOG_FILE,
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('GoLinks startup')

if __name__ == '__main__':
    setup_logging(app)
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=os.environ.get('FLASK_DEBUG', '0') == '1'
    )
