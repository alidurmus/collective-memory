#!/usr/bin/env python3
"""
Agent Hooks Activation Script
Kiro IDE için hook'ları aktifleştiren script
"""

import json
import os
import sys
from pathlib import Path


def activate_hooks():
    """Hook'ları Kiro IDE'de aktifleştir"""

    print("🎣 Agent Hooks aktifleştiriliyor...")

    # Hook dosyalarının varlığını kontrol et
    hook_files = [
        ".kiro/hooks/hooks.json",
        ".kiro/hooks/manifest.json",
        ".kiro/hooks/hook-ui.json",
        ".kiro/hooks/status.json",
        ".kiro/hooks/scripts/hook-manager.py",
        ".kiro/hooks/scripts/test-runner.py",
    ]

    missing_files = []
    for file_path in hook_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Eksik dosyalar:")
        for file in missing_files:
            print(f"  - {file}")
        return False

    # Extension konfigürasyonunu kontrol et
    extensions_file = Path(".kiro/extensions.json")
    if extensions_file.exists():
        try:
            with open(extensions_file, "r", encoding="utf-8") as f:
                extensions = json.load(f)

            # Agent hooks extension'ının varlığını kontrol et
            hook_extension = None
            for ext in extensions.get("extensions", []):
                if ext.get("id") == "collective-memory-agent-hooks":
                    hook_extension = ext
                    break

            if hook_extension:
                print("✅ Agent Hooks extension konfigürasyonu bulundu")
                print(
                    f"   - Durum: {'Aktif' if hook_extension.get('enabled') else 'Pasif'}"
                )
                print(
                    f"   - Otomatik başlatma: {'Evet' if hook_extension.get('auto_start') else 'Hayır'}"
                )
            else:
                print("⚠️ Agent Hooks extension konfigürasyonu bulunamadı")

        except Exception as e:
            print(f"❌ Extension konfigürasyonu okunamadı: {e}")

    # Hook konfigürasyonunu yükle ve doğrula
    try:
        with open(".kiro/hooks/hooks.json", "r", encoding="utf-8") as f:
            hooks_config = json.load(f)

        hooks = hooks_config.get("hooks", [])
        enabled_hooks = [h for h in hooks if h.get("enabled", True)]

        print(f"✅ Hook konfigürasyonu yüklendi")
        print(f"   - Toplam hook: {len(hooks)}")
        print(f"   - Aktif hook: {len(enabled_hooks)}")

        # Hook kategorilerini göster
        categories = {}
        for hook in enabled_hooks:
            trigger_type = hook["trigger"]["type"]
            if trigger_type not in categories:
                categories[trigger_type] = []
            categories[trigger_type].append(hook["name"])

        print("📋 Hook kategorileri:")
        for category, hook_names in categories.items():
            category_name = {
                "file_save": "Dosya Kaydedildiğinde",
                "scheduled": "Zamanlanmış",
                "manual": "Manuel",
            }.get(category, category)

            print(f"   - {category_name}: {len(hook_names)} hook")
            for name in hook_names[:3]:  # İlk 3'ünü göster
                print(f"     • {name}")
            if len(hook_names) > 3:
                print(f"     • ... ve {len(hook_names) - 3} tane daha")

    except Exception as e:
        print(f"❌ Hook konfigürasyonu okunamadı: {e}")
        return False

    # Status dosyasını güncelle
    try:
        status_data = {
            "manager_status": "activated",
            "last_updated": "2025-07-17T13:38:38.441577",
            "active_hooks": len(enabled_hooks),
            "total_hooks": len(hooks),
            "activation_successful": True,
        }

        with open(".kiro/hooks/status.json", "w", encoding="utf-8") as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)

        print("✅ Hook durumu güncellendi")

    except Exception as e:
        print(f"⚠️ Hook durumu güncellenemedi: {e}")

    print("\n🎉 Agent Hooks başarıyla aktifleştirildi!")
    print("\n📖 Kullanım:")
    print("   - Kiro IDE'de sağ panelde 'Agent Hooks' bölümünü kontrol edin")
    print(
        "   - Hook'ları başlatmak için: python .kiro/hooks/scripts/hook-manager.py start"
    )
    print(
        "   - Hook durumunu görmek için: python .kiro/hooks/scripts/hook-manager.py status"
    )

    return True


def main():
    """Ana fonksiyon"""
    if not activate_hooks():
        sys.exit(1)

    print("\n🚀 Hook Manager'ı başlatmak ister misiniz? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ["y", "yes", "evet", "e"]:
            print("\n🔄 Hook Manager başlatılıyor...")
            os.system("python .kiro/hooks/scripts/hook-manager.py start")
    except KeyboardInterrupt:
        print("\n👋 İptal edildi")


if __name__ == "__main__":
    main()
