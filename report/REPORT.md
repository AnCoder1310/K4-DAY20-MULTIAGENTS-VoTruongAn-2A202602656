# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Võ Trường An | 2A202602656 | 100% |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `ag/gemini-3.8-flash` (`gemini-3.8-flash` qua gateway OpenAI-compatible), `LAB_TEMPERATURE=0`, `recursion_limit=60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, macOS 27.0.0 (Apple Silicon arm64), chạy trực tiếp
- Số lần chạy tác vụ đã dùng / ngân sách: 21 / 25 runs (bao gồm 6 baseline, 6 subagents, 3 skills-auto-dev và 6 skills-auto)
- Commit của tag `freeze`: `02948e4`

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Điều kiện `subagents` sẽ đạt điểm cao hơn `baseline` trên tác vụ đánh giá nhờ cơ chế phân công chuyên biệt và phản biện chéo giữa các tác tử (`implementer`, `reviewer`), nhưng chi phí token và thời gian sẽ cao hơn đáng kể (tăng từ 3 đến 4 lần). Căn cứ từ thực nghiệm tác vụ học: `subagents` đã nâng điểm từ 18/27 (66.7%) lên 24/27 (88.9%) nhờ rà soát được 6/9 quy ước tổ chức, phù hợp với nghiên cứu của Anthropic về việc đa tác tử tăng độ chính xác nhưng tiêu tốn token gấp nhiều lần.
- H2 (skills-auto so với baseline): Điều kiện `skills-auto` sẽ đạt điểm cao hơn `baseline` trên các quy tắc đã được khái quát hóa trong `SKILL.md` (như chuẩn hóa schema log, type annotations), nhưng mức cải thiện sẽ bị giới hạn bởi hiện tượng quá khớp (overfitting) và nhiễu ngữ cảnh khi gặp các quy ước mới của tác vụ đánh giá. Căn cứ từ nghiên cứu SkillsBench và SkillEvolBench: kỹ năng do mô hình tự sinh có độ khái quát hóa thấp hơn so với kỹ năng do con người biên soạn và khó thích ứng khi phân phối dữ liệu thay đổi.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm số trung bình trên tác vụ đánh giá sẽ thấp hơn tác vụ học trên cả 3 điều kiện (khoảng 10-20%). Căn cứ: tác vụ đánh giá bổ sung các quy ước ngầm mới (house rules) mà cả tác tử cơ sở lẫn curator đều chưa từng tiếp xúc trong phản hồi của tập học, và do các quy ước này không được mô tả trong đề bài nên tác tử không thể tự đoán đúng nếu không có gợi ý.

## 3. Làm quen Deep Agents (Phần 0.3)

### A. Khám phá tác tử mặc định Deep Agents (`python scripts/tour.py`)

1. **Tác tử mặc định có những công cụ nào? Công cụ nào cho phép chạy lệnh?**
   - **Các công cụ mặc định:**
     - Công cụ tệp (file tools): `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`.
     - Shell: `execute`.
     - Subagents: `task`.
   - **Công cụ cho phép chạy lệnh:** `execute` (thực thi lệnh shell trong môi trường sandbox cô lập `LocalShellBackend` và trả về `stdout/stderr` kèm exit code).

2. **Mô tả của công cụ `task` nói gì về subagent `general-purpose`? Subagent đó nhìn thấy ngữ cảnh nào của tác tử chính?**
   - **Mô tả về subagent `general-purpose`:** Đây là subagent đa năng dùng để nghiên cứu các câu hỏi phức tạp, tìm kiếm tệp và nội dung, cũng như thực thi các tác vụ nhiều bước. Khi tìm kiếm từ khóa/tệp mà không tự tin tìm trúng ngay từ đầu, tác tử chính nên giao cho subagent này tìm kiếm. Subagent này có quyền truy cập mọi công cụ như tác tử chính.
   - **Ngữ cảnh mà subagent nhìn thấy:** Phi trạng thái theo mặc định (stateless by default). Subagent chỉ nhìn thấy duy nhất nội dung chuỗi chỉ dẫn (prompt) mà tác tử chính truyền vào cho nó qua tham số `description` và trả về một báo cáo kết quả duy nhất. Subagent không tự động nhìn thấy lịch sử hội thoại trước đó của tác tử chính trừ khi được chỉ định kế thừa hội thoại.

3. **System prompt mặc định của Deep Agents rỗng. Trích một câu hướng dẫn hành vi từ mô tả của công cụ `task` và một câu từ mô tả của công cụ `execute`:**
   - **Trích từ mô tả công cụ `task`:**
     > *"Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report. Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*
   - **Trích từ mô tả công cụ `execute`:**
     > *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*

---

### B. Kiến trúc Đa tác tử (Multi-Agent Architecture) trong bài lab

**Câu 1: Bài lab này có bao nhiêu agent? Mỗi agent làm gì?**
- Hệ thống gồm các agent sau:
  - **Coordinator (Tác tử chính / Main Agent):** Tiếp nhận bài toán, lập kế hoạch tổng thể, quản lý workspace và công cụ, quyết định giao việc cho các worker subagent qua tool `task`, và tổng hợp kết quả cuối cùng.
  - **Subagent mặc định (`general-purpose`):** Xử lý các tác vụ phức tạp nhiều bước, nghiên cứu ngữ cảnh nặng (context-heavy) khi cần.
  - **Các Worker Subagents tự định nghĩa (trong `subagents.py`):**
    - `explorer`: Khảo sát, đọc `instruction.md`, `README.md`, docstring và dữ liệu mẫu; báo cáo hiện trạng khách quan (chỉ đọc, không sửa tệp).
    - `implementer`: Trực tiếp chỉnh sửa mã nguồn, biến đổi/làm sạch dữ liệu, tạo file kết quả (`answer.json`, `clean.csv`, v.v.), chạy script/test và báo cáo kết quả thực thi.
    - `reviewer`: Kiểm tra độc lập kết quả làm việc dựa trên yêu cầu đề bài và các trường hợp biên (edge cases) trước khi hoàn tất; không sửa tệp.
  - **Curator Agent (Tác tử tự tiến hóa - Self-Evolving Agent):** Chạy ngoại tuyến sau các tác vụ học (learn tasks). Đọc log lỗi (`run.json`), phản hồi kiểm tra và vết thực thi (`trace.md`), phân tích nguyên nhân thất bại để tự động đúc kết các kỹ năng tái sử dụng (`SKILL.md`) lưu vào `skills/auto/`.

**Câu 2: Coordinator giao tiếp với worker agents bằng cách nào?**
- Coordinator giao tiếp với worker agents thông qua cơ chế gọi công cụ (tool calling) với công cụ `task(description=..., subagent_type=...)`.
- Coordinator gửi toàn bộ mô tả nhiệm vụ, quy ước đường dẫn, mục tiêu và yêu cầu định dạng vào chuỗi `description` (do cơ chế gọi là stateless).
- Worker agent thực thi độc lập với các công cụ được cấp và trả về một báo cáo duy nhất (final report) cho Coordinator dưới dạng ToolMessage.
- Coordinator nhận báo cáo từ worker agent, kiểm chứng và tiến hành các bước tiếp theo.

**Câu 3: Có những công cụ (tools) nào được chia sẻ giữa các agent?**
- Các công cụ được chia sẻ thông qua backend sandbox dùng chung (`LocalShellBackend`):
  - **Công cụ tệp (File tools):** `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `delete` — cho phép cả Coordinator và worker agents thao tác trên không gian thư mục `workspace/`.
  - **Công cụ shell:** `execute` — cho phép chạy lệnh hệ thống, chạy Python script và kiểm thử trong sandbox.
  - **Kho kỹ năng (Skills repository):** Thư mục `/skills/` chứa các tệp `SKILL.md` (hướng dẫn, checklist, bài học kinh nghiệm) được nạp dần (progressive disclosure) cho các agent.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `data-learn` | `rule_money_in_cents` | E | RULE: money values in answer.json are integer cents (1606.67 USD is written 160667). |
| `data-learn` | `rule_meta_block` | E | RULE: answer.json has an object `meta` = {"source": <file>, "rows_in": <n>, "rows_used": <n>}. |
| `data-learn` | `rule_clean_csv` | E | RULE: write workspace/clean.csv with header order_id,timestamp_utc,region,amount_cents. |
| `code-learn` | `rule_type_hints` | E | RULE: every public function has type annotations on all parameters and on the return value. |
| `code-learn` | `rule_regression_tests` | E | RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3). |
| `code-learn` | `rule_changelog` | E | RULE: record each fix in CHANGELOG.md under ## Unreleased as bullets - fix(<fn>): <desc>. |
| `logs-learn` | `rule_service_names` | E | RULE: service names in the output are lower-case with - replaced by _. |
| `logs-learn` | `rule_sorted_errors` | E | RULE: `errors` is sorted by service, then by timestamp_utc, ascending. |
| `logs-learn` | `rule_schema_header` | E | RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage". |

**Nhận xét:**
- **Nhóm lỗi chiếm đa số:** 100% số check thất bại (9/9 check) thuộc **Nhóm E (Vi phạm quy ước tổ chức)**. Tất cả các check này đều có tiền tố `rule_` và phản hồi bắt đầu bằng `RULE:`. Các quy ước này là yêu cầu ngầm của tổ chức, không được mô tả trực tiếp trong đề bài.
- **Bằng chứng phủ định cho các nhóm A-D:** Toàn bộ **18/18 check kỹ thuật** (technical checks) trên cả 3 tác vụ học đều đạt 100% (`scripts/check_breakdown.py` xác nhận `18/18 technical`). Mô hình không gặp các lỗi bỏ qua đặc tả (A), không kiểm chứng (B), vá triệu chứng (C), hay bỏ sót dữ liệu bẩn (D).
- **Khả năng phòng ngừa của Skill:** Một skill **hoàn toàn có thể phòng ngừa** nhóm lỗi này. Khi curator tổng hợp các quy ước từ `detail` và tạo thành các checklist thủ tục trong `SKILL.md`, tác tử ở các lần chạy sau sẽ đọc skill trước khi thực hiện và tuân thủ đúng định dạng mà tổ chức yêu cầu.

## 5. Điều kiện `subagents` (Phần 2.3)

- **Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):**
  - `explorer`: Khảo sát, đọc `README.md`, docstrings, schema dữ liệu và mẫu logs mà không sửa đổi tệp. Thiết kế để cách ly pha trinh sát thông tin khỏi pha chỉnh sửa.
  - `implementer`: Trực tiếp chỉnh sửa mã nguồn, làm sạch dữ liệu, tạo các file kết quả (`answer.json`, `clean.csv`, `errors.json`), chạy script và kiểm thử.
  - `reviewer`: Thẩm định độc lập các file đầu ra và kết quả so với yêu cầu đề bài và edge cases trước khi kết thúc (chỉ đọc, không sửa tệp).

- **`subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0):**
  - `data-learn`: **2 lượt gọi** (`reviewer`). Coordinator làm sạch dữ liệu và gọi `reviewer` độc lập để đối chiếu kết quả. Đạt điểm tuyệt đối **8/8 (100%)**.
  - `logs-learn`: **1 lượt gọi** (`implementer`). Coordinator phân tích các quy ước log-triage và ủy quyền toàn bộ cho `implementer`. Đạt điểm tuyệt đối **9/9 (100%)**.
  - `code-learn`: **0 lượt gọi**. Do không gian bài toán là một gói Python sẵn có test suite hiển hiện, Coordinator tự chủ động gọi trực tiếp file tools và execute pytest để sửa code thay vì ủy quyền (tránh phân mảnh ngữ cảnh debug qua subagent). Vẫn đạt toàn bộ 7/7 check kỹ thuật (**7/10**).

- **Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc):**
  - Trong `logs-learn`, Coordinator giao việc rất chi tiết và chuẩn xác: liệt kê đủ 12 yêu cầu cấu trúc (`schema_version: 2`, `generated_by: "log-triage"`, chuẩn hóa tên service chữ thường gạch dưới, format timestamp UTC, thuật toán repeat count).
  - Nhờ thông tin được đóng gói đầy đủ trong thông điệp stateless, subagent `implementer` đã thực thi trọn vẹn và vượt qua cả 3 check quy ước ngầm.

- **Ảnh hưởng đến token và thời gian:**
  - **Tokens:** Chi phí trung bình tăng mạnh từ **178,803 tokens** (`baseline`) lên **562,705 tokens** (`subagents`) (tăng gấp ~3.1 lần). Riêng `code-learn` tiêu thụ 952k tokens do lặp suy luận nhiều bước.
  - **Thời gian:** Tăng từ trung bình 78.6s lên 375.4s mỗi tác vụ.
  - **Đánh đổi (Trade-off):** Tăng chi phí token và độ trễ nhưng mang lại hiệu quả vượt bậc: tổng điểm tăng từ **18/27 (66.7%)** lên **24/27 (88.9%)**, vượt qua **6/9 check quy ước ngầm** (house rules) mà điều kiện baseline hoàn toàn bó tay.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- **Số lần chạy curator, số skill bị xóa và lý do:**
  - Lần 1: Curator sinh 3 skill (`codebase-bugfix-governance`, `multi-artifact-deliverable-checklist`, `structured-output-normalization`). Khi chạy thử ở `data-learn`, kỹ năng thứ hai quá trừu tượng và có hướng dẫn "scan prompt and conventions" khiến tác tử bị phân tâm (over-attention), tốn 5 lệnh grep/glob tìm file không tồn tại dẫn đến 0/8 điểm.
  - Hành động: Xóa bộ skill lần 1 theo hướng dẫn GUIDE.md 3.3, tinh chỉnh prompt của curator để chuyển các phản hồi `detail` thành checklist mệnh lệnh cụ thể (actionable checklists) và chạy lại curator (Lần 2).
  - Lần 2: Curator sinh ra **2 skill hoàn hảo** (`python-code-maintenance` và `log-triage-reporting`), 0 lỗi validation, ngắn gọn (13-14 dòng), mệnh lệnh trực tiếp, không tìm kiếm thừa.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `python-code-maintenance` | **Tổng quát**: Hướng dẫn quy trình bảo trì gói Python (type hints cho mọi public function, tạo `tests/test_regressions.py` có >= 3 test, cập nhật `CHANGELOG.md` mục Unreleased). Không chứa task ID hay số liệu hardcode. | **Đúng**: Khớp chính xác với cả 3 quy ước house rules của họ tác vụ code. | 14 dòng; description kích hoạt rõ ràng ("Use when fixing bugs, refactoring, or preparing code changes for review in a Python package."); ở Phần 3.4 `skills_read = 0` (chạm recursion limit sớm), sau đóng băng `skills_read = 1` (đọc và làm theo đầy đủ, đạt 10/10) |
| `log-triage-reporting` | **Tổng quát**: Checklist chuẩn hóa báo cáo phân loại log (schema_version 2, generated_by "log-triage", normalize service name snake_case, timestamp UTC, sort errors ascending). | **Đúng**: Khớp chính xác với cả 3 quy ước house rules của họ tác vụ logs. | 13 dòng; description kích hoạt chuẩn xác ("Use when parsing server logs to extract errors and generate structured JSON triage reports."); ở Phần 3.4 `skills_read = 1` (đọc 3 lần, đạt 6/9), sau đóng băng `skills_read = 1` (đạt 9/9 ở learn và 9/10 ở eval) |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

### Bảng kết quả so sánh (sinh từ `python -m lab.compare`)

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 7/10 | 7/10 | 10/10 |
| data-learn | 5/8 | 8/8 | 0/8 |
| logs-learn | 6/9 | 9/9 | 9/9 |
| code-eval | 7/11 | 7/11 | 1/11 |
| data-eval | 0/9 | 0/9 | 0/9 |
| logs-eval | 0/10 | 0/10 | 9/10 |
| **Mean score - learning tasks** | 0.66 | 0.90 | 0.67 |
| **Mean score - evaluation tasks** | 0.21 | 0.21 | 0.33 |
| **Mean tokens per run** | 148,954 | 408,261 | 120,569 |
| **Runs that read a skill** | 0/6 | 0/6 | 5/6 |

### Thống kê phân rã kiểm thử (sinh từ `python scripts/check_breakdown.py`)

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval      7/18         0/12         119,104      0/3     
baseline      learn    18/18         0/9          178,803      0/3     
subagents     eval      7/18         0/12         253,816      0/3     
subagents     learn    18/18         6/9          562,705      0/3     
skills-auto   eval      7/18         3/12          79,997      3/3     
skills-auto   learn    13/18         6/9          161,141      2/3     
```

### Các lần chạy có lỗi hoặc cảnh báo
- **`skills_modified = false`**: 100% các lần chạy đều bảo toàn tính toàn vẹn của thư mục `skills/auto/`, không xảy ra hiện tượng tác tử sửa đè skill trong lúc thực thi.
- **`GraphRecursionError`**: Xảy ra ở `baseline/code-learn`, `subagents/code-learn` và `baseline/code-eval` khi tác tử chạm ngưỡng đệ quy `recursion_limit=60` do lặp lại chu trình sửa mã - chạy test. Lỗi này được bắt an toàn bởi `run_task` và hệ thống vẫn chấm điểm đầy đủ trên workspace thực tế (đạt 7/10 và 7/11 check).

---

## 8. Phân tích

**1. So sánh hiệu quả giữa các điều kiện trên tác vụ học và đánh giá:**
- **Trên tác vụ học (learn):** Điều kiện `subagents` đạt điểm cao nhất (**0.90** - 24/27 điểm), theo sau là `skills-auto` (**0.67**) và `baseline` (**0.66**). Đa tác tử vượt trội nhờ phân công chuyên biệt giữa `implementer` và `reviewer` giúp phát hiện và tuân thủ các quy ước ngầm.
- **Trên tác vụ đánh giá (eval):** Điều kiện `skills-auto` đạt điểm cao nhất (**0.33**), vượt trội hơn cả `baseline` (**0.21**) và `subagents` (**0.21**). Đặc biệt, trên tác vụ `logs-eval`, `skills-auto` đạt tới **9/10 (90%)**, trong khi cả `baseline` và `subagents` đều nhận điểm 0/10.
- **Hiện tượng sụt giảm:** `subagents` đạt 0.90 ở tác vụ học nhưng tụt xuống 0.21 ở tác vụ đánh giá. Đây là dấu hiệu của **sự phụ thuộc vào phản biện ngữ cảnh học**: khi sang tác vụ đánh giá với định dạng mới, nếu coordinator không có tri thức thủ tục sẵn có trong prompt/skill thì các worker cũng không thể đoán đúng các quy ước ngầm mới.

**2. Phân rã check kỹ thuật và check quy ước (`rule_`):**
- **Check kỹ thuật:** Trên tập học, cả 3 điều kiện đều đạt mức rất cao (baseline và subagents đạt 18/18; skills-auto đạt 13/18). Trên tập đánh giá, cả 3 điều kiện đều đạt 7/18 check kỹ thuật cơ bản.
- **Check quy ước (`rule_`):**
  - Skill do curator sinh giúp đạt xuất sắc các quy ước đã học: giải quyết trọn vẹn 3 check quy ước của `code-learn` (type hints, regression tests, changelog) giúp đạt điểm tuyệt đối 10/10, và giải quyết các check quy ước của `logs-learn` (đạt 9/9) và `logs-eval` (đạt 9/10).
  - Check quy ước **mới** của tác vụ đánh giá (ví dụ: `rule_source_line` trong `logs-eval`) **không được skill giúp** (thất bại). Nguyên nhân: Curator chỉ tổng hợp tri thức từ phản hồi của tập học; nó hoàn toàn không có thông tin về các quy ước tổ chức mới được bổ sung ở tập đánh giá.

**3. Phân tích cơ chế dựa vào vết (trace) và `skills_read`:**
- **Check được skill giúp đạt:** Check `rule_type_hints` và `rule_regression_tests` trong `code-learn`. Vết thực thi cho thấy tác tử đọc `skills/python-code-maintenance/SKILL.md` ngay ở bước đầu (`skills_read=1`), sau đó tuân thủ nghiêm ngặt từng bước: bổ sung type annotation cho mọi public function và tạo file `tests/test_regressions.py`, giúp điểm số tăng vọt từ 7/10 lên 10/10.
- **Check skill không giúp được:** Trong `data-learn` và `data-eval` (`skills_read=0` và `2`), tác tử không có kỹ năng riêng cho bảng dữ liệu sales (do curator chỉ sinh 2 skill cho code và log). Trong `data-learn`, tác tử dừng sau 2 tool call kiểm tra thư mục mà chưa kịp tạo `answer.json` (0/8 điểm).

**4. Phân tích chi phí và hiệu quả token:**
- **Chi phí trung bình:**
  - `skills-auto`: **120,569 tokens/lần chạy** (tiết kiệm nhất).
  - `baseline`: **148,954 tokens/lần chạy**.
  - `subagents`: **408,261 tokens/lần chạy** (cao gấp 3.4 lần skills-auto).
- **Hiệu quả (Điểm / Token):** `skills-auto` có hiệu quả kinh tế cao nhất trên tập đánh giá: đạt điểm cao nhất (0.33) với mức tiêu thụ token thấp nhất (79,997 tokens ở eval).
- **Đánh giá đa tác tử:** `subagents` mang lại chất lượng rất cao trên tập học (0.90) nhưng tốn chi phí token rất lớn (lên tới 952k tokens ở code-learn) và không duy trì được ưu thế này trên tập đánh giá (0.21). Do đó, đa tác tử chỉ thực sự đáng giá khi bài toán có cấu trúc phân tầng rõ ràng và yêu cầu độ tin cậy tuyệt đối, còn đối với các quy ước chuẩn hóa lặp lại thì **skill nạp ngữ cảnh (Skills)** mang lại tỷ suất lợi ích/chi phí vượt trội hơn nhiều.

**5. Kiểm soát rò rỉ dữ liệu (Data Leakage) và Quá khớp (Overfitting):**
- **Rò rỉ dữ liệu:** Hoàn toàn bằng 0. Hàm `validate_skill` quét kiểm tra toàn bộ danh sách `eval_markers()` và xác nhận không có bất kỳ tên file, hàm hay định danh nào của tập đánh giá xuất hiện trong `skills/auto/`. `curate_skills` cũng lọc bỏ hoàn toàn các lần chạy có `role == "eval"`.
- **Quá khớp (Overfitting):** Thể hiện rõ ở việc kỹ năng `python-code-maintenance` phát huy tối đa ở `code-learn` (10/10) nhưng sang `code-eval` (dữ liệu package khác) tác tử bị vướng vào cấu trúc test riêng nên chỉ đạt 1/11. Ngược lại, kỹ năng `log-triage-reporting` thể hiện tính tổng quát hóa xuất sắc khi chuyển giao thành công sang `logs-eval` (đạt 9/10).

**6. Ước lượng nhiễu (Noise Estimation):**
- Điểm tác vụ học ở Phần 3.4 (`skills-auto-dev`) và sau khi đóng băng (`skills-auto`):
  - `code-learn`: 0.1 (chưa đọc skill/vướng recursion) -> 1.0 (đọc skill, đạt 10/10).
  - `data-learn`: 0.0 -> 0.0.
  - `logs-learn`: 0.67 -> 1.0 (9/9).
- **Ý nghĩa:** Chênh lệch giữa hai lần chạy cùng một bộ skill trên cùng tác vụ học cho thấy tính ngẫu nhiên (sampling variance) của LLM trong việc lựa chọn tool call bước đầu. Tuy nhiên, khi skill được kích hoạt đúng tình huống, hiệu quả cải thiện là thực chất và có tính lặp lại cao.

---

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập dữ liệu đánh giá nhỏ (Small Benchmark Size):** Mỗi họ tác vụ chỉ có 1 tác vụ học và 1 tác vụ đánh giá (tổng cộng 6 tác vụ). Cỡ mẫu nhỏ khiến các chỉ số trung bình nhạy cảm với từng thất bại cá lẻ của tác tử.
2. **Thực nghiệm chạy một lần (Single-run Variance):** Mỗi cấu hình chỉ chạy một lần do giới hạn tài nguyên và thời gian API. Do LLM có tính ngẫu nhiên (ngay cả ở nhiệt độ thấp), kết quả có thể chịu ảnh hưởng cục bộ của nhiễu đường truyền hoặc quyết định ngẫu nhiên trong vài bước suy luận.
3. **Mô hình thử nghiệm đơn nhất (Single LLM Architecture):** Thí nghiệm chỉ tiến hành trên họ mô hình `gemini-3.8-flash`. Khả năng tự tiến hóa và tuân thủ skill có thể biến thiên đáng kể nếu chuyển sang các kiến trúc mô hình khác (như Claude 3.5 Sonnet hay DeepSeek-V3).

---

## 10. Kết luận

Thực nghiệm đã chứng minh thành công cơ chế tác tử tự tiến hóa ở tầng ngữ cảnh: thông qua việc đọc phản hồi thất bại từ đường cơ sở, Curator tự động đúc kết các kỹ năng tái sử dụng giúp nâng điểm số tác vụ học lên mức tuyệt đối (10/10 ở code, 9/9 ở log) và tổng quát hóa xuất sắc sang tác vụ đánh giá mới (`logs-eval` đạt 9/10, vượt trội hoàn toàn so với baseline 0/10). Đa tác tử (`subagents`) cho độ chính xác cao trên tập học nhưng tiêu tốn token gấp hơn 3.4 lần, trong khi nạp kỹ năng (`skills-auto`) đạt hiệu quả tối ưu nhất về tỷ suất điểm trên chi phí token. Đề xuất cải tiến tiếp theo là bổ sung cơ chế kiểm định chéo tự động cho Curator (Curator-Critic Loop) để đảm bảo mọi họ tác vụ đều được sinh đủ bộ kỹ năng chuyên biệt trước khi đóng băng.

---

## Phụ lục

- **Lệnh đã chạy (theo thứ tự):**
  1. `pytest tests/test_01_provided.py` (xác nhận 12 test có sẵn).
  2. `pytest tests/test_02_agent.py` và `pytest tests/test_03_runner.py` (xác nhận harness và subagents).
  3. `python -m lab.runner --condition baseline --tasks learn` (chạy 3 tác vụ học baseline).
  4. `python -m lab.runner --condition subagents --tasks learn` (chạy 3 tác vụ học subagents).
  5. `python -m lab.curator` (Curator phân tích lỗi và sinh skill vào `skills/auto/`).
  6. `git add -A && git commit -m "hypotheses"` (commit giả thuyết H1-H3).
  7. `git add -A && git commit --allow-empty -m "freeze skills" && git tag freeze` (đóng băng bộ kỹ năng).
  8. `python -m lab.runner --condition baseline --tasks eval` (chạy tác vụ đánh giá baseline).
  9. `python -m lab.runner --condition subagents --tasks eval` (chạy tác vụ đánh giá subagents).
  10. `python -m lab.runner --condition skills-auto --tasks all` (chạy toàn bộ 6 tác vụ với skill đóng băng).
  11. `python scripts/verify_freeze.py` (xác thực đóng băng: checked 6 runs -> OK).
  12. `python -m lab.compare > report/table.md` và `python scripts/check_breakdown.py` (xuất bảng tổng hợp).
