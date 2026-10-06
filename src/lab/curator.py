"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.   >>> SINH VIÊN CÀI ĐẶT curate_skills <<<

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import re
from pathlib import Path

from .tasks import eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    import json
    from .model import make_model
    from .tasks import ROOT

    if out_dir is None:
        out_dir = ROOT / "skills" / "auto"
    else:
        out_dir = Path(out_dir)

    results_path = Path(results_dir) / source_condition
    runs = []
    if results_path.exists():
        for run_file in sorted(results_path.glob("*/run.json")):
            try:
                r = json.loads(run_file.read_text(encoding="utf-8"))
            except Exception:
                continue

            if r.get("role") != "learn":
                continue

            trace_file = run_file.parent / "trace.md"
            trace_text = ""
            if trace_file.exists():
                trace_text = trace_file.read_text(encoding="utf-8")[-6000:]

            failed_checks = []
            for c in r.get("checks", []):
                if not c.get("passed", False):
                    failed_checks.append((c.get("name", ""), c.get("detail", "")))

            if failed_checks:
                runs.append({
                    "task": r.get("task", run_file.parent.name),
                    "failed": failed_checks,
                    "trace": trace_text,
                })

    if not runs:
        print("Warning: no failed checks on learning tasks found.")
        return []

    run_summaries = []
    for run in runs:
        checks_str = "\n".join(f"- Check {name}: {detail}" for name, detail in run["failed"])
        task_name = run["task"]
        trace_tail = run["trace"]
        run_summaries.append(f"### Task: {task_name}\nFailed checks:\n{checks_str}\n\nExecution trace (tail):\n{trace_tail}")
    runs_prompt_text = "\n\n".join(run_summaries)

    prompt = (
        f"You are writing reusable SKILLs for an engineering agent in a software/data environment.\n"
        f"Below are failed checks from previous learning tasks, where the review bot reported strict organizational house rules (RULE: ...).\n"
        f"Synthesize these organizational rules into exactly {max_skills} actionable, procedural skills (one per domain: code maintenance, tabular data, log triage).\n\n"
        f"Requirements for each skill:\n"
        f"1. `name`: lowercase alphanumeric with hyphens (e.g., `python-code-maintenance`, `tabular-data-cleaning`, `log-triage-reporting`).\n"
        f"2. `description`: exactly one concise sentence starting with \"Use when ...\" clearly describing the trigger situation.\n"
        f"3. Body: a short, imperative, numbered checklist (under 35 lines) listing the exact organizational formatting conventions required in the feedback (e.g. required schema headers, output file paths like clean.csv or tests/test_regressions.py, changelog formats, monetary integer cents, case normalization, sorting rules).\n"
        f"4. Do NOT tell the agent to search for external convention files; instruct it to apply these concrete formatting rules directly.\n"
        f"5. Do NOT mention specific task IDs or ephemeral file paths.\n\n"
        f"Output format strictly:\n"
        f"=== SKILL: <name> ===\n"
        f"---\n"
        f"name: <name>\n"
        f"description: Use when ...\n"
        f"---\n"
        f"# Title\n\n"
        f"1. Step 1...\n"
        f"2. Step 2...\n"
        f"=== END ===\n\n"
        f"{runs_prompt_text}"
    )

    llm = model or make_model()
    resp = llm.invoke(prompt)
    reply_text = getattr(resp, "content", str(resp))

    written = []
    for name, text in parse_skill_blocks(reply_text):
        if len(written) >= max_skills:
            break
        problems = validate_skill(text, expected_name=name)
        if problems:
            continue
        skill_dir = out_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(text, encoding="utf-8")
        written.append(skill_file)

    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
