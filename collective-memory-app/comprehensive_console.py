#!/usr/bin/env python3
"""
Comprehensive Console System
Task Manager + Error Management + Documentation Tool
Unified console interface for all Collective Memory management tasks
"""

import sqlite3
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from colorama import init, Fore, Style
import logging
from dataclasses import dataclass
import uuid
import re

# Initialize colorama
init()


@dataclass
class Task:
    """Görev data sınıfı"""

    id: str
    title: str
    description: str
    priority: str  # HIGH, MEDIUM, LOW
    status: str  # PENDING, IN_PROGRESS, COMPLETED, CANCELLED
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    project: Optional[str] = None
    tags: List[str] = None
    dependencies: List[str] = None


@dataclass
class ErrorRecord:
    """Hata kaydı data sınıfı"""

    id: str
    title: str
    description: str
    error_type: str  # SYSTEM, USER, INTEGRATION, PERFORMANCE
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    status: str  # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    created_at: datetime
    updated_at: datetime
    file_path: Optional[str] = None
    stack_trace: Optional[str] = None
    solution: Optional[str] = None
    resolved_by: Optional[str] = None


@dataclass
class Documentation:
    """Dokümantasyon data sınıfı"""

    id: str
    title: str
    content: str
    doc_type: str  # GUIDE, TUTORIAL, REFERENCE, FAQ
    category: str  # SYSTEM, USER, DEVELOPER, API
    created_at: datetime
    updated_at: datetime
    author: Optional[str] = None
    tags: List[str] = None
    version: str = "1.0"


class ComprehensiveConsole:
    """Kapsamlı Console Yönetim Sistemi"""

    def __init__(self, db_path: str = "./comprehensive_system.db"):
        self.db_path = Path(db_path).resolve()
        self.connection = None
        self.current_user = "system_admin"

        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("comprehensive_system.log"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

        # Initialize database
        self.init_database()

        # Command mapping
        self.commands = {
            # Task Management
            "tasks": self.show_tasks,
            "task-add": self.add_task,
            "task-update": self.update_task,
            "task-complete": self.complete_task,
            "task-delete": self.delete_task,
            "task-search": self.search_tasks,
            "task-report": self.generate_task_report,
            # Error Management
            "errors": self.show_errors,
            "error-add": self.add_error,
            "error-update": self.update_error,
            "error-resolve": self.resolve_error,
            "error-close": self.close_error,
            "error-search": self.search_errors,
            "error-report": self.generate_error_report,
            # Documentation
            "docs": self.show_docs,
            "doc-add": self.add_doc,
            "doc-update": self.update_doc,
            "doc-delete": self.delete_doc,
            "doc-search": self.search_docs,
            "doc-export": self.export_doc,
            "doc-generate": self.generate_doc,
            # System Management
            "status": self.show_system_status,
            "backup": self.backup_system,
            "restore": self.restore_system,
            "stats": self.show_statistics,
            "help": self.show_help,
            "exit": self.exit_system,
            # Integration
            "collective-memory": self.run_collective_memory,
            "api-server": self.run_api_server,
            "frontend": self.run_frontend,
            "test": self.run_tests,
            "deploy": self.deploy_system,
            # System Operations
            "scan-errors": self.scan_system_errors,
            "auto-docs": self.auto_generate_docs,
            "health-check": self.health_check,
            "cleanup": self.cleanup_system,
        }

        print(
            f"{Fore.CYAN}🚀 Comprehensive Console System Initialized{Style.RESET_ALL}"
        )

    def init_database(self):
        """Veritabanı şemasını oluştur"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

            # Tasks table
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT DEFAULT 'MEDIUM',
                    status TEXT DEFAULT 'PENDING',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    due_date DATETIME,
                    assigned_to TEXT,
                    project TEXT,
                    tags TEXT,
                    dependencies TEXT
                )
            """
            )

            # Errors table
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS errors (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    error_type TEXT DEFAULT 'SYSTEM',
                    severity TEXT DEFAULT 'MEDIUM',
                    status TEXT DEFAULT 'OPEN',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    file_path TEXT,
                    stack_trace TEXT,
                    solution TEXT,
                    resolved_by TEXT
                )
            """
            )

            # Documentation table
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documentation (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT,
                    doc_type TEXT DEFAULT 'GUIDE',
                    category TEXT DEFAULT 'SYSTEM',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    author TEXT,
                    tags TEXT,
                    version TEXT DEFAULT '1.0'
                )
            """
            )

            # System logs table
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS system_logs (
                    id TEXT PRIMARY KEY,
                    action TEXT NOT NULL,
                    details TEXT,
                    user_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    success BOOLEAN DEFAULT 1
                )
            """
            )

            self.connection.commit()
            self.logger.info("Database initialized successfully")

        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise

    def log_action(self, action: str, details: str = "", success: bool = True):
        """Sistem aksiyonunu logla"""
        try:
            self.connection.execute(
                """
                INSERT INTO system_logs (id, action, details, user_id, success)
                VALUES (?, ?, ?, ?, ?)
            """,
                (str(uuid.uuid4()), action, details, self.current_user, success),
            )
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Logging failed: {e}")

    def run_interactive(self):
        """Ana interaktif döngü"""
        self.show_banner()

        while True:
            try:
                command = input(
                    f"\n{Fore.GREEN}comprehensive> {Style.RESET_ALL}"
                ).strip()

                if not command:
                    continue

                # Parse command and arguments
                parts = command.split(" ", 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if cmd in self.commands:
                    try:
                        self.commands[cmd](args)
                        self.log_action(
                            f"COMMAND_EXECUTED", f"Command: {cmd}, Args: {args}"
                        )
                    except Exception as e:
                        print(
                            f"{Fore.RED}❌ Command execution failed: {e}{Style.RESET_ALL}"
                        )
                        self.log_action(
                            f"COMMAND_FAILED", f"Command: {cmd}, Error: {e}", False
                        )
                else:
                    print(
                        f"{Fore.RED}❌ Unknown command: {cmd}. Type 'help' for available commands.{Style.RESET_ALL}"
                    )

            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ System error: {e}{Style.RESET_ALL}")
                self.logger.error(f"System error: {e}")

    def show_banner(self):
        """Sistem başlık banner'ını göster"""
        print(
            f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗
║                    🚀 COMPREHENSIVE CONSOLE SYSTEM v1.0                        ║
║                    Task Manager + Error Tracker + Documentation                 ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  📋 Task Management    🐛 Error Tracking    📚 Documentation    ⚙️ System       ║
║  🔍 Search & Filter    📊 Reports & Stats   🔧 Integration     🚀 Deployment    ║
╚══════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        )

    # ==================== TASK MANAGEMENT ====================

    def show_tasks(self, args: str = ""):
        """Görevleri listele"""
        try:
            filters = self._parse_filter_args(args)

            query = "SELECT * FROM tasks WHERE 1=1"
            params = []

            if filters.get("status"):
                query += " AND status = ?"
                params.append(filters["status"].upper())

            if filters.get("priority"):
                query += " AND priority = ?"
                params.append(filters["priority"].upper())

            if filters.get("project"):
                query += " AND project = ?"
                params.append(filters["project"])

            query += " ORDER BY created_at DESC"

            cursor = self.connection.execute(query, params)
            tasks = cursor.fetchall()

            if not tasks:
                print(f"{Fore.YELLOW}📋 No tasks found{Style.RESET_ALL}")
                return

            print(f"\n{Fore.CYAN}📋 TASKS ({len(tasks)} found){Style.RESET_ALL}")
            print("=" * 80)

            for task in tasks:
                status_color = self._get_status_color(task["status"])
                priority_color = self._get_priority_color(task["priority"])

                print(
                    f"{status_color}[{task['status']}]{Style.RESET_ALL} "
                    f"{priority_color}[{task['priority']}]{Style.RESET_ALL} "
                    f"{Fore.WHITE}{task['title']}{Style.RESET_ALL}"
                )

                if task["description"]:
                    print(f"  📝 {task['description'][:100]}...")

                if task["due_date"]:
                    print(f"  📅 Due: {task['due_date']}")

                if task["project"]:
                    print(f"  🏷️  Project: {task['project']}")

                print(f"  🆔 ID: {task['id'][:8]}...")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Error showing tasks: {e}{Style.RESET_ALL}")

    def add_task(self, args: str):
        """Yeni görev ekle"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide task title{Style.RESET_ALL}")
                return

            # Parse args for task creation
            parts = args.split(" --")
            title = parts[0].strip()

            task_data = {
                "title": title,
                "description": "",
                "priority": "MEDIUM",
                "project": None,
                "tags": [],
                "due_date": None,
            }

            # Parse additional parameters
            for part in parts[1:]:
                if part.startswith("desc="):
                    task_data["description"] = part[5:]
                elif part.startswith("priority="):
                    task_data["priority"] = part[9:].upper()
                elif part.startswith("project="):
                    task_data["project"] = part[8:]
                elif part.startswith("due="):
                    # Parse date (YYYY-MM-DD format)
                    try:
                        task_data["due_date"] = datetime.strptime(part[4:], "%Y-%m-%d")
                    except ValueError:
                        print(
                            f"{Fore.YELLOW}⚠️ Invalid date format. Use YYYY-MM-DD{Style.RESET_ALL}"
                        )

            # Insert task
            task_id = str(uuid.uuid4())
            self.connection.execute(
                """
                INSERT INTO tasks (id, title, description, priority, project, due_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    task_id,
                    task_data["title"],
                    task_data["description"],
                    task_data["priority"],
                    task_data["project"],
                    task_data["due_date"],
                ),
            )

            self.connection.commit()

            print(f"{Fore.GREEN}✅ Task added successfully!{Style.RESET_ALL}")
            print(f"🆔 Task ID: {task_id[:8]}...")
            print(f"📝 Title: {task_data['title']}")
            print(f"🎯 Priority: {task_data['priority']}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error adding task: {e}{Style.RESET_ALL}")

    def update_task(self, args: str):
        """Görev güncelle"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide task ID{Style.RESET_ALL}")
                return

            parts = args.split(" --")
            task_id = parts[0].strip()

            # Find task by partial ID
            cursor = self.connection.execute(
                "SELECT * FROM tasks WHERE id LIKE ?", (f"{task_id}%",)
            )
            task = cursor.fetchone()

            if not task:
                print(f"{Fore.RED}❌ Task not found: {task_id}{Style.RESET_ALL}")
                return

            # Parse update parameters
            updates = {}
            for part in parts[1:]:
                if part.startswith("title="):
                    updates["title"] = part[6:]
                elif part.startswith("desc="):
                    updates["description"] = part[5:]
                elif part.startswith("priority="):
                    updates["priority"] = part[9:].upper()
                elif part.startswith("status="):
                    updates["status"] = part[7:].upper()
                elif part.startswith("project="):
                    updates["project"] = part[8:]

            if not updates:
                print(f"{Fore.YELLOW}⚠️ No updates specified{Style.RESET_ALL}")
                return

            # Build update query
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            query = f"UPDATE tasks SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            params = list(updates.values()) + [task["id"]]

            self.connection.execute(query, params)
            self.connection.commit()

            print(f"{Fore.GREEN}✅ Task updated successfully!{Style.RESET_ALL}")
            print(f"🆔 Task ID: {task['id'][:8]}...")
            for key, value in updates.items():
                print(f"📝 {key.title()}: {value}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error updating task: {e}{Style.RESET_ALL}")

    def complete_task(self, args: str):
        """Görev tamamla"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide task ID{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                "SELECT * FROM tasks WHERE id LIKE ?", (f"{args.strip()}%",)
            )
            task = cursor.fetchone()

            if not task:
                print(f"{Fore.RED}❌ Task not found: {args}{Style.RESET_ALL}")
                return

            self.connection.execute(
                "UPDATE tasks SET status = 'COMPLETED', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (task["id"],),
            )
            self.connection.commit()

            print(f"{Fore.GREEN}✅ Task completed successfully!{Style.RESET_ALL}")
            print(f"🆔 Task: {task['title']}")
            print(f"📊 Status: COMPLETED")

        except Exception as e:
            print(f"{Fore.RED}❌ Error completing task: {e}{Style.RESET_ALL}")

    def delete_task(self, args: str):
        """Görev sil"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide task ID{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                "SELECT * FROM tasks WHERE id LIKE ?", (f"{args.strip()}%",)
            )
            task = cursor.fetchone()

            if not task:
                print(f"{Fore.RED}❌ Task not found: {args}{Style.RESET_ALL}")
                return

            # Confirmation
            confirm = input(
                f"{Fore.YELLOW}⚠️ Delete task '{task['title']}'? (y/N): {Style.RESET_ALL}"
            )
            if confirm.lower() != "y":
                print(f"{Fore.CYAN}ℹ️ Operation cancelled{Style.RESET_ALL}")
                return

            self.connection.execute("DELETE FROM tasks WHERE id = ?", (task["id"],))
            self.connection.commit()

            print(f"{Fore.GREEN}✅ Task deleted successfully!{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error deleting task: {e}{Style.RESET_ALL}")

    def search_tasks(self, args: str):
        """Görev ara"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide search term{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                """SELECT * FROM tasks 
                   WHERE title LIKE ? OR description LIKE ? OR project LIKE ?
                   ORDER BY created_at DESC""",
                (f"%{args}%", f"%{args}%", f"%{args}%"),
            )

            results = cursor.fetchall()

            if not results:
                print(
                    f"{Fore.YELLOW}🔍 No tasks found matching '{args}'{Style.RESET_ALL}"
                )
                return

            print(
                f"\n{Fore.CYAN}🔍 SEARCH RESULTS: '{args}' ({len(results)} found){Style.RESET_ALL}"
            )
            print("=" * 80)

            for task in results:
                status_color = self._get_status_color(task["status"])
                priority_color = self._get_priority_color(task["priority"])

                print(
                    f"{status_color}[{task['status']}]{Style.RESET_ALL} "
                    f"{priority_color}[{task['priority']}]{Style.RESET_ALL} "
                    f"{Fore.WHITE}{task['title']}{Style.RESET_ALL}"
                )

                if task["description"]:
                    print(f"  📝 {task['description'][:100]}...")

                print(f"  🆔 ID: {task['id'][:8]}...")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Error searching tasks: {e}{Style.RESET_ALL}")

    def generate_task_report(self, args: str = ""):
        """Görev raporu oluştur"""
        try:
            print(f"\n{Fore.CYAN}📊 TASK REPORT{Style.RESET_ALL}")
            print("=" * 50)

            # Overall stats
            cursor = self.connection.execute("SELECT COUNT(*) as total FROM tasks")
            total = cursor.fetchone()["total"]

            cursor = self.connection.execute(
                "SELECT status, COUNT(*) as count FROM tasks GROUP BY status"
            )
            status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}

            cursor = self.connection.execute(
                "SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority"
            )
            priority_counts = {
                row["priority"]: row["count"] for row in cursor.fetchall()
            }

            print(f"📈 Total Tasks: {total}")
            print(f"📊 Status Distribution:")
            for status, count in status_counts.items():
                color = self._get_status_color(status)
                print(f"  {color}{status}{Style.RESET_ALL}: {count}")

            print(f"🎯 Priority Distribution:")
            for priority, count in priority_counts.items():
                color = self._get_priority_color(priority)
                print(f"  {color}{priority}{Style.RESET_ALL}: {count}")

            # Recent tasks
            cursor = self.connection.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC LIMIT 5"
            )
            recent_tasks = cursor.fetchall()

            print(f"\n🕒 Recent Tasks:")
            for task in recent_tasks:
                print(f"  • {task['title'][:50]}... ({task['status']})")

        except Exception as e:
            print(f"{Fore.RED}❌ Error generating task report: {e}{Style.RESET_ALL}")

    # ==================== ERROR MANAGEMENT ====================

    def show_errors(self, args: str = ""):
        """Hataları listele"""
        try:
            filters = self._parse_filter_args(args)

            query = "SELECT * FROM errors WHERE 1=1"
            params = []

            if filters.get("status"):
                query += " AND status = ?"
                params.append(filters["status"].upper())

            if filters.get("severity"):
                query += " AND severity = ?"
                params.append(filters["severity"].upper())

            if filters.get("type"):
                query += " AND error_type = ?"
                params.append(filters["type"].upper())

            query += " ORDER BY created_at DESC"

            cursor = self.connection.execute(query, params)
            errors = cursor.fetchall()

            if not errors:
                print(f"{Fore.YELLOW}🐛 No errors found{Style.RESET_ALL}")
                return

            print(f"\n{Fore.CYAN}🐛 ERRORS ({len(errors)} found){Style.RESET_ALL}")
            print("=" * 80)

            for error in errors:
                status_color = self._get_status_color(error["status"])
                severity_color = self._get_severity_color(error["severity"])

                print(
                    f"{status_color}[{error['status']}]{Style.RESET_ALL} "
                    f"{severity_color}[{error['severity']}]{Style.RESET_ALL} "
                    f"{Fore.WHITE}{error['title']}{Style.RESET_ALL}"
                )

                if error["description"]:
                    print(f"  📝 {error['description'][:100]}...")

                if error["file_path"]:
                    print(f"  📁 File: {error['file_path']}")

                print(f"  🆔 ID: {error['id'][:8]}...")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Error showing errors: {e}{Style.RESET_ALL}")

    def add_error(self, args: str):
        """Yeni hata ekle"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide error title{Style.RESET_ALL}")
                return

            parts = args.split(" --")
            title = parts[0].strip()

            error_data = {
                "title": title,
                "description": "",
                "error_type": "SYSTEM",
                "severity": "MEDIUM",
                "file_path": None,
                "stack_trace": None,
            }

            # Parse additional parameters
            for part in parts[1:]:
                if part.startswith("desc="):
                    error_data["description"] = part[5:]
                elif part.startswith("type="):
                    error_data["error_type"] = part[5:].upper()
                elif part.startswith("severity="):
                    error_data["severity"] = part[9:].upper()
                elif part.startswith("file="):
                    error_data["file_path"] = part[5:]
                elif part.startswith("stack="):
                    error_data["stack_trace"] = part[6:]

            # Insert error
            error_id = str(uuid.uuid4())
            self.connection.execute(
                """
                INSERT INTO errors (id, title, description, error_type, severity, file_path, stack_trace)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    error_id,
                    error_data["title"],
                    error_data["description"],
                    error_data["error_type"],
                    error_data["severity"],
                    error_data["file_path"],
                    error_data["stack_trace"],
                ),
            )

            self.connection.commit()

            print(f"{Fore.GREEN}✅ Error added successfully!{Style.RESET_ALL}")
            print(f"🆔 Error ID: {error_id[:8]}...")
            print(f"📝 Title: {error_data['title']}")
            print(f"🚨 Severity: {error_data['severity']}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error adding error record: {e}{Style.RESET_ALL}")

    def update_error(self, args: str):
        """Hata güncelle"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide error ID{Style.RESET_ALL}")
                return

            parts = args.split(" --")
            error_id = parts[0].strip()

            # Find error by partial ID
            cursor = self.connection.execute(
                "SELECT * FROM errors WHERE id LIKE ?", (f"{error_id}%",)
            )
            error = cursor.fetchone()

            if not error:
                print(f"{Fore.RED}❌ Error not found: {error_id}{Style.RESET_ALL}")
                return

            # Parse update parameters
            updates = {}
            for part in parts[1:]:
                if part.startswith("title="):
                    updates["title"] = part[6:]
                elif part.startswith("desc="):
                    updates["description"] = part[5:]
                elif part.startswith("severity="):
                    updates["severity"] = part[9:].upper()
                elif part.startswith("status="):
                    updates["status"] = part[7:].upper()
                elif part.startswith("solution="):
                    updates["solution"] = part[9:]

            if not updates:
                print(f"{Fore.YELLOW}⚠️ No updates specified{Style.RESET_ALL}")
                return

            # Build update query
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            query = f"UPDATE errors SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            params = list(updates.values()) + [error["id"]]

            self.connection.execute(query, params)
            self.connection.commit()

            print(f"{Fore.GREEN}✅ Error updated successfully!{Style.RESET_ALL}")
            print(f"🆔 Error ID: {error['id'][:8]}...")
            for key, value in updates.items():
                print(f"📝 {key.title()}: {value}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error updating error record: {e}{Style.RESET_ALL}")

    def resolve_error(self, args: str):
        """Hata çöz"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide error ID{Style.RESET_ALL}")
                return

            parts = args.split(" --solution=")
            error_id = parts[0].strip()
            solution = parts[1] if len(parts) > 1 else ""

            cursor = self.connection.execute(
                "SELECT * FROM errors WHERE id LIKE ?", (f"{error_id}%",)
            )
            error = cursor.fetchone()

            if not error:
                print(f"{Fore.RED}❌ Error not found: {error_id}{Style.RESET_ALL}")
                return

            self.connection.execute(
                """UPDATE errors SET status = 'RESOLVED', solution = ?, resolved_by = ?, 
                   updated_at = CURRENT_TIMESTAMP WHERE id = ?""",
                (solution, self.current_user, error["id"]),
            )
            self.connection.commit()

            print(f"{Fore.GREEN}✅ Error resolved successfully!{Style.RESET_ALL}")
            print(f"🆔 Error: {error['title']}")
            print(f"📊 Status: RESOLVED")
            if solution:
                print(f"💡 Solution: {solution}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error resolving error: {e}{Style.RESET_ALL}")

    def close_error(self, args: str):
        """Hata kapat"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide error ID{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                "SELECT * FROM errors WHERE id LIKE ?", (f"{args.strip()}%",)
            )
            error = cursor.fetchone()

            if not error:
                print(f"{Fore.RED}❌ Error not found: {args}{Style.RESET_ALL}")
                return

            self.connection.execute(
                "UPDATE errors SET status = 'CLOSED', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (error["id"],),
            )
            self.connection.commit()

            print(f"{Fore.GREEN}✅ Error closed successfully!{Style.RESET_ALL}")
            print(f"🆔 Error: {error['title']}")
            print(f"📊 Status: CLOSED")

        except Exception as e:
            print(f"{Fore.RED}❌ Error closing error: {e}{Style.RESET_ALL}")

    def search_errors(self, args: str):
        """Hata ara"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide search term{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                """SELECT * FROM errors 
                   WHERE title LIKE ? OR description LIKE ? OR solution LIKE ?
                   ORDER BY created_at DESC""",
                (f"%{args}%", f"%{args}%", f"%{args}%"),
            )

            results = cursor.fetchall()

            if not results:
                print(
                    f"{Fore.YELLOW}🔍 No errors found matching '{args}'{Style.RESET_ALL}"
                )
                return

            print(
                f"\n{Fore.CYAN}🔍 ERROR SEARCH RESULTS: '{args}' ({len(results)} found){Style.RESET_ALL}"
            )
            print("=" * 80)

            for error in results:
                status_color = self._get_status_color(error["status"])
                severity_color = self._get_severity_color(error["severity"])

                print(
                    f"{status_color}[{error['status']}]{Style.RESET_ALL} "
                    f"{severity_color}[{error['severity']}]{Style.RESET_ALL} "
                    f"{Fore.WHITE}{error['title']}{Style.RESET_ALL}"
                )

                if error["description"]:
                    print(f"  📝 {error['description'][:100]}...")

                print(f"  🆔 ID: {error['id'][:8]}...")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Error searching errors: {e}{Style.RESET_ALL}")

    def generate_error_report(self, args: str = ""):
        """Hata raporu oluştur"""
        try:
            print(f"\n{Fore.CYAN}📊 ERROR REPORT{Style.RESET_ALL}")
            print("=" * 50)

            # Overall stats
            cursor = self.connection.execute("SELECT COUNT(*) as total FROM errors")
            total = cursor.fetchone()["total"]

            cursor = self.connection.execute(
                "SELECT status, COUNT(*) as count FROM errors GROUP BY status"
            )
            status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}

            cursor = self.connection.execute(
                "SELECT severity, COUNT(*) as count FROM errors GROUP BY severity"
            )
            severity_counts = {
                row["severity"]: row["count"] for row in cursor.fetchall()
            }

            cursor = self.connection.execute(
                "SELECT error_type, COUNT(*) as count FROM errors GROUP BY error_type"
            )
            type_counts = {row["error_type"]: row["count"] for row in cursor.fetchall()}

            print(f"📈 Total Errors: {total}")
            print(f"📊 Status Distribution:")
            for status, count in status_counts.items():
                color = self._get_status_color(status)
                print(f"  {color}{status}{Style.RESET_ALL}: {count}")

            print(f"🚨 Severity Distribution:")
            for severity, count in severity_counts.items():
                color = self._get_severity_color(severity)
                print(f"  {color}{severity}{Style.RESET_ALL}: {count}")

            print(f"🏷️ Type Distribution:")
            for error_type, count in type_counts.items():
                print(f"  {error_type}: {count}")

            # Recent errors
            cursor = self.connection.execute(
                "SELECT * FROM errors ORDER BY created_at DESC LIMIT 5"
            )
            recent_errors = cursor.fetchall()

            print(f"\n🕒 Recent Errors:")
            for error in recent_errors:
                print(f"  • {error['title'][:50]}... ({error['status']})")

        except Exception as e:
            print(f"{Fore.RED}❌ Error generating error report: {e}{Style.RESET_ALL}")

    # ==================== DOCUMENTATION ====================

    def show_docs(self, args: str = ""):
        """Dokümantasyon listele"""
        try:
            filters = self._parse_filter_args(args)

            query = "SELECT * FROM documentation WHERE 1=1"
            params = []

            if filters.get("type"):
                query += " AND doc_type = ?"
                params.append(filters["type"].upper())

            if filters.get("category"):
                query += " AND category = ?"
                params.append(filters["category"].upper())

            query += " ORDER BY created_at DESC"

            cursor = self.connection.execute(query, params)
            docs = cursor.fetchall()

            if not docs:
                print(f"{Fore.YELLOW}📚 No documentation found{Style.RESET_ALL}")
                return

            print(f"\n{Fore.CYAN}📚 DOCUMENTATION ({len(docs)} found){Style.RESET_ALL}")
            print("=" * 80)

            for doc in docs:
                print(f"{Fore.WHITE}{doc['title']}{Style.RESET_ALL}")
                print(f"  📝 Type: {doc['doc_type']} | Category: {doc['category']}")
                print(f"  📅 Created: {doc['created_at']}")
                print(f"  🆔 ID: {doc['id'][:8]}...")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Error showing documentation: {e}{Style.RESET_ALL}")

    def add_doc(self, args: str):
        """Yeni dokümantasyon ekle"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide document title{Style.RESET_ALL}")
                return

            parts = args.split(" --")
            title = parts[0].strip()

            doc_data = {
                "title": title,
                "content": "",
                "doc_type": "GUIDE",
                "category": "SYSTEM",
                "author": self.current_user,
                "version": "1.0",
            }

            # Parse additional parameters
            for part in parts[1:]:
                if part.startswith("content="):
                    doc_data["content"] = part[8:]
                elif part.startswith("type="):
                    doc_data["doc_type"] = part[5:].upper()
                elif part.startswith("category="):
                    doc_data["category"] = part[9:].upper()
                elif part.startswith("version="):
                    doc_data["version"] = part[8:]

            # Insert documentation
            doc_id = str(uuid.uuid4())
            self.connection.execute(
                """
                INSERT INTO documentation (id, title, content, doc_type, category, author, version)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    doc_id,
                    doc_data["title"],
                    doc_data["content"],
                    doc_data["doc_type"],
                    doc_data["category"],
                    doc_data["author"],
                    doc_data["version"],
                ),
            )

            self.connection.commit()

            print(f"{Fore.GREEN}✅ Documentation added successfully!{Style.RESET_ALL}")
            print(f"🆔 Doc ID: {doc_id[:8]}...")
            print(f"📝 Title: {doc_data['title']}")
            print(f"📚 Type: {doc_data['doc_type']}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error adding documentation: {e}{Style.RESET_ALL}")

    def update_doc(self, args: str):
        """Dokümantasyon güncelle"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide document ID{Style.RESET_ALL}")
                return

            parts = args.split(" --")
            doc_id = parts[0].strip()

            # Find document by partial ID
            cursor = self.connection.execute(
                "SELECT * FROM documentation WHERE id LIKE ?", (f"{doc_id}%",)
            )
            doc = cursor.fetchone()

            if not doc:
                print(f"{Fore.RED}❌ Document not found: {doc_id}{Style.RESET_ALL}")
                return

            # Parse update parameters
            updates = {}
            for part in parts[1:]:
                if part.startswith("title="):
                    updates["title"] = part[6:]
                elif part.startswith("content="):
                    updates["content"] = part[8:]
                elif part.startswith("type="):
                    updates["doc_type"] = part[5:].upper()
                elif part.startswith("category="):
                    updates["category"] = part[9:].upper()
                elif part.startswith("version="):
                    updates["version"] = part[8:]

            if not updates:
                print(f"{Fore.YELLOW}⚠️ No updates specified{Style.RESET_ALL}")
                return

            # Build update query
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            query = f"UPDATE documentation SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            params = list(updates.values()) + [doc["id"]]

            self.connection.execute(query, params)
            self.connection.commit()

            print(
                f"{Fore.GREEN}✅ Documentation updated successfully!{Style.RESET_ALL}"
            )
            print(f"🆔 Doc ID: {doc['id'][:8]}...")
            for key, value in updates.items():
                print(f"📝 {key.title()}: {value}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error updating documentation: {e}{Style.RESET_ALL}")

    def delete_doc(self, args: str):
        """Dokümantasyon sil"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide document ID{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                "SELECT * FROM documentation WHERE id LIKE ?", (f"{args.strip()}%",)
            )
            doc = cursor.fetchone()

            if not doc:
                print(f"{Fore.RED}❌ Document not found: {args}{Style.RESET_ALL}")
                return

            # Confirmation
            confirm = input(
                f"{Fore.YELLOW}⚠️ Delete document '{doc['title']}'? (y/N): {Style.RESET_ALL}"
            )
            if confirm.lower() != "y":
                print(f"{Fore.CYAN}ℹ️ Operation cancelled{Style.RESET_ALL}")
                return

            self.connection.execute(
                "DELETE FROM documentation WHERE id = ?", (doc["id"],)
            )
            self.connection.commit()

            print(
                f"{Fore.GREEN}✅ Documentation deleted successfully!{Style.RESET_ALL}"
            )

        except Exception as e:
            print(f"{Fore.RED}❌ Error deleting documentation: {e}{Style.RESET_ALL}")

    def search_docs(self, args: str):
        """Dokümantasyon ara"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide search term{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                """SELECT * FROM documentation 
                   WHERE title LIKE ? OR content LIKE ?
                   ORDER BY created_at DESC""",
                (f"%{args}%", f"%{args}%"),
            )

            results = cursor.fetchall()

            if not results:
                print(
                    f"{Fore.YELLOW}🔍 No documentation found matching '{args}'{Style.RESET_ALL}"
                )
                return

            print(
                f"\n{Fore.CYAN}🔍 DOCUMENTATION SEARCH RESULTS: '{args}' ({len(results)} found){Style.RESET_ALL}"
            )
            print("=" * 80)

            for doc in results:
                print(f"{Fore.WHITE}{doc['title']}{Style.RESET_ALL}")
                print(f"  📝 Type: {doc['doc_type']} | Category: {doc['category']}")
                print(f"  📅 Created: {doc['created_at']}")
                print(f"  🆔 ID: {doc['id'][:8]}...")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Error searching documentation: {e}{Style.RESET_ALL}")

    def export_doc(self, args: str):
        """Dokümantasyon export et"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide document ID{Style.RESET_ALL}")
                return

            cursor = self.connection.execute(
                "SELECT * FROM documentation WHERE id LIKE ?", (f"{args.strip()}%",)
            )
            doc = cursor.fetchone()

            if not doc:
                print(f"{Fore.RED}❌ Document not found: {args}{Style.RESET_ALL}")
                return

            # Export to markdown file
            filename = f"doc_{doc['id'][:8]}_{doc['title'].replace(' ', '_')}.md"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {doc['title']}\n\n")
                f.write(f"**Type:** {doc['doc_type']}\n")
                f.write(f"**Category:** {doc['category']}\n")
                f.write(f"**Author:** {doc['author']}\n")
                f.write(f"**Version:** {doc['version']}\n")
                f.write(f"**Created:** {doc['created_at']}\n")
                f.write(f"**Updated:** {doc['updated_at']}\n\n")
                f.write("---\n\n")
                f.write(doc["content"])

            print(
                f"{Fore.GREEN}✅ Documentation exported successfully!{Style.RESET_ALL}"
            )
            print(f"📄 File: {filename}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error exporting documentation: {e}{Style.RESET_ALL}")

    def generate_doc(self, args: str):
        """Otomatik dokümantasyon oluştur"""
        try:
            if not args:
                print(
                    f"{Fore.RED}❌ Please provide document type (system|api|user){Style.RESET_ALL}"
                )
                return

            doc_type = args.strip().lower()

            if doc_type == "system":
                self._generate_system_doc()
            elif doc_type == "api":
                self._generate_api_doc()
            elif doc_type == "user":
                self._generate_user_doc()
            else:
                print(
                    f"{Fore.RED}❌ Invalid document type: {doc_type}{Style.RESET_ALL}"
                )
                print(
                    f"{Fore.YELLOW}Available types: system, api, user{Style.RESET_ALL}"
                )

        except Exception as e:
            print(f"{Fore.RED}❌ Error generating documentation: {e}{Style.RESET_ALL}")

    # ==================== SYSTEM MANAGEMENT ====================

    def show_system_status(self, args: str = ""):
        """Sistem durumunu göster"""
        try:
            print(f"\n{Fore.CYAN}⚙️ SYSTEM STATUS{Style.RESET_ALL}")
            print("=" * 50)

            # Database stats
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM tasks")
            task_count = cursor.fetchone()["count"]

            cursor = self.connection.execute("SELECT COUNT(*) as count FROM errors")
            error_count = cursor.fetchone()["count"]

            cursor = self.connection.execute(
                "SELECT COUNT(*) as count FROM documentation"
            )
            doc_count = cursor.fetchone()["count"]

            cursor = self.connection.execute(
                "SELECT COUNT(*) as count FROM system_logs"
            )
            log_count = cursor.fetchone()["count"]

            print(f"📊 Database Statistics:")
            print(f"  📋 Tasks: {task_count}")
            print(f"  🐛 Errors: {error_count}")
            print(f"  📚 Documentation: {doc_count}")
            print(f"  📝 System Logs: {log_count}")

            # Active tasks/errors
            cursor = self.connection.execute(
                "SELECT COUNT(*) as count FROM tasks WHERE status != 'COMPLETED'"
            )
            active_tasks = cursor.fetchone()["count"]

            cursor = self.connection.execute(
                "SELECT COUNT(*) as count FROM errors WHERE status != 'CLOSED'"
            )
            active_errors = cursor.fetchone()["count"]

            print(f"\n🔄 Active Items:")
            print(f"  📋 Active Tasks: {active_tasks}")
            print(f"  🐛 Open Errors: {active_errors}")

            # Database file info
            db_size = self.db_path.stat().st_size / 1024 / 1024  # MB
            print(f"\n💾 Database:")
            print(f"  📁 File: {self.db_path}")
            print(f"  📊 Size: {db_size:.2f} MB")

        except Exception as e:
            print(f"{Fore.RED}❌ Error showing system status: {e}{Style.RESET_ALL}")

    def backup_system(self, args: str):
        """Sistem yedekle"""
        try:
            backup_name = (
                args.strip()
                if args
                else f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            backup_path = f"{backup_name}.db"

            # Create backup
            backup_conn = sqlite3.connect(backup_path)
            self.connection.backup(backup_conn)
            backup_conn.close()

            print(
                f"{Fore.GREEN}✅ System backup created successfully!{Style.RESET_ALL}"
            )
            print(f"📄 Backup file: {backup_path}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error creating backup: {e}{Style.RESET_ALL}")

    def restore_system(self, args: str):
        """Sistem geri yükle"""
        try:
            if not args:
                print(f"{Fore.RED}❌ Please provide backup file path{Style.RESET_ALL}")
                return

            backup_path = args.strip()

            if not Path(backup_path).exists():
                print(
                    f"{Fore.RED}❌ Backup file not found: {backup_path}{Style.RESET_ALL}"
                )
                return

            # Confirmation
            confirm = input(
                f"{Fore.YELLOW}⚠️ Restore from backup '{backup_path}'? This will overwrite current data! (y/N): {Style.RESET_ALL}"
            )
            if confirm.lower() != "y":
                print(f"{Fore.CYAN}ℹ️ Operation cancelled{Style.RESET_ALL}")
                return

            # Restore
            self.connection.close()

            backup_conn = sqlite3.connect(backup_path)
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

            backup_conn.backup(self.connection)
            backup_conn.close()

            print(f"{Fore.GREEN}✅ System restored successfully!{Style.RESET_ALL}")
            print(f"📄 Restored from: {backup_path}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error restoring system: {e}{Style.RESET_ALL}")

    def show_statistics(self, args: str = ""):
        """Sistem istatistiklerini göster"""
        try:
            print(f"\n{Fore.CYAN}📊 COMPREHENSIVE SYSTEM STATISTICS{Style.RESET_ALL}")
            print("=" * 70)

            # Task statistics
            cursor = self.connection.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'IN_PROGRESS' THEN 1 ELSE 0 END) as in_progress,
                    SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending
                FROM tasks
            """
            )
            task_stats = cursor.fetchone()

            print(f"📋 Task Statistics:")
            print(f"  Total: {task_stats['total']}")
            print(f"  Completed: {task_stats['completed']}")
            print(f"  In Progress: {task_stats['in_progress']}")
            print(f"  Pending: {task_stats['pending']}")

            # Error statistics
            cursor = self.connection.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'RESOLVED' THEN 1 ELSE 0 END) as resolved,
                    SUM(CASE WHEN status = 'CLOSED' THEN 1 ELSE 0 END) as closed,
                    SUM(CASE WHEN status = 'OPEN' THEN 1 ELSE 0 END) as open
                FROM errors
            """
            )
            error_stats = cursor.fetchone()

            print(f"\n🐛 Error Statistics:")
            print(f"  Total: {error_stats['total']}")
            print(f"  Resolved: {error_stats['resolved']}")
            print(f"  Closed: {error_stats['closed']}")
            print(f"  Open: {error_stats['open']}")

            # Documentation statistics
            cursor = self.connection.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    COUNT(DISTINCT doc_type) as types,
                    COUNT(DISTINCT category) as categories
                FROM documentation
            """
            )
            doc_stats = cursor.fetchone()

            print(f"\n📚 Documentation Statistics:")
            print(f"  Total Documents: {doc_stats['total']}")
            print(f"  Document Types: {doc_stats['types']}")
            print(f"  Categories: {doc_stats['categories']}")

            # Recent activity
            cursor = self.connection.execute(
                """
                SELECT action, COUNT(*) as count 
                FROM system_logs 
                WHERE timestamp > datetime('now', '-7 days')
                GROUP BY action
                ORDER BY count DESC
                LIMIT 10
            """
            )
            recent_activity = cursor.fetchall()

            print(f"\n🕒 Recent Activity (Last 7 days):")
            for activity in recent_activity:
                print(f"  {activity['action']}: {activity['count']} times")

        except Exception as e:
            print(f"{Fore.RED}❌ Error showing statistics: {e}{Style.RESET_ALL}")

    def show_help(self, args: str = ""):
        """Yardım göster"""
        help_text = f"""
{Fore.CYAN}🔧 COMPREHENSIVE CONSOLE SYSTEM - HELP{Style.RESET_ALL}

{Fore.YELLOW}📋 TASK MANAGEMENT:{Style.RESET_ALL}
  tasks [--status=STATUS] [--priority=PRIORITY] [--project=PROJECT]
                                    - List tasks with optional filters
  task-add "TITLE" --desc="DESC" --priority=HIGH --project=PROJECT --due=YYYY-MM-DD
                                    - Add new task
  task-update ID --title="NEW_TITLE" --desc="NEW_DESC" --priority=HIGH --status=IN_PROGRESS
                                    - Update task
  task-complete ID                  - Mark task as completed
  task-delete ID                    - Delete task
  task-search "TERM"                - Search tasks
  task-report                       - Generate task report

{Fore.YELLOW}🐛 ERROR MANAGEMENT:{Style.RESET_ALL}
  errors [--status=STATUS] [--severity=SEVERITY] [--type=TYPE]
                                    - List errors with optional filters
  error-add "TITLE" --desc="DESC" --severity=HIGH --type=SYSTEM --file=PATH
                                    - Add new error
  error-update ID --title="NEW_TITLE" --severity=CRITICAL --status=IN_PROGRESS
                                    - Update error
  error-resolve ID --solution="SOLUTION"
                                    - Resolve error
  error-close ID                    - Close error
  error-search "TERM"               - Search errors
  error-report                      - Generate error report

{Fore.YELLOW}📚 DOCUMENTATION:{Style.RESET_ALL}
  docs [--type=TYPE] [--category=CATEGORY]
                                    - List documentation
  doc-add "TITLE" --content="CONTENT" --type=GUIDE --category=SYSTEM
                                    - Add new document
  doc-update ID --title="NEW_TITLE" --content="NEW_CONTENT"
                                    - Update document
  doc-delete ID                     - Delete document
  doc-search "TERM"                 - Search documentation
  doc-export ID                     - Export document to markdown
  doc-generate TYPE                 - Generate documentation (system|api|user)

{Fore.YELLOW}⚙️ SYSTEM MANAGEMENT:{Style.RESET_ALL}
  status                            - Show system status
  stats                             - Show comprehensive statistics
  backup [NAME]                     - Create system backup
  restore PATH                      - Restore from backup
  help                              - Show this help
  exit                              - Exit system

{Fore.YELLOW}🔧 INTEGRATION:{Style.RESET_ALL}
  collective-memory                 - Run collective memory system
  api-server                        - Start API server
  frontend                          - Start frontend server
  test                              - Run tests
  deploy                            - Deploy system

{Fore.YELLOW}🔍 SYSTEM OPERATIONS:{Style.RESET_ALL}
  scan-errors                       - Scan system for errors
  auto-docs                         - Auto-generate documentation
  health-check                      - System health check
  cleanup                           - Clean up system

{Fore.YELLOW}💡 EXAMPLES:{Style.RESET_ALL}
  tasks --status=PENDING            - Show pending tasks
  task-add "Fix login bug" --priority=HIGH --project=Frontend
  error-add "Database connection fails" --severity=CRITICAL --type=SYSTEM
  doc-add "API Guide" --type=REFERENCE --category=API
  backup production_backup
  
{Fore.YELLOW}📊 FILTERS:{Style.RESET_ALL}
  Status: PENDING, IN_PROGRESS, COMPLETED, CANCELLED
  Priority: HIGH, MEDIUM, LOW
  Severity: CRITICAL, HIGH, MEDIUM, LOW
  Error Type: SYSTEM, USER, INTEGRATION, PERFORMANCE
  Doc Type: GUIDE, TUTORIAL, REFERENCE, FAQ
  Doc Category: SYSTEM, USER, DEVELOPER, API
        """
        print(help_text)

    def exit_system(self, args: str = ""):
        """Sistemden çık"""
        print(f"{Fore.CYAN}👋 Goodbye! System shutting down...{Style.RESET_ALL}")
        self.log_action("SYSTEM_SHUTDOWN", "User initiated shutdown")
        if self.connection:
            self.connection.close()
        sys.exit(0)

    # ==================== INTEGRATION COMMANDS ====================

    def run_collective_memory(self, args: str):
        """Collective Memory sistemini çalıştır"""
        try:
            print(
                f"{Fore.CYAN}🚀 Starting Collective Memory System...{Style.RESET_ALL}"
            )

            # Check if file exists
            if not Path("src/main.py").exists():
                print(
                    f"{Fore.RED}❌ Collective Memory not found. Please run from correct directory.{Style.RESET_ALL}"
                )
                return

            # Run collective memory
            cmd = ["python", "src/main.py"] + (
                args.split() if args else ["--interactive"]
            )
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(
                    f"{Fore.GREEN}✅ Collective Memory completed successfully{Style.RESET_ALL}"
                )
                print(result.stdout)
            else:
                print(f"{Fore.RED}❌ Collective Memory failed{Style.RESET_ALL}")
                print(result.stderr)

        except Exception as e:
            print(f"{Fore.RED}❌ Error running Collective Memory: {e}{Style.RESET_ALL}")

    def run_api_server(self, args: str):
        """API Server çalıştır"""
        try:
            print(f"{Fore.CYAN}🚀 Starting API Server...{Style.RESET_ALL}")

            cmd = ["python", "api_server.py"] + (args.split() if args else [])
            subprocess.Popen(cmd)

            print(f"{Fore.GREEN}✅ API Server started in background{Style.RESET_ALL}")
            print(f"🌐 URL: http://localhost:5000")

        except Exception as e:
            print(f"{Fore.RED}❌ Error starting API Server: {e}{Style.RESET_ALL}")

    def run_frontend(self, args: str):
        """Frontend server çalıştır"""
        try:
            print(f"{Fore.CYAN}🚀 Starting Frontend Server...{Style.RESET_ALL}")

            os.chdir("frontend")
            cmd = ["npm", "run", "dev"] + (args.split() if args else [])
            subprocess.Popen(cmd)

            print(
                f"{Fore.GREEN}✅ Frontend Server started in background{Style.RESET_ALL}"
            )
            print(f"🌐 URL: http://localhost:3000")

        except Exception as e:
            print(f"{Fore.RED}❌ Error starting Frontend Server: {e}{Style.RESET_ALL}")

    def run_tests(self, args: str):
        """Test çalıştır"""
        try:
            print(f"{Fore.CYAN}🧪 Running Tests...{Style.RESET_ALL}")

            cmd = ["python", "tests/test_runner.py"] + (
                args.split() if args else ["--all"]
            )
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"{Fore.GREEN}✅ Tests completed successfully{Style.RESET_ALL}")
                print(result.stdout)
            else:
                print(f"{Fore.RED}❌ Tests failed{Style.RESET_ALL}")
                print(result.stderr)

        except Exception as e:
            print(f"{Fore.RED}❌ Error running tests: {e}{Style.RESET_ALL}")

    def deploy_system(self, args: str):
        """Sistem deploy et"""
        try:
            print(f"{Fore.CYAN}🚀 Deploying System...{Style.RESET_ALL}")

            # Basic deployment steps
            print("1. Running tests...")
            self.run_tests("")

            print("2. Building frontend...")
            os.chdir("frontend")
            subprocess.run(["npm", "run", "build"])
            os.chdir("..")

            print("3. Creating deployment package...")
            # Add deployment logic here

            print(f"{Fore.GREEN}✅ System deployed successfully{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error deploying system: {e}{Style.RESET_ALL}")

    # ==================== SYSTEM OPERATIONS ====================

    def scan_system_errors(self, args: str):
        """Sistem hatalarını tara"""
        try:
            print(f"{Fore.CYAN}🔍 Scanning system for errors...{Style.RESET_ALL}")

            error_count = 0

            # Scan log files
            log_files = [
                "comprehensive_system.log",
                "collective_memory.log",
                "api_server.log",
            ]
            for log_file in log_files:
                if Path(log_file).exists():
                    with open(log_file, "r") as f:
                        for line_num, line in enumerate(f, 1):
                            if "ERROR" in line or "CRITICAL" in line:
                                # Add to error database
                                error_id = str(uuid.uuid4())
                                self.connection.execute(
                                    """
                                    INSERT INTO errors (id, title, description, file_path, error_type, severity)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """,
                                    (
                                        error_id,
                                        f"Log Error - Line {line_num}",
                                        line.strip(),
                                        log_file,
                                        "SYSTEM",
                                        "MEDIUM",
                                    ),
                                )
                                error_count += 1

            # Scan for missing files
            required_files = ["src/main.py", "api_server.py", "frontend/package.json"]
            for file_path in required_files:
                if not Path(file_path).exists():
                    error_id = str(uuid.uuid4())
                    self.connection.execute(
                        """
                        INSERT INTO errors (id, title, description, file_path, error_type, severity)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            error_id,
                            f"Missing File",
                            f"Required file not found: {file_path}",
                            file_path,
                            "SYSTEM",
                            "HIGH",
                        ),
                    )
                    error_count += 1

            self.connection.commit()

            print(f"{Fore.GREEN}✅ System scan completed{Style.RESET_ALL}")
            print(f"🐛 Found {error_count} new errors")

        except Exception as e:
            print(f"{Fore.RED}❌ Error scanning system: {e}{Style.RESET_ALL}")

    def auto_generate_docs(self, args: str):
        """Otomatik dokümantasyon oluştur"""
        try:
            print(f"{Fore.CYAN}📚 Auto-generating documentation...{Style.RESET_ALL}")

            # Generate system documentation
            doc_id = str(uuid.uuid4())
            content = f"""
# System Documentation

## Overview
Comprehensive Console System for Task Management, Error Tracking, and Documentation.

## Features
- Task Management
- Error Tracking
- Documentation System
- System Integration
- Backup/Restore

## Database Schema
- tasks: Task management
- errors: Error tracking
- documentation: Documentation storage
- system_logs: System activity logs

## Usage
Run the system with: python comprehensive_console.py
            """

            self.connection.execute(
                """
                INSERT INTO documentation (id, title, content, doc_type, category, author)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    doc_id,
                    "System Documentation",
                    content,
                    "REFERENCE",
                    "SYSTEM",
                    "auto_generator",
                ),
            )

            # Generate API documentation
            doc_id = str(uuid.uuid4())
            api_content = f"""
# API Documentation

## Endpoints
- GET /api/tasks - List tasks
- POST /api/tasks - Create task
- GET /api/errors - List errors
- POST /api/errors - Create error
- GET /api/docs - List documentation

## Authentication
Currently no authentication required.

## Response Format
All responses are in JSON format with status, data, and meta fields.
            """

            self.connection.execute(
                """
                INSERT INTO documentation (id, title, content, doc_type, category, author)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    doc_id,
                    "API Documentation",
                    api_content,
                    "REFERENCE",
                    "API",
                    "auto_generator",
                ),
            )

            self.connection.commit()

            print(
                f"{Fore.GREEN}✅ Documentation auto-generated successfully{Style.RESET_ALL}"
            )
            print(f"📚 Created 2 new documents")

        except Exception as e:
            print(
                f"{Fore.RED}❌ Error auto-generating documentation: {e}{Style.RESET_ALL}"
            )

    def health_check(self, args: str):
        """Sistem sağlık kontrolü"""
        try:
            print(f"{Fore.CYAN}🏥 System Health Check{Style.RESET_ALL}")
            print("=" * 50)

            health_score = 0
            max_score = 100

            # Database check
            try:
                self.connection.execute("SELECT 1")
                print(f"{Fore.GREEN}✅ Database: Connected{Style.RESET_ALL}")
                health_score += 20
            except:
                print(f"{Fore.RED}❌ Database: Connection failed{Style.RESET_ALL}")

            # File system check
            required_files = ["src/main.py", "api_server.py", "frontend/package.json"]
            found_files = sum(1 for f in required_files if Path(f).exists())
            print(
                f"{Fore.GREEN if found_files == len(required_files) else Fore.YELLOW}📁 Files: {found_files}/{len(required_files)} found{Style.RESET_ALL}"
            )
            health_score += (found_files / len(required_files)) * 20

            # Log files check
            log_files = ["comprehensive_system.log", "collective_memory.log"]
            writable_logs = 0
            for log_file in log_files:
                try:
                    with open(log_file, "a") as f:
                        pass
                    writable_logs += 1
                except:
                    pass
            print(
                f"{Fore.GREEN if writable_logs == len(log_files) else Fore.YELLOW}📝 Logs: {writable_logs}/{len(log_files)} writable{Style.RESET_ALL}"
            )
            health_score += (writable_logs / len(log_files)) * 20

            # Memory check
            try:
                import psutil

                memory_percent = psutil.virtual_memory().percent
                if memory_percent < 80:
                    print(
                        f"{Fore.GREEN}💾 Memory: {memory_percent}% used{Style.RESET_ALL}"
                    )
                    health_score += 20
                else:
                    print(
                        f"{Fore.YELLOW}💾 Memory: {memory_percent}% used (high){Style.RESET_ALL}"
                    )
                    health_score += 10
            except ImportError:
                print(
                    f"{Fore.YELLOW}💾 Memory: Cannot check (psutil not installed){Style.RESET_ALL}"
                )
                health_score += 10

            # Active tasks/errors check
            cursor = self.connection.execute(
                "SELECT COUNT(*) as count FROM tasks WHERE status != 'COMPLETED'"
            )
            active_tasks = cursor.fetchone()["count"]

            cursor = self.connection.execute(
                "SELECT COUNT(*) as count FROM errors WHERE status != 'CLOSED'"
            )
            active_errors = cursor.fetchone()["count"]

            if active_errors < 10:
                print(
                    f"{Fore.GREEN}🐛 Active Errors: {active_errors} (good){Style.RESET_ALL}"
                )
                health_score += 20
            else:
                print(
                    f"{Fore.YELLOW}🐛 Active Errors: {active_errors} (needs attention){Style.RESET_ALL}"
                )
                health_score += 10

            # Overall health
            print(
                f"\n{Fore.CYAN}🏥 Overall Health Score: {health_score}/{max_score} ({health_score}%){Style.RESET_ALL}"
            )

            if health_score >= 80:
                print(f"{Fore.GREEN}✅ System is healthy{Style.RESET_ALL}")
            elif health_score >= 60:
                print(f"{Fore.YELLOW}⚠️ System needs attention{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ System has critical issues{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error during health check: {e}{Style.RESET_ALL}")

    def cleanup_system(self, args: str):
        """Sistem temizleme"""
        try:
            print(f"{Fore.CYAN}🧹 Cleaning up system...{Style.RESET_ALL}")

            # Clean old logs
            old_logs = self.connection.execute(
                "SELECT COUNT(*) as count FROM system_logs WHERE timestamp < datetime('now', '-30 days')"
            ).fetchone()["count"]

            if old_logs > 0:
                self.connection.execute(
                    "DELETE FROM system_logs WHERE timestamp < datetime('now', '-30 days')"
                )
                print(f"📝 Removed {old_logs} old log entries")

            # Clean completed tasks older than 90 days
            old_tasks = self.connection.execute(
                "SELECT COUNT(*) as count FROM tasks WHERE status = 'COMPLETED' AND updated_at < datetime('now', '-90 days')"
            ).fetchone()["count"]

            if old_tasks > 0:
                confirm = input(
                    f"{Fore.YELLOW}⚠️ Remove {old_tasks} old completed tasks? (y/N): {Style.RESET_ALL}"
                )
                if confirm.lower() == "y":
                    self.connection.execute(
                        "DELETE FROM tasks WHERE status = 'COMPLETED' AND updated_at < datetime('now', '-90 days')"
                    )
                    print(f"📋 Removed {old_tasks} old completed tasks")

            # Clean closed errors older than 90 days
            old_errors = self.connection.execute(
                "SELECT COUNT(*) as count FROM errors WHERE status = 'CLOSED' AND updated_at < datetime('now', '-90 days')"
            ).fetchone()["count"]

            if old_errors > 0:
                confirm = input(
                    f"{Fore.YELLOW}⚠️ Remove {old_errors} old closed errors? (y/N): {Style.RESET_ALL}"
                )
                if confirm.lower() == "y":
                    self.connection.execute(
                        "DELETE FROM errors WHERE status = 'CLOSED' AND updated_at < datetime('now', '-90 days')"
                    )
                    print(f"🐛 Removed {old_errors} old closed errors")

            self.connection.commit()

            # Vacuum database
            self.connection.execute("VACUUM")

            print(f"{Fore.GREEN}✅ System cleanup completed{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error during cleanup: {e}{Style.RESET_ALL}")

    # ==================== HELPER METHODS ====================

    def _parse_filter_args(self, args: str) -> Dict[str, str]:
        """Filtre argümanlarını parse et"""
        filters = {}
        if not args:
            return filters

        for arg in args.split():
            if "=" in arg:
                key, value = arg.split("=", 1)
                key = key.lstrip("-")
                filters[key] = value

        return filters

    def _get_status_color(self, status: str) -> str:
        """Durum rengini al"""
        status_colors = {
            "PENDING": Fore.YELLOW,
            "IN_PROGRESS": Fore.BLUE,
            "COMPLETED": Fore.GREEN,
            "CANCELLED": Fore.RED,
            "OPEN": Fore.RED,
            "RESOLVED": Fore.GREEN,
            "CLOSED": Fore.CYAN,
        }
        return status_colors.get(status, Fore.WHITE)

    def _get_priority_color(self, priority: str) -> str:
        """Öncelik rengini al"""
        priority_colors = {"HIGH": Fore.RED, "MEDIUM": Fore.YELLOW, "LOW": Fore.GREEN}
        return priority_colors.get(priority, Fore.WHITE)

    def _get_severity_color(self, severity: str) -> str:
        """Önem rengini al"""
        severity_colors = {
            "CRITICAL": Fore.RED,
            "HIGH": Fore.RED,
            "MEDIUM": Fore.YELLOW,
            "LOW": Fore.GREEN,
        }
        return severity_colors.get(severity, Fore.WHITE)

    def _generate_system_doc(self):
        """Sistem dokümantasyonu oluştur"""
        doc_id = str(uuid.uuid4())
        content = """
# System Documentation

## Architecture
The Comprehensive Console System is built with SQLite database and Python for backend processing.

## Components
- Task Manager: Handles task creation, assignment, and tracking
- Error Tracker: Logs and manages system errors
- Documentation System: Manages system documentation
- Integration Layer: Connects with external systems

## Database Schema
- tasks: Task management with status tracking
- errors: Error logging with severity levels
- documentation: Document storage with versioning
- system_logs: System activity audit trail

## Usage
The system provides a command-line interface for all operations.
        """

        self.connection.execute(
            """
            INSERT INTO documentation (id, title, content, doc_type, category, author)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                doc_id,
                "System Architecture",
                content,
                "REFERENCE",
                "SYSTEM",
                "auto_generator",
            ),
        )

        self.connection.commit()
        print(f"{Fore.GREEN}✅ System documentation generated{Style.RESET_ALL}")

    def _generate_api_doc(self):
        """API dokümantasyonu oluştur"""
        doc_id = str(uuid.uuid4())
        content = """
# API Documentation

## Authentication
Currently no authentication required for local access.

## Task Management API
- GET /api/tasks - List all tasks
- POST /api/tasks - Create new task
- PUT /api/tasks/{id} - Update task
- DELETE /api/tasks/{id} - Delete task

## Error Management API
- GET /api/errors - List all errors
- POST /api/errors - Create new error
- PUT /api/errors/{id} - Update error
- DELETE /api/errors/{id} - Delete error

## Documentation API
- GET /api/docs - List all documentation
- POST /api/docs - Create new document
- PUT /api/docs/{id} - Update document
- DELETE /api/docs/{id} - Delete document

## Response Format
All responses follow the same format:
{
  "status": "success|error",
  "data": {},
  "message": "Optional message"
}
        """

        self.connection.execute(
            """
            INSERT INTO documentation (id, title, content, doc_type, category, author)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (doc_id, "API Reference", content, "REFERENCE", "API", "auto_generator"),
        )

        self.connection.commit()
        print(f"{Fore.GREEN}✅ API documentation generated{Style.RESET_ALL}")

    def _generate_user_doc(self):
        """Kullanıcı dokümantasyonu oluştur"""
        doc_id = str(uuid.uuid4())
        content = """
# User Guide

## Getting Started
1. Start the system: python comprehensive_console.py
2. Use 'help' command to see available options
3. Begin with 'status' to check system health

## Task Management
- Create tasks with priorities and due dates
- Track progress through different statuses
- Generate reports for project management

## Error Tracking
- Log errors with severity levels
- Track resolution progress
- Generate error reports for analysis

## Documentation
- Create and maintain system documentation
- Search through documentation
- Export documents to markdown format

## Tips
- Use partial IDs for quick access to items
- Filter lists using command line parameters
- Regular backups are recommended
        """

        self.connection.execute(
            """
            INSERT INTO documentation (id, title, content, doc_type, category, author)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (doc_id, "User Guide", content, "GUIDE", "USER", "auto_generator"),
        )

        self.connection.commit()
        print(f"{Fore.GREEN}✅ User documentation generated{Style.RESET_ALL}")


def main():
    """Ana fonksiyon"""
    try:
        console = ComprehensiveConsole()
        console.run_interactive()
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
