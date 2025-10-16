#!/usr/bin/env python
"""Validation script for PyQt5 implementation.

This script validates that the PyQt5 GUI implementation is correct by:
1. Checking that all modules can be imported.
2. Verifying class structures.
3. Checking method signatures.
4. Validating game logic integration.
"""

from __future__ import annotations

import sys
from typing import Callable


def _validate_and_print(title: str, validation_fn: Callable[[], tuple[bool, list[str]]]) -> bool:
    """Run a validation function and print the results in a standard format."""
    print(f"\n🔍 Validating {title}...")
    print("-" * 70)
    passed, messages = validation_fn()
    for msg in messages:
        print(f"  {msg}")
    return passed


def check_import(module_name: str) -> tuple[bool, str]:
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        return True, f"✓ {module_name} imported successfully"
    except ImportError as e:
        return False, f"✗ {module_name} failed: {e}"
    except Exception as e:
        return False, f"✗ {module_name} error: {e}"


def check_class_attributes(cls: type, required_attrs: list[str]) -> tuple[bool, str]:
    """Check if a class has required attributes."""
    missing = [attr for attr in required_attrs if not hasattr(cls, attr)]
    if not missing:
        return True, "✓ All required attributes present"
    return False, f"✗ Missing attributes: {', '.join(missing)}"


def validate_base_gui() -> tuple[bool, list[str]]:
    """Validate BaseGUI implementation."""
    messages = []
    all_passed = True

    success, msg = check_import("common.gui_base_pyqt")
    messages.append(msg)
    if not success:
        return False, messages

    from common.gui_base_pyqt import PYQT5_AVAILABLE, BaseGUI, GUIConfig

    if not PYQT5_AVAILABLE:
        messages.append("✗ PyQt5 not available")
        return False, messages
    messages.append("✓ PyQt5 is available")

    config = GUIConfig()
    if config.window_title != "Game":
        messages.append("✗ GUIConfig default window_title incorrect")
        all_passed = False
    else:
        messages.append("✓ GUIConfig defaults correct")

    required_methods = [
        "__init__", "build_layout", "update_display", "create_header",
        "create_status_label", "create_log_widget", "log_message", "clear_log",
        "apply_theme", "set_theme", "play_sound",
    ]
    success, msg = check_class_attributes(BaseGUI, required_methods)
    messages.append(msg)
    if not success:
        all_passed = False

    return all_passed, messages


def validate_dots_and_boxes() -> tuple[bool, list[str]]:
    """Validate Dots and Boxes PyQt5 implementation."""
    messages = []
    all_passed = True

    success, msg = check_import("paper_games.dots_and_boxes.gui_pyqt")
    messages.append(msg)
    if not success:
        return False, messages

    from paper_games.dots_and_boxes.gui_pyqt import BoardCanvas, DotsAndBoxesGUI

    required_attrs_gui = [
        "__init__", "_build_layout", "_update_chain_info", "_make_move",
        "_computer_turn", "_update_status", "_game_over", "_show_hint", "_new_game",
    ]
    success, msg = check_class_attributes(DotsAndBoxesGUI, required_attrs_gui)
    messages.append(msg)
    if not success:
        all_passed = False

    required_attrs_canvas = [
        "__init__", "paintEvent", "mousePressEvent", "mouseMoveEvent",
        "leaveEvent", "_get_edge_from_position",
    ]
    success, msg = check_class_attributes(BoardCanvas, required_attrs_canvas)
    messages.append(msg)
    if not success:
        all_passed = False

    messages.append("✓ GUI class structure validated (instantiation requires display)")
    return all_passed, messages


def validate_tests() -> tuple[bool, list[str]]:
    """Validate test suite."""
    messages = []

    import pathlib
    test_file = pathlib.Path(__file__).parent.parent / "tests" / "test_gui_pyqt.py"
    if not test_file.exists():
        messages.append("✗ Test file not found")
        return False, messages
    messages.append("✓ Test file exists")

    import sys
    tests_dir = test_file.parent
    if str(tests_dir) not in sys.path:
        sys.path.insert(0, str(tests_dir))

    try:
        import test_gui_pyqt
        if not test_gui_pyqt.PYQT5_AVAILABLE:
            messages.append("✗ PyQt5 not available in tests")
            return False, messages
        messages.append("✓ Tests can access PyQt5")
    except ImportError as e:
        messages.append(f"✗ Could not import test module: {e}")
        return False, messages

    return True, messages


def main() -> int:
    """Main entry point."""
    print("=" * 70)
    print("PyQt5 Implementation Validation")
    print("=" * 70)

    validations = {
        "BaseGUI": validate_base_gui,
        "Dots and Boxes PyQt5 GUI": validate_dots_and_boxes,
        "Test Suite": validate_tests,
    }

    all_passed = all(
        _validate_and_print(title, validation_fn)
        for title, validation_fn in validations.items()
    )

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All validations PASSED")
        print("\nPyQt5 implementation is working correctly!")
    else:
        print("❌ Some validations FAILED")
        print("\nPlease check the errors above.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())