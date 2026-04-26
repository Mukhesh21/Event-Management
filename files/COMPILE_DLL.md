# How to Compile engine.c to engine.dll

## Option 1: Visual Studio (RECOMMENDED) ⭐

### Why Visual Studio?
- Professional IDE
- Best compiler optimization
- Easy debugging
- Most reliable results

### Step-by-Step Instructions

#### 1. Install Visual Studio Community

1. Go to: https://visualstudio.microsoft.com/vs/community/
2. Download "Visual Studio Community 2022"
3. Run the installer
4. Select **"Desktop development with C++"**
5. Click Install (this will take 10-15 minutes)
6. Restart your computer

#### 2. Create New DLL Project

1. Open Visual Studio
2. File → New → Project
3. Search for "DLL" in the search box
4. Select **"Dynamic-Link Library (DLL)"**
5. Choose location and project name: `EventManagement`
6. Click Create

#### 3. Add engine.c

1. Right-click on "Source Files" in Solution Explorer
2. Select "Add → Existing Item"
3. Find and select `engine.c`
4. Click Add

#### 4. Delete Default Files

You'll see these files created by default:
- `pch.cpp`
- `pch.h`
- `dllmain.cpp`

Right-click each and Delete them (not needed for our code).

#### 5. Configure Project Settings

1. Right-click Project → Properties
2. Go to: Configuration Properties → C/C++ → Precompiled Headers
3. Change "Precompiled Header" to "Not Using Precompiled Headers"
4. Click OK

#### 6. Build the DLL

1. Select menu: Build → Configuration Manager
2. Set Configuration to: **Release** (not Debug)
3. Platform: **x64** (for 64-bit Python)
4. Click OK
5. Press Ctrl+Shift+B to build
6. You should see: "Build: 1 succeeded"

#### 7. Find engine.dll

The compiled file is at:
```
C:\Users\YourUsername\source\repos\EventManagement\x64\Release\engine.dll
```

1. Copy this file
2. Paste it in your project folder (same as app.py)

**Done!** You now have `engine.dll` 🎉

---

## Option 2: MinGW (Command Line)

### Why MinGW?
- Lightweight (~100 MB)
- No bloat
- Good for quick compilation

### Installation Steps

#### 1. Download MinGW

1. Go to: https://www.mingw-w64.org/
2. Click "Downloads"
3. Download **"x86_64-w64-mingw32-gcc"** (for 64-bit)
4. Run installer
5. Keep default settings
6. Choose Installation Folder: `C:\mingw-w64`
7. Click Install

#### 2. Add MinGW to PATH

1. Open "Edit environment variables"
2. Search in Start Menu: "environment"
3. Click "Edit the system environment variables"
4. Click "Environment Variables..." button
5. Under "System variables", find "Path"
6. Click Edit
7. Click "New"
8. Add: `C:\mingw-w64\bin`
9. Click OK three times

#### 3. Verify Installation

Open Command Prompt and type:
```bash
gcc --version
```

Should show version number (like 13.1.0).

#### 4. Compile engine.c to DLL

Open Command Prompt in your project folder and run:

```bash
gcc -shared -o engine.dll engine.c
```

This creates `engine.dll` in same folder. Done! 🎉

---

## Option 3: Using Pre-Compiled Binary

If you don't want to compile yourself:

1. **Find a Windows machine with Visual Studio** (school computer lab?)
2. **Ask your professor or classmate** who has compiled version
3. **Download from online** (if available)
4. **Place engine.dll** in your project folder
5. **Run app.py**

---

## Verify DLL Works

After compiling, test if it works:

### Test 1: Check File Exists

```bash
dir engine.dll
```

Should show: `engine.dll` with a file size (should be 10-50 KB)

### Test 2: Test in Python

Create a test script `test_dll.py`:

```python
import ctypes

try:
    lib = ctypes.CDLL("./engine.dll")
    print("✓ DLL loaded successfully!")
    
    # Test add_event function
    lib.add_event.argtypes = [ctypes.c_char_p, ctypes.c_char_p, 
                              ctypes.c_char_p, ctypes.c_int, 
                              ctypes.c_int, ctypes.c_int, 
                              ctypes.c_int, ctypes.c_float]
    lib.add_event.restype = ctypes.c_int
    
    result = lib.add_event(b"Test Event", b"Meeting", b"Office", 5, 8, 7, 10, 100.0)
    
    if result == 1:
        print("✓ add_event() works!")
    else:
        print("✗ add_event() failed")
        
except Exception as e:
    print(f"✗ Error: {e}")
```

Run it:
```bash
python test_dll.py
```

If you see "✓ DLL loaded successfully!" it works!

---

## Troubleshooting Compilation

### Error: "gcc: command not found"

**Solution**: MinGW not installed or not in PATH
- Reinstall MinGW
- Add `C:\mingw-w64\bin` to PATH
- Restart Command Prompt

### Error: "MSVCRT.dll not found"

**Solution**: Missing Visual C++ Redistributable
- Download from: https://support.microsoft.com/en-us/help/2977003
- Run installer
- Choose: **Visual C++ 2022 Redistributable**
- Restart

### Error: "Cannot open file"

**Solution**: File permissions issue
- Run Command Prompt as Administrator
- Make sure you're in correct folder

### Error: "Windows cannot find engine.dll"

**Solution**: DLL not in right location
- Copy engine.dll to same folder as app.py
- Check with: `dir engine.dll`

### Error: "The specified module could not be found"

**Solution**: 32-bit vs 64-bit mismatch
- Check Python bitness: `python -c "import struct; print(struct.calcsize('P') * 8)"`
- Compile matching version:
  - For 64-bit Python: use x64 build
  - For 32-bit Python: use x86 build

---

## DLL Bitness Compatibility

**Important**: Your DLL and Python must match!

### Check Your Python Version

```bash
python -c "import struct; print(struct.calcsize('P') * 8)"
```

Output: `64` or `32`

### Compile Matching DLL

#### Visual Studio:
1. Configuration Manager
2. Set Platform to: **x64** (for 64-bit) or **Win32** (for 32-bit)
3. Build

#### MinGW:
```bash
# For 64-bit (default)
gcc -shared -o engine.dll engine.c

# For 32-bit
i686-w64-mingw32-gcc -shared -o engine.dll engine.c
```

---

## Build Using Batch File

Create `compile.bat` to automate compilation:

```batch
@echo off
echo Compiling engine.c to engine.dll...
gcc -shared -o engine.dll engine.c
if errorlevel 1 (
    echo Compilation failed!
    pause
    exit /b 1
)
echo Success! engine.dll created.
pause
```

Double-click `compile.bat` to compile automatically.

---

## What's in engine.dll?

The compiled DLL contains these functions:

```c
int add_event(char title[], char category[], char location[], 
              int deadline, int urgency, int importance, int guests, float budget)

int delete_event(int event_id)

void get_all_events(char *result, int max_len)

void generate_schedule(char *result, int max_len)

void get_analytics(char *result, int max_len)

int update_event_status(int event_id, int new_status)

void search_events(char *query, char *result, int max_len)
```

All these are called from Python via ctypes in `app.py`.

---

## DLL File Size Reference

Typical sizes:
- **Debug build**: 200-500 KB (has debugging info)
- **Release build**: 10-50 KB (optimized)

Use **Release build** for smaller, faster DLL.

---

## If All Else Fails...

1. **Try online compiler**: https://www.onlinegdb.com/
2. **Ask on forums**: Stack Overflow, Reddit r/cpp
3. **Find pre-compiled**: Search GitHub for similar projects
4. **Use WSL2**: Windows Subsystem for Linux (advanced)

---

## Next Step

After getting `engine.dll`:

1. Place in project folder
2. Run `python app.py`
3. Go to `http://localhost:5000`
4. Start using the application!

---

**Questions? Read the troubleshooting section above or ask for help! 💪**
