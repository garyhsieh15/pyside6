# Repository Guidelines

## 使用正體中文說明

## Project Structure & Module Organization
- `main.py` is the application entry point for the PySide6 desktop UI.
- `ui/` holds Qt Designer `.ui` files (e.g., `ui/main_win.ui`, `ui/dialog_run.ui`).
- `ui/generated/` contains auto-generated Python modules from the `.ui` files. Edit the `.ui` files and regenerate rather than editing these Python files directly.
- `YOLOv8/` holds standalone data/vision utility scripts.
- `images/` and `images_test/` store UI assets referenced by Qt resource files.
- `*.qrc` and `*_rc.py` are Qt resource definitions and their generated Python outputs.

## Build, Test, and Development Commands
- `python main.py` — run the main desktop application.
- `python YOLOv8/<script>.py` — run a specific YOLOv8 utility script (each script is standalone).
- If you modify Qt resources or `.ui` files, regenerate the Python outputs with the Qt tools used by your workflow (for example, `pyside6-uic` for `.ui` and `pyside6-rcc` for `.qrc`).
  - Recommended: `scripts/regenerate_ui.sh` to refresh `ui/generated/*.py` after editing `.ui`.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation.
- Keep UI logic in `main.py` and treat generated UI modules as read-only.
- Filenames and function names follow a simple, descriptive style (e.g., `data_deal_with.py`, `get_img_info.py`).

## Testing Guidelines
- No automated test framework is configured in this repository.
- If you add tests, document the framework and expected command in this file.

## Commit & Pull Request Guidelines
- Recent commit messages are short and action-oriented (e.g., “add…”, “update…”). Follow this lightweight pattern unless the project adopts a stricter convention.
- PRs should include a brief summary, steps to verify, and screenshots or screen recordings for UI changes.

## Configuration & Asset Notes
- Qt assets are referenced via `.qrc` files (`apprcc.qrc`, `test.qrc`, `test_test.qrc`). Keep asset paths stable to avoid broken icons in the UI.
- Generated files (`UI/*.py`, `*_rc.py`) can be overwritten by tooling; avoid manual edits and regenerate from source files instead.
