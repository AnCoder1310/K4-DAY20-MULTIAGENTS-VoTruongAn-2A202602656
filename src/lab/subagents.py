"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when you need to inspect files, read instructions, explore docstrings, "
                "or examine data samples without making any changes. This subagent analyzes and reports facts accurately."
            ),
            "system_prompt": (
                "You are an exploratory assistant. Your job is to read workspace files, search code or logs, "
                "inspect schemas and docstrings, and report objective findings clearly without modifying any files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when you need to write or edit code, clean data files, create output JSON/CSV files, "
                "or execute scripts and test suites. This subagent performs changes and tests results."
            ),
            "system_prompt": (
                "You are an implementation assistant. Your job is to modify code, clean and transform data, "
                "create required output files according to specifications, and run shell commands to verify tests."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use when you need an independent check of results against task requirements and edge cases "
                "before finishing. This subagent validates outputs and tests without editing files."
            ),
            "system_prompt": (
                "You are a quality review assistant. Your job is to verify output files and code against task specifications, "
                "check edge cases, and report any discrepancies without modifying any files."
            ),
        },
    ]
