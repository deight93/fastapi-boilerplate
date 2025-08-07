import importlib
from pathlib import Path

model_dir = Path(__file__).parent

for file in model_dir.glob("*.py"):
    if file.name == "__init__.py":
        continue

    module_name = file.stem  # 파일명에서 .py 제거
    importlib.import_module(f"{__name__}.{module_name}")
