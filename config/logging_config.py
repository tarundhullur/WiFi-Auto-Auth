"""
Professional logging configuration for WiFi Auto Auth application.
Provides structured, configurable logging with multiple output handlers and log rotation.
"""

import os
import sys
import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class LoggerFactory:
    """Factory class for creating and managing loggers."""

    _loggers = {}
    _configured = False

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger with the specified name.

        Args:
            name: Logger name (typically __name__ of the calling module)

        Returns:
            Configured logger instance
        """
        if not cls._configured:
            cls._setup_logging()

        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)

        return cls._loggers[name]

    @classmethod
    def _setup_logging(cls) -> None:
        """Set up the global logging configuration."""
        if cls._configured:
            return

        # Create formatters
        simple_formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] [%(name)s:%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Set up root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(cls._get_log_level())

        # Clear existing handlers to avoid duplicates
        root_logger.handlers.clear()

        # Console handler
        if cls._is_console_logging_enabled():
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(cls._get_console_log_level())
            console_handler.setFormatter(simple_formatter)
            root_logger.addHandler(console_handler)

        # File handler with rotation
        if cls._is_file_logging_enabled():
            file_handler = cls._create_file_handler(detailed_formatter)
            file_handler.setLevel(logging.DEBUG)  # Always capture all levels in file
            root_logger.addHandler(file_handler)

        cls._configured = True

    @classmethod
    def _get_log_level(cls) -> int:
        """Get the overall log level from environment variables."""
        level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
        return getattr(logging, level_str, logging.INFO)

    @classmethod
    def _get_console_log_level(cls) -> int:
        """Get the console log level from environment variables."""
        level_str = os.getenv('CONSOLE_LOG_LEVEL', os.getenv('LOG_LEVEL', 'INFO')).upper()
        return getattr(logging, level_str, logging.INFO)

    @classmethod
    def _is_console_logging_enabled(cls) -> bool:
        """Check if console logging is enabled."""
        return os.getenv('CONSOLE_LOGGING_ENABLED', 'true').lower() == 'true'

    @classmethod
    def _is_file_logging_enabled(cls) -> bool:
        """Check if file logging is enabled."""
        return os.getenv('LOG_FILE_ENABLED', 'true').lower() == 'true'

    @classmethod
    def _create_file_handler(cls, formatter: logging.Formatter) -> logging.Handler:
        """Create a rotating file handler."""
        log_dir = Path(os.getenv('LOG_DIR', './logs'))
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / 'wifi_auto_auth.log'

        # Get rotation settings from environment
        max_bytes = int(os.getenv('LOG_MAX_BYTES', '10485760'))  # 10MB default
        backup_count = int(os.getenv('LOG_BACKUP_COUNT', '5'))

        # Use RotatingFileHandler for size-based rotation
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )

        handler.setFormatter(formatter)
        return handler

    @classmethod
    def configure_from_args(cls, args) -> None:
        """
        Configure logging based on command line arguments.

        Args:
            args: Parsed command line arguments with logging options
        """
        if hasattr(args, 'log_level'):
            os.environ['LOG_LEVEL'] = args.log_level
        if hasattr(args, 'log_file'):
            os.environ['LOG_FILE_ENABLED'] = 'true' if args.log_file else 'false'
        if hasattr(args, 'log_dir'):
            os.environ['LOG_DIR'] = args.log_dir
        if hasattr(args, 'console_logging'):
            os.environ['CONSOLE_LOGGING_ENABLED'] = 'true' if args.console_logging else 'false'

        # Reconfigure logging with new settings
        cls._configured = False
        cls._setup_logging()


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger.

    Args:
        name: Logger name (typically __name__ of the calling module)

    Returns:
        Configured logger instance
    """
    return LoggerFactory.get_logger(name)


def setup_logging_from_env() -> None:
    """Set up logging configuration from environment variables."""
    LoggerFactory._setup_logging()


# Convenience functions for common logging patterns
def log_function_entry(logger: logging.Logger, func_name: str, *args, **kwargs) -> None:
    """Log function entry with parameters."""
    params = []
    if args:
        params.append(f"args={args}")
    if kwargs:
        params.append(f"kwargs={kwargs}")

    param_str = ", ".join(params) if params else "no parameters"
    logger.debug(f"Entering {func_name}({param_str})")


def log_function_exit(logger: logging.Logger, func_name: str, return_value=None) -> None:
    """Log function exit with return value."""
    if return_value is not None:
        logger.debug(f"Exiting {func_name} with return value: {return_value}")
    else:
        logger.debug(f"Exiting {func_name}")


def log_exception(logger: logging.Logger, exc: Exception, message: str = "Exception occurred") -> None:
    """Log an exception with full traceback."""
    logger.exception(f"{message}: {exc}")