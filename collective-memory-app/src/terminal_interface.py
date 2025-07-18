#!/usr/bin/env python3
"""
Terminal Interface - İnteraktif komut satırı arayüzü
Enhanced semantic search capabilities ile güçlendirilmiş
"""

import os
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Optional

# Try to import tabulate, fallback to simple formatting
try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

# Core imports
from .database_manager import DatabaseManager
from .file_monitor import DataFolderMonitor
from .content_indexer import ContentIndexer
from .query_engine import QueryEngine, SearchQuery, SearchResult

# Enhanced imports
try:
    from .enhanced_query_engine import (
        EnhancedQueryEngine,
        EnhancedSearchQuery,
        EnhancedSearchResult,
    )

    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False
    print("Enhanced query engine not available. Using basic search.")


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
        
        # Connect to database and initialize
        if not self.database_manager.connect():
            print("[-] Database connection failed")
            return
        
        if not self.database_manager.initialize_database():
            print("[-] Database initialization failed")
            return
            
        self.file_monitor = DataFolderMonitor(str(self.data_path))
        self.content_indexer = ContentIndexer()

        # Initialize appropriate query engine
        if ENHANCED_AVAILABLE:
            self.query_engine = EnhancedQueryEngine(self.database_manager)
            self.use_enhanced = True
            print("Enhanced semantic search enabled")
        else:
            self.query_engine = QueryEngine(self.database_manager)
            self.use_enhanced = False
            print("Using basic search mode")

        self.max_results_display = 20
        self.preview_length = 150

        # Enhanced search settings
        self.semantic_search_enabled = True
        self.ai_scoring_enabled = True
        self.entity_extraction_enabled = True

    def interactive_mode(self):
        """Enhanced interactive mode with robust input handling"""
        self._show_welcome_message()
        
        # Initialize interactive session state
        interrupt_count = 0
        max_interrupts = 3
        command_history = []
        
        while True:
            try:
                # Get user input with proper error handling
                user_input = self._get_user_input("search> ")
                
                # Reset interrupt count on successful input
                interrupt_count = 0
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Add to command history
                if user_input not in command_history:
                    command_history.append(user_input)
                    # Keep history limited
                    if len(command_history) > 100:
                        command_history.pop(0)
                
                # Process the command
                if not self._process_interactive_command(user_input):
                    break  # Exit requested
                    
            except KeyboardInterrupt:
                interrupt_count += 1
                if interrupt_count >= max_interrupts:
                    print(f"\n\nExiting due to {max_interrupts} consecutive interrupts...")
                    break
                else:
                    remaining = max_interrupts - interrupt_count
                    print(f"\nPress Ctrl+C {remaining} more time(s) to exit, or continue with commands...")
                    
            except EOFError:
                print("\nEnd of input detected. Exiting...")
                break
                
            except Exception as e:
                print(f"Unexpected error: {e}")
                print("Type 'help' for available commands or 'quit' to exit.")
                # Continue running instead of crashing
                continue
    
    def _show_welcome_message(self):
        """Display welcome message and available commands"""
        print("\n" + "="*60)
        print("[*] Collective Memory Interactive Search")
        print("="*60)
        print(f"[*] Data Path: {self.data_path}")
        print(f"[*]  Database: {self.db_path}")
        
        if self.use_enhanced:
            print("[*] AI-Powered Semantic Search: [+] Enabled")
        else:
            print("[*] Basic Search Mode: [!]  Enhanced features disabled")
        
        print("\n[*] Available Commands:")
        print("  help                    - Show detailed help")
        print("  stats                   - Show database statistics")
        print("  search <term>           - Search for content")
        
        if self.use_enhanced:
            print("  semantic <term>         - Semantic search with AI scoring")
            print("  intent <query>          - Analyze query intent")
            print("  suggestions <term>      - Get semantic suggestions")
            print("  settings                - Show/modify search settings")
        
        print("  quit | exit             - Exit interactive mode")
        print("  history                 - Show command history")
        print("\n[!] Tip: Type any command without arguments for usage help")
        print("="*60 + "\n")
    
    def _get_user_input(self, prompt: str) -> str:
        """Get user input with comprehensive error handling"""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            # Re-raise these to be handled by the main loop
            raise
        except Exception as e:
            print(f"Input error: {e}")
            return ""
    
    def _process_interactive_command(self, user_input: str) -> bool:
        """Process interactive command and return False if exit requested"""
        try:
            # Validate input
            if not self._validate_command_input(user_input):
                return True  # Continue running
            
            # Parse command and arguments
            parts = user_input.split(" ", 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            # Handle exit commands
            if command in ["quit", "exit", "q"]:
                print("\n[-] Goodbye!")
                return False
            
            # Handle help command
            elif command == "help":
                if args:
                    self._show_command_help(args.strip())
                else:
                    self._show_interactive_help()
            
            # Handle stats command
            elif command == "stats":
                self._show_statistics()
            
            # Handle search command
            elif command == "search":
                if args:
                    self._execute_search_command(args)
                else:
                    print("[-] Please provide search terms")
                    print("[!] Usage: search <your search terms>")
            
            # Handle semantic search (enhanced mode only)
            elif command == "semantic":
                if not self.use_enhanced:
                    print("[-] Semantic search not available in basic mode")
                    print("[!] Install sentence-transformers for enhanced features")
                elif args:
                    self._perform_semantic_search(args)
                else:
                    print("[-] Please provide search terms")
                    print("[!] Usage: semantic <your search terms>")
            
            # Handle intent analysis (enhanced mode only)
            elif command == "intent":
                if not self.use_enhanced:
                    print("[-] Intent analysis not available in basic mode")
                elif args:
                    self._analyze_query_intent(args)
                else:
                    print("[-] Please provide a query")
                    print("[!] Usage: intent <your query>")
            
            # Handle suggestions (enhanced mode only)
            elif command == "suggestions":
                if not self.use_enhanced:
                    print("[-] Suggestions not available in basic mode")
                elif args:
                    self._show_semantic_suggestions(args)
                else:
                    print("[-] Please provide a term")
                    print("[!] Usage: suggestions <your term>")
            
            # Handle settings (enhanced mode only)
            elif command == "settings":
                if not self.use_enhanced:
                    print("[-] Settings not available in basic mode")
                else:
                    self._show_search_settings()
            
            # Handle history command
            elif command == "history":
                print("[*] Command history feature coming soon!")
            
            # Handle unknown commands
            else:
                self._handle_unknown_command(command)
            
            return True  # Continue running
            
        except Exception as e:
            print(f"[-] Error processing command '{user_input}': {e}")
            print("[!] Type 'help' for available commands")
            return True  # Continue running despite error
    
    def _validate_command_input(self, user_input: str) -> bool:
        """Validate command input"""
        if not user_input or not user_input.strip():
            return False
        
        if len(user_input) > 1000:  # Prevent extremely long commands
            print("[-] Command too long (max 1000 characters)")
            return False
        
        return True
    
    def _execute_search_command(self, search_terms: str):
        """Execute basic search command"""
        try:
            query = SearchQuery(text=search_terms)
            print(f"[*] Searching for: '{search_terms}'")
            results = self.query_engine.search(query)
            self._display_search_results(results, query)
        except Exception as e:
            print(f"[-] Search failed: {e}")
            print("[!] Try simplifying your search terms")
    
    def _show_interactive_help(self):
        """Show comprehensive interactive help"""
        print("\n" + "="*60)
        print("[*] Collective Memory - Interactive Help")
        print("="*60)
        
        print("\n[*] Basic Search Commands:")
        print("  search <terms>          - Search for content in files")
        print("  stats                   - Show database statistics")
        print("  help [command]          - Show help (optionally for specific command)")
        
        if self.use_enhanced:
            print("\n[*] AI-Enhanced Commands:")
            print("  semantic <terms>        - AI-powered semantic search")
            print("  intent <query>          - Analyze what you're looking for")
            print("  suggestions <term>      - Get related search suggestions")
            print("  settings                - Configure search behavior")
        
        print("\n[*]  System Commands:")
        print("  history                 - Show recent commands")
        print("  quit | exit | q         - Exit interactive mode")
        
        print("\n[!] Tips:")
        print("  • Use quotes for exact phrases: search \"exact phrase\"")
        print("  • Commands are case-insensitive")
        print("  • Press Ctrl+C three times to force exit")
        print("  • Type 'help <command>' for detailed command help")
        
        if not self.use_enhanced:
            print("\n[!]  Enhanced Features Disabled:")
            print("  Install sentence-transformers for AI-powered search")
        
        print("="*60)
    
    def _show_command_help(self, command: str):
        """Show help for specific command"""
        command = command.lower()
        
        if command == "search":
            print("\n[*] Search Command Help:")
            print("  Usage: search <your search terms>")
            print("  Description: Search for content across all indexed files")
            print("  Examples:")
            print("    search database")
            print("    search \"user authentication\"")
            print("    search API documentation")
        
        elif command == "semantic" and self.use_enhanced:
            print("\n[*] Semantic Search Help:")
            print("  Usage: semantic <your search terms>")
            print("  Description: AI-powered search that understands meaning")
            print("  Examples:")
            print("    semantic how to connect database")
            print("    semantic user login process")
            print("    semantic error handling patterns")
        
        elif command == "stats":
            print("\n[*] Statistics Command Help:")
            print("  Usage: stats")
            print("  Description: Show database and indexing statistics")
            print("  Information displayed:")
            print("    • Total indexed files")
            print("    • File type distribution")
            print("    • Recent file activity")
        
        elif command in ["quit", "exit"]:
            print("\n[*] Exit Commands Help:")
            print("  Usage: quit | exit | q")
            print("  Description: Exit interactive mode")
            print("  Alternative: Press Ctrl+C three times")
        
        else:
            print(f"[-] No help available for command: {command}")
            print("[!] Type 'help' to see all available commands")
    
    def _handle_unknown_command(self, command: str):
        """Handle unknown commands with suggestions"""
        print(f"[-] Unknown command: '{command}'")
        
        # Simple command suggestions
        suggestions = []
        available_commands = ["search", "stats", "help", "quit", "exit"]
        
        if self.use_enhanced:
            available_commands.extend(["semantic", "intent", "suggestions", "settings"])
        
        # Find similar commands (simple string matching)
        for cmd in available_commands:
            if command in cmd or cmd in command:
                suggestions.append(cmd)
        
        if suggestions:
            print(f"[!] Did you mean: {', '.join(suggestions)}?")
        else:
            print("[!] Type 'help' to see all available commands")

    def _perform_semantic_search(self, query_text: str):
        """Perform enhanced semantic search"""
        if not self.use_enhanced:
            print("Enhanced search not available")
            return

        print(f"\nSemantic Search: '{query_text}'")

        # Create enhanced query
        query = EnhancedSearchQuery(
            text=query_text,
            use_semantic_search=self.semantic_search_enabled,
            use_ai_scoring=self.ai_scoring_enabled,
            extract_entities=self.entity_extraction_enabled,
            semantic_similarity_threshold=0.6,
        )

        # Analyze intent first
        intent = self.query_engine.analyze_query_intent(query_text)
        print(f"Detected Intent: {intent}")

        # Perform search
        results = self.query_engine.search(query)
        self._display_enhanced_results(results, query)

    def _run_semantic_search_command(self, args):
        """Execute semantic search from command line arguments"""
        if not self.use_enhanced:
            print("[-] Enhanced semantic search is not available.")
            print("[!] Install sentence-transformers for semantic search capabilities:")
            print("   pip install sentence-transformers")
            return

        # Join query arguments
        query_text = " ".join(args.query)
        
        if not query_text.strip():
            print("[-] Please provide search terms")
            print("[!] Usage: semantic <your search terms>")
            return

        print(f"[*] Performing semantic search for: '{query_text}'")
        
        try:
            # Create enhanced query with command line options
            query = EnhancedSearchQuery(
                text=query_text,
                use_semantic_search=True,
                use_ai_scoring=not args.no_ai_scoring,
                extract_entities=not args.no_entities,
                semantic_similarity_threshold=args.threshold,
            )
            
            # Apply filters
            if args.type:
                # Add file type filter
                query.file_types = [f".{args.type.lstrip('.')}"]
                
            if args.days:
                # Add date filter
                query.date_from = datetime.now(timezone.utc) - timedelta(days=args.days)
            
            # Set sorting and limit
            query.sort_by = args.sort
            query.limit = args.limit
            
            # Show configuration
            print(f"[*] Configuration:")
            print(f"   • AI Scoring: {'[+] Enabled' if not args.no_ai_scoring else '[-] Disabled'}")
            print(f"   • Entity Extraction: {'[+] Enabled' if not args.no_entities else '[-] Disabled'}")
            print(f"   • Similarity Threshold: {args.threshold}")
            print(f"   • Sort By: {args.sort}")
            print(f"   • Max Results: {args.limit}")
            
            if args.type:
                print(f"   • File Type Filter: {args.type}")
            if args.days:
                print(f"   • Date Filter: Last {args.days} days")
            
            # Analyze intent first
            if not args.no_ai_scoring:
                intent = self.query_engine.analyze_query_intent(query_text)
                print(f"[*] Detected Intent: {intent}")
            
            # Perform search
            print("[*] Searching...")
            results = self.query_engine.search(query)
            
            # Display results
            self._display_enhanced_results(results, query)
            
        except Exception as e:
            print(f"[-] Semantic search failed: {e}")
            print("[!] Try using basic search instead: search <your terms>")

    def _analyze_query_intent(self, query_text: str):
        """Analyze and display query intent"""
        if not self.use_enhanced:
            print("Enhanced features not available")
            return

        intent = self.query_engine.analyze_query_intent(query_text)
        print("\nQuery Intent Analysis")
        print(f"Query: '{query_text}'")
        print(f"Detected Intent: {intent}")

        # Provide intent-specific suggestions
        if intent == "explain":
            print(
                "Tip: Looking for explanatory content. Try semantic search for better results."
            )
        elif intent == "find":
            print(
                "Tip: Searching for specific items. Consider using filters for better results."
            )
        elif intent == "list":
            print("Tip: Looking for comprehensive lists. Try broader search terms.")
        elif intent == "compare":
            print(
                "Tip: Comparing concepts. Use semantic search to find related content."
            )

    def _show_semantic_suggestions(self, query_text: str):
        """Show semantic query suggestions"""
        if not self.use_enhanced:
            print("Enhanced features not available")
            return

        suggestions = self.query_engine.get_semantic_suggestions(query_text, limit=5)

        print(f"\nSemantic Suggestions for '{query_text}'")
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")
        else:
            print("No suggestions available")

    def _show_search_settings(self):
        """Show and allow modification of search settings"""
        print("\nSearch Settings")
        print(
            f"1. Semantic Search: {'Enabled' if self.semantic_search_enabled else 'Disabled'}"
        )
        print(f"2. AI Scoring: {'Enabled' if self.ai_scoring_enabled else 'Disabled'}")
        print(
            f"3. Entity Extraction: {'Enabled' if self.entity_extraction_enabled else 'Disabled'}"
        )
        print(f"4. Max Results: {self.max_results_display}")

        print("\nToggle settings by typing number (1-4) or press Enter to continue:")
        choice = input().strip()

        if choice == "1":
            self.semantic_search_enabled = not self.semantic_search_enabled
            print(
                f"Semantic Search: {'Enabled' if self.semantic_search_enabled else 'Disabled'}"
            )
        elif choice == "2":
            self.ai_scoring_enabled = not self.ai_scoring_enabled
            print(f"AI Scoring: {'Enabled' if self.ai_scoring_enabled else 'Disabled'}")
        elif choice == "3":
            self.entity_extraction_enabled = not self.entity_extraction_enabled
            print(
                f"Entity Extraction: {'Enabled' if self.entity_extraction_enabled else 'Disabled'}"
            )
        elif choice == "4":
            try:
                new_max = int(input("Enter new max results (10-100): "))
                if 10 <= new_max <= 100:
                    self.max_results_display = new_max
                    print(f"Max Results set to: {new_max}")
                else:
                    print("Please enter a number between 10 and 100")
            except ValueError:
                print("Invalid number")

    def _display_enhanced_results(
        self, results: List, query, save_to_file: Optional[str] = None
    ):
        """Display enhanced search results with AI scores"""

        if not results:
            message = "No results found"
            print(message)
            if save_to_file:
                self._save_results_to_file([], query, save_to_file, message)
            return

        message = f"Found {len(results)} results with AI-powered scoring"
        print(f"\n{message}")

        # Display results with enhanced information
        for i, result in enumerate(results[: self.max_results_display], 1):
            print(f"\n {i}. {result.file_name}")
            print(f"   {result.file_path}")
            print(
                f"   Size: {self._format_file_size(result.file_size)} | Modified: {result.modified_at}"
            )

            # Enhanced scoring information
            if self.use_enhanced:
                print(
                    f"   Relevance: {result.relevance_score:.2f} | Semantic: {result.semantic_score:.2f}"
                )
                print(
                    f"   AI Scores - Quality: {result.content_quality_score:.2f} | Freshness: {result.freshness_score:.2f}"
                )

                # Show detected entities if available
                if result.detected_entities:
                    entities_str = ", ".join(result.detected_entities[:5])
                    print(f"   Entities: {entities_str}")

                # Show contextual snippets
                if result.contextual_snippets:
                    print(f"   Context: {result.contextual_snippets[0][:100]}...")

            # Show highlights
            if result.match_highlights:
                highlights_str = " | ".join(result.match_highlights[:3])
                print(f"   Highlights: {highlights_str}")

            # Show content preview
            preview = (
                result.content_preview[:150] + "..."
                if len(result.content_preview) > 150
                else result.content_preview
            )
            print(f"   Preview: {preview}")

        # Show additional results info
        if len(results) > self.max_results_display:
            remaining = len(results) - self.max_results_display
            print(f"\n {remaining} more results available. Use settings to show more.")

        # Save to file if requested
        if save_to_file:
            self._save_enhanced_results_to_file(results, query, save_to_file, message)

    def _save_enhanced_results_to_file(
        self, results: List, query, file_path: str, message: str
    ):
        """Save enhanced search results to file"""
        try:
            # Use collective-memory directory for saving
            if not os.path.isabs(file_path):
                file_path = self.collective_memory_dir / file_path

            with open(file_path, "w", encoding="utf-8") as f:
                # Write header
                f.write(f"# Enhanced Search Results\n\n")
                f.write(f"**Query:** {query.text}\n")
                f.write(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Results:** {len(results)}\n")
                f.write(f"**Mode:** AI-Powered Semantic Search\n\n")

                # Write settings
                f.write(f"## Search Settings\n\n")
                f.write(
                    f"- Semantic Search: {'Enabled' if query.use_semantic_search else 'Disabled'}\n"
                )
                f.write(
                    f"- AI Scoring: {'Enabled' if query.use_ai_scoring else 'Disabled'}\n"
                )
                f.write(
                    f"- Entity Extraction: {'Enabled' if query.extract_entities else 'Disabled'}\n"
                )
                f.write(
                    f"- Similarity Threshold: {query.semantic_similarity_threshold}\n\n"
                )

                # Write results
                f.write(f"## Results\n\n")
                for i, result in enumerate(results, 1):
                    f.write(f"### {i}. {result.file_name}\n\n")
                    f.write(f"- **Path:** `{result.file_path}`\n")
                    f.write(f"- **Size:** {self._format_file_size(result.file_size)}\n")
                    f.write(f"- **Modified:** {result.modified_at}\n")
                    f.write(f"- **Relevance Score:** {result.relevance_score:.3f}\n")
                    f.write(f"- **Semantic Score:** {result.semantic_score:.3f}\n")
                    f.write(
                        f"- **Content Quality:** {result.content_quality_score:.3f}\n"
                    )
                    f.write(f"- **Freshness:** {result.freshness_score:.3f}\n")

                    if result.detected_entities:
                        entities_str = ", ".join(result.detected_entities)
                        f.write(f"- **Entities:** {entities_str}\n")

                    if result.match_highlights:
                        highlights_str = " | ".join(result.match_highlights)
                        f.write(f"- **Highlights:** {highlights_str}\n")

                    f.write(
                        f"\n**Preview:**\n```\n{result.content_preview[:300]}\n```\n\n"
                    )

                    if result.contextual_snippets:
                        f.write(f"**Context Snippets:**\n")
                        for snippet in result.contextual_snippets:
                            f.write(f"- {snippet}\n")
                        f.write(f"\n")

                    f.write(f"---\n\n")

            print(f"\nEnhanced results saved to: {file_path}")

        except Exception as e:
            print(f"\nFailed to save results: {e}")

    def _show_help(self):
        """Yardım mesajını gösterir"""
        help_text = f"""
Collective Memory Query System - Help

Basic Search:
  search <term>           - Simple text search
  find <term>             - Alias for search
  <term>                  - Direct search (no command needed)

Advanced Search:
  search -k keyword1,keyword2    - Search by keywords
  search -t md,txt               - Search specific file types
  search -d 7                    - Files modified in last 7 days
  search -s 1000                 - Files larger than 1000 bytes
  search -p docs/                - Search in specific path

Filters:
  search "exact phrase"          - Exact phrase matching
  search term -x exclude_path    - Exclude specific paths
  search term --sort date        - Sort by date/size/name/relevance
  search term --limit 10         - Limit results

System Commands:
  help                   - Show this help
  stats                  - Show system statistics
  index                  - Reindex all files
  monitor                - Start file monitoring
  cursor_history [--limit=N] [--workspaces]  - Cursor chat geçmişini göster
  quit/exit/q            - Exit program

Examples:
  search Context7                    - Find files containing "Context7"
  search -k todo,implementation      - Find files with specific keywords
  search -t md -d 3                  - Markdown files from last 3 days
  search "Context7 ERP" -p docs/     - Exact phrase in docs folder
"""
        print(help_text)

    def _show_statistics(self):
        """Sistem istatistiklerini gösterir"""
        print("\nSystem Statistics")

        try:
            stats = self.query_engine.get_search_statistics()

            if not stats:
                print("No statistics available")
                return

            print(f"  Total files: {stats.get('total_files', 0)}")

            # File types
            file_types = stats.get("file_types", [])
            if file_types:
                print("\n  File types:")
                for ext, count in file_types[:10]:  # Top 10
                    print(f"    {ext or 'no extension'}: {count} files")

            # Recent files
            recent_files = stats.get("recent_files", [])
            if recent_files:
                print("\n  Recent files:")
                for name, date in recent_files:
                    print(f"    {name}: {date}")

        except Exception as e:
            print(f"Error getting statistics: {e}")

    def _reindex_all_files(self):
        """Tüm dosyaları yeniden indeksler"""
        print("\nReindexing all files...")

        try:
            indexed_count = 0
            for root, dirs, files in os.walk(self.data_path):
                for file in files:
                    file_path = Path(root) / file

                    # Sadece markdown dosyaları
                    if file_path.suffix.lower() in [".md", ".markdown", ".txt"]:
                        try:
                            file_id = self.database_manager.add_or_update_file(
                                str(file_path)
                            )
                            if file_id:
                                indexed_count += 1
                        except Exception as e:
                            print(f"Error indexing {file_path}: {e}")

            print(f"Reindexing completed: {indexed_count} files processed")

        except Exception as e:
            print(f"Reindexing failed: {e}")

    def _start_file_monitoring(self):
        """Dosya izlemeyi başlatır"""
        if self.file_monitor and self.file_monitor.is_running:
            print("File monitoring already running")
            return

        try:
            self.file_monitor = DataFolderMonitor(
                str(self.data_path), callback=self._on_file_change
            )

            print("Starting file monitoring...")
            print("Press Ctrl+C to stop monitoring and return to search")

            self.file_monitor.run_forever()

        except Exception as e:
            print(f"File monitoring error: {e}")

    def _on_file_change(
        self, event_type: str, src_path: str, dest_path: Optional[str] = None
    ):
        """Dosya değişikliği callback'i"""
        if event_type in ["created", "modified"]:
            try:
                file_id = self.database_manager.add_or_update_file(src_path)
                if file_id:
                    print(f"File indexed: {Path(src_path).name}")
            except Exception as e:
                print(f"Indexing error: {e}")

    def _process_search_command(self, command: str):
        """Arama komutunu işler"""

        # Komut parsing
        query = self._parse_search_command(command)

        if not query:
            return

        # Arama yap
        print("\nSearching...")
        results = self.query_engine.search(query)

        # Sonuçları göster
        self._display_search_results(results, query)

    def _parse_search_command(self, command: str) -> Optional[SearchQuery]:
        """Arama komutunu parse eder"""

        try:
            # Basit komut parsing
            parts = command.split()

            # "search" veya "find" keyword'ünü kaldır
            if parts[0].lower() in ["search", "find"]:
                parts = parts[1:]

            if not parts:
                print("Empty search query")
                return None

            query = SearchQuery()

            # Argümanları parse et
            i = 0
            while i < len(parts):
                part = parts[i]

                if part.startswith("-"):
                    # Flag parsing
                    if part == "-k" and i + 1 < len(parts):
                        # Keywords
                        query.keywords = parts[i + 1].split(",")
                        i += 2
                    elif part == "-t" and i + 1 < len(parts):
                        # File types
                        query.file_types = parts[i + 1].split(",")
                        i += 2
                    elif part == "-d" and i + 1 < len(parts):
                        # Days ago
                        days = int(parts[i + 1])
                        query.date_from = datetime.now(timezone.utc) - timedelta(days=days)
                        i += 2
                    elif part == "-s" and i + 1 < len(parts):
                        # Min size
                        query.min_size = int(parts[i + 1])
                        i += 2
                    elif part == "-p" and i + 1 < len(parts):
                        # Include paths
                        query.include_paths = [parts[i + 1]]
                        i += 2
                    elif part == "-x" and i + 1 < len(parts):
                        # Exclude paths
                        query.exclude_paths = [parts[i + 1]]
                        i += 2
                    elif part == "--sort" and i + 1 < len(parts):
                        # Sort by
                        query.sort_by = parts[i + 1]
                        i += 2
                    elif part == "--limit" and i + 1 < len(parts):
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
                        query.text += " " + part
                    i += 1

            return query

        except Exception as e:
            print(f"Error parsing command: {e}")
            return None

    def _display_search_results(
        self,
        results: List[SearchResult],
        query: SearchQuery,
        save_to_file: Optional[str] = None,
    ):
        """Arama sonuçlarını gösterir ve isteğe bağlı olarak dosyaya kaydeder"""

        if not results:
            message = "No results found"
            print(message)
            if save_to_file:
                self._save_results_to_file([], query, save_to_file, message)
            return

        message = f"Found {len(results)} results"
        print(f"\n{message}")

        # Dosyaya kaydet
        if save_to_file:
            self._save_results_to_file(results, query, save_to_file, message)

        # Sonuçları tablo formatında göster
        table_data = []
        for i, result in enumerate(results[: self.max_results_display], 1):

            # File size formatı
            size_str = self._format_file_size(result.file_size)

            # Modified date formatı
            try:
                date_str = datetime.fromisoformat(
                    result.modified_at.replace("Z", "+00:00")
                ).strftime("%Y-%m-%d %H:%M")
            except:
                date_str = result.modified_at[:16]

            # Preview
            preview = result.content_preview[: self.preview_length]
            if len(result.content_preview) > self.preview_length:
                preview += "..."

            table_data.append(
                [
                    i,
                    result.file_name,
                    result.file_extension,
                    size_str,
                    date_str,
                    (
                        f"{result.relevance_score:.1f}"
                        if query.sort_by == "relevance"
                        else "-"
                    ),
                    preview,
                ]
            )

        headers = ["#", "File", "Type", "Size", "Modified", "Score", "Preview"]
        if TABULATE_AVAILABLE:
            print(f"\n{tabulate(table_data, headers=headers, tablefmt='grid')}")
        else:
            # Simple table formatting fallback
            print(f"\n{' | '.join(headers)}")
            print("-" * 80)
            for row in table_data:
                print(f"{' | '.join(str(cell) for cell in row)}")

        # Highlights göster
        if results and results[0].match_highlights:
            print(f"\nMatch highlights (first result):")
            for highlight in results[0].match_highlights[:3]:
                print(f"  ... {highlight.strip()} ...")

        # Daha fazla sonuç varsa bildir
        if len(results) > self.max_results_display:
            remaining = len(results) - self.max_results_display
            print(f"\n {remaining} more results available. Use --limit to show more.")

    def _save_results_to_file(
        self,
        results: List[SearchResult],
        query: SearchQuery,
        file_path: str,
        message: str,
    ):
        """Arama sonuçlarını dosyaya kaydeder"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Header
                f.write(f"# Collective Memory - Search Results\n\n")
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
                        date_str = datetime.fromisoformat(
                            result.modified_at.replace("Z", "+00:00")
                        ).strftime("%Y-%m-%d %H:%M")
                    except:
                        date_str = result.modified_at[:16]
                    f.write(f"- **Modified:** {date_str}\n")

                    # Score
                    if query.sort_by == "relevance":
                        f.write(
                            f"- **Relevance Score:** {result.relevance_score:.1f}\n"
                        )

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

                f.write(
                    f"*Generated by Collective Memory v1.0.0 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
                )

            print(f"Results saved to: {file_path}")

        except Exception as e:
            print(f"Error saving file: {e}")

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

        if args.command == "search":
            query = SearchQuery(
                text=args.text or "",
                keywords=args.keywords.split(",") if args.keywords else [],
                file_types=args.file_types.split(",") if args.file_types else [],
                sort_by=args.sort_by,
                limit=args.limit,
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

        elif args.command == "semantic":
            self._run_semantic_search_command(args)

        elif args.command == "index":
            self._reindex_all_files()

        elif args.command == "stats":
            self._show_statistics()

        elif args.command == "monitor":
            self._start_file_monitoring()

    def cmd_cursor_history(self, args: str):
        """Cursor chat geçmişini görüntüle - Enhanced version"""
        if not self.data_path:
            print("Data path belirtilmedi. --data-path kullanın.")
            return

        try:
            cursor_reader = EnhancedCursorDatabaseReader()

            if not cursor_reader.is_cursor_available():
                print("Cursor veritabanı bulunamadı.")
                return

            # Argüman parsing
            parts = args.strip().split() if args.strip() else []
            limit = 10
            show_workspaces = False

            for part in parts:
                if part.startswith("--limit="):
                    try:
                        limit = int(part.split("=")[1])
                    except ValueError:
                        print(f"Geçersiz limit değeri: {part}")
                        return
                elif part == "--workspaces":
                    show_workspaces = True

            if show_workspaces:
                # Tüm workspace'leri göster
                print("Cursor Workspace Özeti:")
                workspaces = cursor_reader.get_all_workspaces_summary()

                if not workspaces:
                    print("Hiçbir workspace bulunamadı.")
                    return

                for workspace_key, workspace_data in workspaces.items():
                    info = workspace_data["info"]
                    print(f"\n{workspace_key}")
                    print(f"   Path: {info.get('path', 'Bilinmiyor')}")
                    print(f"   Chat sayısı: {workspace_data['chat_count']}")
                    print(
                        f"   Son aktivite: {workspace_data.get('last_activity', 'Bilinmiyor')}"
                    )
                    print(f"   DB: {workspace_data['db_path']}")

            else:
                # Mevcut proje için chat geçmişi
                print(f"Cursor Chat Geçmişi ({limit} sonuç):")
                chats = cursor_reader.get_project_chat_history(self.data_path, limit)

                if not chats:
                    print("Bu proje için chat geçmişi bulunamadı.")
                    return

                for i, chat in enumerate(chats, 1):
                    chat_type = chat.get("type", "unknown")
                    key_type = chat.get("key_type", "unknown")
                    summary = chat.get("summary", "Özet yok")

                    # Chat type icons
                    type_icons = {
                        "conversation": "[C]",
                        "code_generation": "[G]",
                        "inline_chat": "[I]",
                        "message_array": "[M]",
                        "raw_content": "[R]",
                        "raw_string": "[S]",
                    }

                    icon = type_icons.get(chat_type, "[?]")

                    print(f"\n{i:2d}. {icon} [{chat_type}] - {key_type}")
                    print(f"     ID: {chat.get('id', 'N/A')}")
                    print(f"     Özet: {summary}")

                    # Ek bilgiler
                    if "message_count" in chat:
                        print(f"     Mesaj sayısı: {chat['message_count']}")

                    if "prompt" in chat and "response" in chat:
                        prompt_preview = (
                            chat["prompt"][:100] + "..."
                            if len(chat["prompt"]) > 100
                            else chat["prompt"]
                        )
                        print(f"     Prompt: {prompt_preview}")

        except Exception as e:
            print(f"Cursor geçmiş okuma hatası: {e}")

    def cmd_help(self, args: str):
        """Yardım komutlarını göster"""
        # ... existing help content ...

        print("Enhanced Cursor Commands:")
        print(
            "  cursor_history [--limit=N] [--workspaces]  - Cursor chat geçmişini göster"
        )
        print("    Örnekler:")
        print("      cursor_history                          - Son 10 chat'i göster")
        print("      cursor_history --limit=20               - Son 20 chat'i göster")
        print(
            "      cursor_history --workspaces             - Tüm workspace'leri göster"
        )

    def cleanup(self):
        """Temizlik işlemleri"""
        if self.file_monitor:
            self.file_monitor.stop_monitoring()

        if self.database_manager:
            self.database_manager.disconnect()


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description="Collective Memory Query System")

    # Genel argümanlar
    parser.add_argument("--data-path", default="../data", help="Data directory path")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )

    # Komut argümanları
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search command
    search_parser = subparparsers.add_parser("search", help="Search files")
    search_parser.add_argument("text", nargs="?", help="Search text")
    search_parser.add_argument("-k", "--keywords", help="Keywords (comma-separated)")
    search_parser.add_argument(
        "-t", "--file-types", help="File types (comma-separated)"
    )
    search_parser.add_argument("-d", "--days", type=int, help="Modified in last N days")
    search_parser.add_argument("-s", "--min-size", type=int, help="Minimum file size")
    search_parser.add_argument("-p", "--include-path", help="Include path")
    search_parser.add_argument("-x", "--exclude-path", help="Exclude path")
    search_parser.add_argument(
        "--sort-by",
        default="relevance",
        choices=["relevance", "date", "size", "name"],
        help="Sort by",
    )
    search_parser.add_argument("--limit", type=int, default=20, help="Result limit")

    # Semantic search command (enhanced mode)
    semantic_parser = subparsers.add_parser("semantic", help="Semantic search with AI scoring")
    semantic_parser.add_argument("query", nargs="+", help="Search query text")
    semantic_parser.add_argument(
        "--type", "-t", help="Filter by file type (e.g., md, py)"
    )
    semantic_parser.add_argument(
        "--days", "-d", type=int, help="Filter by days (e.g., 7 for last week)"
    )
    semantic_parser.add_argument(
        "--limit", "-l", type=int, default=10, help="Limit results (default: 10)"
    )
    semantic_parser.add_argument(
        "--sort", "-s", choices=["relevance", "date", "size"],
        default="relevance", help="Sort results by (default: relevance)"
    )
    semantic_parser.add_argument(
        "--threshold", type=float, default=0.6, 
        help="Semantic similarity threshold (0.0-1.0, default: 0.6)"
    )
    semantic_parser.add_argument(
        "--no-ai-scoring", action="store_true", 
        help="Disable AI scoring (faster but less accurate)"
    )
    semantic_parser.add_argument(
        "--no-entities", action="store_true", 
        help="Disable entity extraction"
    )

    # Other commands
    subparsers.add_parser("index", help="Reindex all files")
    subparsers.add_parser("stats", help="Show statistics")
    subparsers.add_parser("monitor", help="Start file monitoring")

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
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        interface.cleanup()


if __name__ == "__main__":
    main()