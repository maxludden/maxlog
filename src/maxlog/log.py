# ruff: noqa: F401
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Union, List, Dict, Any, Optional, Tuple
from collections.abc import Sequence
from os import getenv, environ
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL


import loguru
from loguru import logger
from dotenv import load_dotenv
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.text import Text, TextType
from rich.box import ROUNDED
from rich.style import Style, StyleType

load_dotenv()

class Log:
    """A custom project loguru.logger for MaxLog.
    
    Attributes:
        rich_level (int): The level at which to log to the console.
        proj_dir (Path, optional): The project directory. Defualts to None, in \
            which case the project directory is set from the environmental \
            variable VIRTUAL_ENV_PROMPT.
        console (rich.console.Console): The rich console.
        logger (loguru.Logger, optional): The loguru logger.
        handlers (List[Dict[str, Any]], optional): The loguru handlers. Defaults \
            to None, in which case the handlers are set to the default handlers.
    """
    FORMAT: str = """{time:hh:mm:ss:SSS A} | {file.name: ^13} |  \
    Line {line: ^5} | {level: ^8} ﰲ  {message}"""

    def __init__(
        self,
        rich_level: Union[str,int] = "SUCCESS",
        project_dir: Optional[str|Path] = None,
        console: Optional[Console] = None,
        logger: Optional[loguru.Logger] = logger,
        handlers: List[Dict[str, Any]] = []) -> None:
        # Set logger
        if logger is None:
            logger = loguru.logger
        self.logger: loguru.Logger = logger
        self.logger.remove()
        
        # Set rich level
        self.rich_level = rich_level
        
        # Set console
        if console is None:
            console = Console()
        self.console = console

        # Set project path
        self.proj_dir = project_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._create_log_files()
        
        if len(handlers) == 0:
            handlers = []
            for file in self.log_dir.iterdir():
                handlers.append(self._write_handler(file))

        handlers.append(
            dict(
                sink=self._console_sink,
                format="{message}",
                filter=self._rich_filter,
                backtrace=False,
                diagnose=False,
            )
        )
        
        logger.remove()
        logger.configure(
            handlers=handlers,
            extra={"project_path": self.proj_dir}
        )

    @property
    def proj_dir(self) -> Path:
        return self._project_path

    @proj_dir.setter
    def proj_dir(self, project_path: Optional[Union[str, Path]]) -> None:
        if project_path is None:
            load_dotenv()
            venv = getenv("VIRTUAL_ENV_PROMPT")
            if venv is None:
                raise ValueError(
                    "No project path provided and no environmental variable found."
                )
            else:
                self._project_path = Path('/Users/maxludden/dev/py/') / venv
        elif isinstance(project_path, str):
            self._project_path = Path(project_path)
        elif isinstance(project_path, Path):
            self._project_path = project_path
        else:
            raise TypeError(
                "project_path must be a str or Path object."
            )
            
    @property
    def log_dir(self) -> Path:
        """Create log directory."""
        return self.proj_dir / "logs"

    @property
    def rich_level(self) -> int:
        return self._rich_level

    @rich_level.setter
    def rich_level(self, rich_level: Union[str, int]) -> None:
        """Set the level at which to log to the console."""
        if isinstance(rich_level, str):
            rich_level = rich_level.upper()
            match rich_level:
                case "TRACE":
                    self._rich_level = 5
                case "DEBUG":
                    self._rich_level = 10
                case "INFO":
                    self._rich_level = 20
                case "SUCCESS":
                    self._rich_level = 25
                case "WARNING":
                    self._rich_level = 30
                case "ERROR":
                    self._rich_level = 40
                case "CRITICAL":
                    self._rich_level = 50
                case _:
                    raise ValueError(
                        "rich_level must be one of: TRACE, DEBUG, INFO, SUCCESS, \
                            WARNING, ERROR, CRITICAL"
                    )
        elif isinstance(rich_level, int):
            if rich_level < 0 or rich_level > 50:
                raise ValueError(
                    "rich_level must be an integer between 0 and 50."
                )
            else:
                self._rich_level = rich_level
        else:
            raise TypeError(
                "rich_level must be a str or int."
            )

    def _console_sink(self, msg: loguru.Message) -> None:
        """A loguru sink that prints to the console.
        
        Args:
            msg (loguru.Message): The loguru message to print.
        """
        
        record: loguru.Record = msg.record
        level_str: str = str(record['level'].name)
        style: Style = Style.null()
        
        match level_str:
            case "TRACE":
                style = Style(color="#aaaaaa", italic=True)
            case "DEBUG":
                style = Style(color="#ffabf4", italic=True, bold=True)
            case "INFO":
                style = Style(color="#a71aff", bold=True)
            case "SUCCESS":
                style = Style(color="#6e88ff", bold=True)
            case "WARNING":
                style = Style(color="#E6EF85", bold=True, italic=True)
            case "ERROR":
                style = Style(color="#ffaf00", bold=True)
            case "CRITICAL":
                style = Style(color="#ffffff", bgcolor="#ff0000", bold=True, blink=True)
        
        reversed_style: Style = style + Style(reverse=True)
        
        width: int = self.console.width - 2
        
        time: Text = Text(self.console.get_datetime().strftime("%H:%M:%S"), style=style)
        level: Text = Text(str(f"  {level_str}  "), style=reversed_style)
        message: Text = Text(record['message'], style=style)
        
        table = Table(
            show_header = False,
            show_footer = False,
            show_edge = False,
            show_lines = False,
            expand = True,
            width=width
        )
        table.add_column("Time", justify="right", ratio=1, min_width = 10)
        table.add_column("Level", justify="center", ratio=1, min_width = 10)
        table.add_column("Message", justify="left", ratio=10)
        table.add_row(time, level, message)
        if record["level"].no >= self.rich_level:
            self.console.log(table, log_locals=True)
        else:
            self.console.log(table)

    def _rich_filter(self, record: loguru.Record) -> bool:
        """A loguru filter that determines whether to log to the console.
        
        Args:
            record (loguru.Record): The loguru record to filter.
        
        Returns:
            bool: Whether to log the record to the console.
        """
        return record["level"].no >= self.rich_level

    def _run_patcher(self, run: int) ->

    def _create_log_files(
        self,
        log_files: Optional[List[str]] = None) -> None:
        """Create log files."""
        if log_files is None:
            log_files = [
                "debug.log",
                "info.log",
            ]
        self.log_dir.mkdir(parents=True, exist_ok=True)
        for file in log_files:
            (self.log_dir / file).touch(exist_ok=True)

    def _write_env_vars(self) -> None:
        """Assign MaxLog environmental variables."""
        environ['MAXLOG_PROJECT_PATH'] = str(self.proj_dir)
        environ['MAXLOG_LOG_DIR'] = str(self.log_dir)

    def _write_handler(
        self,
        sink: str|Path,
        format: Optional[str] = None) -> Dict[str, Any]:
        """Create a loguru handler."""
        # handler
        if isinstance(sink, str):
            sink = Path(sink)

        # level
        level: str = sink.stem.upper()
        if level not in [
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL"]:
            raise ValueError(f"Sink is not a valid log level: {level}")

        # format
        if format is None:
            format = self.FORMAT

        return {
            "sink": str(sink),
            "format": format,
            "level": level,
            "diagnose": True,
            "backtrace": True,
            "colorize": True
        }

    def get_logger(self) -> loguru.Logger:
        return self.logger
    