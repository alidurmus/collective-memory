#!/usr/bin/env python3
"""
Collective Memory Error and Task Management System
Kullanıcı dostu komut sistemi
"""

import sys
import os

sys.path.append("./src")

from error_task_manager import ErrorTaskManager
from document_analyzer import DocumentAnalyzer
from colorama import init, Fore, Style

init()


def print_usage():
    """Kullanım talimatları"""
    print(
        f"\n{Fore.CYAN}🔧 Collective Memory - Hata ve Görev Yönetim Sistemi{Style.RESET_ALL}"
    )
    print("=" * 60)
    print(f"{Fore.YELLOW}KULLANIM:{Style.RESET_ALL}")
    print("  python error_manager.py [komut]")
    print()
    print(f"{Fore.GREEN}KOMUTLAR:{Style.RESET_ALL}")
    print("  hatalar          - Tüm hataları listele")
    print("  aktif-hatalar    - Sadece aktif hataları listele")
    print("  görevler         - Tüm görevleri listele")
    print("  bekleyen-görevler- Sadece bekleyen görevleri listele")
    print("  status           - Sistem durumu özeti")
    print("  analiz           - Dokümantasyon analizi çalıştır")
    print("  düzelt [error_id]- Hatayı düzeltildi olarak işaretle")
    print("  tamamla [task_id]- Görevi tamamlandı olarak işaretle")
    print()
    print(f"{Fore.BLUE}ÖRNEKLER:{Style.RESET_ALL}")
    print("  python error_manager.py status")
    print("  python error_manager.py hatalar")
    print("  python error_manager.py düzelt BACKEND_SERVER_DOWN")
    print("  python error_manager.py tamamla TASK_001")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    etm = ErrorTaskManager()

    if not etm.connect():
        print(f"{Fore.RED}❌ Veritabanı bağlantısı kurulamadı!{Style.RESET_ALL}")
        return

    try:
        if command == "hatalar":
            etm.list_errors_console()

        elif command == "aktif-hatalar":
            etm.list_errors_console("aktif")

        elif command == "görevler":
            etm.list_tasks_console()

        elif command == "bekleyen-görevler":
            etm.list_tasks_console("beklemede")

        elif command == "status":
            # Sistem durumunu göster
            active_errors = etm.get_errors("aktif")
            all_errors = etm.get_errors()
            pending_tasks = etm.get_tasks("beklemede")
            completed_tasks = etm.get_tasks("tamamlandı")

            print(f"\n{Fore.CYAN}📊 SİSTEM DURUMU{Style.RESET_ALL}")
            print("=" * 50)
            print(f"🔴 Aktif Hatalar: {len(active_errors)}")
            print(f"📋 Toplam Hatalar: {len(all_errors)}")
            print(f"⏳ Bekleyen Görevler: {len(pending_tasks)}")
            print(f"✅ Tamamlanan Görevler: {len(completed_tasks)}")

            if active_errors:
                print(f"\n{Fore.YELLOW}🔴 AKTİF HATALAR:{Style.RESET_ALL}")
                for error in active_errors[:10]:  # İlk 10 tanesi
                    print(f"• {error['error_code']}: {error['error_title']}")
                if len(active_errors) > 10:
                    print(f"  ... ve {len(active_errors) - 10} tane daha")

            if pending_tasks:
                print(f"\n{Fore.BLUE}⏳ BEKLEYEN GÖREVLER:{Style.RESET_ALL}")
                for task in pending_tasks[:10]:  # İlk 10 tanesi
                    print(f"• {task['task_code']}: {task['task_title']}")
                if len(pending_tasks) > 10:
                    print(f"  ... ve {len(pending_tasks) - 10} tane daha")

        elif command == "analiz":
            print(
                f"\n{Fore.CYAN}📚 Dokümantasyon Analizi Başlatılıyor...{Style.RESET_ALL}"
            )

            analyzer = DocumentAnalyzer()
            results = analyzer.analyze_all_docs(".")

            print(
                f"{Fore.YELLOW}📊 {len(results)} dosya analiz edildi{Style.RESET_ALL}"
            )

            save_stats = analyzer.save_analysis_to_db(etm, results)

            print(f"\n{Fore.GREEN}✅ KAYDETME İSTATİSTİKLERİ:{Style.RESET_ALL}")
            print(f"📄 Analiz edilen dosyalar: {save_stats['analyzed_files']}")
            print(f"🔴 Kaydedilen hatalar: {save_stats['saved_errors']}")
            print(f"📋 Kaydedilen görevler: {save_stats['saved_tasks']}")
            print(f"❌ Kaydetme hataları: {save_stats['failed_saves']}")

        elif command == "düzelt":
            if len(sys.argv) < 3:
                print(
                    f"{Fore.RED}❌ Hata ID'si gerekli! Örnek: python error_manager.py düzelt BACKEND_SERVER_DOWN{Style.RESET_ALL}"
                )
                return

            error_id = sys.argv[2]
            if etm.update_error_status(error_id, "düzeltildi"):
                print(
                    f"{Fore.GREEN}✅ Hata {error_id} düzeltildi olarak işaretlendi{Style.RESET_ALL}"
                )
            else:
                print(f"{Fore.RED}❌ Hata güncellenemedi: {error_id}{Style.RESET_ALL}")

        elif command == "tamamla":
            if len(sys.argv) < 3:
                print(
                    f"{Fore.RED}❌ Görev ID'si gerekli! Örnek: python error_manager.py tamamla TASK_001{Style.RESET_ALL}"
                )
                return

            task_id = sys.argv[2]
            if etm.update_task_status(task_id, "tamamlandı"):
                print(
                    f"{Fore.GREEN}✅ Görev {task_id} tamamlandı olarak işaretlendi{Style.RESET_ALL}"
                )
            else:
                print(f"{Fore.RED}❌ Görev güncellenemedi: {task_id}{Style.RESET_ALL}")

        else:
            print(f"{Fore.RED}❌ Bilinmeyen komut: {command}{Style.RESET_ALL}")
            print_usage()

    except Exception as e:
        print(f"{Fore.RED}❌ Hata oluştu: {str(e)}{Style.RESET_ALL}")
    finally:
        etm.close()


if __name__ == "__main__":
    main()
