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

# Try to import readline for auto-completion and history navigation
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

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
from .progress_manager import ProgressManager
from .command_processor import CommandProcessor

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

        # Initialize progress manager
        self.progress_manager = ProgressManager()

        # Enhanced search settings
        self.semantic_search_enabled = True
        self.ai_scoring_enabled = True
        self.entity_extraction_enabled = True

    def interactive_mode(self):
        """Enhanced interactive mode with CommandProcessor"""
        self._show_welcome_message()
        
        # Initialize command processor
        command_processor = CommandProcessor(self)
        
        # Initialize interactive session state
        interrupt_count = 0
        max_interrupts = 3
        
        while True:
            try:
                # Get user input with proper error handling
                user_input = self._get_user_input("search> ")
                
                # Reset interrupt count on successful input
                interrupt_count = 0
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Process the command using CommandProcessor
                if not command_processor.process_command(user_input):
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
        print("🧠 Collective Memory Interactive Search v4.0")
        print("="*60)
        print(f"📁 Data Path: {self.data_path}")
        print(f"🗄️  Database: {self.db_path}")
        
        if self.use_enhanced:
            print("🤖 AI-Powered Semantic Search: ✅ Enabled")
        else:
            print("🔍 Basic Search Mode: ⚠️  Enhanced features disabled")
        
        print("\n📋 Core Commands:")
        print("  help (h, ?)             - Show detailed help")
        print("  search (s, find)        - Search for content")
        print("  stats (st)              - Show database statistics")
        
        if self.use_enhanced:
            print("\n🤖 AI Commands:")
            print("  semantic (sem)          - Semantic search with AI scoring")
            print("  intent                  - Analyze query intent")
            print("  suggestions             - Get semantic suggestions")
            print("  settings                - Configure search behavior")
        
        print("\n🛠️  System Commands:")
        print("  history                 - Show command history")
        print("  index                   - Reindex all files")
        print("  monitor                 - Start file monitoring")
        print("  clear (cls)             - Clear screen")
        print("  version (v)             - Show version info")
        print("  quit (q, x, exit)       - Exit interactive mode")
        
        print("\n💡 Tips:")
        print("  • Use command aliases for faster typing (e.g., 's' for search)")
        print("  • Type command without arguments for usage help")
        print("  • Press Ctrl+C three times to force exit")
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
        """Execute basic search command with progress feedback"""
        try:
            # Start progress tracking for search
            self.progress_manager.start_operation("Search", show_spinner=True)
            
            # Create query
            self.progress_manager.update_progress(message="Creating search query")
            query = SearchQuery(text=search_terms)
            print(f"\n🔍 Searching for: '{search_terms}'")
            
            # Perform search
            self.progress_manager.update_progress(message="Searching database")
            results = self.query_engine.search(query)
            
            # Finish progress tracking
            self.progress_manager.finish_operation(
                success=True,
                message=f"Found {len(results)} results",
                show_stats=True
            )
            
            # Display results
            self._display_search_results(results, query)
            
        except KeyboardInterrupt:
            self.progress_manager.finish_operation(
                success=False,
                message="Search cancelled by user"
            )
        except Exception as e:
            self.progress_manager.finish_operation(
                success=False,
                message=f"Search failed: {e}"
            )
            print(f"❌ Search failed: {e}")
            print("💡 Try simplifying your search terms")
    
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
        """Perform enhanced semantic search with progress indicators"""
        if not self.use_enhanced:
            print("❌ Enhanced search not available")
            return

        print(f"\n🤖 Semantic Search: '{query_text}'")

        try:
            # Start progress tracking
            self.progress_manager.start_operation("Semantic Search", show_spinner=True)
            
            # Create enhanced query
            self.progress_manager.update_progress(message="Creating enhanced query")
            query = EnhancedSearchQuery(
                text=query_text,
                use_semantic_search=self.semantic_search_enabled,
                use_ai_scoring=self.ai_scoring_enabled,
                extract_entities=self.entity_extraction_enabled,
                semantic_similarity_threshold=0.6,
            )

            # Analyze intent first
            self.progress_manager.update_progress(message="Analyzing query intent")
            intent = self.query_engine.analyze_query_intent(query_text)
            print(f"\n🎯 Detected Intent: {intent}")

            # Perform search
            self.progress_manager.update_progress(message="Performing semantic search")
            results = self.query_engine.search(query)
            
            # Finish progress tracking
            self.progress_manager.finish_operation(
                success=True, 
                message=f"Found {len(results)} results",
                show_stats=True
            )
            
            # Display results
            self._display_enhanced_results(results, query)
            
        except KeyboardInterrupt:
            self.progress_manager.finish_operation(
                success=False, 
                message="Semantic search cancelled by user"
            )
        except Exception as e:
            self.progress_manager.finish_operation(
                success=False, 
                message=f"Semantic search failed: {e}"
            )
            print(f"❌ Error: {e}")

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
        """Reindex all files with enhanced progress tracking and performance feedback"""
        try:
            # Enhanced file type support
            supported_extensions = [
                ".md", ".markdown", ".txt", ".py", ".js", ".ts", ".jsx", ".tsx",
                ".html", ".css", ".json", ".yaml", ".yml", ".xml", ".csv",
                ".rst", ".org", ".tex", ".log"
            ]
            
            # Phase 1: Scanning with progress indicator
            print("📊 Scanning directory structure...")
            self.progress_manager.start_operation("Directory Scan", show_spinner=True)
            
            total_files = 0
            directories_scanned = 0
            file_size_total = 0
            
            for root, dirs, files in os.walk(self.data_path):
                directories_scanned += 1
                self.progress_manager.update_progress(
                    message=f"Scanning {Path(root).name} ({directories_scanned} dirs)"
                )
                
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in supported_extensions:
                        total_files += 1
                        try:
                            file_size_total += file_path.stat().st_size
                        except (OSError, IOError):
                            pass  # Skip files we can't access
                
                # Check for cancellation during scan
                if self.progress_manager.is_cancelled():
                    self.progress_manager.finish_operation(success=False, message="Scan cancelled")
                    return
            
            self.progress_manager.finish_operation(
                success=True,
                message=f"Found {total_files} files in {directories_scanned} directories",
                show_stats=True
            )
            
            if total_files == 0:
                print("📁 No supported files found to index")
                print(f"💡 Supported extensions: {', '.join(supported_extensions)}")
                return
            
            # Show scan summary
            size_mb = file_size_total / (1024 * 1024)
            print(f"📈 Scan Summary: {total_files} files ({size_mb:.1f} MB) in {directories_scanned} directories")
            
            # Phase 2: Indexing with detailed progress
            self.progress_manager.start_operation(
                "File Indexing", 
                total_items=total_files
            )
            
            indexed_count = 0
            error_count = 0
            skipped_count = 0
            bytes_processed = 0
            
            # Set up cancellation handler
            self.progress_manager.set_cancellation_handler(lambda: print("Cleaning up indexing operation..."))
            
            for root, dirs, files in os.walk(self.data_path):
                for file in files:
                    file_path = Path(root) / file

                    # Check for cancellation with enhanced handling
                    if self.progress_manager.is_cancelled():
                        print(f"\n🛑 Indexing cancelled by user")
                        break

                    # Only index supported file types
                    if file_path.suffix.lower() in supported_extensions:
                        try:
                            # Get file info for progress display
                            file_stat = file_path.stat()
                            file_size = file_stat.st_size
                            
                            # Update progress with detailed information
                            size_str = self._format_file_size(file_size)
                            relative_path = file_path.relative_to(self.data_path)
                            
                            self.progress_manager.update_progress(
                                message=f"{relative_path} ({size_str})"
                            )
                            
                            # Perform indexing
                            file_id = self.database_manager.add_or_update_file(str(file_path))
                            
                            if file_id:
                                indexed_count += 1
                                bytes_processed += file_size
                            else:
                                skipped_count += 1
                            
                        except KeyboardInterrupt:
                            self.progress_manager.cancel_operation()
                            break
                        except (OSError, IOError) as e:
                            error_count += 1
                            print(f"\n⚠️  File access error {file_path.name}: {e}")
                        except Exception as e:
                            error_count += 1
                            print(f"\n❌ Indexing error {file_path.name}: {e}")
                    else:
                        # Count unsupported files as skipped
                        skipped_count += 1
                
                # Check for cancellation at directory level
                if self.progress_manager.is_cancelled():
                    break

            # Phase 3: Finish with comprehensive statistics
            if self.progress_manager.is_cancelled():
                self.progress_manager.finish_operation(
                    success=False,
                    message=f"Indexing cancelled - {indexed_count} files processed, {error_count} errors",
                    show_stats=True
                )
            else:
                # Build success message with detailed stats
                success_parts = [f"{indexed_count} files indexed"]
                
                if skipped_count > 0:
                    success_parts.append(f"{skipped_count} skipped")
                if error_count > 0:
                    success_parts.append(f"{error_count} errors")
                
                success_message = ", ".join(success_parts)
                
                self.progress_manager.finish_operation(
                    success=True,
                    message=success_message,
                    show_stats=True
                )
                
                # Show additional statistics
                if bytes_processed > 0:
                    mb_processed = bytes_processed / (1024 * 1024)
                    print(f"📊 Data processed: {mb_processed:.1f} MB")
                
                # Show indexing efficiency
                if indexed_count > 0:
                    print(f"✨ Indexing completed successfully!")
                    if error_count > 0:
                        error_rate = (error_count / total_files) * 100
                        print(f"⚠️  Error rate: {error_rate:.1f}% ({error_count}/{total_files})")
                        
        except Exception as e:
            print(f"❌ Fatal indexing error: {e}")
            self.progress_manager.finish_operation(
                success=False,
                message=f"Indexing failed: {e}"
            )

        except Exception as e:
            self.progress_manager.finish_operation(
                success=False,
                message=f"Indexing failed: {e}"
            )
            print(f"❌ Reindexing failed: {e}")

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


class ProgressManager:
    """Enhanced progress tracking and feedback system for long-running operations"""
    
    def __init__(self):
        self.current_operation = None
        self.start_time = None
        self.progress_bar = None
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.spinner_index = 0
        self.cancelled = False
        self.operation_stack = []  # Stack for nested operations
        self.performance_stats = {}  # Performance tracking
        self.last_update_time = None
        self.update_interval = 0.1  # Minimum time between updates (100ms)
        
        # Try to import tqdm for better progress bars
        try:
            from tqdm import tqdm
            self.tqdm_available = True
            self.tqdm = tqdm
        except ImportError:
            self.tqdm_available = False
            self.tqdm = None
            
        # Try to import threading for cancellation handling
        try:
            import threading
            self.threading_available = True
            self.cancel_event = threading.Event()
        except ImportError:
            self.threading_available = False
            self.cancel_event = None
    
    def start_operation(self, operation_name: str, total_items: int = None, show_spinner: bool = False, 
                       show_eta: bool = True, unit: str = "items"):
        """Start a new operation with enhanced progress tracking"""
        # Handle nested operations
        if self.current_operation:
            self.operation_stack.append({
                'name': self.current_operation,
                'start_time': self.start_time,
                'progress_bar': self.progress_bar
            })
        
        self.current_operation = operation_name
        self.start_time = datetime.now()
        self.cancelled = False
        self.last_update_time = self.start_time
        
        # Clear cancel event if available
        if self.cancel_event:
            self.cancel_event.clear()
        
        print(f"🔄 {operation_name}...")
        
        if total_items and self.tqdm_available:
            # Enhanced tqdm progress bar with ETA and performance metrics
            bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}"
            if show_eta:
                bar_format += " [{elapsed}<{remaining}, {rate_fmt}]"
            else:
                bar_format += " [{elapsed}, {rate_fmt}]"
                
            self.progress_bar = self.tqdm(
                total=total_items,
                desc=operation_name,
                unit=unit,
                bar_format=bar_format,
                dynamic_ncols=True,
                leave=False,
                miniters=1,
                maxinterval=0.5
            )
        elif show_spinner:
            # Enhanced spinner for operations with unknown duration
            print(f"   {self.spinner_chars[0]} Starting...", end='\r')
            self.progress_bar = None
        else:
            # Simple text-based progress
            self.progress_bar = None
            
        # Initialize performance tracking
        self.performance_stats[operation_name] = {
            'start_time': self.start_time,
            'items_processed': 0,
            'last_rate': 0.0
        }
    
    def update_progress(self, current_item: int = None, message: str = None, increment: int = 1, 
                       force_update: bool = False):
        """Update progress with enhanced timing and cancellation handling"""
        if self.cancelled or (self.cancel_event and self.cancel_event.is_set()):
            return False
            
        # Throttle updates to prevent performance issues
        current_time = datetime.now()
        if not force_update and self.last_update_time:
            time_diff = (current_time - self.last_update_time).total_seconds()
            if time_diff < self.update_interval:
                return True
        
        self.last_update_time = current_time
        
        try:
            # Update performance stats
            if self.current_operation in self.performance_stats:
                stats = self.performance_stats[self.current_operation]
                stats['items_processed'] += increment
                
                # Calculate processing rate
                elapsed = (current_time - stats['start_time']).total_seconds()
                if elapsed > 0:
                    stats['last_rate'] = stats['items_processed'] / elapsed
            
            if self.progress_bar and hasattr(self.progress_bar, 'update'):
                # Update tqdm progress bar with enhanced information
                self.progress_bar.update(increment)
                if message:
                    # Include performance info in description
                    perf_info = self._get_performance_info()
                    desc = f"{self.current_operation}: {message}"
                    if perf_info:
                        desc += f" ({perf_info})"
                    self.progress_bar.set_description(desc)
                    
            elif message:
                # Enhanced spinner with performance information
                self.spinner_index = (self.spinner_index + 1) % len(self.spinner_chars)
                spinner = self.spinner_chars[self.spinner_index]
                
                # Add timing information for long operations
                elapsed = (current_time - self.start_time).total_seconds()
                if elapsed > 5:  # Show timing after 5 seconds
                    timing_info = f" ({self._format_duration_short(elapsed)})"
                    print(f"   {spinner} {message}{timing_info}...", end='\r')
                else:
                    print(f"   {spinner} {message}...", end='\r')
            
            return True
            
        except KeyboardInterrupt:
            self.cancelled = True
            print(f"\n⚠️  Operation '{self.current_operation}' cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Progress update error: {e}")
            return True  # Continue despite error
    
    def finish_operation(self, success: bool = True, message: str = None, show_stats: bool = True,
                        show_performance: bool = True):
        """Finish current operation with enhanced statistics and performance feedback"""
        if self.progress_bar and hasattr(self.progress_bar, 'close'):
            self.progress_bar.close()
        
        # Calculate comprehensive duration and performance metrics
        end_time = datetime.now()
        duration = end_time - self.start_time if self.start_time else None
        
        # Get performance statistics
        perf_stats = self.performance_stats.get(self.current_operation, {})
        items_processed = perf_stats.get('items_processed', 0)
        avg_rate = perf_stats.get('last_rate', 0.0)
        
        # Show result with enhanced information
        if self.cancelled or (self.cancel_event and self.cancel_event.is_set()):
            status = "⚠️"
            result_message = f"Operation '{self.current_operation}' was cancelled"
            if items_processed > 0:
                result_message += f" (processed {items_processed} items)"
        elif success:
            status = "✅"
            result_message = message or f"{self.current_operation} completed successfully"
            if items_processed > 0:
                result_message += f" ({items_processed} items processed)"
        else:
            status = "❌"
            result_message = message or f"{self.current_operation} failed"
            if items_processed > 0:
                result_message += f" (processed {items_processed} items before failure)"
        
        print(f"\n{status} {result_message}")
        
        # Show detailed timing and performance information
        if show_stats and duration:
            duration_str = self._format_duration(duration)
            print(f"   ⏱️  Duration: {duration_str}")
            
            if show_performance and items_processed > 0 and avg_rate > 0:
                rate_str = self._format_rate(avg_rate)
                print(f"   📊 Performance: {rate_str}")
                
                # Show efficiency metrics for large operations
                if items_processed > 100:
                    efficiency = self._calculate_efficiency(duration.total_seconds(), items_processed)
                    print(f"   ⚡ Efficiency: {efficiency}")
        
        # Clean up performance stats
        if self.current_operation in self.performance_stats:
            del self.performance_stats[self.current_operation]
        
        # Restore previous operation if nested
        if self.operation_stack:
            prev_op = self.operation_stack.pop()
            self.current_operation = prev_op['name']
            self.start_time = prev_op['start_time']
            self.progress_bar = prev_op['progress_bar']
        else:
            # Reset state
            self.current_operation = None
            self.start_time = None
            self.progress_bar = None
            
        self.cancelled = False
    
    def _get_performance_info(self) -> str:
        """Get current performance information string"""
        if self.current_operation not in self.performance_stats:
            return ""
            
        stats = self.performance_stats[self.current_operation]
        rate = stats.get('last_rate', 0.0)
        
        if rate > 0:
            return self._format_rate(rate)
        return ""
    
    def _format_rate(self, rate: float) -> str:
        """Format processing rate for display"""
        if rate >= 1000:
            return f"{rate/1000:.1f}k items/s"
        elif rate >= 1:
            return f"{rate:.1f} items/s"
        else:
            return f"{rate:.2f} items/s"
    
    def _calculate_efficiency(self, duration_seconds: float, items_processed: int) -> str:
        """Calculate and format efficiency metrics"""
        if duration_seconds <= 0 or items_processed <= 0:
            return "N/A"
            
        items_per_second = items_processed / duration_seconds
        
        if items_per_second >= 100:
            return "Excellent"
        elif items_per_second >= 50:
            return "Good"
        elif items_per_second >= 10:
            return "Fair"
        else:
            return "Slow"
    
    def _format_duration(self, duration) -> str:
        """Format duration for display with enhanced precision"""
        total_seconds = duration.total_seconds()
        
        if total_seconds < 0.001:
            return f"{total_seconds*1000000:.0f}μs"
        elif total_seconds < 1:
            return f"{total_seconds*1000:.0f}ms"
        elif total_seconds < 60:
            return f"{total_seconds:.2f}s"
        elif total_seconds < 3600:
            minutes = int(total_seconds // 60)
            seconds = total_seconds % 60
            return f"{minutes}m {seconds:.1f}s"
        else:
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = total_seconds % 60
            return f"{hours}h {minutes}m {seconds:.0f}s"
    
    def _format_duration_short(self, total_seconds: float) -> str:
        """Format duration in short format for inline display"""
        if total_seconds < 60:
            return f"{total_seconds:.0f}s"
        elif total_seconds < 3600:
            minutes = int(total_seconds // 60)
            return f"{minutes}m"
        else:
            hours = int(total_seconds // 3600)
            return f"{hours}h"
    
    def show_spinner_message(self, message: str, show_timing: bool = True):
        """Show an enhanced spinner with message for unknown duration operations"""
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_chars)
        spinner = self.spinner_chars[self.spinner_index]
        
        if show_timing and self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            if elapsed > 3:  # Show timing after 3 seconds
                timing_info = f" ({self._format_duration_short(elapsed)})"
                print(f"   {spinner} {message}{timing_info}...", end='\r')
                return
        
        print(f"   {spinner} {message}...", end='\r')
    
    def is_cancelled(self) -> bool:
        """Check if operation was cancelled"""
        return self.cancelled or (self.cancel_event and self.cancel_event.is_set())
    
    def cancel_operation(self):
        """Cancel current operation with enhanced cleanup"""
        self.cancelled = True
        
        # Set cancel event if available
        if self.cancel_event:
            self.cancel_event.set()
        
        # Close progress bar
        if self.progress_bar and hasattr(self.progress_bar, 'close'):
            self.progress_bar.close()
        
        # Show cancellation message with timing
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            duration_str = self._format_duration_short(elapsed)
            print(f"\n⚠️  Cancelling '{self.current_operation}' (ran for {duration_str})...")
        else:
            print(f"\n⚠️  Cancelling '{self.current_operation}'...")
    
    def set_cancellation_handler(self, handler_func):
        """Set a custom cancellation handler function"""
        if self.threading_available:
            import signal
            def signal_handler(signum, frame):
                self.cancel_operation()
                if handler_func:
                    handler_func()
            signal.signal(signal.SIGINT, signal_handler)
    
    def get_operation_stats(self) -> dict:
        """Get current operation statistics"""
        if not self.current_operation or self.current_operation not in self.performance_stats:
            return {}
            
        stats = self.performance_stats[self.current_operation].copy()
        if self.start_time:
            stats['elapsed_seconds'] = (datetime.now() - self.start_time).total_seconds()
        return stats


class CommandProcessor:
    """Enhanced command processor with unified command handling, aliases, and suggestions"""
    
    def __init__(self, terminal_interface):
        self.terminal_interface = terminal_interface
        self.commands = self._register_commands()
        self.aliases = self._register_aliases()
        self.command_history = []
        self.history_file = terminal_interface.collective_memory_dir / "config" / "command_history.txt"
        self.max_history = 1000
        self.current_history_index = 0
        
        # Load persistent history
        self._load_history()
        
        # Initialize auto-completion
        self._init_auto_completion()
        
    def _register_commands(self):
        """Register all available commands with their handlers"""
        return {
            'help': self._cmd_help,
            'search': self._cmd_search,
            'semantic': self._cmd_semantic,
            'intent': self._cmd_intent,
            'suggestions': self._cmd_suggestions,
            'settings': self._cmd_settings,
            'stats': self._cmd_stats,
            'history': self._cmd_history,
            'index': self._cmd_index,
            'monitor': self._cmd_monitor,
            'quit': self._cmd_quit,
            'exit': self._cmd_quit,
            'clear': self._cmd_clear,
            'version': self._cmd_version,
        }
    
    def _register_aliases(self):
        """Register command aliases for convenience"""
        return {
            'h': 'help',
            's': 'search',
            'sem': 'semantic',
            'q': 'quit',
            'x': 'exit',
            'st': 'stats',
            'cls': 'clear',
            'v': 'version',
            '?': 'help',
            'find': 'search',
        }
    
    def process_command(self, command_line: str) -> bool:
        """
        Process command with comprehensive error handling and suggestions
        Returns False if exit requested, True otherwise
        """
        try:
            # Validate and parse command
            if not self._validate_command_input(command_line):
                return True
            
            # Add to history
            self._add_to_history(command_line)
            
            # Parse command and arguments
            parts = command_line.strip().split()
            if not parts:
                return True
                
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Resolve aliases
            resolved_command = self.aliases.get(command, command)
            
            # Execute command
            if resolved_command in self.commands:
                return self.commands[resolved_command](args)
            else:
                return self._handle_unknown_command(command, args)
                
        except KeyboardInterrupt:
            print("\n⚠️  Command interrupted")
            return True
        except Exception as e:
            print(f"❌ Error processing command '{command_line}': {e}")
            print("💡 Type 'help' for available commands")
            return True
    
    def _validate_command_input(self, command_line: str) -> bool:
        """Validate command input"""
        if not command_line or not command_line.strip():
            return False
        
        if len(command_line) > 1000:
            print("❌ Command too long (max 1000 characters)")
            return False
        
        return True
    
    def _add_to_history(self, command_line: str):
        """Add command to history"""
        if command_line and command_line not in self.command_history:
            self.command_history.append(command_line)
            # Keep history limited
            if len(self.command_history) > 100:
                self.command_history.pop(0)
    
    def _handle_unknown_command(self, command: str, args: list) -> bool:
        """Handle unknown commands with intelligent suggestions"""
        print(f"❌ Unknown command: '{command}'")
        
        # Find similar commands using simple string matching
        suggestions = self._find_similar_commands(command)
        
        if suggestions:
            print(f"💡 Did you mean: {', '.join(suggestions)}?")
        else:
            print("💡 Type 'help' to see all available commands")
        
        return True
    
    def _find_similar_commands(self, command: str) -> list:
        """Find similar commands using string similarity"""
        suggestions = []
        all_commands = list(self.commands.keys()) + list(self.aliases.keys())
        
        # Exact substring matches
        for cmd in all_commands:
            if command in cmd or cmd in command:
                if cmd not in suggestions:
                    suggestions.append(cmd)
        
        # Levenshtein-like similarity (simple version)
        if not suggestions:
            for cmd in all_commands:
                if self._simple_similarity(command, cmd) > 0.6:
                    if cmd not in suggestions:
                        suggestions.append(cmd)
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _simple_similarity(self, s1: str, s2: str) -> float:
        """Simple string similarity calculation"""
        if not s1 or not s2:
            return 0.0
        
        # Simple character overlap ratio
        s1_chars = set(s1.lower())
        s2_chars = set(s2.lower())
        
        if not s1_chars or not s2_chars:
            return 0.0
        
        intersection = len(s1_chars.intersection(s2_chars))
        union = len(s1_chars.union(s2_chars))
        
        return intersection / union if union > 0 else 0.0
    
    # Command handlers
    def _cmd_help(self, args: list) -> bool:
        """Handle help command"""
        if args:
            command = args[0].lower()
            resolved_command = self.aliases.get(command, command)
            self.terminal_interface._show_command_help(resolved_command)
        else:
            self.terminal_interface._show_interactive_help()
        return True
    
    def _cmd_search(self, args: list) -> bool:
        """Handle search command"""
        if args:
            search_terms = " ".join(args)
            self.terminal_interface._execute_search_command(search_terms)
        else:
            print("❌ Please provide search terms")
            print("💡 Usage: search <your search terms>")
            print("💡 Example: search database connection")
        return True
    
    def _cmd_semantic(self, args: list) -> bool:
        """Handle semantic search command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Semantic search not available in basic mode")
            print("💡 Install sentence-transformers for enhanced features")
            return True
            
        if args:
            search_terms = " ".join(args)
            self.terminal_interface._perform_semantic_search(search_terms)
        else:
            print("❌ Please provide search terms")
            print("💡 Usage: semantic <your search terms>")
            print("💡 Example: semantic how to connect database")
        return True
    
    def _cmd_intent(self, args: list) -> bool:
        """Handle intent analysis command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Intent analysis not available in basic mode")
            return True
            
        if args:
            query = " ".join(args)
            self.terminal_interface._analyze_query_intent(query)
        else:
            print("❌ Please provide a query")
            print("💡 Usage: intent <your query>")
            print("💡 Example: intent how to fix database errors")
        return True
    
    def _cmd_suggestions(self, args: list) -> bool:
        """Handle suggestions command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Suggestions not available in basic mode")
            return True
            
        if args:
            term = " ".join(args)
            self.terminal_interface._show_semantic_suggestions(term)
        else:
            print("❌ Please provide a term")
            print("💡 Usage: suggestions <your term>")
            print("💡 Example: suggestions database")
        return True
    
    def _cmd_settings(self, args: list) -> bool:
        """Handle settings command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Settings not available in basic mode")
            return True
            
        self.terminal_interface._show_search_settings()
        return True
    
    def _cmd_stats(self, args: list) -> bool:
        """Handle stats command"""
        self.terminal_interface._show_statistics()
        return True
    
    def _cmd_history(self, args: list) -> bool:
        """Handle history command with search and options"""
        if not self.command_history:
            print("📜 No command history available")
            return True
        
        # Parse arguments
        search_term = None
        show_all = False
        limit = 10
        
        i = 0
        while i < len(args):
            arg = args[i]
            if arg == "--all" or arg == "-a":
                show_all = True
            elif arg == "--limit" or arg == "-l":
                if i + 1 < len(args):
                    try:
                        limit = int(args[i + 1])
                        i += 1
                    except ValueError:
                        print("❌ Invalid limit value")
                        return True
            elif arg == "--search" or arg == "-s":
                if i + 1 < len(args):
                    search_term = args[i + 1]
                    i += 1
            elif not arg.startswith("-"):
                # Treat as search term if no --search flag
                search_term = arg
            i += 1
        
        # Get history to display
        if search_term:
            history_to_show = self.search_history(search_term)
            print(f"📜 Command History (search: '{search_term}'):")
        elif show_all:
            history_to_show = self.command_history
            print("📜 Complete Command History:")
        else:
            history_to_show = self.command_history[-limit:]
            print(f"📜 Recent Command History (last {len(history_to_show)}):")
        
        if not history_to_show:
            if search_term:
                print(f"   No commands found matching '{search_term}'")
            else:
                print("   No commands in history")
            return True
        
        # Display history
        for i, cmd in enumerate(history_to_show, 1):
            if search_term:
                # Highlight search term
                highlighted = cmd.replace(search_term, f"**{search_term}**")
                print(f"  {i:2d}. {highlighted}")
            else:
                print(f"  {i:2d}. {cmd}")
        
        # Show summary
        total_commands = len(self.command_history)
        if not show_all and total_commands > len(history_to_show):
            remaining = total_commands - len(history_to_show)
            print(f"   ... and {remaining} more commands")
            print(f"   💡 Use 'history --all' to see all {total_commands} commands")
        
        # Show usage help
        if not args:
            print("\n💡 History command options:")
            print("   history <term>          - Search history for term")
            print("   history --search <term> - Search history for term")
            print("   history --all           - Show all history")
            print("   history --limit <n>     - Show last n commands")
        
        return True
    
    def _cmd_index(self, args: list) -> bool:
        """Handle index command"""
        print("🔄 Starting file indexing...")
        self.terminal_interface._reindex_all_files()
        return True
    
    def _cmd_monitor(self, args: list) -> bool:
        """Handle monitor command"""
        print("👁️  Starting file monitoring...")
        print("💡 Press Ctrl+C to stop monitoring")
        self.terminal_interface._start_file_monitoring()
        return True
    
    def _cmd_quit(self, args: list) -> bool:
        """Handle quit/exit commands"""
        print("👋 Goodbye!")
        return False
    
    def _cmd_clear(self, args: list) -> bool:
        """Handle clear command"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.terminal_interface._show_welcome_message()
        return True
    
    def _cmd_version(self, args: list) -> bool:
        """Handle version command"""
        print("🧠 Collective Memory Terminal Interface")
        print("   Version: 4.0.0")
        print("   Enhanced Features:", "✅ Enabled" if self.terminal_interface.use_enhanced else "❌ Disabled")
        print("   Database:", str(self.terminal_interface.db_path))
        return True
    
    def get_available_commands(self) -> dict:
        """Get all available commands with descriptions"""
        descriptions = {
            'help': 'Show help information',
            'search': 'Search for content in files',
            'semantic': 'AI-powered semantic search',
            'intent': 'Analyze query intent',
            'suggestions': 'Get semantic suggestions',
            'settings': 'Configure search settings',
            'stats': 'Show database statistics',
            'history': 'Show command history',
            'index': 'Reindex all files',
            'monitor': 'Start file monitoring',
            'quit': 'Exit the application',
            'exit': 'Exit the application',
            'clear': 'Clear screen and show welcome',
            'version': 'Show version information',
        }
        return descriptions
    
    # Enhanced History and Auto-completion Features
    
    def _load_history(self):
        """Load command history from persistent storage"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.command_history = [line.strip() for line in f.readlines() if line.strip()]
                    # Limit history size
                    if len(self.command_history) > self.max_history:
                        self.command_history = self.command_history[-self.max_history:]
                print(f"📜 Loaded {len(self.command_history)} commands from history")
        except Exception as e:
            print(f"⚠️  Could not load command history: {e}")
    
    def _save_history(self):
        """Save command history to persistent storage"""
        try:
            # Ensure config directory exists
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                for command in self.command_history[-self.max_history:]:
                    f.write(f"{command}\n")
        except Exception as e:
            print(f"⚠️  Could not save command history: {e}")
    
    def _add_to_history(self, command_line: str):
        """Add command to history with deduplication and persistence"""
        if command_line and command_line.strip():
            # Remove duplicates - if command exists, move it to end
            if command_line in self.command_history:
                self.command_history.remove(command_line)
            
            self.command_history.append(command_line)
            
            # Limit history size
            if len(self.command_history) > self.max_history:
                self.command_history.pop(0)
            
            # Save to persistent storage
            self._save_history()
            
            # Reset history navigation index
            self.current_history_index = len(self.command_history)
    
    def _init_auto_completion(self):
        """Initialize auto-completion system"""
        try:
            import readline
            
            # Set up completion function
            readline.set_completer(self._complete_command)
            readline.parse_and_bind("tab: complete")
            
            # Enable history navigation with arrow keys
            readline.parse_and_bind("set editing-mode emacs")
            
            # Load history into readline
            for command in self.command_history:
                readline.add_history(command)
                
            print("🔧 Auto-completion and history navigation enabled")
            
        except ImportError:
            print("⚠️  Auto-completion not available (readline module not found)")
        except Exception as e:
            print(f"⚠️  Could not initialize auto-completion: {e}")
    
    def _complete_command(self, text: str, state: int):
        """Auto-completion function for commands and arguments"""
        try:
            # Get all possible completions
            options = []
            
            # If we're at the beginning of the line, complete commands
            line = readline.get_line_buffer()
            if not line or line.isspace() or len(line.split()) <= 1:
                # Complete command names and aliases
                all_commands = list(self.commands.keys()) + list(self.aliases.keys())
                options = [cmd for cmd in all_commands if cmd.startswith(text.lower())]
            else:
                # Complete arguments (basic file path completion)
                options = self._complete_file_paths(text)
            
            # Return the state-th option
            if state < len(options):
                return options[state]
            else:
                return None
                
        except Exception:
            return None
    
    def _complete_file_paths(self, text: str) -> list:
        """Complete file paths for command arguments"""
        try:
            import glob
            
            # If text is empty, show current directory contents
            if not text:
                pattern = "*"
            else:
                pattern = f"{text}*"
            
            # Get matching files and directories
            matches = glob.glob(pattern)
            
            # Add trailing slash for directories
            completions = []
            for match in matches:
                if os.path.isdir(match):
                    completions.append(f"{match}/")
                else:
                    completions.append(match)
            
            return completions[:10]  # Limit to 10 completions
            
        except Exception:
            return []
    
    def search_history(self, search_term: str) -> list:
        """Search through command history"""
        if not search_term:
            return self.command_history[-10:]  # Return last 10 if no search term
        
        matches = []
        search_lower = search_term.lower()
        
        for command in reversed(self.command_history):
            if search_lower in command.lower():
                matches.append(command)
                if len(matches) >= 10:  # Limit to 10 matches
                    break
        
        return matches
    
    def get_history_navigation(self, direction: str) -> str:
        """Navigate through command history (up/down)"""
        if not self.command_history:
            return ""
        
        if direction == "up":
            if self.current_history_index > 0:
                self.current_history_index -= 1
        elif direction == "down":
            if self.current_history_index < len(self.command_history) - 1:
                self.current_history_index += 1
            else:
                return ""  # At the end, return empty
        
        if 0 <= self.current_history_index < len(self.command_history):
            return self.command_history[self.current_history_index]
        
        return ""


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
    search_parser = subparsers.add_parser("search", help="Search files")
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