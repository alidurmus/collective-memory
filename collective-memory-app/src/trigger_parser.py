#!/usr/bin/env python3
"""
Trigger Parser - Yorum satırı tetikleyici sistemi modülü
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class TriggerParser:
    """Yorum satırı tetikleyici sistemi sınıfı"""

    def __init__(self):
        # Desteklenen dosya uzantıları ve yorum karakterleri
        self.comment_patterns = {
            ".py": r"#\s*@collect-memory:\s*(.+)",
            ".js": r"//\s*@collect-memory:\s*(.+)",
            ".ts": r"//\s*@collect-memory:\s*(.+)",
            ".jsx": r"//\s*@collect-memory:\s*(.+)",
            ".tsx": r"//\s*@collect-memory:\s*(.+)",
            ".java": r"//\s*@collect-memory:\s*(.+)",
            ".cpp": r"//\s*@collect-memory:\s*(.+)",
            ".c": r"//\s*@collect-memory:\s*(.+)",
            ".h": r"//\s*@collect-memory:\s*(.+)",
            ".php": r"//\s*@collect-memory:\s*(.+)",
            ".rb": r"#\s*@collect-memory:\s*(.+)",
            ".go": r"//\s*@collect-memory:\s*(.+)",
            ".rs": r"//\s*@collect-memory:\s*(.+)",
            ".swift": r"//\s*@collect-memory:\s*(.+)",
            ".kt": r"//\s*@collect-memory:\s*(.+)",
            ".scala": r"//\s*@collect-memory:\s*(.+)",
            ".sh": r"#\s*@collect-memory:\s*(.+)",
            ".bash": r"#\s*@collect-memory:\s*(.+)",
            ".zsh": r"#\s*@collect-memory:\s*(.+)",
            ".sql": r"--\s*@collect-memory:\s*(.+)",
            ".css": r"/\*\s*@collect-memory:\s*(.+)\s*\*/",
            ".html": r"<!--\s*@collect-memory:\s*(.+)\s*-->",
            ".xml": r"<!--\s*@collect-memory:\s*(.+)\s*-->",
            ".yml": r"#\s*@collect-memory:\s*(.+)",
            ".yaml": r"#\s*@collect-memory:\s*(.+)",
            ".json": r"//\s*@collect-memory:\s*(.+)",  # JSON5 style
            ".md": r"<!--\s*@collect-memory:\s*(.+)\s*-->",
            ".rst": r"..\s*@collect-memory:\s*(.+)",
            ".tex": r"%\s*@collect-memory:\s*(.+)",
            ".r": r"#\s*@collect-memory:\s*(.+)",
            ".m": r"%\s*@collect-memory:\s*(.+)",  # MATLAB
            ".lua": r"--\s*@collect-memory:\s*(.+)",
            ".pl": r"#\s*@collect-memory:\s*(.+)",  # Perl
            ".vim": r'"\s*@collect-memory:\s*(.+)',
            ".dockerfile": r"#\s*@collect-memory:\s*(.+)",
        }

        # Arama yapılacak dosya uzantıları
        self.searchable_extensions = set(self.comment_patterns.keys())

    def find_trigger_in_project(self, project_path: Path) -> Optional[Dict[str, Any]]:
        """Proje içinde @collect-memory tetikleyicisini bul"""

        for file_path in project_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.searchable_extensions:
                trigger_data = self.find_trigger_in_file(file_path)
                if trigger_data:
                    return trigger_data

        return None

    def find_trigger_in_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Dosya içinde @collect-memory tetikleyicisini bul"""

        file_extension = file_path.suffix.lower()
        if file_extension not in self.comment_patterns:
            return None

        pattern = self.comment_patterns[file_extension]

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Regex ile tetikleyiciyi ara
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)

            for match in matches:
                request_text = match.group(1).strip()
                if request_text:
                    # Satır numarasını bul
                    line_number = content[: match.start()].count("\n") + 1

                    return {
                        "found": True,
                        "request": request_text,
                        "file_path": str(file_path),
                        "line_number": line_number,
                        "full_match": match.group(0),
                        "file_extension": file_extension,
                        "timestamp": file_path.stat().st_mtime,
                    }

        except Exception as e:
            print(f"Dosya okuma hatası {file_path}: {e}")

        return None

    def find_all_triggers_in_project(self, project_path: Path) -> List[Dict[str, Any]]:
        """Proje içindeki tüm @collect-memory tetikleyicilerini bul"""

        triggers = []

        for file_path in project_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.searchable_extensions:
                trigger_data = self.find_trigger_in_file(file_path)
                if trigger_data:
                    triggers.append(trigger_data)

        # Zaman damgasına göre sırala (en yeni önce)
        triggers.sort(key=lambda x: x["timestamp"], reverse=True)

        return triggers

    def validate_trigger_syntax(self, trigger_text: str) -> Dict[str, Any]:
        """Tetikleyici sözdizimini doğrula"""

        validation_result = {"valid": True, "warnings": [], "suggestions": []}

        # Boş istek kontrolü
        if not trigger_text.strip():
            validation_result["valid"] = False
            validation_result["warnings"].append("Boş istek metni")
            return validation_result

        # Çok kısa istek kontrolü
        if len(trigger_text.strip()) < 5:
            validation_result["warnings"].append("Çok kısa istek metni")
            validation_result["suggestions"].append("Daha açıklayıcı bir istek yazın")

        # Çok uzun istek kontrolü
        if len(trigger_text) > 200:
            validation_result["warnings"].append("Çok uzun istek metni")
            validation_result["suggestions"].append("İsteği daha kısa ve öz tutun")

        # Özel karakter kontrolü
        if any(char in trigger_text for char in ["<", ">", "|", "&"]):
            validation_result["warnings"].append("Özel karakterler tespit edildi")
            validation_result["suggestions"].append(
                "Özel karakterleri kullanmaktan kaçının"
            )

        return validation_result

    def extract_request_keywords(self, request_text: str) -> List[str]:
        """İstek metninden anahtar kelimeleri çıkar"""

        # Yaygın bağlayıcı kelimeleri çıkar
        stopwords = {
            "ve",
            "veya",
            "ile",
            "için",
            "bir",
            "bu",
            "şu",
            "o",
            "da",
            "de",
            "ta",
            "te",
            "dan",
            "den",
            "tan",
            "ten",
            "a",
            "e",
            "i",
            "in",
            "on",
            "and",
            "or",
            "with",
            "for",
            "a",
            "an",
            "the",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "can",
            "to",
        }

        # Kelimeleri ayır ve temizle
        words = re.findall(r"\b\w+\b", request_text.lower())
        keywords = [word for word in words if word not in stopwords and len(word) > 2]

        return keywords

    def suggest_similar_requests(
        self, current_request: str, previous_requests: List[str]
    ) -> List[str]:
        """Benzer istekleri öner"""

        current_keywords = set(self.extract_request_keywords(current_request))
        similar_requests = []

        for prev_request in previous_requests:
            prev_keywords = set(self.extract_request_keywords(prev_request))

            # Jaccard benzerliği
            intersection = current_keywords.intersection(prev_keywords)
            union = current_keywords.union(prev_keywords)

            if union and len(intersection) / len(union) > 0.3:  # %30 benzerlik
                similar_requests.append(prev_request)

        return similar_requests

    def remove_trigger_from_file(self, file_path: Path, line_number: int) -> bool:
        """Dosyadan tetikleyici yorumu kaldır"""

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if 1 <= line_number <= len(lines):
                # Satırı kaldır
                lines.pop(line_number - 1)

                # Dosyayı yeniden yaz
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)

                return True

        except Exception as e:
            print(f"Tetikleyici kaldırma hatası: {e}")

        return False

    def get_supported_extensions(self) -> List[str]:
        """Desteklenen dosya uzantılarını al"""
        return sorted(list(self.searchable_extensions))

    def get_comment_syntax_for_extension(self, extension: str) -> str:
        """Dosya uzantısı için yorum sözdizimini al"""

        # Örnek yorum formatları
        examples = {
            ".py": "# @collect-memory: Your request here",
            ".js": "// @collect-memory: Your request here",
            ".ts": "// @collect-memory: Your request here",
            ".java": "// @collect-memory: Your request here",
            ".html": "<!-- @collect-memory: Your request here -->",
            ".css": "/* @collect-memory: Your request here */",
            ".sql": "-- @collect-memory: Your request here",
            ".yml": "# @collect-memory: Your request here",
            ".md": "<!-- @collect-memory: Your request here -->",
        }

        return examples.get(extension, f"# @collect-memory: Your request here")

    def get_usage_statistics(self, project_path: Path) -> Dict[str, Any]:
        """Kullanım istatistiklerini al"""

        all_triggers = self.find_all_triggers_in_project(project_path)

        stats = {
            "total_triggers": len(all_triggers),
            "files_with_triggers": len(set(t["file_path"] for t in all_triggers)),
            "most_used_extensions": {},
            "recent_requests": [t["request"] for t in all_triggers[:5]],
            "average_request_length": 0,
        }

        if all_triggers:
            # Uzantı istatistikleri
            extension_counts = {}
            total_length = 0

            for trigger in all_triggers:
                ext = trigger["file_extension"]
                extension_counts[ext] = extension_counts.get(ext, 0) + 1
                total_length += len(trigger["request"])

            stats["most_used_extensions"] = extension_counts
            stats["average_request_length"] = total_length / len(all_triggers)

        return stats
