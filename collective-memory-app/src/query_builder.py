#!/usr/bin/env python3
"""
Query Builder - Yapılandırılmış sorgu oluşturma ve panoya kopyalama modülü
"""

import pyperclip
from typing import Dict, Any, List
from datetime import datetime, timezone


class QueryBuilder:
    """Sorgu oluşturma ve panoya kopyalama sınıfı"""

    def __init__(self):
        self.query_templates = {
            "structured_prompt": self._build_structured_prompt,
            "simple_prompt": self._build_simple_prompt,
            "context_aware_prompt": self._build_context_aware_prompt,
        }

    def build_query(
        self, context_data: Dict[str, Any], template_type: str = "structured_prompt"
    ) -> str:
        """Bağlam verilerinden yapılandırılmış sorgu oluştur"""
        if template_type not in self.query_templates:
            template_type = "structured_prompt"

        return self.query_templates[template_type](context_data)

    def _build_structured_prompt(self, context_data: Dict[str, Any]) -> str:
        """Yapılandırılmış prompt oluştur"""
        query_parts = []

        # Başlık
        query_parts.append("# 🧠 Collective Memory - Akıllı Bağlam")
        query_parts.append(f"**Proje:** {context_data.get('project_path', 'Unknown')}")
        query_parts.append(f"**Zaman:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
        query_parts.append(
            f"**İstek:** {context_data.get('user_request', 'Genel bağlam')}"
        )
        query_parts.append("")

        # Proje Kuralları
        if context_data["sources"]["rules"]["found"]:
            query_parts.append("## 📜 Proje Kuralları")
            query_parts.append("**Bu kurallara kesinlikle uymalısın:**")
            query_parts.append("")

            for rule in context_data["sources"]["rules"]["rules"]:
                query_parts.append(f"### {rule['name']}")
                query_parts.append(f"```")
                query_parts.append(rule["content"])
                query_parts.append(f"```")
                query_parts.append("")

        # Geçmiş Sohbetler
        if context_data["sources"]["chats"]["found"]:
            query_parts.append("## 💬 Geçmiş Sohbet Bağlamı")
            query_parts.append("**Bu proje hakkında daha önce konuştuklarımız:**")
            query_parts.append("")

            for i, chat in enumerate(context_data["sources"]["chats"]["chats"][:3]):
                query_parts.append(f"### Sohbet {i+1}")
                if "summary" in chat:
                    query_parts.append(chat["summary"])
                query_parts.append("")

        # Proje Dokümantasyonu
        if context_data["sources"]["docs"]["found"]:
            query_parts.append("## 📚 Proje Dokümantasyonu")
            query_parts.append("**İlgili dokümanlar:**")
            query_parts.append("")

            for doc in context_data["sources"]["docs"]["docs"][:5]:
                query_parts.append(f"### {doc['name']}")
                query_parts.append(f"```")
                query_parts.append(doc["content"][:800])  # İlk 800 karakter
                query_parts.append(f"```")
                query_parts.append("")

        # Görev Talimatları
        query_parts.append("## 🎯 Görev")
        query_parts.append(
            f"**Ana İstek:** {context_data.get('user_request', 'Genel bağlam')}"
        )
        query_parts.append("")
        query_parts.append("**Lütfen:**")
        query_parts.append("- Yukarıdaki kuralları kesinlikle uygula")
        query_parts.append("- Geçmiş sohbetlerden edindiğin bilgileri dikkate al")
        query_parts.append("- Proje dokümantasyonuna uygun öneriler sun")
        query_parts.append("- Kodlama standartlarını koru")
        query_parts.append("- Türkçe kullanıcı arayüzü, İngilizce kod")
        query_parts.append("")

        return "\n".join(query_parts)

    def _build_simple_prompt(self, context_data: Dict[str, Any]) -> str:
        """Basit prompt oluştur"""
        query_parts = []

        query_parts.append(f"Proje: {context_data.get('project_path', 'Unknown')}")
        query_parts.append(f"İstek: {context_data.get('user_request', 'Genel bağlam')}")
        query_parts.append("")

        # Kurallar
        if context_data["sources"]["rules"]["found"]:
            query_parts.append("Kurallar:")
            for rule in context_data["sources"]["rules"]["rules"]:
                query_parts.append(f"- {rule['content'][:200]}...")
            query_parts.append("")

        # Sohbet özeti
        if context_data["sources"]["chats"]["found"]:
            query_parts.append("Geçmiş sohbetler:")
            query_parts.append(context_data["sources"]["chats"]["summary"])
            query_parts.append("")

        return "\n".join(query_parts)

    def _build_context_aware_prompt(self, context_data: Dict[str, Any]) -> str:
        """Bağlam-bilinçli prompt oluştur"""
        query_parts = []

        # Özet başlangıç
        query_parts.append("# Context-Aware Development Request")
        query_parts.append("")

        # Proje özeti
        project_name = context_data.get("project_path", "").split("/")[-1]
        query_parts.append(f"**Project:** {project_name}")
        query_parts.append(
            f"**Request:** {context_data.get('user_request', 'General context')}"
        )
        query_parts.append("")

        # Mevcut bağlam bilgisi
        context_summary = self._get_context_summary(context_data)
        query_parts.append(f"**Available Context:** {context_summary}")
        query_parts.append("")

        # Koşullu içerik ekleme
        if context_data["sources"]["rules"]["found"]:
            query_parts.append("**Project Rules Active** ✅")

        if context_data["sources"]["chats"]["found"]:
            query_parts.append("**Chat History Available** ✅")

        if context_data["sources"]["docs"]["found"]:
            query_parts.append("**Documentation Available** ✅")

        query_parts.append("")
        query_parts.append("Please provide a solution considering the above context.")

        return "\n".join(query_parts)

    def _get_context_summary(self, context_data: Dict[str, Any]) -> str:
        """Bağlam özetini al"""
        summary_parts = []

        if context_data["sources"]["rules"]["found"]:
            rules_count = len(context_data["sources"]["rules"]["rules"])
            summary_parts.append(f"{rules_count} rules")

        if context_data["sources"]["chats"]["found"]:
            chats_count = len(context_data["sources"]["chats"]["chats"])
            summary_parts.append(f"{chats_count} chats")

        if context_data["sources"]["docs"]["found"]:
            docs_count = len(context_data["sources"]["docs"]["docs"])
            summary_parts.append(f"{docs_count} docs")

        return ", ".join(summary_parts) if summary_parts else "No context"

    def copy_to_clipboard(self, query: str) -> bool:
        """Sorguyu panoya kopyala"""
        try:
            pyperclip.copy(query)
            return True
        except Exception as e:
            print(f"Panoya kopyalama hatası: {e}")
            return False

    def save_to_file(self, query: str, filename: str = None) -> bool:
        """Sorguyu dosyaya kaydet"""
        if not filename:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"collective_memory_query_{timestamp}.md"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(query)
            return True
        except Exception as e:
            print(f"Dosya kaydetme hatası: {e}")
            return False

    def get_query_stats(self, query: str) -> Dict[str, Any]:
        """Sorgu istatistiklerini al"""
        lines = query.split("\n")
        words = query.split()

        return {
            "total_chars": len(query),
            "total_words": len(words),
            "total_lines": len(lines),
            "estimated_tokens": len(words) * 1.3,  # Yaklaşık token sayısı
            "sections": query.count("##"),
            "code_blocks": query.count("```") // 2,
        }

    def preview_query(self, query: str, max_lines: int = 20) -> str:
        """Sorgu önizlemesi"""
        lines = query.split("\n")

        if len(lines) <= max_lines:
            return query

        preview_lines = lines[:max_lines]
        remaining = len(lines) - max_lines

        preview_lines.append(f"\n... ({remaining} satır daha)")

        return "\n".join(preview_lines)
