#!/usr/bin/env python3
"""
Third-Party Integrations - External service connections
Phase 4 Advanced Enterprise Feature: Multi-platform integrations
"""

import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import base64
import hashlib


# Integration Base Classes
class IntegrationError(Exception):
    """Base exception for integration errors"""

    pass


class BaseIntegration(ABC):
    """Base class for all third-party integrations"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._authenticated = False

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the service"""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """Test connection to the service"""
        pass

    @abstractmethod
    def sync_data(self, data: Any) -> bool:
        """Sync data to the service"""
        pass


# Notion Integration
class NotionIntegration(BaseIntegration):
    """Notion workspace integration for knowledge management"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.database_id = config.get("database_id")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def authenticate(self) -> bool:
        """Test Notion API authentication"""
        try:
            response = requests.get(
                f"{self.base_url}/users/me", headers=self.headers, timeout=10
            )
            self._authenticated = response.status_code == 200
            return self._authenticated
        except Exception as e:
            self.logger.error(f"Notion authentication failed: {e}")
            return False

    def test_connection(self) -> bool:
        """Test Notion database connection"""
        if not self._authenticated and not self.authenticate():
            return False

        try:
            response = requests.get(
                f"{self.base_url}/databases/{self.database_id}",
                headers=self.headers,
                timeout=10,
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Notion connection test failed: {e}")
            return False

    def sync_data(self, search_results: List[Dict]) -> bool:
        """Sync search results to Notion database"""
        if not self.test_connection():
            return False

        try:
            for result in search_results[:10]:  # Limit to 10 results
                page_data = {
                    "parent": {"database_id": self.database_id},
                    "properties": {
                        "Name": {
                            "title": [
                                {"text": {"content": result.get("title", "Unknown")}}
                            ]
                        },
                        "File Path": {
                            "rich_text": [
                                {"text": {"content": result.get("file_path", "")}}
                            ]
                        },
                        "Score": {"number": float(result.get("score", 0))},
                        "Synced": {"date": {"start": datetime.now().isoformat()}},
                    },
                }

                response = requests.post(
                    f"{self.base_url}/pages",
                    headers=self.headers,
                    json=page_data,
                    timeout=15,
                )

                if response.status_code != 200:
                    self.logger.warning(f"Failed to sync result: {response.text}")

            return True
        except Exception as e:
            self.logger.error(f"Notion sync failed: {e}")
            return False


# Obsidian Integration
class ObsidianIntegration(BaseIntegration):
    """Obsidian vault integration for note management"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.vault_path = Path(config.get("vault_path", ""))
        self.sync_folder = config.get("sync_folder", "Collective Memory")

    def authenticate(self) -> bool:
        """Check if vault path is accessible"""
        try:
            self._authenticated = self.vault_path.exists() and self.vault_path.is_dir()
            return self._authenticated
        except Exception as e:
            self.logger.error(f"Obsidian vault access failed: {e}")
            return False

    def test_connection(self) -> bool:
        """Test Obsidian vault write access"""
        if not self.authenticate():
            return False

        try:
            test_file = self.vault_path / "test_connection.md"
            test_file.write_text("# Test Connection\nThis is a test file.")
            test_file.unlink()  # Delete test file
            return True
        except Exception as e:
            self.logger.error(f"Obsidian connection test failed: {e}")
            return False

    def sync_data(self, search_results: List[Dict]) -> bool:
        """Create Obsidian notes from search results"""
        if not self.test_connection():
            return False

        try:
            sync_dir = self.vault_path / self.sync_folder
            sync_dir.mkdir(exist_ok=True)

            # Create index file
            index_content = f"# Collective Memory Search Results\n\n"
            index_content += (
                f"**Synced:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            for result in search_results:
                title = result.get("title", "Unknown")
                safe_title = "".join(
                    c for c in title if c.isalnum() or c in (" ", "-", "_")
                )

                # Create individual note
                note_path = sync_dir / f"{safe_title}.md"
                note_content = f"# {title}\n\n"
                note_content += f"**File Path:** `{result.get('file_path', '')}`\n"
                note_content += f"**Score:** {result.get('score', 0):.2f}\n"
                note_content += f"**Synced:** {datetime.now().isoformat()}\n\n"

                if "content" in result:
                    note_content += f"## Content\n\n{result['content']}\n\n"

                note_path.write_text(note_content, encoding="utf-8")

                # Add to index
                index_content += f"- [[{safe_title}]]\n"

            # Save index
            index_path = sync_dir / "Search Results Index.md"
            index_path.write_text(index_content, encoding="utf-8")

            return True
        except Exception as e:
            self.logger.error(f"Obsidian sync failed: {e}")
            return False


# VS Code Integration
class VSCodeIntegration(BaseIntegration):
    """VS Code workspace integration"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.workspace_path = Path(config.get("workspace_path", ""))
        self.extension_id = "collective-memory.vscode-extension"

    def authenticate(self) -> bool:
        """Check VS Code workspace access"""
        try:
            self._authenticated = self.workspace_path.exists()
            return self._authenticated
        except Exception as e:
            self.logger.error(f"VS Code workspace access failed: {e}")
            return False

    def test_connection(self) -> bool:
        """Test VS Code workspace configuration"""
        if not self.authenticate():
            return False

        try:
            vscode_dir = self.workspace_path / ".vscode"
            vscode_dir.mkdir(exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"VS Code connection test failed: {e}")
            return False

    def sync_data(self, search_results: List[Dict]) -> bool:
        """Create VS Code snippets and settings"""
        if not self.test_connection():
            return False

        try:
            vscode_dir = self.workspace_path / ".vscode"

            # Create search results as code snippets
            snippets = {
                "Collective Memory Search Results": {
                    "prefix": "cm-search",
                    "body": [
                        "// Collective Memory Search Results",
                        f"// Generated: {datetime.now().isoformat()}",
                        "// Top search results:",
                    ],
                    "description": "Collective Memory search results",
                }
            }

            for i, result in enumerate(search_results[:5]):
                snippets[f"Search Result {i+1}"] = {
                    "prefix": f"cm-result-{i+1}",
                    "body": [
                        f"// File: {result.get('file_path', '')}",
                        f"// Score: {result.get('score', 0):.2f}",
                        f"// {result.get('content', '')[:100]}...",
                    ],
                    "description": f"Search result {i+1}",
                }

            snippets_file = vscode_dir / "collective-memory.code-snippets"
            snippets_file.write_text(json.dumps(snippets, indent=2))

            # Update settings
            settings_file = vscode_dir / "settings.json"
            settings = {}
            if settings_file.exists():
                try:
                    settings = json.loads(settings_file.read_text())
                except:
                    pass

            settings["collective-memory.lastSync"] = datetime.now().isoformat()
            settings["collective-memory.resultsCount"] = len(search_results)

            settings_file.write_text(json.dumps(settings, indent=2))

            return True
        except Exception as e:
            self.logger.error(f"VS Code sync failed: {e}")
            return False


# Slack Integration
class SlackIntegration(BaseIntegration):
    """Slack workspace integration for team notifications"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.webhook_url = config.get("webhook_url")
        self.channel = config.get("channel", "#general")

    def authenticate(self) -> bool:
        """Test Slack webhook"""
        try:
            test_payload = {
                "text": "Collective Memory integration test",
                "channel": self.channel,
            }
            response = requests.post(self.webhook_url, json=test_payload, timeout=10)
            self._authenticated = response.status_code == 200
            return self._authenticated
        except Exception as e:
            self.logger.error(f"Slack authentication failed: {e}")
            return False

    def test_connection(self) -> bool:
        """Test Slack connection"""
        return self.authenticate()

    def sync_data(self, search_results: List[Dict]) -> bool:
        """Send search summary to Slack"""
        if not self.test_connection():
            return False

        try:
            message = f"🔍 *Collective Memory Search Report*\n"
            message += f"Found {len(search_results)} results\n"
            message += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

            if search_results:
                message += "*Top Results:*\n"
                for i, result in enumerate(search_results[:3]):
                    score = result.get("score", 0)
                    title = result.get("title", "Unknown")
                    message += f"{i+1}. {title} (Score: {score:.2f})\n"

            payload = {
                "text": message,
                "channel": self.channel,
                "username": "Collective Memory Bot",
                "icon_emoji": ":brain:",
            }

            response = requests.post(self.webhook_url, json=payload, timeout=15)

            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Slack sync failed: {e}")
            return False


# Integration Manager
class IntegrationManager:
    """Manages all third-party integrations"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = (
            Path(config_path)
            if config_path
            else Path(".collective-memory/integrations.json")
        )
        self.integrations = {}
        self.logger = logging.getLogger(__name__)

        # Available integration types
        self.integration_types = {
            "notion": NotionIntegration,
            "obsidian": ObsidianIntegration,
            "vscode": VSCodeIntegration,
            "slack": SlackIntegration,
        }

        self.load_configurations()

    def load_configurations(self):
        """Load integration configurations"""
        if not self.config_path.exists():
            self.create_default_config()
            return

        try:
            with open(self.config_path, "r") as f:
                configs = json.load(f)

            for name, config in configs.items():
                integration_type = config.get("type")
                if integration_type in self.integration_types:
                    self.integrations[name] = self.integration_types[integration_type](
                        config
                    )

        except Exception as e:
            self.logger.error(f"Failed to load integration configs: {e}")

    def create_default_config(self):
        """Create default integration configuration file"""
        default_config = {
            "notion_workspace": {
                "type": "notion",
                "enabled": False,
                "api_key": "your_notion_api_key",
                "database_id": "your_database_id",
            },
            "obsidian_vault": {
                "type": "obsidian",
                "enabled": False,
                "vault_path": "/path/to/obsidian/vault",
                "sync_folder": "Collective Memory",
            },
            "vscode_workspace": {
                "type": "vscode",
                "enabled": False,
                "workspace_path": "/path/to/vscode/workspace",
            },
            "slack_notifications": {
                "type": "slack",
                "enabled": False,
                "webhook_url": "your_slack_webhook_url",
                "channel": "#collective-memory",
            },
        }

        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(default_config, f, indent=2)

    def sync_to_all(self, search_results: List[Dict]) -> Dict[str, bool]:
        """Sync data to all enabled integrations"""
        results = {}

        for name, integration in self.integrations.items():
            try:
                if integration.config.get("enabled", False):
                    success = integration.sync_data(search_results)
                    results[name] = success

                    if success:
                        self.logger.info(f"Successfully synced to {name}")
                    else:
                        self.logger.warning(f"Failed to sync to {name}")
                else:
                    results[name] = False

            except Exception as e:
                self.logger.error(f"Error syncing to {name}: {e}")
                results[name] = False

        return results

    def test_all_connections(self) -> Dict[str, bool]:
        """Test all integration connections"""
        results = {}

        for name, integration in self.integrations.items():
            try:
                if integration.config.get("enabled", False):
                    success = integration.test_connection()
                    results[name] = success
                else:
                    results[name] = False
            except Exception as e:
                self.logger.error(f"Error testing {name}: {e}")
                results[name] = False

        return results

    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrations"""
        status = {}

        for name, integration in self.integrations.items():
            config = integration.config
            status[name] = {
                "type": config.get("type"),
                "enabled": config.get("enabled", False),
                "authenticated": integration._authenticated,
                "last_sync": config.get("last_sync"),
                "config_valid": bool(
                    integration.test_connection() if config.get("enabled") else True
                ),
            }

        return status


# Export main integration manager
integration_manager = IntegrationManager()
