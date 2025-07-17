#!/usr/bin/env python3
"""
Test script for Enhanced Cursor Reader Integration
vscode-cursorchat-downloader insights ile geliştirilmiş Cursor reader test
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from cursor_reader import EnhancedCursorDatabaseReader
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def test_cursor_detection():
    """Cursor veritabanı detection test"""
    print(f"{Fore.CYAN}🔍 Testing Cursor Database Detection{Style.RESET_ALL}")

    cursor_reader = EnhancedCursorDatabaseReader()

    if cursor_reader.is_cursor_available():
        print(f"{Fore.GREEN}✅ Cursor database paths found:{Style.RESET_ALL}")
        for path in cursor_reader.cursor_db_paths:
            print(f"   📁 {path}")
    else:
        print(f"{Fore.YELLOW}⚠️  No Cursor database paths found{Style.RESET_ALL}")

    return cursor_reader.is_cursor_available()


def test_workspace_discovery(cursor_reader):
    """Workspace discovery test"""
    print(f"\n{Fore.CYAN}🗂️  Testing Workspace Discovery{Style.RESET_ALL}")

    workspaces = cursor_reader.find_workspace_databases()

    if workspaces:
        print(f"{Fore.GREEN}✅ Found {len(workspaces)} workspace(s):{Style.RESET_ALL}")
        for workspace_key, workspace_data in workspaces.items():
            info = workspace_data["info"]
            print(f"   🗂️  {workspace_key}")
            print(f"       📁 Path: {info.get('path', 'Unknown')}")
            print(f"       🗄️  DB: {workspace_data['db_path']}")
    else:
        print(f"{Fore.YELLOW}⚠️  No workspaces found{Style.RESET_ALL}")

    return workspaces


def test_chat_history(cursor_reader, workspaces):
    """Chat history extraction test"""
    print(f"\n{Fore.CYAN}💬 Testing Chat History Extraction{Style.RESET_ALL}")

    if not workspaces:
        print(
            f"{Fore.YELLOW}⚠️  No workspaces available for chat testing{Style.RESET_ALL}"
        )
        return

    # Test first workspace
    first_workspace = list(workspaces.values())[0]
    db_path = first_workspace["db_path"]

    print(f"   🧪 Testing with: {db_path}")

    try:
        chats = cursor_reader.extract_complete_chat_history(db_path)

        if chats:
            print(f"{Fore.GREEN}✅ Found {len(chats)} chat entries:{Style.RESET_ALL}")

            # Show first few chats
            for i, chat in enumerate(chats[:3], 1):
                chat_type = chat.get("type", "unknown")
                key_type = chat.get("key_type", "unknown")
                summary = chat.get("summary", "No summary")[:100] + "..."

                type_icons = {
                    "conversation": "💬",
                    "code_generation": "💻",
                    "inline_chat": "📝",
                    "message_array": "📋",
                    "raw_content": "📄",
                    "raw_string": "📜",
                }

                icon = type_icons.get(chat_type, "❓")

                print(f"   {i}. {icon} [{chat_type}] - {key_type}")
                print(f"      📝 {summary}")

                if "message_count" in chat:
                    print(f"      📊 Messages: {chat['message_count']}")

        else:
            print(
                f"{Fore.YELLOW}⚠️  No chat history found in this workspace{Style.RESET_ALL}"
            )

    except Exception as e:
        print(f"{Fore.RED}❌ Chat extraction error: {e}{Style.RESET_ALL}")


def test_project_matching(cursor_reader):
    """Project-specific chat matching test"""
    print(f"\n{Fore.CYAN}🎯 Testing Project-Specific Chat Matching{Style.RESET_ALL}")

    # Test with current project path
    project_path = Path(__file__).parent.parent  # collective-memory

    try:
        chats = cursor_reader.get_project_chat_history(project_path, limit=5)

        if chats:
            print(
                f"{Fore.GREEN}✅ Found {len(chats)} project-specific chats:{Style.RESET_ALL}"
            )
            for i, chat in enumerate(chats, 1):
                summary = chat.get("summary", "No summary")[:80] + "..."
                print(f"   {i}. {chat.get('type', 'unknown')} - {summary}")
        else:
            print(f"{Fore.YELLOW}⚠️  No project-specific chats found{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}❌ Project matching error: {e}{Style.RESET_ALL}")


def main():
    """Main test function"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🧪 Enhanced Cursor Reader Integration Test{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   vscode-cursorchat-downloader insights{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    # Test 1: Cursor Detection
    if not test_cursor_detection():
        print(
            f"\n{Fore.RED}❌ Cursor detection failed. Tests aborted.{Style.RESET_ALL}"
        )
        return

    cursor_reader = EnhancedCursorDatabaseReader()

    # Test 2: Workspace Discovery
    workspaces = test_workspace_discovery(cursor_reader)

    # Test 3: Chat History Extraction
    test_chat_history(cursor_reader, workspaces)

    # Test 4: Project-Specific Matching
    test_project_matching(cursor_reader)

    # Summary
    print(f"\n{Fore.CYAN}📊 Test Summary:{Style.RESET_ALL}")
    print(
        f"   ✅ Cursor detection: {'Working' if cursor_reader.is_cursor_available() else 'Failed'}"
    )
    print(f"   ✅ Workspace discovery: {len(workspaces) if workspaces else 0} found")
    print(f"   ✅ Enhanced features: vscode-cursorchat-downloader integration")

    print(f"\n{Fore.GREEN}🎉 Enhanced Cursor Reader test completed!{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}💡 Usage Examples:{Style.RESET_ALL}")
    print(f"   python src/main.py --interactive")
    print(f"   > cursor_history")
    print(f"   > cursor_history --limit=20")
    print(f"   > cursor_history --workspaces")


if __name__ == "__main__":
    main()
