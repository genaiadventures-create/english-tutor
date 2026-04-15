import os
import tempfile

try:
    from openclaw.tools import tool
except ImportError:
    # Local test fallback when OpenClaw runtime is unavailable.
    def tool(func):
        return func


@tool
def delete_file(file_path: str) -> bool:
    """
    Delete a temporary/generated file after it has been sent to the user.
    Only allows deleting regular files inside approved cleanup directories.
    Returns True when the file was deleted, False when it did not exist.
    """
    cleaned_path = (file_path or "").strip()
    if not cleaned_path:
        raise ValueError("file_path must be a non-empty string")

    if not os.path.isabs(cleaned_path):
        raise ValueError("file_path must be an absolute path")

    resolved_path = os.path.realpath(cleaned_path)
    allowed_roots = _allowed_cleanup_roots()
    if not any(_is_within_directory(resolved_path, root) for root in allowed_roots):
        raise ValueError("file_path must be inside an approved cleanup directory")

    if not os.path.exists(resolved_path):
        return False

    if not os.path.isfile(resolved_path):
        raise ValueError("file_path must point to a regular file")

    os.unlink(resolved_path)
    return True


def _allowed_cleanup_roots() -> list[str]:
    roots = [os.path.realpath(tempfile.gettempdir())]
    configured = os.getenv("ENGLISH_TUTOR_AUDIO_DIR", "").strip()
    if configured:
        roots.append(os.path.realpath(os.path.abspath(configured)))
    else:
        roots.append(os.path.realpath(os.path.join(os.getcwd(), ".english_tutor_audio")))
    return roots


def _is_within_directory(path: str, directory: str) -> bool:
    if path == directory:
        return True
    return path.startswith(directory + os.sep)
