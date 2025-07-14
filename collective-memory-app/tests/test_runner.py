#!/usr/bin/env python3
"""
Collective Memory Test Runner
Tüm testleri çalıştırmak için ana script
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_api_server():
    """API server'ın çalışıp çalışmadığını kontrol et"""
    try:
        response = requests.get("http://localhost:5000/system/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_frontend_server():
    """Frontend server'ın çalışıp çalışmadığını kontrol et"""
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_backend_tests():
    """Backend testlerini çalıştır"""
    print("🔧 Backend API Testleri Çalıştırılıyor...")
    
    if not check_api_server():
        print("❌ API server çalışmıyor. Lütfen önce 'python api_server.py' komutunu çalıştırın.")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_api_endpoints.py", 
            "-v", "--tb=short"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Backend testleri başarılı!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Backend testleri başarısız!")
        print(e.stdout)
        print(e.stderr)
        return False

def run_frontend_tests():
    """Frontend UI testlerini çalıştır"""
    print("🌐 Frontend UI Testleri Çalıştırılıyor...")
    
    if not check_frontend_server():
        print("❌ Frontend server çalışmıyor. Lütfen önce 'npm run dev' komutunu çalıştırın.")
        return False
    
    try:
        # Frontend dizinine geç
        os.chdir("frontend")
        
        result = subprocess.run([
            "npx", "playwright", "test", 
            "--reporter=html"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Frontend testleri başarılı!")
        print(result.stdout)
        
        # Ana dizine geri dön
        os.chdir("..")
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Frontend testleri başarısız!")
        print(e.stdout)
        print(e.stderr)
        os.chdir("..")
        return False

def run_basic_tests():
    """Temel modül testlerini çalıştır"""
    print("⚙️ Temel Modül Testleri Çalıştırılıyor...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_basic.py", 
            "-v", "--tb=short"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Temel testler başarılı!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Temel testler başarısız!")
        print(e.stdout)
        print(e.stderr)
        return False

def install_playwright_browsers():
    """Playwright browser'ları yükle"""
    print("📦 Playwright Browser'ları Yükleniyor...")
    
    try:
        os.chdir("frontend")
        subprocess.run(["npx", "playwright", "install"], check=True)
        os.chdir("..")
        print("✅ Browser'lar başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Browser kurulumu başarısız!")
        os.chdir("..")
        return False

def main():
    """Ana test çalıştırıcı"""
    print("🚀 Collective Memory v2.1 Test Suite")
    print("=====================================")
    
    # Test arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Test type seçenekleri
    if "--help" in args or "-h" in args:
        print("""
Test Seçenekleri:
  --basic        : Sadece temel modül testleri
  --api          : Sadece API endpoint testleri
  --ui           : Sadece UI testleri
  --install      : Playwright browser'ları yükle
  --all          : Tüm testleri çalıştır (varsayılan)
  
Örnek kullanım:
  python test_runner.py --basic
  python test_runner.py --api
  python test_runner.py --ui
  python test_runner.py --all
        """)
        return
    
    # Browser kurulumu
    if "--install" in args:
        install_playwright_browsers()
        return
    
    results = []
    
    # Test türleri
    if "--basic" in args or "--all" in args or not args:
        results.append(("Basic", run_basic_tests()))
    
    if "--api" in args or "--all" in args or not args:
        results.append(("API", run_backend_tests()))
    
    if "--ui" in args or "--all" in args or not args:
        results.append(("UI", run_frontend_tests()))
    
    # Sonuçları özetle
    print("\n📊 Test Sonuçları")
    print("=================")
    
    all_passed = True
    for test_type, passed in results:
        status = "✅ BAŞARILI" if passed else "❌ BAŞARISIZ"
        print(f"{test_type} Testleri: {status}")
        if not passed:
            all_passed = False
    
    print(f"\n{'🎉 TÜM TESTLER BAŞARILI!' if all_passed else '⚠️ BAZI TESTLER BAŞARISIZ!'}")
    
    if not all_passed:
        print("\nBaşarısız testler için:")
        print("- API testleri: Sunucuların çalıştığından emin olun")
        print("- UI testleri: 'python test_runner.py --install' ile browser'ları kurun")
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main() 