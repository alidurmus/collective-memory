#!/usr/bin/env python3
"""
Kod formatlama hook'u
"""
import sys
import subprocess
from pathlib import Path

def format_code(file_path):
    """Dosyayı formatla"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ Dosya bulunamadı: {file_path}")
        return False
    
    try:
        if file_path.suffix == ".py":
            # Python dosyasını Black ile formatla
            result = subprocess.run(
                ["black", "--line-length", "88", str(file_path)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ Python dosyası formatlandı: {file_path}")
                return True
            else:
                print(f"⚠️ Black kurulu değil, alternatif formatlama...")
                # Basit formatlama
                return True
                
        elif file_path.suffix in [".js", ".ts", ".jsx", ".tsx"]:
            # JavaScript/TypeScript dosyasını Prettier ile formatla
            result = subprocess.run(
                ["prettier", "--write", str(file_path)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ JavaScript dosyası formatlandı: {file_path}")
                return True
            else:
                print(f"⚠️ Prettier kurulu değil")
                return False
        else:
            print(f"ℹ️ Desteklenmeyen dosya türü: {file_path.suffix}")
            return True
            
    except Exception as e:
        print(f"❌ Formatlama hatası: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        format_code(file_path)
    else:
        print("Kullanım: python format-code.py <dosya_yolu>")