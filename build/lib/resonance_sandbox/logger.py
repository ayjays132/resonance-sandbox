import os
import sys
import json
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any

# ANSI color codes for futuristic terminal styling
_RESET = "\x1b[0m"
_LEVEL_COLORS = {
    "DEBUG": "\x1b[38;5;245m",    # Grey
    "INFO": "\x1b[38;5;39m",      # Blue
    "WARNING": "\x1b[38;5;220m",  # Yellow
    "ERROR": "\x1b[38;5;196m",    # Red
    "CRITICAL": "\x1b[38;5;199m", # Magenta
}

class _ColoredFormatter(logging.Formatter):
    """Formatter that adds ANSI colors based on log level."""
    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname
        color = _LEVEL_COLORS.get(level, _RESET)
        record.levelname = f"{color}{level}{_RESET}"
        record.msg = f"{color}{record.getMessage()}{_RESET}"
        return super().format(record)

class _JSONFormatter(logging.Formatter):
    """Formatter that outputs JSON-encoded log entries."""
    def format(self, record: logging.LogRecord) -> str:
        entry: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        return json.dumps(entry, ensure_ascii=False)

def setup_logger(
    name: str = "resonance",
    log_file: str = "logs/resonance.log",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5
) -> Logger:
    """
    Create a layered logger with:
      - Colored console output at INFO level and above.
      - Rotating JSON file output at DEBUG level and above.
      - Automatically creates 'logs/' directory.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # Clear existing handlers
    logger.handlers.clear()

    # 1) Console handler (layer 1)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch_fmt = "[%(asctime)s] %(levelname)s %(name)s → %(message)s"
    ch.setFormatter(_ColoredFormatter(ch_fmt, datefmt="%H:%M:%S"))
    logger.addHandler(ch)

    # 2) Rotating file handler (layer 2)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    fh = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh_fmt = "%(asctime)s %(levelname)s %(name)s %(module)s:%(lineno)d - %(message)s"
    fh.setFormatter(_JSONFormatter(fh_fmt, datefmt="%Y-%m-%dT%H:%M:%S"))
    logger.addHandler(fh)

    # Wrap with LoggerAdapter for structured context
    adapter = logging.LoggerAdapter(logger, {"layer": "core"})
    return adapter
