#!/usr/bin/env python3
"""
Progress Manager - Comprehensive progress tracking and feedback system
Provides progress bars, spinners, timing, and cancellation handling for long operations
"""

import time
import threading
import signal
import sys
from datetime import datetime, timezone
from typing import Optional, Callable, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class OperationStats:
    """Statistics for a completed operation"""
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_items: Optional[int] = None
    processed_items: int = 0
    success: bool = True
    error_message: Optional[str] = None
    custom_stats: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration(self) -> float:
        """Get operation duration in seconds"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()
    
    @property
    def items_per_second(self) -> float:
        """Get processing rate in items per second"""
        duration = self.duration
        if duration > 0 and self.processed_items > 0:
            return self.processed_items / duration
        return 0.0


class ProgressIndicator:
    """Base class for progress indicators"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = time.time()
        self.last_update = self.start_time
        self.is_active = False
        
    def start(self):
        """Start the progress indicator"""
        self.is_active = True
        
    def update(self, current: Optional[int] = None, message: Optional[str] = None):
        """Update the progress indicator"""
        self.last_update = time.time()
        
    def finish(self, success: bool = True, message: Optional[str] = None):
        """Finish the progress indicator"""
        self.is_active = False
        
    def get_elapsed_time(self) -> float:
        """Get elapsed time since start"""
        return time.time() - self.start_time


class ProgressBar(ProgressIndicator):
    """Progress bar for operations with known total items"""
    
    def __init__(self, operation_name: str, total_items: int, width: int = 50):
        super().__init__(operation_name)
        self.total_items = total_items
        self.current_items = 0
        self.width = width
        self.last_printed_length = 0
        
    def start(self):
        """Start the progress bar"""
        super().start()
        print(f"\n🔄 {self.operation_name}")
        self._print_bar()
        
    def update(self, current: Optional[int] = None, message: Optional[str] = None):
        """Update the progress bar"""
        super().update(current, message)
        
        if current is not None:
            self.current_items = min(current, self.total_items)
        else:
            self.current_items = min(self.current_items + 1, self.total_items)
            
        self._print_bar(message)
        
    def _print_bar(self, message: Optional[str] = None):
        """Print the progress bar"""
        if not self.is_active:
            return
            
        # Calculate progress
        progress = self.current_items / self.total_items if self.total_items > 0 else 0
        filled_width = int(self.width * progress)
        
        # Create bar
        bar = "█" * filled_width + "░" * (self.width - filled_width)
        percentage = progress * 100
        
        # Calculate rate and ETA
        elapsed = self.get_elapsed_time()
        rate = self.current_items / elapsed if elapsed > 0 else 0
        
        if rate > 0 and self.current_items < self.total_items:
            remaining_items = self.total_items - self.current_items
            eta_seconds = remaining_items / rate
            eta_str = self._format_time(eta_seconds)
        else:
            eta_str = "00:00"
        
        # Format the line
        status_line = f"\r[{bar}] {percentage:5.1f}% ({self.current_items}/{self.total_items}) "
        status_line += f"Rate: {rate:.1f}/s ETA: {eta_str}"
        
        if message:
            # Truncate message if too long
            max_msg_len = 80 - len(status_line)
            if len(message) > max_msg_len:
                message = message[:max_msg_len-3] + "..."
            status_line += f" | {message}"
        
        # Clear previous line if it was longer
        if len(status_line) < self.last_printed_length:
            status_line += " " * (self.last_printed_length - len(status_line))
        
        print(status_line, end="", flush=True)
        self.last_printed_length = len(status_line)
        
    def finish(self, success: bool = True, message: Optional[str] = None):
        """Finish the progress bar"""
        super().finish(success, message)
        
        # Print final state
        if success:
            self.current_items = self.total_items
            self._print_bar()
            elapsed = self.get_elapsed_time()
            rate = self.total_items / elapsed if elapsed > 0 else 0
            final_msg = message or f"Completed in {self._format_time(elapsed)} ({rate:.1f}/s)"
            print(f"\n✅ {final_msg}")
        else:
            error_msg = message or "Operation failed"
            print(f"\n❌ {error_msg}")
        
        print()  # Add blank line
        
    def _format_time(self, seconds: float) -> str:
        """Format time in MM:SS format"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"


class Spinner(ProgressIndicator):
    """Spinner for operations with unknown duration"""
    
    SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, operation_name: str):
        super().__init__(operation_name)
        self.spinner_index = 0
        self.message = ""
        self.thread = None
        self.stop_event = threading.Event()
        
    def start(self):
        """Start the spinner"""
        super().start()
        print(f"\n🔄 {self.operation_name}")
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()
        
    def update(self, current: Optional[int] = None, message: Optional[str] = None):
        """Update the spinner message"""
        super().update(current, message)
        if message:
            self.message = message
            
    def _spin(self):
        """Spinner animation loop"""
        while not self.stop_event.is_set():
            char = self.SPINNER_CHARS[self.spinner_index]
            elapsed = self.get_elapsed_time()
            elapsed_str = f"{elapsed:.1f}s"
            
            status_line = f"\r{char} {elapsed_str}"
            if self.message:
                status_line += f" | {self.message}"
            
            print(status_line, end="", flush=True)
            
            self.spinner_index = (self.spinner_index + 1) % len(self.SPINNER_CHARS)
            time.sleep(0.1)
            
    def finish(self, success: bool = True, message: Optional[str] = None):
        """Finish the spinner"""
        super().finish(success, message)
        
        # Stop the spinner thread
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join(timeout=0.5)
        
        # Clear the spinner line
        print("\r" + " " * 80 + "\r", end="")
        
        # Print final message
        elapsed = self.get_elapsed_time()
        if success:
            final_msg = message or f"Completed in {elapsed:.1f}s"
            print(f"✅ {final_msg}")
        else:
            error_msg = message or "Operation failed"
            print(f"❌ {error_msg}")
        
        print()  # Add blank line


class ProgressManager:
    """Comprehensive progress management system"""
    
    def __init__(self):
        self.current_operation: Optional[ProgressIndicator] = None
        self.operation_stats: OperationStats = None
        self.cancelled = False
        self.cancellation_handler: Optional[Callable] = None
        self.operation_history: List[OperationStats] = []
        
        # Set up signal handlers for graceful cancellation
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """Set up signal handlers for Ctrl+C cancellation"""
        def signal_handler(signum, frame):
            if self.current_operation and self.current_operation.is_active:
                print("\n\n🛑 Operation cancellation requested...")
                self.cancel_operation()
            else:
                # If no operation is running, exit normally
                print("\n\nExiting...")
                sys.exit(0)
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, signal_handler)
        
    def start_operation(self, operation_name: str, total_items: Optional[int] = None, 
                       show_spinner: bool = False, unit: str = "items", show_eta: bool = True) -> bool:
        """
        Start a new operation with progress tracking
        
        Args:
            operation_name: Name of the operation
            total_items: Total number of items (for progress bar)
            show_spinner: Use spinner instead of progress bar
            
        Returns:
            True if operation started successfully
        """
        # Finish any existing operation
        if self.current_operation and self.current_operation.is_active:
            self.finish_operation(success=False, message="Interrupted by new operation")
        
        # Reset cancellation state
        self.cancelled = False
        
        # Create operation stats
        self.operation_stats = OperationStats(
            name=operation_name,
            start_time=datetime.now(timezone.utc),
            total_items=total_items
        )
        
        # Create appropriate progress indicator
        if show_spinner or total_items is None:
            self.current_operation = Spinner(operation_name)
        else:
            self.current_operation = ProgressBar(operation_name, total_items)
        
        # Start the indicator
        self.current_operation.start()
        return True
        
    def update_progress(self, current_item: Optional[int] = None, 
                       message: Optional[str] = None) -> bool:
        """
        Update progress for the current operation
        
        Args:
            current_item: Current item number (for progress bars)
            message: Status message to display
            
        Returns:
            True if update was successful, False if cancelled
        """
        if self.cancelled:
            return False
            
        if self.current_operation and self.current_operation.is_active:
            self.current_operation.update(current_item, message)
            
            # Update stats
            if self.operation_stats and current_item is not None:
                self.operation_stats.processed_items = current_item
                
        return True
        
    def finish_operation(self, success: bool = True, message: Optional[str] = None,
                        show_stats: bool = False, show_performance: bool = False, 
                        custom_stats: Optional[Dict[str, Any]] = None) -> OperationStats:
        """
        Finish the current operation
        
        Args:
            success: Whether the operation succeeded
            message: Final message to display
            show_stats: Whether to show detailed statistics
            custom_stats: Additional statistics to record
            
        Returns:
            OperationStats object with operation details
        """
        if self.current_operation and self.current_operation.is_active:
            self.current_operation.finish(success, message)
            
        # Finalize stats
        if self.operation_stats:
            self.operation_stats.end_time = datetime.now(timezone.utc)
            self.operation_stats.success = success
            if not success and message:
                self.operation_stats.error_message = message
            if custom_stats:
                self.operation_stats.custom_stats.update(custom_stats)
                
            # Show detailed stats if requested
            if show_stats or show_performance:
                self._show_operation_stats(self.operation_stats)
                
            # Add to history
            self.operation_history.append(self.operation_stats)
            
            # Keep only last 10 operations in history
            if len(self.operation_history) > 10:
                self.operation_history.pop(0)
                
            stats = self.operation_stats
            self.operation_stats = None
            return stats
            
        return None
        
    def cancel_operation(self):
        """Cancel the current operation"""
        self.cancelled = True
        
        # Call cancellation handler if set
        if self.cancellation_handler:
            try:
                self.cancellation_handler()
            except Exception as e:
                print(f"Warning: Cancellation handler failed: {e}")
                
        # Finish current operation as cancelled
        if self.current_operation and self.current_operation.is_active:
            self.finish_operation(success=False, message="Operation cancelled by user")
            
    def is_cancelled(self) -> bool:
        """Check if the current operation has been cancelled"""
        return self.cancelled
        
    def set_cancellation_handler(self, handler: Callable):
        """Set a handler to be called when operation is cancelled"""
        self.cancellation_handler = handler
        
    def _show_operation_stats(self, stats: OperationStats):
        """Show detailed operation statistics"""
        print(f"\n📊 Operation Statistics:")
        print(f"   • Name: {stats.name}")
        print(f"   • Duration: {stats.duration:.2f}s")
        print(f"   • Status: {'✅ Success' if stats.success else '❌ Failed'}")
        
        if stats.total_items:
            print(f"   • Items: {stats.processed_items}/{stats.total_items}")
            completion_rate = (stats.processed_items / stats.total_items) * 100
            print(f"   • Completion: {completion_rate:.1f}%")
            
        if stats.items_per_second > 0:
            print(f"   • Rate: {stats.items_per_second:.1f} items/s")
            
        if stats.custom_stats:
            print(f"   • Additional Stats:")
            for key, value in stats.custom_stats.items():
                print(f"     - {key}: {value}")
                
        if not stats.success and stats.error_message:
            print(f"   • Error: {stats.error_message}")
            
    def get_operation_history(self) -> List[OperationStats]:
        """Get history of recent operations"""
        return self.operation_history.copy()
        
    def get_current_operation_stats(self) -> Optional[OperationStats]:
        """Get stats for the current operation"""
        return self.operation_stats


# Convenience functions for simple progress tracking
def with_progress_bar(operation_name: str, total_items: int):
    """Decorator for functions that need progress tracking"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            progress_manager = ProgressManager()
            progress_manager.start_operation(operation_name, total_items)
            try:
                result = func(progress_manager, *args, **kwargs)
                progress_manager.finish_operation(success=True)
                return result
            except Exception as e:
                progress_manager.finish_operation(success=False, message=str(e))
                raise
        return wrapper
    return decorator


def with_spinner(operation_name: str):
    """Decorator for functions that need spinner progress tracking"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            progress_manager = ProgressManager()
            progress_manager.start_operation(operation_name, show_spinner=True)
            try:
                result = func(progress_manager, *args, **kwargs)
                progress_manager.finish_operation(success=True)
                return result
            except Exception as e:
                progress_manager.finish_operation(success=False, message=str(e))
                raise
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test the progress manager
    import random
    
    def test_progress_bar():
        """Test progress bar functionality"""
        pm = ProgressManager()
        pm.start_operation("Test Progress Bar", total_items=100)
        
        for i in range(100):
            time.sleep(0.05)  # Simulate work
            pm.update_progress(i + 1, f"Processing item {i + 1}")
            
            if pm.is_cancelled():
                break
                
        pm.finish_operation(success=True, show_stats=True)
        
    def test_spinner():
        """Test spinner functionality"""
        pm = ProgressManager()
        pm.start_operation("Test Spinner", show_spinner=True)
        
        for i in range(50):
            time.sleep(0.1)  # Simulate work
            pm.update_progress(message=f"Processing step {i + 1}")
            
            if pm.is_cancelled():
                break
                
        pm.finish_operation(success=True, show_stats=True)
    
    print("Testing Progress Manager...")
    print("Press Ctrl+C to test cancellation")
    
    try:
        test_progress_bar()
        time.sleep(1)
        test_spinner()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")