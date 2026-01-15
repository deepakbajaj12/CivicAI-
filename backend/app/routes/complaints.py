from flask import Blueprint, request, jsonify
from app.models import Database
from app.services import AIService
from app.config import Config

complaint_bp = Blueprint('complaints', __name__)

def init_routes(app):
    """Initialize database and AI service"""
    app.db = Database(Config.MONGO_URI)
    app.ai_service = AIService(Config.AI_PROVIDER)
    app.register_blueprint(complaint_bp, url_prefix='/api')

@complaint_bp.route('/complaints', methods=['POST'])
def create_complaint():
    """Submit a new complaint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'description' not in data:
            return jsonify({'error': 'Description is required'}), 400
        
        complaint_text = data['description']
        citizen_name = data.get('citizen_name', 'Anonymous')
        citizen_email = data.get('citizen_email', '')
        location = data.get('location', '')
        
        # Analyze complaint using AI
        from flask import current_app
        analysis = current_app.ai_service.analyze_complaint(complaint_text)
        
        # Create complaint document
        complaint_data = {
            'citizen_name': citizen_name,
            'citizen_email': citizen_email,
            'location': location,
            'description': complaint_text,
            'category': analysis['category'],
            'urgency': analysis['urgency'],
            'summary': analysis['summary'],
            'reasoning': analysis['reasoning'],
            'status': 'pending'
        }
        
        # Save to database
        complaint_id = current_app.db.create_complaint(complaint_data)
        
        # Get created complaint
        complaint = current_app.db.get_complaint(complaint_id)
        
        return jsonify({
            'success': True,
            'complaint': complaint,
            'message': 'Complaint submitted successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Invalid data provided'}), 400
    except Exception as e:
        # Log error for debugging but don't expose details
        return jsonify({'error': 'Failed to process complaint'}), 500

@complaint_bp.route('/complaints', methods=['GET'])
def get_complaints():
    """Get all complaints with pagination and filters"""
    try:
        from flask import current_app
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        category = request.args.get('category')
        urgency = request.args.get('urgency')
        status = request.args.get('status')
        
        # Build filters
        filters = {}
        if category:
            filters['category'] = category
        if urgency:
            filters['urgency'] = urgency
        if status:
            filters['status'] = status
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Get complaints
        complaints = current_app.db.get_all_complaints(limit=limit, skip=skip, filters=filters)
        total = current_app.db.get_complaints_count(filters=filters)
        
        return jsonify({
            'success': True,
            'complaints': complaints,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid query parameters'}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve complaints'}), 500

@complaint_bp.route('/complaints/<complaint_id>', methods=['GET'])
def get_complaint(complaint_id):
    """Get a specific complaint"""
    try:
        from flask import current_app
        complaint = current_app.db.get_complaint(complaint_id)
        
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        return jsonify({
            'success': True,
            'complaint': complaint
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve complaint'}), 500

@complaint_bp.route('/complaints/<complaint_id>', methods=['PUT'])
def update_complaint(complaint_id):
    """Update a complaint (admin only)"""
    try:
        from flask import current_app
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Only allow status updates for now
        allowed_fields = ['status']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        success = current_app.db.update_complaint(complaint_id, update_data)
        
        if not success:
            return jsonify({'error': 'Complaint not found or not updated'}), 404
        
        complaint = current_app.db.get_complaint(complaint_id)
        
        return jsonify({
            'success': True,
            'complaint': complaint,
            'message': 'Complaint updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update complaint'}), 500

@complaint_bp.route('/complaints/<complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    """Delete a complaint (admin only)"""
    try:
        from flask import current_app
        success = current_app.db.delete_complaint(complaint_id)
        
        if not success:
            return jsonify({'error': 'Complaint not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Complaint deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to delete complaint'}), 500

@complaint_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get complaint statistics (admin dashboard)"""
    try:
        from flask import current_app
        stats = current_app.db.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

@complaint_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'CivicAI API is running',
        'ai_provider': Config.AI_PROVIDER
    }), 200
