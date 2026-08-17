"""结构化日志配置。所有节的 __main__ demo 都通过此模块初始化 logger。"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

FORMAT = "%(asctime)s [%(module)s|%(levelname)-7s] %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    module: str = "main",
    level: int = logging.INFO,
    logfile: str | Path | None = None,
) -> logging.Logger:
    """配置并返回一个 logger。

    Args:
        module: 日志格式中显示的节标识（如 "7.3"）。
        level: 日志级别。
        logfile: 可选日志文件；父目录自动创建。
    """
    logger = logging.getLogger(module)
    logger.setLevel(level)
    logger.propagate = False
    logger.handlers.clear()

    formatter = logging.Formatter(FORMAT.replace("%(module)s", module), DATE_FMT)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    if logfile is not None:
        path = Path(logfile)
        path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(path, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger