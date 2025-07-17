@echo off
echo 🚀 Collective Memory Agent Hooks başlatılıyor...
echo.

REM Hook manager'ı arka planda başlat
start /B python .kiro/hooks/scripts/hook-manager.py start

echo ✅ Agent Hooks aktifleştirildi!
echo.
echo 📋 Aktif özellikler:
echo   - Otomatik test çalıştırma (dosya kaydedildiğinde)
echo   - Kod formatlama (Python/JavaScript)
echo   - Güvenlik taraması (dependency değişikliklerinde)
echo   - API dokümantasyon güncelleme
echo   - Veritabanı migration kontrolü
echo   - Sistem sağlık izleme
echo   - Otomatik temizlik
echo.
echo 🛑 Durdurmak için: Ctrl+C veya terminali kapatın
echo.

pause