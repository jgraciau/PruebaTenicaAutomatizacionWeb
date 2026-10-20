from pathlib import Path

EXCLUDED_DIRS = frozenset({
    ".git", ".gradle", ".idea", ".vscode", ".graphify", "build",
    "target", "out", "dist", "venv", ".venv", "__pycache__",
    "node_modules", "gradle", ".pytest_cache", ".axet-code",
})
JAVA_SUFFIX = ".java"
FEATURE_SUFFIX = ".feature"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2]
