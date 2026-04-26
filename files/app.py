"""
Smart Event Management System - Flask Server
Connects C backend (engine.dll) with HTML frontend
Author: Your Name
Version: 1.0
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import ctypes
import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)  # Enable CORS for all routes

# ==================== C DLL SETUP ====================
# Load the compiled C DLL (engine.dll) into Python
# Make sure engine.dll is in the same directory as app.py

try:
    # Load the C library
    lib = ctypes.CDLL("./engine.dll")
    
    # Define function signatures for ctypes
    # This tells Python what data types each C function expects and returns
    
    # int add_event(char title[], char category[], char location[], 
    #               int deadline, int urgency, int importance, int guests, float budget)
    lib.add_event.argtypes = [
        ctypes.c_char_p,  # title
        ctypes.c_char_p,  # category
        ctypes.c_char_p,  # location
        ctypes.c_int,     # deadline
        ctypes.c_int,     # urgency
        ctypes.c_int,     # importance
        ctypes.c_int,     # guests
        ctypes.c_float    # budget
    ]
    lib.add_event.restype = ctypes.c_int
    
    # int delete_event(int event_id)
    lib.delete_event.argtypes = [ctypes.c_int]
    lib.delete_event.restype = ctypes.c_int
    
    # void get_all_events(char *result, int max_len)
    lib.get_all_events.argtypes = [ctypes.c_char_p, ctypes.c_int]
    lib.get_all_events.restype = None
    
    # void generate_schedule(char *result, int max_len)
    lib.generate_schedule.argtypes = [ctypes.c_char_p, ctypes.c_int]
    lib.generate_schedule.restype = None
    
    # void get_analytics(char *result, int max_len)
    lib.get_analytics.argtypes = [ctypes.c_char_p, ctypes.c_int]
    lib.get_analytics.restype = None
    
    # int update_event_status(int event_id, int new_status)
    lib.update_event_status.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.update_event_status.restype = ctypes.c_int
    
    # void search_events(char *query, char *result, int max_len)
    lib.search_events.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    lib.search_events.restype = None
    
    print("[✓] Successfully loaded engine.dll")
    DLL_LOADED = True
    
except Exception as e:
    print(f"[✗] Error loading engine.dll: {e}")
    print("[!] Make sure engine.dll is in the same directory as app.py")
    DLL_LOADED = False


# ==================== HELPER FUNCTIONS ====================

def encode_str(s):
    """Convert Python string to bytes for C functions"""
    if isinstance(s, str):
        return s.encode('utf-8')
    return s


def decode_str(b):
    """Convert C bytes to Python string"""
    if isinstance(b, bytes):
        return b.decode('utf-8')
    return b


# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    """
    Main route - Serve the HTML frontend
    Returns the index.html file which contains the UI
    """
    return render_template('index.html')


@app.route('/api/events/add', methods=['POST'])
def add_event_route():
    """
    API route to add a new event
    
    Expected JSON format:
    {
        "title": "Project Submission",
        "category": "Deadline",
        "location": "College",
        "deadline": 5,
        "urgency": 8,
        "importance": 9,
        "guests": 0,
        "budget": 0.0
    }
    
    Returns: {"success": true/false, "message": "..."}
    """
    if not DLL_LOADED:
        return jsonify({"success": False, "message": "C engine not loaded"}), 500
    
    try:
        data = request.get_json()
        
        # Extract and validate data
        title = data.get('title', '').strip()
        category = data.get('category', 'Other').strip()
        location = data.get('location', '').strip()
        deadline = int(data.get('deadline', 1))
        urgency = int(data.get('urgency', 5))
        importance = int(data.get('importance', 5))
        guests = int(data.get('guests', 0))
        budget = float(data.get('budget', 0.0))
        
        # Validate inputs
        if not title:
            return jsonify({"success": False, "message": "Title is required"}), 400
        
        if deadline < 1 or deadline > 365:
            return jsonify({"success": False, "message": "Deadline must be 1-365 days"}), 400
        
        if urgency < 1 or urgency > 10:
            return jsonify({"success": False, "message": "Urgency must be 1-10"}), 400
        
        if importance < 1 or importance > 10:
            return jsonify({"success": False, "message": "Importance must be 1-10"}), 400
        
        # Call C function
        result = lib.add_event(
            encode_str(title),
            encode_str(category),
            encode_str(location),
            deadline,
            urgency,
            importance,
            guests,
            budget
        )
        
        if result:
            return jsonify({
                "success": True,
                "message": f"Event '{title}' added successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to add event (storage full or invalid data)"
            }), 400
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route('/api/events/delete', methods=['POST'])
def delete_event_route():
    """
    API route to delete an event by ID
    
    Expected JSON: {"event_id": 1}
    Returns: {"success": true/false, "message": "..."}
    """
    if not DLL_LOADED:
        return jsonify({"success": False, "message": "C engine not loaded"}), 500
    
    try:
        data = request.get_json()
        event_id = int(data.get('event_id', 0))
        
        if event_id <= 0:
            return jsonify({"success": False, "message": "Invalid event ID"}), 400
        
        result = lib.delete_event(event_id)
        
        if result:
            return jsonify({"success": True, "message": f"Event {event_id} deleted"})
        else:
            return jsonify({"success": False, "message": "Event not found"}), 404
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route('/api/events/all', methods=['GET'])
def get_events_route():
    """
    API route to get all events
    
    Returns JSON with all events:
    {
        "events": [
            {"id": 1, "title": "...", "category": "...", ...},
            ...
        ]
    }
    """
    if not DLL_LOADED:
        return jsonify({"error": "C engine not loaded"}), 500
    
    try:
        # Create buffer to receive C output
        buffer = ctypes.create_string_buffer(8000)
        
        # Call C function
        lib.get_all_events(buffer, 8000)
        
        # Convert buffer to string and parse JSON
        result_str = decode_str(buffer.value)
        result_json = json.loads(result_str)
        
        return jsonify(result_json)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/events/schedule', methods=['GET'])
def schedule_route():
    """
    API route to generate smart schedule
    Uses C algorithm to sort events by priority score
    
    Returns optimally ordered events:
    {
        "schedule": [
            {"id": 1, "title": "...", "priority_score": 345, "position": 1},
            ...
        ]
    }
    """
    if not DLL_LOADED:
        return jsonify({"error": "C engine not loaded"}), 500
    
    try:
        # Create buffer
        buffer = ctypes.create_string_buffer(8000)
        
        # Call C function
        lib.generate_schedule(buffer, 8000)
        
        # Parse result
        result_str = decode_str(buffer.value)
        result_json = json.loads(result_str)
        
        return jsonify(result_json)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analytics', methods=['GET'])
def analytics_route():
    """
    API route to get analytics and statistics
    
    Returns:
    {
        "total_events": 5,
        "total_budget": 50000.00,
        "total_guests": 250,
        "completed": 2,
        "pending": 3,
        "avg_importance": 7.5
    }
    """
    if not DLL_LOADED:
        return jsonify({"error": "C engine not loaded"}), 500
    
    try:
        buffer = ctypes.create_string_buffer(500)
        lib.get_analytics(buffer, 500)
        
        result_str = decode_str(buffer.value)
        result_json = json.loads(result_str)
        
        return jsonify(result_json)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/events/status', methods=['POST'])
def update_status_route():
    """
    API route to update event status
    
    Expected JSON: {"event_id": 1, "status": 1}
    Status: 0=Pending, 1=In Progress, 2=Completed
    """
    if not DLL_LOADED:
        return jsonify({"success": False, "message": "C engine not loaded"}), 500
    
    try:
        data = request.get_json()
        event_id = int(data.get('event_id', 0))
        status = int(data.get('status', 0))
        
        if event_id <= 0:
            return jsonify({"success": False, "message": "Invalid event ID"}), 400
        
        if status < 0 or status > 2:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        
        result = lib.update_event_status(event_id, status)
        
        if result:
            status_names = ["Pending", "In Progress", "Completed"]
            return jsonify({"success": True, "message": f"Status updated to {status_names[status]}"})
        else:
            return jsonify({"success": False, "message": "Event not found"}), 404
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route('/api/events/search', methods=['GET'])
def search_route():
    """
    API route to search events by title or category
    
    Query parameter: ?q=search_query
    
    Returns matching events
    """
    if not DLL_LOADED:
        return jsonify({"error": "C engine not loaded"}), 500
    
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({"results": []})
        
        buffer = ctypes.create_string_buffer(8000)
        lib.search_events(encode_str(query), buffer, 8000)
        
        result_str = decode_str(buffer.value)
        result_json = json.loads(result_str)
        
        return jsonify(result_json)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint - verify server is running
    """
    return jsonify({
        "status": "online",
        "engine": "loaded" if DLL_LOADED else "not_loaded",
        "timestamp": datetime.now().isoformat()
    })


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    # Print startup information
    print("\n" + "="*60)
    print("  Smart Event Management System - Flask Server")
    print("="*60)
    print("\n[*] Server starting...")
    print(f"[*] DLL Status: {'LOADED ✓' if DLL_LOADED else 'NOT LOADED ✗'}")
    print("[*] Database: In-memory (C structures)")
    print("[*] Frontend: index.html")
    print("\n[*] Available endpoints:")
    print("    GET  /                  → Serve frontend")
    print("    POST /api/events/add    → Add new event")
    print("    POST /api/events/delete → Delete event")
    print("    GET  /api/events/all    → Get all events")
    print("    GET  /api/events/schedule → Generate smart schedule")
    print("    POST /api/events/status → Update event status")
    print("    GET  /api/events/search → Search events")
    print("    GET  /api/analytics     → Get statistics")
    print("    GET  /api/health        → Health check")
    
    print("\n[*] Access the application:")
    print("    URL: http://localhost:5000")
    print("\n" + "="*60 + "\n")
    
    # Run Flask server
    # debug=True: Auto-reload on code changes
    # host='0.0.0.0': Accept connections from any IP
    # port=5000: Standard development port
    app.run(debug=True, host='127.0.0.1', port=5000)
