# Smart Event Management System - Complete Setup Guide

##Project Overview

A professional event management system built with three technologies:
- **C Language**: High-performance backend with smart scheduling algorithm
- **Python Flask**: API server connecting frontend to C backend
- **HTML/CSS/JavaScript**: Modern, responsive web interface

---

## Installation Steps

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

## Running the Project

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

## How to Use

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

## C Code Explanation

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
