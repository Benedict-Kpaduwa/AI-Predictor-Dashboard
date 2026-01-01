#!/usr/bin/env python3
"""
Test script to verify the Vercel deployment setup locally
"""

import sys
import os

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✓ FastAPI imported")
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False
    
    try:
        import pandas
        print("✓ Pandas imported")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import numpy
        print("✓ NumPy imported")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✓ Scikit-learn imported")
    except ImportError as e:
        print(f"✗ Scikit-learn import failed: {e}")
        return False
    
    try:
        import mangum
        print("✓ Mangum imported")
    except ImportError as e:
        print(f"✗ Mangum import failed: {e}")
        return False
    
    return True

def test_api_handler():
    """Test that the API handler can be imported"""
    print("\nTesting API handler...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        from api.index import handler
        print("✓ API handler imported successfully")
        return True
    except ImportError as e:
        print(f"✗ API handler import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ API handler error: {e}")
        return False

def test_main_app():
    """Test that the main FastAPI app can be imported"""
    print("\nTesting main FastAPI app...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        from main import app
        print("✓ FastAPI app imported successfully")
        print(f"  App title: {app.title}")
        print(f"  Routes: {len(app.routes)} routes registered")
        return True
    except ImportError as e:
        print(f"✗ FastAPI app import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ FastAPI app error: {e}")
        return False

def test_file_structure():
    """Test that required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'vercel.json',
        'requirements.txt',
        'api/index.py',
        'backend/main.py',
        'backend/ml_model.py',
        'backend/data_processor.py',
        'backend/pdf_generator.py',
        'frontend/package.json',
        'frontend/vite.config.ts',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("Vercel Deployment Setup Test")
    print("=" * 60)
    
    results = []
    
    # Test file structure
    results.append(("File Structure", test_file_structure()))
    
    # Test imports
    results.append(("Python Imports", test_imports()))
    
    # Test main app
    results.append(("FastAPI App", test_main_app()))
    
    # Test API handler
    results.append(("API Handler", test_api_handler()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! Ready for Vercel deployment.")
        print("\nNext steps:")
        print("1. Commit your changes: git add . && git commit -m 'Ready for Vercel'")
        print("2. Push to GitHub: git push origin main")
        print("3. Deploy on Vercel: https://vercel.com/new")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install dependencies: cd backend && pip install -r requirements.txt")
        print("- Ensure all required files exist")
        print("- Check file paths and imports")
        return 1

if __name__ == "__main__":
    sys.exit(main())

