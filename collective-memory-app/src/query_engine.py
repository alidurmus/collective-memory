#!/usr/bin/env python3
"""
Query Engine - Full-text search ve filtreleme sistemi
Veritabanından gelişmiş arama ve filtreleme işlemleri yapar
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from colorama import init, Fore, Style
import logging
from dataclasses import dataclass, field

# Colorama initialize
init()


@dataclass
class SearchQuery:
    """Arama sorgusu veri yapısı"""
    text: str = ""
    keywords: List[str] = field(default_factory=list)
    file_types: List[str] = field(default_factory=list)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    content_type: Optional[str] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    include_paths: List[str] = field(default_factory=list)
    exclude_paths: List[str] = field(default_factory=list)
    sort_by: str = "relevance"  # relevance, date, size, name
    sort_order: str = "desc"  # asc, desc
    limit: int = 50
    use_semantic_search: bool = False  # Semantic search option
    
    def __post_init__(self):
        # No longer needed since we use field(default_factory=list)
        pass

@dataclass
class SearchResult:
    """Arama sonucu veri yapısı"""
    file_id: int
    file_path: str
    file_name: str
    file_extension: str
    file_size: int
    modified_at: str
    content_preview: str
    relevance_score: float
    match_highlights: List[str]
    content_type: str
    line_count: int
    word_count: int

class QueryEngine:
    """Gelişmiş arama ve filtreleme motoru"""
    
    def __init__(self, database_manager):
        self.db_manager = database_manager
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Stopwords for relevance scoring
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'as', 'is', 'was', 'are', 'were', 'be', 'been',
            've', 'bir', 'bu', 'da', 'de', 'ile', 'o', 'için', 'var', 'olan'
        }
        
    def search(self, query: SearchQuery) -> List[SearchResult]:
        """Ana arama fonksiyonu"""
        
        if not self.db_manager.connection:
            print(f"{Fore.RED}❌ Database connection required{Style.RESET_ALL}")
            return []
            
        try:
            # SQL sorgusu oluştur
            sql_query, params = self._build_sql_query(query)
            
            # Veritabanından sonuçları al
            cursor = self.db_manager.connection.cursor()
            cursor.execute(sql_query, params)
            raw_results = cursor.fetchall()
            
            # Sonuçları işle
            results = []
            for row in raw_results:
                result = self._process_search_result(row, query)
                if result:
                    results.append(result)
                    
            # Relevance scoring
            if query.sort_by == "relevance":
                results = self._calculate_relevance_scores(results, query)
                
            # Sıralama
            results = self._sort_results(results, query)
            
            # Limit uygula
            return results[:query.limit]
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            print(f"{Fore.RED}❌ Search failed: {e}{Style.RESET_ALL}")
            return []
            
    def _build_sql_query(self, query: SearchQuery) -> Tuple[str, List]:
        """SQL sorgusu oluşturur"""
        
        base_query = '''
            SELECT DISTINCT f.*, fc.content_text, fc.content_preview, 
                   fc.line_count, fc.word_count, fc.char_count
            FROM files f
            LEFT JOIN file_contents fc ON f.id = fc.file_id
            WHERE f.is_active = 1
        '''
        
        conditions = []
        params = []
        
        # Text search
        if query.text:
            text_conditions = []
            search_terms = self._extract_search_terms(query.text)
            
            for term in search_terms:
                like_term = f"%{term}%"
                text_conditions.append(
                    "(f.file_name LIKE ? OR f.file_path LIKE ? OR fc.content_text LIKE ?)"
                )
                params.extend([like_term, like_term, like_term])
                
            if text_conditions:
                conditions.append(f"({' AND '.join(text_conditions)})")
                
        # Keywords search
        if query.keywords:
            keyword_conditions = []
            for keyword in query.keywords:
                like_keyword = f"%{keyword}%"
                keyword_conditions.append("fc.content_text LIKE ?")
                params.append(like_keyword)
                
            if keyword_conditions:
                conditions.append(f"({' AND '.join(keyword_conditions)})")
                
        # File types
        if query.file_types:
            type_conditions = []
            for file_type in query.file_types:
                if not file_type.startswith('.'):
                    file_type = '.' + file_type
                type_conditions.append("f.file_extension = ?")
                params.append(file_type.lower())
                
            if type_conditions:
                conditions.append(f"({' OR '.join(type_conditions)})")
                
        # Date range
        if query.date_from:
            conditions.append("f.modified_at >= ?")
            params.append(query.date_from.isoformat())
            
        if query.date_to:
            conditions.append("f.modified_at <= ?")
            params.append(query.date_to.isoformat())
            
        # File size
        if query.min_size:
            conditions.append("f.file_size >= ?")
            params.append(query.min_size)
            
        if query.max_size:
            conditions.append("f.file_size <= ?")
            params.append(query.max_size)
            
        # Include paths
        if query.include_paths:
            path_conditions = []
            for path in query.include_paths:
                path_conditions.append("f.file_path LIKE ?")
                params.append(f"%{path}%")
                
            if path_conditions:
                conditions.append(f"({' OR '.join(path_conditions)})")
                
        # Exclude paths
        if query.exclude_paths:
            for path in query.exclude_paths:
                conditions.append("f.file_path NOT LIKE ?")
                params.append(f"%{path}%")
                
        # Add conditions to query
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
            
        # Add basic ordering (relevance scoring yapılacaksa daha sonra sıralanır)
        if query.sort_by != "relevance":
            order_map = {
                "date": "f.modified_at",
                "size": "f.file_size",
                "name": "f.file_name"
            }
            
            order_field = order_map.get(query.sort_by, "f.modified_at")
            order_dir = "DESC" if query.sort_order == "desc" else "ASC"
            base_query += f" ORDER BY {order_field} {order_dir}"
            
        return base_query, params
        
    def _extract_search_terms(self, text: str) -> List[str]:
        """Arama terimlerini çıkarır"""
        
        # Quotes içindeki exact phrases
        exact_phrases = re.findall(r'"([^"]*)"', text)
        
        # Quotes'u kaldır
        text = re.sub(r'"[^"]*"', '', text)
        
        # Kelime ayıkla
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Stopwords'u filtrele
        filtered_words = [word for word in words if word not in self.stopwords and len(word) > 2]
        
        # Exact phrases'i ekle
        terms = filtered_words + exact_phrases
        
        return list(set(terms))  # Unique terms
        
    def _process_search_result(self, row, query: SearchQuery) -> Optional[SearchResult]:
        """Raw veritabanı sonucunu SearchResult'a çevirir"""
        
        try:
            # Highlight matches
            highlights = self._find_highlights(row, query)
            
            # Content type belirleme (basit)
            content_type = self._determine_content_type(row)
            
            return SearchResult(
                file_id=row['id'],
                file_path=row['file_path'],
                file_name=row['file_name'],
                file_extension=row['file_extension'],
                file_size=row['file_size'],
                modified_at=row['modified_at'],
                content_preview=row['content_preview'] or "",
                relevance_score=0.0,  # Sonra hesaplanacak
                match_highlights=highlights,
                content_type=content_type,
                line_count=row['line_count'] or 0,
                word_count=row['word_count'] or 0
            )
            
        except Exception as e:
            self.logger.error(f"Error processing search result: {e}")
            return None
            
    def _find_highlights(self, row, query: SearchQuery) -> List[str]:
        """Eşleşen kısımları vurgular"""
        
        highlights = []
        content = row['content_text'] or ""
        
        # Text search highlights
        if query.text:
            terms = self._extract_search_terms(query.text)
            for term in terms:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                matches = pattern.finditer(content)
                
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end]
                    
                    # Highlight the term
                    highlighted = pattern.sub(
                        f"{Fore.YELLOW}\\g<0>{Style.RESET_ALL}", 
                        context
                    )
                    highlights.append(highlighted)
                    
                    if len(highlights) >= 3:  # Max 3 highlights per term
                        break
                        
        # Keyword highlights
        if query.keywords:
            for keyword in query.keywords:
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                matches = pattern.finditer(content)
                
                for match in matches:
                    start = max(0, match.start() - 30)
                    end = min(len(content), match.end() + 30)
                    context = content[start:end]
                    
                    highlighted = pattern.sub(
                        f"{Fore.CYAN}\\g<0>{Style.RESET_ALL}", 
                        context
                    )
                    highlights.append(highlighted)
                    
                    if len(highlights) >= 5:  # Max total highlights
                        break
                        
        return highlights[:5]  # Max 5 highlights
        
    def _determine_content_type(self, row) -> str:
        """İçerik tipini belirler"""
        
        file_name = row['file_name'].lower()
        file_path = row['file_path'].lower()
        
        if 'readme' in file_name:
            return 'readme'
        elif 'todo' in file_name:
            return 'todo'
        elif 'report' in file_name:
            return 'report'
        elif 'doc' in file_path or 'docs' in file_path:
            return 'documentation'
        elif 'config' in file_name:
            return 'configuration'
        elif 'guide' in file_name:
            return 'guide'
        else:
            return 'general'
            
    def _calculate_relevance_scores(self, results: List[SearchResult], query: SearchQuery) -> List[SearchResult]:
        """Relevance skorları hesaplar"""
        
        if not query.text and not query.keywords:
            return results
            
        search_terms = []
        if query.text:
            search_terms.extend(self._extract_search_terms(query.text))
        if query.keywords:
            search_terms.extend(query.keywords)
            
        for result in results:
            score = 0.0
            
            # File name matching (yüksek ağırlık)
            for term in search_terms:
                if term.lower() in result.file_name.lower():
                    score += 10.0
                    
            # File path matching (orta ağırlık)
            for term in search_terms:
                if term.lower() in result.file_path.lower():
                    score += 5.0
                    
            # Content matching (normal ağırlık)
            content = result.content_preview.lower()
            for term in search_terms:
                term_count = content.count(term.lower())
                score += term_count * 2.0
                
            # File size normalization (küçük dosyalar biraz daha yüksek skor)
            if result.file_size > 0:
                size_factor = min(1.0, 10000 / result.file_size)
                score *= (0.5 + size_factor * 0.5)
                
            # Content type bonus
            type_bonus = {
                'readme': 1.2,
                'documentation': 1.1,
                'guide': 1.1,
                'todo': 1.0,
                'report': 1.0,
                'configuration': 0.9,
                'general': 1.0
            }
            score *= type_bonus.get(result.content_type, 1.0)
            
            # Recent files bonus (son 7 gün)
            try:
                modified_date = datetime.fromisoformat(result.modified_at.replace('Z', '+00:00'))
                days_ago = (datetime.now() - modified_date).days
                if days_ago <= 7:
                    score *= 1.1
            except:
                pass
                
            result.relevance_score = score
            
        return results
        
    def _sort_results(self, results: List[SearchResult], query: SearchQuery) -> List[SearchResult]:
        """Sonuçları sıralar"""
        
        reverse = query.sort_order == "desc"
        
        if query.sort_by == "relevance":
            return sorted(results, key=lambda x: x.relevance_score, reverse=reverse)
        elif query.sort_by == "date":
            return sorted(results, key=lambda x: x.modified_at, reverse=reverse)
        elif query.sort_by == "size":
            return sorted(results, key=lambda x: x.file_size, reverse=reverse)
        elif query.sort_by == "name":
            return sorted(results, key=lambda x: x.file_name, reverse=reverse)
        else:
            return results
            
    def suggest_queries(self, partial_text: str, limit: int = 5) -> List[str]:
        """Sorgu önerileri sunar"""
        
        if not self.db_manager.connection or len(partial_text) < 2:
            return []
            
        try:
            cursor = self.db_manager.connection.cursor()
            
            # File name suggestions
            cursor.execute('''
                SELECT DISTINCT file_name 
                FROM files 
                WHERE is_active = 1 AND file_name LIKE ?
                ORDER BY file_name
                LIMIT ?
            ''', (f"%{partial_text}%", limit))
            
            suggestions = [row['file_name'] for row in cursor.fetchall()]
            
            # Content keywords suggestions (basit)
            if len(suggestions) < limit:
                cursor.execute('''
                    SELECT DISTINCT f.file_name
                    FROM files f
                    JOIN file_contents fc ON f.id = fc.file_id
                    WHERE f.is_active = 1 AND fc.content_text LIKE ?
                    ORDER BY f.modified_at DESC
                    LIMIT ?
                ''', (f"%{partial_text}%", limit - len(suggestions)))
                
                content_suggestions = [row['file_name'] for row in cursor.fetchall()]
                suggestions.extend(content_suggestions)
                
            return list(set(suggestions))[:limit]
            
        except Exception as e:
            self.logger.error(f"Suggestion error: {e}")
            return []
            
    def get_search_statistics(self) -> Dict:
        """Arama istatistiklerini döndürür"""
        
        if not self.db_manager.connection:
            return {}
            
        try:
            cursor = self.db_manager.connection.cursor()
            
            # Toplam dosya sayısı
            cursor.execute("SELECT COUNT(*) as total FROM files WHERE is_active = 1")
            total_files = cursor.fetchone()['total']
            
            # Dosya türleri
            cursor.execute('''
                SELECT file_extension, COUNT(*) as count
                FROM files 
                WHERE is_active = 1 
                GROUP BY file_extension
                ORDER BY count DESC
            ''')
            file_types = [(row['file_extension'], row['count']) for row in cursor.fetchall()]
            
            # Son güncellenen dosyalar
            cursor.execute('''
                SELECT file_name, modified_at
                FROM files 
                WHERE is_active = 1 
                ORDER BY modified_at DESC
                LIMIT 5
            ''')
            recent_files = [(row['file_name'], row['modified_at']) for row in cursor.fetchall()]
            
            return {
                'total_files': total_files,
                'file_types': file_types,
                'recent_files': recent_files
            }
            
        except Exception as e:
            self.logger.error(f"Statistics error: {e}")
            return {}

def main():
    """Ana fonksiyon - test için"""
    print(f"{Fore.CYAN}🚀 Query Engine Test Starting...{Style.RESET_ALL}")
    
    # Mock database manager için basit test
    class MockDB:
        def __init__(self):
            self.connection = None
            
    mock_db = MockDB()
    query_engine = QueryEngine(mock_db)
    
    # Test query
    test_query = SearchQuery(
        text="TODO Context7",
        keywords=["system", "implementation"],
        file_types=["md"],
        sort_by="relevance",
        limit=10
    )
    
    print(f"{Fore.GREEN}✅ Query Engine initialized{Style.RESET_ALL}")
    print(f"  📊 Test query: {test_query.text}")
    print(f"  🔍 Keywords: {test_query.keywords}")
    print(f"  📄 File types: {test_query.file_types}")
    
    # Search terms extraction test
    search_terms = query_engine._extract_search_terms('context7 "exact phrase" system')
    print(f"{Fore.YELLOW}🔤 Extracted terms: {search_terms}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}✅ Query Engine test completed{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 