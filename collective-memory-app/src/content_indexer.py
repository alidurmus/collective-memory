#!/usr/bin/env python3
"""
Content Indexer - Markdown dosyalarını parse etme ve indeksleme sistemi
Dosya içeriklerini analiz eder ve aranabilir hale getirir
"""

import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from colorama import init, Fore, Style
import logging

try:
    import markdown
    from markdown.extensions import codehilite, fenced_code, tables, toc
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

# Colorama initialize
init()

class ContentIndexer:
    """Markdown içerik indeksleme ve analiz sistemi"""
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'as', 'is', 'was', 'are', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            # Turkish stop words
            've', 'bir', 'bu', 'da', 'de', 'ile', 'o', 'için', 'var', 'olan',
            'den', 'dan', 'deki', 'nin', 'nın', 'nun', 'nün', 'si', 'sı', 'su',
            'şu', 'her', 'hiç', 'daha', 'çok', 'az', 'en', 'gibi', 'kadar'
        }
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Markdown processor
        if MARKDOWN_AVAILABLE:
            self.md = markdown.Markdown(
                extensions=['codehilite', 'fenced_code', 'tables', 'toc'],
                extension_configs={
                    'codehilite': {'css_class': 'highlight'},
                    'toc': {'permalink': True}
                }
            )
        else:
            self.md = None
            print(f"{Fore.YELLOW}⚠️  Markdown library not available. Using basic text parsing.{Style.RESET_ALL}")
            
    def extract_metadata(self, content: str) -> Dict:
        """Markdown dosyasından metadata çıkarır"""
        metadata = {
            'title': '',
            'headings': [],
            'code_blocks': [],
            'links': [],
            'images': [],
            'tables': [],
            'lists': [],
            'emphasis': [],
            'language': 'unknown'
        }
        
        lines = content.split('\n')
        
        # Başlık (ilk H1 veya dosya adı)
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
                break
                
        # Başlıkları çıkar
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level <= 6:  # H1-H6
                    heading_text = line[level:].strip()
                    metadata['headings'].append({
                        'level': level,
                        'text': heading_text,
                        'line': i + 1
                    })
                    
        # Code blocks
        in_code_block = False
        code_lang = ''
        code_content = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if in_code_block:
                    # Code block sonu
                    metadata['code_blocks'].append({
                        'language': code_lang,
                        'content': '\n'.join(code_content),
                        'line_start': i - len(code_content),
                        'line_end': i
                    })
                    in_code_block = False
                    code_content = []
                else:
                    # Code block başlangıcı
                    code_lang = line.strip()[3:].strip()
                    in_code_block = True
            elif in_code_block:
                code_content.append(line)
                
        # Links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        for i, line in enumerate(lines):
            for match in re.finditer(link_pattern, line):
                metadata['links'].append({
                    'text': match.group(1),
                    'url': match.group(2),
                    'line': i + 1
                })
                
        # Images ![alt](url)
        image_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        for i, line in enumerate(lines):
            for match in re.finditer(image_pattern, line):
                metadata['images'].append({
                    'alt': match.group(1),
                    'url': match.group(2),
                    'line': i + 1
                })
                
        # Tables (basit tespit)
        for i, line in enumerate(lines):
            if '|' in line and line.strip().startswith('|'):
                metadata['tables'].append({
                    'line': i + 1,
                    'content': line.strip()
                })
                
        # Lists
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('+ '):
                metadata['lists'].append({
                    'type': 'unordered',
                    'content': stripped[2:],
                    'line': i + 1
                })
            elif re.match(r'^\d+\.\s', stripped):
                metadata['lists'].append({
                    'type': 'ordered',
                    'content': re.sub(r'^\d+\.\s', '', stripped),
                    'line': i + 1
                })
                
        # Emphasis (bold, italic)
        emphasis_patterns = [
            (r'\*\*([^*]+)\*\*', 'bold'),
            (r'\*([^*]+)\*', 'italic'),
            (r'__([^_]+)__', 'bold'),
            (r'_([^_]+)_', 'italic')
        ]
        
        for i, line in enumerate(lines):
            for pattern, emp_type in emphasis_patterns:
                for match in re.finditer(pattern, line):
                    metadata['emphasis'].append({
                        'type': emp_type,
                        'text': match.group(1),
                        'line': i + 1
                    })
                    
        # Dil tespit etme (basit)
        turkish_words = ['ve', 'bir', 'bu', 'için', 'olan', 'ile', 'da', 'de']
        english_words = ['the', 'and', 'or', 'in', 'on', 'at', 'to', 'for']
        
        content_lower = content.lower()
        turkish_count = sum(1 for word in turkish_words if word in content_lower)
        english_count = sum(1 for word in english_words if word in content_lower)
        
        if turkish_count > english_count:
            metadata['language'] = 'turkish'
        elif english_count > turkish_count:
            metadata['language'] = 'english'
        else:
            metadata['language'] = 'mixed'
            
        return metadata
        
    def extract_keywords(self, content: str, min_length: int = 3, max_keywords: int = 100) -> List[Tuple[str, int]]:
        """İçerikten anahtar kelimeleri çıkarır"""
        
        # Markdown syntax'ını temizle
        clean_content = self._clean_markdown(content)
        
        # Kelimeleri ayır
        words = re.findall(r'\b[a-zA-ZçğıöşüÇĞIİÖŞÜ]{' + str(min_length) + ',}\b', clean_content.lower())
        
        # Stop words'leri filtrele
        filtered_words = [word for word in words if word not in self.stop_words]
        
        # Frekans hesapla
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
            
        # Sıralı liste olarak döndür
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_keywords[:max_keywords]
        
    def _clean_markdown(self, content: str) -> str:
        """Markdown syntax'ını temizler"""
        
        # Code blocks'ları kaldır
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'`[^`]+`', '', content)
        
        # Links'leri temizle
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        
        # Images'leri kaldır
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)
        
        # Headers'leri temizle
        content = re.sub(r'^#{1,6}\s*', '', content, flags=re.MULTILINE)
        
        # Emphasis'leri temizle
        content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^*]+)\*', r'\1', content)
        content = re.sub(r'__([^_]+)__', r'\1', content)
        content = re.sub(r'_([^_]+)_', r'\1', content)
        
        # Tables'leri temizle
        content = re.sub(r'\|[^|\n]*\|', '', content)
        
        # Lists'leri temizle
        content = re.sub(r'^[\s]*[-*+]\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\d+\.\s+', '', content, flags=re.MULTILINE)
        
        # Fazla boşlukları temizle
        content = re.sub(r'\s+', ' ', content)
        
        return content.strip()
        
    def create_content_summary(self, content: str, max_length: int = 500) -> str:
        """İçerikten özet çıkarır"""
        
        clean_content = self._clean_markdown(content)
        
        # Paragrafları ayır
        paragraphs = [p.strip() for p in clean_content.split('\n\n') if p.strip()]
        
        summary = ""
        for paragraph in paragraphs:
            if len(summary) + len(paragraph) <= max_length:
                summary += paragraph + "\n\n"
            else:
                # Kalan karakterde ne kadar sığarsa
                remaining = max_length - len(summary)
                if remaining > 50:  # En az 50 karakter varsa
                    summary += paragraph[:remaining-3] + "..."
                break
                
        return summary.strip()
        
    def analyze_content_structure(self, content: str) -> Dict:
        """İçerik yapısını analiz eder"""
        
        metadata = self.extract_metadata(content)
        keywords = self.extract_keywords(content)
        summary = self.create_content_summary(content)
        
        # İçerik istatistikleri
        lines = content.count('\n') + 1
        words = len(content.split())
        chars = len(content)
        
        # Başlık hiyerarşisi
        heading_levels = [h['level'] for h in metadata['headings']]
        
        # Komplekslik skoru (basit)
        complexity_score = 0
        complexity_score += len(metadata['headings']) * 2
        complexity_score += len(metadata['code_blocks']) * 5
        complexity_score += len(metadata['links']) * 1
        complexity_score += len(metadata['tables']) * 3
        complexity_score += len(metadata['lists']) * 1
        
        return {
            'metadata': metadata,
            'keywords': keywords,
            'summary': summary,
            'statistics': {
                'lines': lines,
                'words': words,
                'characters': chars,
                'heading_count': len(metadata['headings']),
                'code_block_count': len(metadata['code_blocks']),
                'link_count': len(metadata['links']),
                'table_count': len(metadata['tables']),
                'list_count': len(metadata['lists'])
            },
            'complexity_score': complexity_score,
            'heading_levels': heading_levels,
            'content_type': self._determine_content_type(metadata)
        }
        
    def _determine_content_type(self, metadata: Dict) -> str:
        """İçerik türünü belirler"""
        
        if len(metadata['code_blocks']) > 3:
            return 'technical_documentation'
        elif len(metadata['tables']) > 2:
            return 'data_documentation'
        elif len(metadata['headings']) > 5:
            return 'structured_document'
        elif len(metadata['lists']) > 5:
            return 'checklist_or_guide'
        elif metadata['title'].lower().startswith('todo'):
            return 'todo_list'
        elif metadata['title'].lower().startswith('readme'):
            return 'readme'
        elif 'report' in metadata['title'].lower():
            return 'report'
        else:
            return 'general_document'
            
    def create_search_index(self, file_path: str, content: str) -> Dict:
        """Dosya için arama indexi oluşturur"""
        
        analysis = self.analyze_content_structure(content)
        
        # Searchable content
        searchable_items = []
        
        # Başlık ve içerik
        if analysis['metadata']['title']:
            searchable_items.append({
                'type': 'title',
                'content': analysis['metadata']['title'],
                'weight': 10
            })
            
        # Başlıklar
        for heading in analysis['metadata']['headings']:
            searchable_items.append({
                'type': 'heading',
                'content': heading['text'],
                'weight': 5 + (7 - heading['level'])  # H1 daha yüksek ağırlık
            })
            
        # Anahtar kelimeler
        for keyword, freq in analysis['keywords'][:20]:  # Top 20 keywords
            searchable_items.append({
                'type': 'keyword',
                'content': keyword,
                'weight': min(freq, 5)  # Max 5 ağırlık
            })
            
        # Code blocks
        for code_block in analysis['metadata']['code_blocks']:
            if code_block['language']:
                searchable_items.append({
                    'type': 'code_language',
                    'content': code_block['language'],
                    'weight': 3
                })
                
        # Links
        for link in analysis['metadata']['links']:
            searchable_items.append({
                'type': 'link_text',
                'content': link['text'],
                'weight': 2
            })
            
        return {
            'file_path': file_path,
            'searchable_items': searchable_items,
            'analysis': analysis,
            'indexed_at': datetime.now().isoformat()
        }

def main():
    """Ana fonksiyon - test için"""
    print(f"{Fore.CYAN}🚀 Content Indexer Test Starting...{Style.RESET_ALL}")
    
    # Content indexer oluştur
    indexer = ContentIndexer()
    
    # Test content
    test_content = """# Test Markdown Document

Bu bir test dökümanıdır. **Kalın** ve *italic* yazı içerir.

## Kod Örneği

```python
def hello_world():
    print("Hello, World!")
```

## Liste

- Item 1
- Item 2
- Item 3

## Bağlantılar

[GitHub](https://github.com)

## Tablo

| Kolon 1 | Kolon 2 |
|---------|---------|
| Veri 1  | Veri 2  |

Bu döküman Context7 ERP sistemi için hazırlanmıştır.
"""
    
    # Content analizi
    analysis = indexer.analyze_content_structure(test_content)
    
    print(f"{Fore.GREEN}✅ Content Analysis Results:{Style.RESET_ALL}")
    print(f"  📊 Statistics: {analysis['statistics']}")
    print(f"  🏷️  Content Type: {analysis['content_type']}")
    print(f"  📈 Complexity Score: {analysis['complexity_score']}")
    print(f"  🔑 Top Keywords: {analysis['keywords'][:10]}")
    
    # Search index
    search_index = indexer.create_search_index("test.md", test_content)
    print(f"{Fore.YELLOW}📝 Search Index Created: {len(search_index['searchable_items'])} items{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}✅ Content Indexer test completed{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 