# Smart Event Management System - Complete Setup Guide

## 📋 Project Overview

A professional event management system built with three technologies:
- **C Language**: High-performance backend with smart scheduling algorithm
- **Python Flask**: API server connecting frontend to C backend
- **HTML/CSS/JavaScript**: Modern, responsive web interface

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   index.html (Frontend)                      │
│              Modern UI with Dark Theme                       │
│         (HTML5, CSS3, Vanilla JavaScript)                   │
└────────────────────┬────────────────────────────────────────┘
                     │ JSON API Calls
                     │ (AJAX/Fetch)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   app.py (Flask Server)                      │
│      Routes, Request Handling, Data Validation              │
│            (Python 3.x with Flask)                          │
└────────────────────┬────────────────────────────────────────┘
                     │ ctypes Library
                     │ (C Interop)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   engine.dll (C Backend)                     │
│    Event Management, Smart Scheduling Algorithm            │
│         (Compiled C code - engine.c)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 7/10/11 (64-bit)
- **RAM**: 2 GB
- **Disk Space**: 500 MB
- **Python**: 3.8 or higher
- **Visual C++ Redistributable**: For running compiled DLL

### Recommended
- **OS**: Windows 10/11 (Latest)
- **RAM**: 4 GB
- **Python**: 3.10 or higher

---

## 📦 Installation Steps

### Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

### Step 2: Install Required Python Packages

Open Command Prompt (cmd.exe) in your project folder and run:

```bash
pip install flask flask-cors
```

This installs:
- **Flask**: Web server framework
- **Flask-CORS**: Enable cross-origin requests

### Step 3: Compile C Code to DLL

#### Option A: Using Visual Studio (Recommended)

1. Install Visual Studio Community (free) from https://visualstudio.microsoft.com/
2. During installation, select "Desktop development with C++"
3. Create a new "Dynamic-Link Library (DLL)" project
4. Copy `engine.c` code into your project
5. Build → Release
6. Copy generated `engine.dll` to your project folder

#### Option B: Using MinGW (Alternative)

1. Install MinGW from https://www.mingw-w64.org/
2. Open Command Prompt in your project folder:
   ```bash
   gcc -shared -o engine.dll engine.c
   ```

#### Option C: Use Pre-compiled DLL (If Available)

If you have a pre-compiled `engine.dll`, simply place it in the project folder.

---

## 🚀 Running the Project

### Step 1: Prepare Project Folder

Create a folder structure like this:
```
SmartEventManager/
├── engine.dll          (Compiled C library)
├── engine.c           (C source - for reference)
├── app.py             (Flask server)
├── index.html         (Frontend)
└── requirements.txt   (Optional - for dependencies)
```

### Step 2: Start the Server

1. Open Command Prompt
2. Navigate to project folder:
   ```bash
   cd C:\Path\To\SmartEventManager
   ```

3. Run Flask server:
   ```bash
   python app.py
   ```

4. You should see:
   ```
   ============================================================
     Smart Event Management System - Flask Server
   ============================================================
   
   [*] Server starting...
   [*] DLL Status: LOADED ✓
   [*] Available endpoints:
       GET  /                  → Serve frontend
       POST /api/events/add    → Add new event
       ...
   
   [*] Access the application:
       URL: http://localhost:5000
   ============================================================
   ```

### Step 3: Open Application

1. Open your web browser
2. Go to: **http://localhost:5000**
3. Application should load with the beautiful UI

---

## 🎯 How to Use

### Adding an Event

1. Click **"Create Event"** in hero section or navigation
2. Fill in event details:
   - **Title**: Event name (required)
   - **Category**: Conference, Meeting, Deadline, Party, etc.
   - **Location**: Where the event happens
   - **Deadline**: Days from now (1-365)
   - **Urgency**: 1-10 scale (10 = most urgent)
   - **Importance**: 1-10 scale (10 = most important)
   - **Expected Guests**: Number of attendees
   - **Budget**: Amount in dollars
3. Click **"Create Event"**
4. Event appears in Events Dashboard

### Viewing Dashboard

- **Dashboard** shows all events in a table
- Search events by title or category
- Quick status updates with buttons
- Delete events if needed

### Smart Schedule

- Click **"Generate Schedule"** button
- Algorithm calculates optimal order based on:
  - Deadline (closest first)
  - Urgency level
  - Importance level
- Shows priority score for each event
- Priority Score = (100 - deadline*10) + (urgency*15) + (importance*12)

### Analytics

Real-time statistics:
- Total events count
- Total budget allocated
- Total expected guests
- Average importance level
- Completed vs pending events

---

## 🔧 How C + Python + HTML Work Together

### 1. Frontend (HTML/JavaScript)
```
User clicks "Create Event"
        ↓
JavaScript collects form data
        ↓
Sends JSON to /api/events/add endpoint
```

### 2. Backend (Python Flask)
```
Receives JSON from frontend
        ↓
Validates data (checks deadline, urgency range, etc)
        ↓
Calls C function using ctypes library
        ↓
Receives result from C code
        ↓
Returns JSON response to frontend
```

### 3. Engine (C DLL)
```
Receives parameters (title, deadline, urgency, etc)
        ↓
Creates Event structure
        ↓
Calculates priority score using algorithm
        ↓
Stores in global events array
        ↓
Returns success/failure code to Python
```

### 4. Data Flow Example

```
index.html
├─ User inputs: "Project Submission", deadline=5, urgency=8
├─ Fetch POST to /api/events/add
│
↓ (Network)
│
app.py
├─ Receives: {"title": "Project Submission", "deadline": 5, ...}
├─ Validates: deadline is 1-365 ✓, urgency is 1-10 ✓
├─ Calls: lib.add_event("Project Submission", "Deadline", ..., 5, 8, ...)
│
↓ (ctypes Library)
│
engine.dll (C)
├─ Creates Event structure
├─ Calculates: priority_score = (100 - 5*10) + (8*15) + (importance*12)
├─ Stores in events[] array
├─ Returns: 1 (success)
│
↓ (ctypes Library)
│
app.py
├─ Receives: 1 (success code)
├─ Returns JSON: {"success": true, "message": "Event added"}
│
↓ (Network)
│
index.html
├─ Shows notification: "Event added successfully"
├─ Refreshes dashboard table
└─ Calls /api/events/all to fetch all events
```

---

## 📚 C Code Explanation

### Priority Calculation Algorithm

```c
int calculate_priority_score(int deadline, int urgency, int importance) {
    // Deadline weight: lower deadline = higher priority
    int deadline_weight = 100 - (deadline * 10);
    
    // Double priority for urgent deadlines (1-3 days)
    if (deadline <= 3) {
        deadline_weight *= 2;
    }
    
    // Direct urgency and importance factors
    int urgency_weight = urgency * 15;
    int importance_weight = importance * 12;
    
    // Final score
    return deadline_weight + urgency_weight + importance_weight;
}
```

**Example Calculation:**
- Event: "Project Submission"
- Deadline: 5 days, Urgency: 8/10, Importance: 9/10
- Score = (100 - 50) + (8*15) + (9*12)
- Score = 50 + 120 + 108 = **278**

### Data Structure

```c
typedef struct {
    int id;                    // Unique ID
    char title[100];           // Event name
    char category[30];         // Type of event
    char location[100];        // Where
    int deadline;              // Days
    int urgency;               // 1-10
    int importance;            // 1-10
    int guests;                // Count
    float budget;              // Money
    int priority_score;        // Calculated
    int status;                // 0=Pending, 1=Progress, 2=Done
    int created_day;           // Timestamp
} Event;
```

---

## 🔌 API Endpoints Reference

### 1. GET `/`
**Returns**: index.html frontend page

### 2. POST `/api/events/add`
**Request**:
```json
{
    "title": "Conference 2024",
    "category": "Conference",
    "location": "New York Convention Center",
    "deadline": 7,
    "urgency": 8,
    "importance": 9,
    "guests": 250,
    "budget": 5000.00
}
```
**Response**: `{"success": true, "message": "Event added successfully"}`

### 3. GET `/api/events/all`
**Returns**: All events as JSON array
```json
{
    "events": [
        {
            "id": 1,
            "title": "Conference 2024",
            "category": "Conference",
            "deadline": 7,
            "urgency": 8,
            "importance": 9,
            "priority_score": 345,
            "status": 0,
            "budget": 5000.00
        }
    ]
}
```

### 4. POST `/api/events/delete`
**Request**: `{"event_id": 1}`
**Response**: `{"success": true, "message": "Event 1 deleted"}`

### 5. GET `/api/events/schedule`
**Returns**: Events sorted by priority score
```json
{
    "schedule": [
        {
            "id": 1,
            "title": "Project Submission",
            "priority_score": 278,
            "position": 1,
            "deadline": 5
        }
    ]
}
```

### 6. GET `/api/analytics`
**Returns**: System statistics
```json
{
    "total_events": 5,
    "total_budget": 15000.00,
    "total_guests": 500,
    "completed": 2,
    "pending": 3,
    "avg_importance": 7.5
}
```

### 7. POST `/api/events/status`
**Request**: `{"event_id": 1, "status": 1}`
**Response**: `{"success": true, "message": "Status updated to In Progress"}`

### 8. GET `/api/events/search`
**Query**: `/api/events/search?q=conference`
**Returns**: Matching events array

### 9. GET `/api/health`
**Returns**: Server status and engine info

---

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
**Solution**:
```bash
pip install flask flask-cors
```

### Error: "engine.dll not found"
**Solution**:
1. Make sure `engine.dll` is in the same folder as `app.py`
2. Check if it's actually compiled correctly
3. Try recompiling with Visual Studio or MinGW

### Port 5000 already in use
**Solution**:
```bash
# Edit app.py, change last line:
# app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001 instead
```

### "Failed to load engine.dll" on startup
**Possible Causes**:
1. Missing Visual C++ Redistributable
2. engine.dll is 32-bit but Python is 64-bit (or vice versa)
3. engine.dll is corrupted

**Solution**:
- Install Visual C++ Redistributable from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Recompile engine.dll to match Python bitness
- Verify Python: `python -c "import struct; print(struct.calcsize('P') * 8)"`

### Events not appearing in dashboard
1. Check browser console (F12 → Console) for errors
2. Check Flask server output for errors
3. Try refreshing the page (Ctrl+F5)
4. Check if server is running: http://localhost:5000/api/health

---

## 📝 Viva Questions & Answers

### Q1: What is the advantage of using C for backend?
**A**: C provides:
- **Performance**: Compiled code runs much faster than Python
- **Memory Efficiency**: Uses less RAM for the same operations
- **Real-time Processing**: Can handle thousands of events quickly
- **Reliability**: Low-level control prevents crashes

### Q2: Why use Flask as middleware?
**A**:
- **API Interface**: Provides HTTP endpoints for web access
- **Data Validation**: Checks user input before sending to C
- **Cross-Platform**: Works on Windows, Mac, Linux
- **Easy Integration**: Simple to connect C code with ctypes
- **Scalability**: Can handle multiple simultaneous requests

### Q3: How does the priority calculation work?
**A**: 
Priority Score = (100 - Deadline×10) + (Urgency×15) + (Importance×12)
- Lower deadline = Higher priority (urgent)
- Higher urgency = Higher priority
- Higher importance = Higher priority
- Deadlines within 3 days get doubled weight

### Q4: What happens when you sort events?
**A**: Uses bubble sort algorithm (O(n²)):
1. Compares adjacent events by priority score
2. Swaps if order is wrong
3. Repeats until fully sorted
4. Returns optimally ordered schedule

### Q5: How are events stored?
**A**: 
- In-memory array in C: `Event events[MAX_EVENTS]` (100 max)
- Resets when server restarts (no database)
- Fast access: O(1) for direct ID lookup, O(n) for search

### Q6: Can you add different event types?
**A**: Yes! In `index.html`, modify the category select:
```html
<option value="Meeting">Meeting</option>
<option value="Custom Event">Custom Event</option>
```

### Q7: How to add persistence (database)?
**A**: In `app.py`, replace in-memory storage with:
- SQLite: `import sqlite3`
- PostgreSQL: `import psycopg2`
- MongoDB: `import pymongo`

### Q8: What is ctypes?
**A**: Python library that:
- Allows calling C functions from Python
- Handles type conversions (Python → C → Python)
- Manages memory passing between languages
- `ctypes.CDLL()` loads DLL, `c_int`, `c_char_p` define types

### Q9: How to modify the algorithm?
**A**: Edit `calculate_priority_score()` in `engine.c`:
```c
// Example: Give more weight to urgency
int urgency_weight = urgency * 25;  // Was 15
```
Then recompile and replace `engine.dll`.

### Q10: Can this handle real-world usage?
**A**: 
- **Current Capacity**: 100 events maximum
- **For Production**:
  - Increase `MAX_EVENTS` in engine.c
  - Add database for persistence
  - Use proper authentication (Flask-Login)
  - Deploy on cloud server (Heroku, AWS, Azure)
  - Add more event properties (categories, tags, etc)

---

## 🎓 Learning Resources

### C Programming
- Arrays and Structures: Used for event storage
- Pointers and Memory: How ctypes transfers data
- Functions: Modular backend logic
- Sorting Algorithms: Optimization techniques

### Python & Flask
- Decorators: `@app.route()` for endpoints
- JSON: Data format for API
- Context Manager: Resource handling
- Modules: Importing libraries (ctypes, flask)

### Web Technologies
- HTML/CSS: UI structure and styling
- JavaScript: Frontend interactivity
- Fetch API: AJAX requests to backend
- DOM Manipulation: Dynamic content updates

---

## 📞 Support

If you encounter issues:

1. **Check Error Messages**: Read console output carefully
2. **Google the Error**: Usually someone has solved it
3. **Verify Installation**: Reinstall Python and packages
4. **Ask for Help**: Show your error to someone technical
5. **Read Documentation**: https://flask.palletsprojects.com/

---

## 🏆 Project Features

✅ Professional UI with dark theme and gradients
✅ Real-time analytics dashboard
✅ Smart event scheduling algorithm
✅ Full CRUD operations (Create, Read, Update, Delete)
✅ Search functionality
✅ Responsive design (works on mobile too)
✅ Event status tracking
✅ Budget management
✅ Guest count tracking
✅ Event categorization
✅ Clean, commented code
✅ Production-ready architecture

---

**Built with ❤️ for your college project presentation**
