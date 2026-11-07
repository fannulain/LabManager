"""
Core Logging Configuration and Audit Trail System.
Logs all operational actions, security authentications, errors, and access checks.
"""

import json
import logging
import os
from datetime import datetime, timezone

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
DEFAULT_LOG_FILE = os.path.join(LOG_DIR, "system.log")

def setup_logging(log_file=None):
    """Set up structured file and console logging."""
    os.makedirs(LOG_DIR, exist_ok=True)
    target_file = log_file or DEFAULT_LOG_FILE

    logger = logging.getLogger("LabManager")
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if already configured
    if not logger.handlers:
        file_handler = logging.FileHandler(target_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logging()

def audit_log(action: str, user_id: str = None, details: dict = None, level: str = "INFO"):
    """
    Structured audit logging for security, operations, and compliance.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "user_id": user_id or "anonymous",
        "details": details or {}
    }
    msg = f"AUDIT: {action} | User: {entry['user_id']} | Details: {json.dumps(entry['details'])}"
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(msg)
