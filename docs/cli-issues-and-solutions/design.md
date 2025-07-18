# CLI Issues and Solutions - Design Document

## Overview

Bu tasarım dokümanı, Collective Memory sisteminde CLI (Command Line Interface) ile ilgili sorunları ve çözümlerini detaylandırır. Hafızadaki bilgiler kullanılarak, mevcut sistem mimarisine uygun CLI çözümleri tasarlanmıştır.

## Memory Context

### System Status
- **Smart Context Bridge:** Phase 4 %100 tamamlanmış
- **JSON Chat System:** Tam entegre edilmiş
- **Enterprise Features:** Phase 3 %100 tamamlanmış
- **Documentation Standards:** Düzeltilmiş ve standartlaştırılmış

### Related Components
- ContextBridgeCLI sınıfı
- chat_cli.py - JSON Chat System CLI
- api_server.py - API server
- Smart Context Bridge CLI entegrasyonu

## Architecture

### Current State
Mevcut CLI implementasyonunun durumu ve sınırlılıkları:

- **ContextBridgeCLI:** `start()` metodu yok, `cmd_start()` kullanılıyor
- **CLI Komutları:** Tutarsız komut yapısı
- **Error Handling:** Yetersiz hata yönetimi
- **Documentation:** CLI kullanımı dokümantasyonda yanlış

### Proposed Solution
Yeni CLI implementasyon yaklaşımı:

- **Unified CLI Interface:** Tüm CLI komutları için tutarlı arayüz
- **Proper Method Names:** Doğru metod isimleri kullanımı
- **Comprehensive Error Handling:** Kapsamlı hata yönetimi
- **Updated Documentation:** Doğru CLI kullanım dokümantasyonu

## Components and Interfaces

### 1. ContextBridgeCLI Fix
```python
class ContextBridgeCLI:
    """Fixed ContextBridgeCLI with proper method names"""
    
    def __init__(self):
        self.bridge = SmartContextBridge()
        self.logger = logging.getLogger(__name__)
        
    def cmd_start(self):
        """Start Smart Context Bridge - CORRECT METHOD NAME"""
        try:
            self.bridge.start_monitoring()
            self.logger.info("Smart Context Bridge started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Smart Context Bridge: {e}")
            return False
            
    def cmd_status(self):
        """Get Smart Context Bridge status"""
        try:
            status = self.bridge.get_status()
            return status
        except Exception as e:
            self.logger.error(f"Failed to get status: {e}")
            return None
            
    def cmd_stop(self):
        """Stop Smart Context Bridge"""
        try:
            self.bridge.stop_monitoring()
            self.logger.info("Smart Context Bridge stopped successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop Smart Context Bridge: {e}")
            return False
```

### 2. Unified CLI Manager
```python
class CollectiveMemoryCLI:
    """Unified CLI manager for all Collective Memory commands"""
    
    def __init__(self):
        self.context_bridge = ContextBridgeCLI()
        self.chat_manager = JSONChatManager()
        self.api_server = None
        
    def start_context_bridge(self):
        """Start Smart Context Bridge"""
        return self.context_bridge.cmd_start()
        
    def start_api_server(self):
        """Start API server"""
        try:
            self.api_server = CollectiveMemoryAPI()
            self.api_server.run()
            return True
        except Exception as e:
            self.logger.error(f"Failed to start API server: {e}")
            return False
            
    def create_chat(self, title: str):
        """Create new chat conversation"""
        try:
            conversation_id = self.chat_manager.create_conversation({
                'title': title,
                'created_at': datetime.now().isoformat()
            })
            return conversation_id
        except Exception as e:
            self.logger.error(f"Failed to create chat: {e}")
            return None
```

### 3. CLI Error Handler
```python
class CLIErrorHandler:
    """Comprehensive CLI error handling"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def handle_method_not_found(self, method_name: str, available_methods: list):
        """Handle method not found errors"""
        error_msg = f"Method '{method_name}' not found. Available methods: {available_methods}"
        self.logger.error(error_msg)
        return {
            'error': 'method_not_found',
            'message': error_msg,
            'available_methods': available_methods
        }
        
    def handle_import_error(self, module_name: str, error: Exception):
        """Handle import errors"""
        error_msg = f"Failed to import {module_name}: {error}"
        self.logger.error(error_msg)
        return {
            'error': 'import_error',
            'message': error_msg,
            'suggestion': f"Check if {module_name} is properly installed"
        }
        
    def handle_configuration_error(self, config_key: str, error: Exception):
        """Handle configuration errors"""
        error_msg = f"Configuration error for {config_key}: {error}"
        self.logger.error(error_msg)
        return {
            'error': 'configuration_error',
            'message': error_msg,
            'suggestion': f"Check configuration for {config_key}"
        }
```

## Data Models

### CLI Command Model
```python
@dataclass
class CLICommand:
    """CLI command model"""
    
    name: str
    description: str
    method_name: str
    arguments: List[str]
    options: Dict[str, Any]
    examples: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            'name': self.name,
            'description': self.description,
            'method_name': self.method_name,
            'arguments': self.arguments,
            'options': self.options,
            'examples': self.examples
        }
```

### CLI Error Model
```python
@dataclass
class CLIError:
    """CLI error model"""
    
    error_type: str
    message: str
    command: str
    timestamp: datetime
    suggestion: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            'error_type': self.error_type,
            'message': self.message,
            'command': self.command,
            'timestamp': self.timestamp.isoformat(),
            'suggestion': self.suggestion,
            'details': self.details
        }
```

## Error Handling

### Method Name Errors
```python
def fix_method_name_errors(self):
    """Fix method name related errors"""
    
    # Common method name mappings
    method_mappings = {
        'start': 'cmd_start',
        'stop': 'cmd_stop',
        'status': 'cmd_status',
        'config': 'cmd_config',
        'analyze': 'cmd_analyze'
    }
    
    def get_correct_method_name(method_name: str) -> str:
        """Get correct method name from mapping"""
        return method_mappings.get(method_name, method_name)
        
    def validate_method_exists(obj, method_name: str) -> bool:
        """Validate if method exists on object"""
        return hasattr(obj, method_name) and callable(getattr(obj, method_name))
```

### Import Error Handling
```python
def handle_import_errors(self):
    """Handle import-related errors"""
    
    def safe_import(module_name: str, class_name: str = None):
        """Safely import module or class"""
        try:
            if class_name:
                module = __import__(module_name, fromlist=[class_name])
                return getattr(module, class_name)
            else:
                return __import__(module_name)
        except ImportError as e:
            self.logger.error(f"Import error for {module_name}: {e}")
            return None
        except AttributeError as e:
            self.logger.error(f"Attribute error for {class_name} in {module_name}: {e}")
            return None
```

### Configuration Error Handling
```python
def handle_configuration_errors(self):
    """Handle configuration-related errors"""
    
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration"""
        required_keys = ['enabled', 'debug_mode', 'log_level']
        
        for key in required_keys:
            if key not in config:
                self.logger.error(f"Missing required config key: {key}")
                return False
                
        return True
        
    def load_config_safely(config_path: str) -> Dict[str, Any]:
        """Safely load configuration"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            if not validate_config(config):
                return self.get_default_config()
                
            return config
            
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_path}, using defaults")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return self.get_default_config()
```

## Testing Strategy

### CLI Method Testing
```python
class TestCLIMethods:
    """Test CLI method functionality"""
    
    def test_context_bridge_start_method(self):
        """Test ContextBridgeCLI start method"""
        cli = ContextBridgeCLI()
        
        # Test correct method name
        assert hasattr(cli, 'cmd_start')
        assert callable(getattr(cli, 'cmd_start'))
        
        # Test incorrect method name
        assert not hasattr(cli, 'start')
        
    def test_method_name_mapping(self):
        """Test method name mapping"""
        cli = CollectiveMemoryCLI()
        
        # Test method name corrections
        assert cli.get_correct_method_name('start') == 'cmd_start'
        assert cli.get_correct_method_name('status') == 'cmd_status'
        
    def test_error_handling(self):
        """Test error handling"""
        error_handler = CLIErrorHandler()
        
        # Test method not found error
        result = error_handler.handle_method_not_found('start', ['cmd_start', 'cmd_stop'])
        assert result['error'] == 'method_not_found'
        assert 'start' in result['message']
```

### Integration Testing
```python
class TestCLIIntegration:
    """Test CLI integration"""
    
    def test_unified_cli_interface(self):
        """Test unified CLI interface"""
        cli = CollectiveMemoryCLI()
        
        # Test context bridge integration
        assert hasattr(cli, 'start_context_bridge')
        assert callable(cli.start_context_bridge)
        
        # Test chat system integration
        assert hasattr(cli, 'create_chat')
        assert callable(cli.create_chat)
        
    def test_error_recovery(self):
        """Test error recovery mechanisms"""
        cli = CollectiveMemoryCLI()
        
        # Test graceful error handling
        result = cli.start_context_bridge()
        # Should not crash even if bridge fails to start
        assert isinstance(result, bool)
```

## Implementation Guidelines

### Code Standards
- Use consistent method naming convention (cmd_* for CLI methods)
- Implement comprehensive error handling
- Add detailed logging for debugging
- Follow PEP 8 style guidelines

### Security Considerations
- Validate all CLI input before processing
- Implement proper authentication for sensitive commands
- Sanitize user input to prevent injection attacks
- Use secure communication protocols

### Performance Optimization
- Use efficient command parsing
- Implement command caching where appropriate
- Optimize import statements
- Monitor and profile performance bottlenecks

## Deployment Considerations

### Environment Variables
```bash
# CLI Configuration
CLI_DEBUG_MODE=false
CLI_LOG_LEVEL=INFO
CLI_TIMEOUT=30

# Error Handling
CLI_ERROR_RETRY_COUNT=3
CLI_ERROR_RETRY_DELAY=1

# Security
CLI_AUTH_REQUIRED=true
CLI_SSL_ENABLED=true
```

### Production Deployment
- Use proper logging configuration
- Implement monitoring and alerting
- Set up backup and recovery procedures
- Configure security settings

## Maintenance and Monitoring

### Health Checks
```python
def cli_health_check() -> Dict[str, Any]:
    """CLI health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'available_commands': get_available_commands(),
        'error_count': get_error_count()
    }
```

### Monitoring Metrics
- CLI command execution metrics
- Error rates and failure patterns
- Response time measurements
- User activity patterns

### Troubleshooting
- Common CLI error scenarios and solutions
- Diagnostic tools and procedures
- Log analysis and debugging techniques
- Performance optimization guidelines

## Integration Points

### Smart Context Bridge Integration
```python
def integrate_with_context_bridge(self):
    """Integrate CLI with Smart Context Bridge"""
    try:
        # Use correct method name
        self.context_bridge.cmd_start()
        self.logger.info("Context Bridge integration successful")
        return True
    except Exception as e:
        self.logger.error(f"Context Bridge integration failed: {e}")
        return False
```

### JSON Chat System Integration
```python
def integrate_with_chat_system(self):
    """Integrate CLI with JSON Chat System"""
    try:
        # Use chat CLI commands
        conversation_id = self.chat_manager.create_conversation({
            'title': 'CLI Integration Test',
            'created_at': datetime.now().isoformat()
        })
        return conversation_id
    except Exception as e:
        self.logger.error(f"Chat system integration failed: {e}")
        return None
```

### Enterprise Features Integration
```python
def integrate_with_enterprise_features(self):
    """Integrate CLI with Enterprise Features"""
    try:
        # Start API server with CLI
        self.api_server = CollectiveMemoryAPI()
        self.api_server.run()
        return True
    except Exception as e:
        self.logger.error(f"Enterprise features integration failed: {e}")
        return False
```

## Success Criteria

### Technical Metrics
- All CLI methods use correct naming convention
- 100% error handling coverage
- <100ms response time for CLI commands
- 99.9% CLI availability

### User Experience Metrics
- Clear error messages for users
- Comprehensive help documentation
- Intuitive command structure
- Consistent behavior across all commands

---

**Document Version:** 1.0  
**Last Updated:** 18 Temmuz 2025  
**Status:** Draft  
**Memory Integration:** ✅ Active 