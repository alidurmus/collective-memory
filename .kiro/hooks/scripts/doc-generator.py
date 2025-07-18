#!/usr/bin/env python3
"""
Dokümantasyon üretme hook'u
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

def generate_api_docs():
    """API dokümantasyonu üret"""
    print("📚 API dokümantasyonu üretiliyor...")
    
    # API dosyalarını bul
    api_files = []
    for pattern in ["**/api/**/*.py", "**/views/**/*.py"]:
        api_files.extend(Path(".").glob(pattern))
    
    if not api_files:
        print("ℹ️ API dosyası bulunamadı")
        return
    
    docs = {
        "timestamp": datetime.now().isoformat(),
        "api_files": [],
        "endpoints": []
    }
    
    for api_file in api_files:
        print(f"📄 İşleniyor: {api_file}")
        
        try:
            with open(api_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Basit endpoint tespiti
            endpoints = []
            lines = content.split("\n")
            
            for i, line in enumerate(lines):
                line = line.strip()
                if any(decorator in line for decorator in ["@app.route", "@bp.route", "def "]):
                    if "def " in line and "(" in line:
                        func_name = line.split("def ")[1].split("(")[0].strip()
                        endpoints.append({
                            "function": func_name,
                            "line": i + 1,
                            "file": str(api_file)
                        })
            
            docs["api_files"].append({
                "file": str(api_file),
                "endpoints": endpoints,
                "line_count": len(lines)
            })
            
            docs["endpoints"].extend(endpoints)
            
        except Exception as e:
            print(f"❌ Dosya işlenirken hata: {api_file} - {e}")
    
    # Dokümantasyonu kaydet
    docs_dir = Path("docs/api")
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON raporu
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = docs_dir / f"api_analysis_{timestamp}.json"
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)
    
    # Markdown raporu
    md_file = docs_dir / "API_ENDPOINTS.md"
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# API Endpoints\n\n")
        f.write(f"Son güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for api_file_info in docs["api_files"]:
            f.write(f"## {api_file_info['file']}\n\n")
            
            if api_file_info["endpoints"]:
                for endpoint in api_file_info["endpoints"]:
                    f.write(f"- `{endpoint['function']}()` (satır {endpoint['line']})\n")
            else:
                f.write("- Endpoint bulunamadı\n")
            
            f.write("\n")
    
    print(f"📋 API dokümantasyonu güncellendi:")
    print(f"  - JSON: {json_file}")
    print(f"  - Markdown: {md_file}")
    print(f"  - Toplam endpoint: {len(docs['endpoints'])}")

if __name__ == "__main__":
    generate_api_docs()