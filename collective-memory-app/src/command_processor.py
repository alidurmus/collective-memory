#!/usr/bin/env python3
"""
Command Processor - Enhanced command handling for terminal interface
Provides command registration, argument parsing, suggestions, and help system
"""

import shlex
import difflib
from typing import Dict, List, Callable, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandInfo:
    """Information about a registered command"""
    name: str
    handler: Callable
    description: str
    usage: str
    aliases: List[str]
    examples: List[str]


class CommandProcessor:
    """Enhanced command processor with intelligent suggestions and help"""
    
    def __init__(self, terminal_interface):
        self.terminal_interface = terminal_interface
        self.commands: Dict[str, CommandInfo] = {}
        self.aliases: Dict[str, str] = {}
        self.command_history: List[str] = []
        
        # Register all commands
        self._register_commands()
        
    def _register_commands(self):
        """Register all available commands with their handlers"""
        
        # Basic search commands
        self._register_command(
            name="search",
            handler=self._cmd_search,
            description="Search for content in files",
            usage="search <search terms>",
            aliases=["s", "find"],
            examples=[
                "search database connection",
                "search \"user authentication\"",
                "search API documentation"
            ]
        )
        
        # Semantic search (if available)
        if self.terminal_interface.use_enhanced:
            self._register_command(
                name="semantic",
                handler=self._cmd_semantic_search,
                description="AI-powered semantic search",
                usage="semantic <search terms>",
                aliases=["sem", "ai"],
                examples=[
                    "semantic how to connect database",
                    "semantic user login process",
                    "semantic error handling patterns"
                ]
            )
            
            self._register_command(
                name="intent",
                handler=self._cmd_analyze_intent,
                description="Analyze query intent",
                usage="intent <query>",
                aliases=["analyze"],
                examples=[
                    "intent how to setup authentication",
                    "intent find all database errors"
                ]
            )
            
            self._register_command(
                name="suggestions",
                handler=self._cmd_get_suggestions,
                description="Get semantic suggestions",
                usage="suggestions <term>",
                aliases=["suggest"],
                examples=[
                    "suggestions authentication",
                    "suggestions database"
                ]
            )
            
            self._register_command(
                name="settings",
                handler=self._cmd_show_settings,
                description="Configure search behavior",
                usage="settings",
                aliases=["config", "cfg"],
                examples=["settings"]
            )
        
        # System commands
        self._register_command(
            name="stats",
            handler=self._cmd_show_stats,
            description="Show database statistics",
            usage="stats",
            aliases=["st", "statistics"],
            examples=["stats"]
        )
        
        self._register_command(
            name="index",
            handler=self._cmd_reindex,
            description="Reindex all files",
            usage="index",
            aliases=["reindex", "rebuild"],
            examples=["index"]
        )
        
        self._register_command(
            name="monitor",
            handler=self._cmd_start_monitor,
            description="Start file monitoring",
            usage="monitor",
            aliases=["watch"],
            examples=["monitor"]
        )
        
        self._register_command(
            name="history",
            handler=self._cmd_show_history,
            description="Show command history",
            usage="history [count]",
            aliases=["hist", "h"],
            examples=[
                "history",
                "history 10"
            ]
        )
        
        self._register_command(
            name="clear",
            handler=self._cmd_clear_screen,
            description="Clear the screen",
            usage="clear",
            aliases=["cls"],
            examples=["clear"]
        )
        
        self._register_command(
            name="version",
            handler=self._cmd_show_version,
            description="Show version information",
            usage="version",
            aliases=["v", "ver"],
            examples=["version"]
        )
        
        self._register_command(
            name="help",
            handler=self._cmd_show_help,
            description="Show help information",
            usage="help [command]",
            aliases=["?", "h"],
            examples=[
                "help",
                "help search",
                "help semantic"
            ]
        )
        
        # Exit commands
        self._register_command(
            name="quit",
            handler=self._cmd_quit,
            description="Exit interactive mode",
            usage="quit",
            aliases=["exit", "q", "x"],
            examples=["quit"]
        )
        
    def _register_command(self, name: str, handler: Callable, description: str,
                         usage: str, aliases: List[str] = None, examples: List[str] = None):
        """Register a command with its handler and metadata"""
        if aliases is None:
            aliases = []
        if examples is None:
            examples = []
            
        command_info = CommandInfo(
            name=name,
            handler=handler,
            description=description,
            usage=usage,
            aliases=aliases,
            examples=examples
        )
        
        # Register main command
        self.commands[name] = command_info
        
        # Register aliases
        for alias in aliases:
            self.aliases[alias] = name
            
    def process_command(self, command_line: str) -> bool:
        """
        Process a command line and execute the appropriate handler
        
        Args:
            command_line: The command line to process
            
        Returns:
            True to continue, False to exit
        """
        # Add to history
        if command_line.strip():
            self.command_history.append(command_line.strip())
            # Keep only last 100 commands
            if len(self.command_history) > 100:
                self.command_history.pop(0)
        
        try:
            # Parse command and arguments
            parts = self._parse_command_line(command_line)
            if not parts:
                return True
                
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Find command handler
            handler = self._find_command_handler(command)
            if handler:
                return handler(args)
            else:
                self._handle_unknown_command(command)
                return True
                
        except Exception as e:
            print(f"❌ Error processing command: {e}")
            print("💡 Type 'help' for available commands")
            return True
            
    def _parse_command_line(self, command_line: str) -> List[str]:
        """Parse command line into command and arguments"""
        try:
            # Use shlex to handle quoted arguments properly
            return shlex.split(command_line.strip())
        except ValueError as e:
            print(f"❌ Command parsing error: {e}")
            return []
            
    def _find_command_handler(self, command: str) -> Optional[Callable]:
        """Find the handler for a command or alias"""
        # Check direct command
        if command in self.commands:
            return self.commands[command].handler
            
        # Check aliases
        if command in self.aliases:
            main_command = self.aliases[command]
            return self.commands[main_command].handler
            
        return None
        
    def _handle_unknown_command(self, command: str):
        """Handle unknown commands with intelligent suggestions"""
        print(f"❌ Unknown command: '{command}'")
        
        # Find similar commands
        suggestions = self._get_command_suggestions(command)
        if suggestions:
            print(f"💡 Did you mean: {', '.join(suggestions[:3])}?")
        else:
            print("💡 Type 'help' to see all available commands")
            
    def _get_command_suggestions(self, command: str) -> List[str]:
        """Get suggestions for similar commands"""
        all_commands = list(self.commands.keys()) + list(self.aliases.keys())
        
        # Use difflib to find similar commands
        suggestions = difflib.get_close_matches(
            command, all_commands, n=5, cutoff=0.6
        )
        
        return suggestions
        
    # Command handlers
    def _cmd_search(self, args: List[str]) -> bool:
        """Handle search command"""
        if not args:
            print("❌ Please provide search terms")
            print("💡 Usage: search <your search terms>")
            return True
            
        search_terms = " ".join(args)
        self.terminal_interface._execute_search_command(search_terms)
        return True
        
    def _cmd_semantic_search(self, args: List[str]) -> bool:
        """Handle semantic search command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Semantic search not available in basic mode")
            print("💡 Install sentence-transformers for enhanced features")
            return True
            
        if not args:
            print("❌ Please provide search terms")
            print("💡 Usage: semantic <your search terms>")
            return True
            
        search_terms = " ".join(args)
        self.terminal_interface._perform_semantic_search(search_terms)
        return True
        
    def _cmd_analyze_intent(self, args: List[str]) -> bool:
        """Handle intent analysis command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Intent analysis not available in basic mode")
            return True
            
        if not args:
            print("❌ Please provide a query")
            print("💡 Usage: intent <your query>")
            return True
            
        query = " ".join(args)
        self.terminal_interface._analyze_query_intent(query)
        return True
        
    def _cmd_get_suggestions(self, args: List[str]) -> bool:
        """Handle suggestions command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Suggestions not available in basic mode")
            return True
            
        if not args:
            print("❌ Please provide a term")
            print("💡 Usage: suggestions <your term>")
            return True
            
        term = " ".join(args)
        self.terminal_interface._show_semantic_suggestions(term)
        return True
        
    def _cmd_show_settings(self, args: List[str]) -> bool:
        """Handle settings command"""
        if not self.terminal_interface.use_enhanced:
            print("❌ Settings not available in basic mode")
            return True
            
        self.terminal_interface._show_search_settings()
        return True
        
    def _cmd_show_stats(self, args: List[str]) -> bool:
        """Handle stats command"""
        self.terminal_interface._show_statistics()
        return True
        
    def _cmd_reindex(self, args: List[str]) -> bool:
        """Handle reindex command"""
        print("🔄 Starting file reindexing...")
        self.terminal_interface._reindex_all_files()
        return True
        
    def _cmd_start_monitor(self, args: List[str]) -> bool:
        """Handle monitor command"""
        print("👁️  Starting file monitoring...")
        print("💡 File monitoring feature coming soon!")
        return True
        
    def _cmd_show_history(self, args: List[str]) -> bool:
        """Handle history command"""
        count = 10  # Default count
        
        if args:
            try:
                count = int(args[0])
                count = max(1, min(count, len(self.command_history)))
            except ValueError:
                print("❌ Invalid count. Using default of 10.")
                count = 10
                
        if not self.command_history:
            print("📝 No command history available")
            return True
            
        print(f"\n📝 Command History (last {count}):")
        recent_commands = self.command_history[-count:]
        
        for i, cmd in enumerate(recent_commands, 1):
            print(f"  {i:2d}. {cmd}")
            
        print()
        return True
        
    def _cmd_clear_screen(self, args: List[str]) -> bool:
        """Handle clear screen command"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        return True
        
    def _cmd_show_version(self, args: List[str]) -> bool:
        """Handle version command"""
        print("\n🧠 Collective Memory v4.0")
        print("📅 Enhanced Terminal Interface")
        print("🤖 AI-Powered Semantic Search")
        
        if self.terminal_interface.use_enhanced:
            print("✅ Enhanced features: Enabled")
        else:
            print("⚠️  Enhanced features: Disabled")
            
        print()
        return True
        
    def _cmd_show_help(self, args: List[str]) -> bool:
        """Handle help command"""
        if args:
            # Show help for specific command
            command = args[0].lower()
            self._show_command_help(command)
        else:
            # Show general help
            self._show_general_help()
        return True
        
    def _cmd_quit(self, args: List[str]) -> bool:
        """Handle quit command"""
        print("\n👋 Goodbye!")
        return False
        
    def _show_general_help(self):
        """Show general help with all commands"""
        print("\n" + "="*60)
        print("🧠 Collective Memory - Interactive Help")
        print("="*60)
        
        # Group commands by category
        basic_commands = ["search", "stats", "help"]
        ai_commands = ["semantic", "intent", "suggestions", "settings"] if self.terminal_interface.use_enhanced else []
        system_commands = ["index", "monitor", "history", "clear", "version", "quit"]
        
        if basic_commands:
            print("\n🔍 Basic Commands:")
            for cmd_name in basic_commands:
                if cmd_name in self.commands:
                    cmd = self.commands[cmd_name]
                    aliases_str = f" ({', '.join(cmd.aliases)})" if cmd.aliases else ""
                    print(f"  {cmd.name}{aliases_str:<15} - {cmd.description}")
        
        if ai_commands:
            print("\n🤖 AI-Enhanced Commands:")
            for cmd_name in ai_commands:
                if cmd_name in self.commands:
                    cmd = self.commands[cmd_name]
                    aliases_str = f" ({', '.join(cmd.aliases)})" if cmd.aliases else ""
                    print(f"  {cmd.name}{aliases_str:<15} - {cmd.description}")
        
        if system_commands:
            print("\n🛠️  System Commands:")
            for cmd_name in system_commands:
                if cmd_name in self.commands:
                    cmd = self.commands[cmd_name]
                    aliases_str = f" ({', '.join(cmd.aliases)})" if cmd.aliases else ""
                    print(f"  {cmd.name}{aliases_str:<15} - {cmd.description}")
        
        print("\n💡 Tips:")
        print("  • Use command aliases for faster typing (e.g., 's' for search)")
        print("  • Type 'help <command>' for detailed command help")
        print("  • Press Ctrl+C three times to force exit")
        print("  • Use quotes for exact phrases: search \"exact phrase\"")
        
        if not self.terminal_interface.use_enhanced:
            print("\n⚠️  Enhanced Features Disabled:")
            print("  Install sentence-transformers for AI-powered search")
        
        print("="*60 + "\n")
        
    def _show_command_help(self, command_name: str):
        """Show detailed help for a specific command"""
        # Check if it's an alias
        if command_name in self.aliases:
            command_name = self.aliases[command_name]
            
        if command_name not in self.commands:
            print(f"❌ No help available for command: {command_name}")
            suggestions = self._get_command_suggestions(command_name)
            if suggestions:
                print(f"💡 Did you mean: {', '.join(suggestions[:3])}?")
            return
            
        cmd = self.commands[command_name]
        
        print(f"\n📖 Help for '{cmd.name}' command:")
        print(f"   Description: {cmd.description}")
        print(f"   Usage: {cmd.usage}")
        
        if cmd.aliases:
            print(f"   Aliases: {', '.join(cmd.aliases)}")
            
        if cmd.examples:
            print(f"   Examples:")
            for example in cmd.examples:
                print(f"     {example}")
                
        print()
        
    def get_available_commands(self) -> List[str]:
        """Get list of all available commands"""
        return list(self.commands.keys())
        
    def get_command_aliases(self) -> Dict[str, str]:
        """Get mapping of aliases to commands"""
        return self.aliases.copy()
        
    def get_command_history(self) -> List[str]:
        """Get command history"""
        return self.command_history.copy()