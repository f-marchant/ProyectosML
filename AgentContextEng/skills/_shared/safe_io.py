"""Small standard-library helpers for safe CLI persistence."""
import json
import os
import tempfile
import time


class SafeIOError(ValueError):
    """Expected input or persistence error suitable for a CLI message."""


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SafeIOError(f"No se pudo leer JSON '{path}': {exc}") from exc


def atomic_write_text(path, content):
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".tmp-", dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except OSError:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def atomic_write_json(path, value):
    atomic_write_text(path, json.dumps(value, ensure_ascii=False, indent=1))


class FileLock:
    def __init__(self, path, timeout=5.0, poll=0.05):
        self.path = path + ".lock"
        self.timeout = timeout
        self.poll = poll
        self.fd = None

    def __enter__(self):
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(self.fd, str(os.getpid()).encode("ascii"))
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise SafeIOError(f"No se pudo obtener el lock '{self.path}'")
                time.sleep(self.poll)
            except OSError as exc:
                raise SafeIOError(f"No se pudo crear el lock '{self.path}': {exc}") from exc

    def __exit__(self, exc_type, exc, tb):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        try:
            os.unlink(self.path)
        except FileNotFoundError:
            pass
        return False


def require_finite_nonnegative(value, name):
    if value < 0 or value != value or value in (float("inf"), float("-inf")):
        raise SafeIOError(f"{name} debe ser un numero finito no negativo")
    return value
