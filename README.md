# maxlog


[![PyPI version](https://badge.fury.io/py/maxlog.svg)](https://badge.fury.io/py/maxlog)
## Installation

```bash
pip install maxlog
```

## Usage

```python
# Create an instance of the Log class
log = Log(rich_level="INFO", project_dir="/path/to/project")

# Log messages at different levels
log.info("This is an informational message")
log.warning("This is a warning message")
log.error("This is an error message")

# Change the rich level to log only messages with level DEBUG and above
log.rich_level = "DEBUG"

# Log a message with level DEBUG
log.debug("This is a debug message")
```
