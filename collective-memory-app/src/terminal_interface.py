#!/usr/bin/env python3
"""
Terminal Interface - İnteraktif komut satırı arayüzü
Enhanced semantic search capabilities ile güçlendirilmiş
"""

import os
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from colorama import init, Fore, Style

# Core imports
from database_manager import DatabaseManager
from file_monitor import DataFolderMonitor
from content_indexer import ContentIndexer
from query_engine import QueryEngine, SearchQuery, SearchResult

# Enhanced imports
try:
    from enhanced_query_engine import (
        EnhancedQueryEngine, EnhancedSearchQuery, EnhancedSearchResult
    )
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False
    print("⚠️  Enhanced query engine not available. Using basic search.")

# Initialize colorama
init()


class TerminalInterface:
    """İnteraktif terminal arayüzü - Enhanced semantic search ile"""
    
    def __init__(self, data_path: str = "../data"):
        self.data_path = Path(data_path).resolve()
        # Use organized .collective-memory directory structure
        self.collective_memory_dir = self.data_path / ".collective-memory"
        self.db_path = self.collective_memory_dir / "database" / "collective_memory.db"
        
        # Ensure .collective-memory directory structure exists
        self.collective_memory_dir.mkdir(exist_ok=True)
        (self.collective_memory_dir / "database").mkdir(exist_ok=True)
        (self.collective_memory_dir / "cache").mkdir(exist_ok=True)
        (self.collective_memory_dir / "logs").mkdir(exist_ok=True)
        (self.collective_memory_dir / "config").mkdir(exist_ok=True)
        
        self.database_manager = DatabaseManager(str(self.db_path))
        self.file_monitor = DataFolderMonitor(str(self.data_path))
        self.content_indexer = ContentIndexer()
        
        # Initialize appropriate query engine
        if ENHANCED_AVAILABLE:
            self.query_engine = EnhancedQueryEngine(self.database_manager)
            self.use_enhanced = True
            print(f"{Fore.GREEN}🚀 Enhanced semantic search enabled{Style.RESET_ALL}")
        else:
            self.query_engine = QueryEngine(self.database_manager)
            self.use_enhanced = False
            print(f"{Fore.YELLOW}⚠️  Using basic search mode{Style.RESET_ALL}")
        
        self.max_results_display = 20
        
        # Enhanced search settings
        self.semantic_search_enabled = True
        self.ai_scoring_enabled = True
        self.entity_extraction_enabled = True
    
    def interactive_mode(self):
        """İnteraktif mod - Enhanced features ile"""
        print(f"\n{Fore.CYAN}🧠 Collective Memory Interactive Search{Style.RESET_ALL}")
        print(f"📁 Data Path: {self.data_path}")
        if self.use_enhanced:
            print(f"{Fore.GREEN}🤖 AI-Powered Semantic Search: Enabled{Style.RESET_ALL}")
        print(f"💾 Database: {self.db_path}")
        print(f"\n{Fore.YELLOW}Commands:{Style.RESET_ALL}")
        print("  help          - Show help")
        print("  stats         - Show database statistics") 
        print("  search <term> - Search for content")
        if self.use_enhanced:
            print("  semantic <term>   - Semantic search with AI scoring")
            print("  intent <query>    - Analyze query intent")
            print("  suggestions <term> - Get semantic suggestions")
            print("  settings      - Show/modify search settings")
        print("  quit          - Exit interactive mode")
        print()
        
        while True:
            try:
                user_input = input(f"{Fore.GREEN}search> {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                parts = user_input.split(' ', 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == "quit" or command == "exit":
                    print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                    break
                elif command == "help":
                    self._show_help()
                elif command == "stats":
                    self._show_statistics()
                elif command == "search":
                    if args:
                        query = SearchQuery(text=args)
                        results = self.query_engine.search(query)
                        self._display_search_results(results, query)
                    else:
                        print(f"{Fore.RED}❌ Please provide search terms{Style.RESET_ALL}")
                elif command == "semantic" and self.use_enhanced:
                    if args:
                        self._perform_semantic_search(args)
                    else:
                        print(f"{Fore.RED}❌ Please provide search terms{Style.RESET_ALL}")
                elif command == "intent" and self.use_enhanced:
                    if args:
                        self._analyze_query_intent(args)
                    else:
                        print(f"{Fore.RED}❌ Please provide a query{Style.RESET_ALL}")
                elif command == "suggestions" and self.use_enhanced:
                    if args:
                        self._show_semantic_suggestions(args)
                    else:
                        print(f"{Fore.RED}❌ Please provide a term{Style.RESET_ALL}")
                elif command == "settings" and self.use_enhanced:
                    self._show_search_settings()
                else:
                    print(f"{Fore.RED}❌ Unknown command: {command}. Type 'help' for available commands.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    
    def _perform_semantic_search(self, query_text: str):
        """Perform enhanced semantic search"""
        if not self.use_enhanced:
            print(f"{Fore.RED}❌ Enhanced search not available{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}🧠 Semantic Search: '{query_text}'{Style.RESET_ALL}")
        
        # Create enhanced query
        query = EnhancedSearchQuery(
            text=query_text,
            use_semantic_search=self.semantic_search_enabled,
            use_ai_scoring=self.ai_scoring_enabled,
            extract_entities=self.entity_extraction_enabled,
            semantic_similarity_threshold=0.6
        )
        
        # Analyze intent first
        intent = self.query_engine.analyze_query_intent(query_text)
        print(f"🎯 Detected Intent: {intent}")
        
        # Perform search
        results = self.query_engine.search(query)
        self._display_enhanced_results(results, query)
    
    def _analyze_query_intent(self, query_text: str):
        """Analyze and display query intent"""
        if not self.use_enhanced:
            print(f"{Fore.RED}❌ Enhanced features not available{Style.RESET_ALL}")
            return
        
        intent = self.query_engine.analyze_query_intent(query_text)
        print(f"\n{Fore.CYAN}🎯 Query Intent Analysis{Style.RESET_ALL}")
        print(f"Query: '{query_text}'")
        print(f"Detected Intent: {Fore.GREEN}{intent}{Style.RESET_ALL}")
        
        # Provide intent-specific suggestions
        if intent == 'explain':
            print(f"{Fore.YELLOW}💡 Tip: Looking for explanatory content. Try semantic search for better results.{Style.RESET_ALL}")
        elif intent == 'find':
            print(f"{Fore.YELLOW}💡 Tip: Searching for specific items. Consider using filters for better results.{Style.RESET_ALL}")
        elif intent == 'list':
            print(f"{Fore.YELLOW}💡 Tip: Looking for comprehensive lists. Try broader search terms.{Style.RESET_ALL}")
        elif intent == 'compare':
            print(f"{Fore.YELLOW}💡 Tip: Comparing concepts. Use semantic search to find related content.{Style.RESET_ALL}")
    
    def _show_semantic_suggestions(self, query_text: str):
        """Show semantic query suggestions"""
        if not self.use_enhanced:
            print(f"{Fore.RED}❌ Enhanced features not available{Style.RESET_ALL}")
            return
        
        suggestions = self.query_engine.get_semantic_suggestions(query_text, limit=5)
        
        print(f"\n{Fore.CYAN}💡 Semantic Suggestions for '{query_text}'{Style.RESET_ALL}")
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print(f"{Fore.YELLOW}No suggestions available{Style.RESET_ALL}")
    
    def _show_search_settings(self):
        """Show and allow modification of search settings"""
        print(f"\n{Fore.CYAN}⚙️  Search Settings{Style.RESET_ALL}")
        print(f"1. Semantic Search: {Fore.GREEN if self.semantic_search_enabled else Fore.RED}{'Enabled' if self.semantic_search_enabled else 'Disabled'}{Style.RESET_ALL}")
        print(f"2. AI Scoring: {Fore.GREEN if self.ai_scoring_enabled else Fore.RED}{'Enabled' if self.ai_scoring_enabled else 'Disabled'}{Style.RESET_ALL}")
        print(f"3. Entity Extraction: {Fore.GREEN if self.entity_extraction_enabled else Fore.RED}{'Enabled' if self.entity_extraction_enabled else 'Disabled'}{Style.RESET_ALL}")
        print(f"4. Max Results: {self.max_results_display}")
        
        print(f"\n{Fore.YELLOW}Toggle settings by typing number (1-4) or press Enter to continue:{Style.RESET_ALL}")
        choice = input().strip()
        
        if choice == "1":
            self.semantic_search_enabled = not self.semantic_search_enabled
            print(f"Semantic Search: {Fore.GREEN if self.semantic_search_enabled else Fore.RED}{'Enabled' if self.semantic_search_enabled else 'Disabled'}{Style.RESET_ALL}")
        elif choice == "2":
            self.ai_scoring_enabled = not self.ai_scoring_enabled
            print(f"AI Scoring: {Fore.GREEN if self.ai_scoring_enabled else Fore.RED}{'Enabled' if self.ai_scoring_enabled else 'Disabled'}{Style.RESET_ALL}")
        elif choice == "3":
            self.entity_extraction_enabled = not self.entity_extraction_enabled
            print(f"Entity Extraction: {Fore.GREEN if self.entity_extraction_enabled else Fore.RED}{'Enabled' if self.entity_extraction_enabled else 'Disabled'}{Style.RESET_ALL}")
        elif choice == "4":
            try:
                new_max = int(input("Enter new max results (10-100): "))
                if 10 <= new_max <= 100:
                    self.max_results_display = new_max
                    print(f"Max Results set to: {new_max}")
                else:
                    print(f"{Fore.RED}Please enter a number between 10 and 100{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid number{Style.RESET_ALL}")
    
    def _display_enhanced_results(self, results: List, query, save_to_file: Optional[str] = None):
        """Display enhanced search results with AI scores"""
        
        if not results:
            message = "📭 No results found"
            print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            if save_to_file:
                self._save_results_to_file([], query, save_to_file, message)
            return
            
        message = f"✅ Found {len(results)} results with AI-powered scoring"
        print(f"\n{Fore.GREEN}{message}{Style.RESET_ALL}")
        
        # Display results with enhanced information
        for i, result in enumerate(results[:self.max_results_display], 1):
            print(f"\n{Fore.CYAN}📄 {i}. {result.file_name}{Style.RESET_ALL}")
            print(f"   📁 {result.file_path}")
            print(f"   📊 Size: {self._format_file_size(result.file_size)} | Modified: {result.modified_at}")
            
            # Enhanced scoring information
            if self.use_enhanced:
                print(f"   🎯 Relevance: {result.relevance_score:.2f} | Semantic: {result.semantic_score:.2f}")
                print(f"   🤖 AI Scores - Quality: {result.content_quality_score:.2f} | Freshness: {result.freshness_score:.2f}")
                
                # Show detected entities if available
                if result.detected_entities:
                    entities_str = ", ".join(result.detected_entities[:5])
                    print(f"   🏷️  Entities: {entities_str}")
                
                # Show contextual snippets
                if result.contextual_snippets:
                    print(f"   📝 Context: {result.contextual_snippets[0][:100]}...")
            
            # Show highlights
            if result.match_highlights:
                highlights_str = " | ".join(result.match_highlights[:3])
                print(f"   ✨ Highlights: {highlights_str}")
            
            # Show content preview
            preview = result.content_preview[:150] + "..." if len(result.content_preview) > 150 else result.content_preview
            print(f"   📖 Preview: {preview}")
        
        # Show additional results info
        if len(results) > self.max_results_display:
            remaining = len(results) - self.max_results_display
            print(f"\n{Fore.YELLOW}📄 {remaining} more results available. Use settings to show more.{Style.RESET_ALL}")
        
        # Save to file if requested
        if save_to_file:
            self._save_enhanced_results_to_file(results, query, save_to_file, message)
    
    def _save_enhanced_results_to_file(self, results: List, query, file_path: str, message: str):
        """Save enhanced search results to file"""
        try:
            # Use collective-memory directory for saving
            if not os.path.isabs(file_path):
                file_path = self.collective_memory_dir / file_path
            
            with open(file_path, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"# 🧠 Enhanced Search Results\n\n")
                f.write(f"**Query:** {query.text}\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Results:** {len(results)}\n")
                f.write(f"**Mode:** AI-Powered Semantic Search\n\n")
                
                # Write settings
                f.write(f"## ⚙️ Search Settings\n\n")
                f.write(f"- Semantic Search: {'✅' if query.use_semantic_search else '❌'}\n")
                f.write(f"- AI Scoring: {'✅' if query.use_ai_scoring else '❌'}\n")
                f.write(f"- Entity Extraction: {'✅' if query.extract_entities else '❌'}\n")
                f.write(f"- Similarity Threshold: {query.semantic_similarity_threshold}\n\n")
                
                # Write results
                f.write(f"## 📊 Results\n\n")
                for i, result in enumerate(results, 1):
                    f.write(f"### {i}. {result.file_name}\n\n")
                    f.write(f"- **Path:** `{result.file_path}`\n")
                    f.write(f"- **Size:** {self._format_file_size(result.file_size)}\n")
                    f.write(f"- **Modified:** {result.modified_at}\n")
                    f.write(f"- **Relevance Score:** {result.relevance_score:.3f}\n")
                    f.write(f"- **Semantic Score:** {result.semantic_score:.3f}\n")
                    f.write(f"- **Content Quality:** {result.content_quality_score:.3f}\n")
                    f.write(f"- **Freshness:** {result.freshness_score:.3f}\n")
                    
                    if result.detected_entities:
                        entities_str = ", ".join(result.detected_entities)
                        f.write(f"- **Entities:** {entities_str}\n")
                    
                    if result.match_highlights:
                        highlights_str = " | ".join(result.match_highlights)
                        f.write(f"- **Highlights:** {highlights_str}\n")
                    
                    f.write(f"\n**Preview:**\n```\n{result.content_preview[:300]}\n```\n\n")
                    
                    if result.contextual_snippets:
                        f.write(f"**Context Snippets:**\n")
                        for snippet in result.contextual_snippets:
                            f.write(f"- {snippet}\n")
                        f.write(f"\n")
                    
                    f.write(f"---\n\n")
            
            print(f"\n{Fore.GREEN}💾 Enhanced results saved to: {file_path}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to save results: {e}{Style.RESET_ALL}")

    def _show_help(self):
        """Yardım mesajını gösterir"""
        help_text = f"""
{Fore.CYAN}📖 Collective Memory Query System - Help{Style.RESET_ALL}

{Fore.YELLOW}Basic Search:{Style.RESET_ALL}
  search <term>           - Simple text search
  find <term>             - Alias for search
  <term>                  - Direct search (no command needed)

{Fore.YELLOW}Advanced Search:{Style.RESET_ALL}
  search -k keyword1,keyword2    - Search by keywords
  search -t md,txt               - Search specific file types
  search -d 7                    - Files modified in last 7 days
  search -s 1000                 - Files larger than 1000 bytes
  search -p docs/                - Search in specific path

{Fore.YELLOW}Filters:{Style.RESET_ALL}
  search "exact phrase"          - Exact phrase matching
  search term -x exclude_path    - Exclude specific paths
  search term --sort date        - Sort by date/size/name/relevance
  search term --limit 10         - Limit results

{Fore.YELLOW}System Commands:{Style.RESET_ALL}
  help                   - Show this help
  stats                  - Show system statistics
  index                  - Reindex all files
  monitor                - Start file monitoring
  cursor_history [--limit=N] [--workspaces]  - Cursor chat geçmişini göster
  quit/exit/q            - Exit program

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  search Context7                    - Find files containing "Context7"
  search -k todo,implementation      - Find files with specific keywords
  search -t md -d 3                  - Markdown files from last 3 days
  search "Context7 ERP" -p docs/     - Exact phrase in docs folder
"""
        print(help_text)
        
    def _show_statistics(self):
        """Sistem istatistiklerini gösterir"""
        print(f"\n{Fore.CYAN}📊 System Statistics{Style.RESET_ALL}")
        
        try:
            stats = self.query_engine.get_search_statistics()
            
            if not stats:
                print(f"{Fore.YELLOW}⚠️  No statistics available{Style.RESET_ALL}")
                return
                
            print(f"  📁 Total files: {stats.get('total_files', 0)}")
            
            # File types
            file_types = stats.get('file_types', [])
            if file_types:
                print(f"\n  📄 File types:")
                for ext, count in file_types[:10]:  # Top 10
                    print(f"    {ext or 'no extension'}: {count} files")
                    
            # Recent files
            recent_files = stats.get('recent_files', [])
            if recent_files:
                print(f"\n  🕐 Recent files:")
                for name, date in recent_files:
                    print(f"    {name}: {date}")
                    
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting statistics: {e}{Style.RESET_ALL}")
            
    def _reindex_all_files(self):
        """Tüm dosyaları yeniden indeksler"""
        print(f"\n{Fore.CYAN}🔄 Reindexing all files...{Style.RESET_ALL}")
        
        try:
            indexed_count = 0
            for root, dirs, files in os.walk(self.data_path):
                for file in files:
                    file_path = Path(root) / file
                    
                    # Sadece markdown dosyaları
                    if file_path.suffix.lower() in ['.md', '.markdown', '.txt']:
                        try:
                            file_id = self.database_manager.add_or_update_file(str(file_path))
                            if file_id:
                                indexed_count += 1
                        except Exception as e:
                            print(f"{Fore.YELLOW}⚠️  Error indexing {file_path}: {e}{Style.RESET_ALL}")
                            
            print(f"{Fore.GREEN}✅ Reindexing completed: {indexed_count} files processed{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Reindexing failed: {e}{Style.RESET_ALL}")
            
    def _start_file_monitoring(self):
        """Dosya izlemeyi başlatır"""
        if self.file_monitor and self.file_monitor.is_running:
            print(f"{Fore.YELLOW}⚠️  File monitoring already running{Style.RESET_ALL}")
            return
            
        try:
            self.file_monitor = DataFolderMonitor(
                str(self.data_path),
                callback=self._on_file_change
            )
            
            print(f"{Fore.CYAN}🔍 Starting file monitoring...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Press Ctrl+C to stop monitoring and return to search{Style.RESET_ALL}")
            
            self.file_monitor.run_forever()
            
        except Exception as e:
            print(f"{Fore.RED}❌ File monitoring error: {e}{Style.RESET_ALL}")
            
    def _on_file_change(self, event_type: str, src_path: str, dest_path: Optional[str] = None):
        """Dosya değişikliği callback'i"""
        if event_type in ['created', 'modified']:
            try:
                file_id = self.database_manager.add_or_update_file(src_path)
                if file_id:
                    print(f"{Fore.GREEN}📝 File indexed: {Path(src_path).name}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  Indexing error: {e}{Style.RESET_ALL}")
                
    def _process_search_command(self, command: str):
        """Arama komutunu işler"""
        
        # Komut parsing
        query = self._parse_search_command(command)
        
        if not query:
            return
            
        # Arama yap
        print(f"\n{Fore.CYAN}🔍 Searching...{Style.RESET_ALL}")
        results = self.query_engine.search(query)
        
        # Sonuçları göster
        self._display_search_results(results, query)
        
    def _parse_search_command(self, command: str) -> Optional[SearchQuery]:
        """Arama komutunu parse eder"""
        
        try:
            # Basit komut parsing
            parts = command.split()
            
            # "search" veya "find" keyword'ünü kaldır
            if parts[0].lower() in ['search', 'find']:
                parts = parts[1:]
                
            if not parts:
                print(f"{Fore.YELLOW}⚠️  Empty search query{Style.RESET_ALL}")
                return None
                
            query = SearchQuery()
            
            # Argümanları parse et
            i = 0
            while i < len(parts):
                part = parts[i]
                
                if part.startswith('-'):
                    # Flag parsing
                    if part == '-k' and i + 1 < len(parts):
                        # Keywords
                        query.keywords = parts[i + 1].split(',')
                        i += 2
                    elif part == '-t' and i + 1 < len(parts):
                        # File types
                        query.file_types = parts[i + 1].split(',')
                        i += 2
                    elif part == '-d' and i + 1 < len(parts):
                        # Days ago
                        days = int(parts[i + 1])
                        query.date_from = datetime.now() - timedelta(days=days)
                        i += 2
                    elif part == '-s' and i + 1 < len(parts):
                        # Min size
                        query.min_size = int(parts[i + 1])
                        i += 2
                    elif part == '-p' and i + 1 < len(parts):
                        # Include paths
                        query.include_paths = [parts[i + 1]]
                        i += 2
                    elif part == '-x' and i + 1 < len(parts):
                        # Exclude paths
                        query.exclude_paths = [parts[i + 1]]
                        i += 2
                    elif part == '--sort' and i + 1 < len(parts):
                        # Sort by
                        query.sort_by = parts[i + 1]
                        i += 2
                    elif part == '--limit' and i + 1 < len(parts):
                        # Limit
                        query.limit = int(parts[i + 1])
                        i += 2
                    else:
                        i += 1
                else:
                    # Text search
                    if not query.text:
                        query.text = part
                    else:
                        query.text += ' ' + part
                    i += 1
                    
            return query
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error parsing command: {e}{Style.RESET_ALL}")
            return None
            
    def _display_search_results(self, results: List[SearchResult], query: SearchQuery, save_to_file: Optional[str] = None):
        """Arama sonuçlarını gösterir ve isteğe bağlı olarak dosyaya kaydeder"""
        
        if not results:
            message = "📭 No results found"
            print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            if save_to_file:
                self._save_results_to_file([], query, save_to_file, message)
            return
            
        message = f"✅ Found {len(results)} results"
        print(f"\n{Fore.GREEN}{message}{Style.RESET_ALL}")
        
        # Dosyaya kaydet
        if save_to_file:
            self._save_results_to_file(results, query, save_to_file, message)
        
        # Sonuçları tablo formatında göster
        table_data = []
        for i, result in enumerate(results[:self.max_results_display], 1):
            
            # File size formatı
            size_str = self._format_file_size(result.file_size)
            
            # Modified date formatı
            try:
                date_str = datetime.fromisoformat(result.modified_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            except:
                date_str = result.modified_at[:16]
                
            # Preview
            preview = result.content_preview[:self.preview_length]
            if len(result.content_preview) > self.preview_length:
                preview += "..."
                
            table_data.append([
                i,
                result.file_name,
                result.file_extension,
                size_str,
                date_str,
                f"{result.relevance_score:.1f}" if query.sort_by == "relevance" else "-",
                preview
            ])
            
        headers = ["#", "File", "Type", "Size", "Modified", "Score", "Preview"]
        print(f"\n{tabulate(table_data, headers=headers, tablefmt='grid')}")
        
        # Highlights göster
        if results and results[0].match_highlights:
            print(f"\n{Fore.CYAN}🔍 Match highlights (first result):{Style.RESET_ALL}")
            for highlight in results[0].match_highlights[:3]:
                print(f"  ... {highlight.strip()} ...")
                
        # Daha fazla sonuç varsa bildir
        if len(results) > self.max_results_display:
            remaining = len(results) - self.max_results_display
            print(f"\n{Fore.YELLOW}📄 {remaining} more results available. Use --limit to show more.{Style.RESET_ALL}")
    
    def _save_results_to_file(self, results: List[SearchResult], query: SearchQuery, file_path: str, message: str):
        """Arama sonuçlarını dosyaya kaydeder"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # Header
                f.write(f"# 🔍 Collective Memory - Search Results\n\n")
                f.write(f"**Search Query:** `{query.text}`\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Results:** {message}\n\n")
                
                if not results:
                    f.write("No results found for this query.\n")
                    return
                    
                f.write("---\n\n")
                
                # Results
                for i, result in enumerate(results, 1):
                    f.write(f"## {i}. {result.file_name}\n\n")
                    f.write(f"- **File:** `{result.file_path}`\n")
                    f.write(f"- **Type:** {result.file_extension}\n")
                    f.write(f"- **Size:** {self._format_file_size(result.file_size)}\n")
                    
                    # Modified date
                    try:
                        date_str = datetime.fromisoformat(result.modified_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
                    except:
                        date_str = result.modified_at[:16]
                    f.write(f"- **Modified:** {date_str}\n")
                    
                    # Score
                    if query.sort_by == "relevance":
                        f.write(f"- **Relevance Score:** {result.relevance_score:.1f}\n")
                    
                    # Preview
                    if result.content_preview:
                        f.write(f"\n**Preview:**\n```\n{result.content_preview[:500]}")
                        if len(result.content_preview) > 500:
                            f.write("...")
                        f.write("\n```\n")
                    
                    # Highlights
                    if result.match_highlights:
                        f.write(f"\n**Match Highlights:**\n")
                        for highlight in result.match_highlights[:3]:  # İlk 3 match
                            f.write(f"- {highlight}\n")
                    
                    f.write(f"\n---\n\n")
                
                f.write(f"*Generated by Collective Memory v1.0.0 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            
            print(f"{Fore.GREEN}💾 Results saved to: {file_path}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving file: {e}{Style.RESET_ALL}")
            
    def _format_file_size(self, size: int) -> str:
        """Dosya boyutunu formatlar"""
        if size < 1024:
            return f"{size}B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f}KB"
        else:
            return f"{size/(1024*1024):.1f}MB"
            
    def run_command_mode(self, args):
        """Komut satırı modu"""
        
        if args.command == 'search':
            query = SearchQuery(
                text=args.text or "",
                keywords=args.keywords.split(',') if args.keywords else [],
                file_types=args.file_types.split(',') if args.file_types else [],
                sort_by=args.sort_by,
                limit=args.limit
            )
            
            # Date range
            if args.days:
                query.date_from = datetime.now() - timedelta(days=args.days)
                
            # Size filter
            if args.min_size:
                query.min_size = args.min_size
                
            # Path filters
            if args.include_path:
                query.include_paths = [args.include_path]
            if args.exclude_path:
                query.exclude_paths = [args.exclude_path]
                
            # Arama yap
            results = self.query_engine.search(query)
            self._display_search_results(results, query)
            
        elif args.command == 'index':
            self._reindex_all_files()
            
        elif args.command == 'stats':
            self._show_statistics()
            
        elif args.command == 'monitor':
            self._start_file_monitoring()
            
    def cmd_cursor_history(self, args: str):
        """Cursor chat geçmişini görüntüle - Enhanced version"""
        if not self.data_path:
            print(f"{Fore.RED}❌ Data path belirtilmedi. --data-path kullanın.{Style.RESET_ALL}")
            return
            
        try:
            cursor_reader = EnhancedCursorDatabaseReader()
            
            if not cursor_reader.is_cursor_available():
                print(f"{Fore.YELLOW}⚠️  Cursor veritabanı bulunamadı.{Style.RESET_ALL}")
                return
            
            # Argüman parsing
            parts = args.strip().split() if args.strip() else []
            limit = 10
            show_workspaces = False
            
            for part in parts:
                if part.startswith('--limit='):
                    try:
                        limit = int(part.split('=')[1])
                    except ValueError:
                        print(f"{Fore.RED}❌ Geçersiz limit değeri: {part}{Style.RESET_ALL}")
                        return
                elif part == '--workspaces':
                    show_workspaces = True
            
            if show_workspaces:
                # Tüm workspace'leri göster
                print(f"{Fore.CYAN}📊 Cursor Workspace Özeti:{Style.RESET_ALL}")
                workspaces = cursor_reader.get_all_workspaces_summary()
                
                if not workspaces:
                    print(f"{Fore.YELLOW}⚠️  Hiçbir workspace bulunamadı.{Style.RESET_ALL}")
                    return
                    
                for workspace_key, workspace_data in workspaces.items():
                    info = workspace_data['info']
                    print(f"\n{Fore.GREEN}🗂️  {workspace_key}{Style.RESET_ALL}")
                    print(f"   📁 Path: {info.get('path', 'Bilinmiyor')}")
                    print(f"   💬 Chat sayısı: {workspace_data['chat_count']}")
                    print(f"   ⏰ Son aktivite: {workspace_data.get('last_activity', 'Bilinmiyor')}")
                    print(f"   🗄️  DB: {workspace_data['db_path']}")
                    
            else:
                # Mevcut proje için chat geçmişi
                print(f"{Fore.CYAN}💬 Cursor Chat Geçmişi ({limit} sonuç):{Style.RESET_ALL}")
                chats = cursor_reader.get_project_chat_history(self.data_path, limit)
                
                if not chats:
                    print(f"{Fore.YELLOW}⚠️  Bu proje için chat geçmişi bulunamadı.{Style.RESET_ALL}")
                    return
                
                for i, chat in enumerate(chats, 1):
                    chat_type = chat.get('type', 'unknown')
                    key_type = chat.get('key_type', 'unknown')
                    summary = chat.get('summary', 'Özet yok')
                    
                    # Chat type icons
                    type_icons = {
                        'conversation': '💬',
                        'code_generation': '💻',
                        'inline_chat': '📝',
                        'message_array': '📋',
                        'raw_content': '📄',
                        'raw_string': '📜'
                    }
                    
                    icon = type_icons.get(chat_type, '❓')
                    
                    print(f"\n{Fore.GREEN}{i:2d}. {icon} [{chat_type}] - {key_type}{Style.RESET_ALL}")
                    print(f"     {Fore.BLUE}ID:{Style.RESET_ALL} {chat.get('id', 'N/A')}")
                    print(f"     {Fore.MAGENTA}📝 Özet:{Style.RESET_ALL} {summary}")
                    
                    # Ek bilgiler
                    if 'message_count' in chat:
                        print(f"     {Fore.CYAN}📊 Mesaj sayısı:{Style.RESET_ALL} {chat['message_count']}")
                    
                    if 'prompt' in chat and 'response' in chat:
                        prompt_preview = chat['prompt'][:100] + "..." if len(chat['prompt']) > 100 else chat['prompt']
                        print(f"     {Fore.YELLOW}❓ Prompt:{Style.RESET_ALL} {prompt_preview}")
                        
        except Exception as e:
            print(f"{Fore.RED}❌ Cursor geçmiş okuma hatası: {e}{Style.RESET_ALL}")

    def cmd_help(self, args: str):
        """Yardım komutlarını göster"""
        # ... existing help content ...
        
        print(f"{Fore.CYAN}📚 Enhanced Cursor Commands:{Style.RESET_ALL}")
        print("  cursor_history [--limit=N] [--workspaces]  - Cursor chat geçmişini göster")
        print("    Örnekler:")
        print("      cursor_history                          - Son 10 chat'i göster")
        print("      cursor_history --limit=20               - Son 20 chat'i göster") 
        print("      cursor_history --workspaces             - Tüm workspace'leri göster")

    def cleanup(self):
        """Temizlik işlemleri"""
        if self.file_monitor:
            self.file_monitor.stop_monitoring()
            
        if self.database_manager:
            self.database_manager.disconnect()

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description='Collective Memory Query System')
    
    # Genel argümanlar
    parser.add_argument('--data-path', default='../data', help='Data directory path')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    # Komut argümanları
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search files')
    search_parser.add_argument('text', nargs='?', help='Search text')
    search_parser.add_argument('-k', '--keywords', help='Keywords (comma-separated)')
    search_parser.add_argument('-t', '--file-types', help='File types (comma-separated)')
    search_parser.add_argument('-d', '--days', type=int, help='Modified in last N days')
    search_parser.add_argument('-s', '--min-size', type=int, help='Minimum file size')
    search_parser.add_argument('-p', '--include-path', help='Include path')
    search_parser.add_argument('-x', '--exclude-path', help='Exclude path')
    search_parser.add_argument('--sort-by', default='relevance', 
                              choices=['relevance', 'date', 'size', 'name'], help='Sort by')
    search_parser.add_argument('--limit', type=int, default=20, help='Result limit')
    
    # Other commands
    subparsers.add_parser('index', help='Reindex all files')
    subparsers.add_parser('stats', help='Show statistics')
    subparsers.add_parser('monitor', help='Start file monitoring')
    
    args = parser.parse_args()
    
    # Interface oluştur
    interface = TerminalInterface(args.data_path)
    
    try:
        if args.interactive or not args.command:
            # İnteraktif mod
            interface.interactive_mode()
        else:
            # Komut modu
            interface.run_command_mode(args)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    finally:
        interface.cleanup()

if __name__ == "__main__":
    main() 