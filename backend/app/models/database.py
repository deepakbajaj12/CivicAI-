from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

class Database:
    """MongoDB database connection and operations"""
    
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database()
        self.complaints = self.db.complaints
        
    def create_complaint(self, complaint_data):
        """Create a new complaint"""
        complaint_data['created_at'] = datetime.utcnow()
        complaint_data['updated_at'] = datetime.utcnow()
        result = self.complaints.insert_one(complaint_data)
        return str(result.inserted_id)
    
    def get_complaint(self, complaint_id):
        """Get a complaint by ID"""
        try:
            complaint = self.complaints.find_one({'_id': ObjectId(complaint_id)})
            if complaint:
                complaint['_id'] = str(complaint['_id'])
            return complaint
        except Exception:
            return None
    
    def get_all_complaints(self, limit=100, skip=0, filters=None):
        """Get all complaints with pagination and filters"""
        query = filters or {}
        complaints = list(self.complaints.find(query)
                         .sort('created_at', -1)
                         .skip(skip)
                         .limit(limit))
        for complaint in complaints:
            complaint['_id'] = str(complaint['_id'])
        return complaints
    
    def get_complaints_count(self, filters=None):
        """Get total count of complaints"""
        query = filters or {}
        return self.complaints.count_documents(query)
    
    def update_complaint(self, complaint_id, update_data):
        """Update a complaint"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.complaints.update_one(
                {'_id': ObjectId(complaint_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    def delete_complaint(self, complaint_id):
        """Delete a complaint"""
        try:
            result = self.complaints.delete_one({'_id': ObjectId(complaint_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    def get_statistics(self):
        """Get complaint statistics"""
        total = self.complaints.count_documents({})
        
        # Count by category
        by_category = {}
        for category in ['Road', 'Water', 'Electricity', 'Sanitation', 'Safety', 'Other']:
            by_category[category] = self.complaints.count_documents({'category': category})
        
        # Count by urgency
        by_urgency = {}
        for urgency in ['Low', 'Medium', 'High', 'Critical']:
            by_urgency[urgency] = self.complaints.count_documents({'urgency': urgency})
        
        return {
            'total': total,
            'by_category': by_category,
            'by_urgency': by_urgency
        }
