# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Võ Trường An | 2A202602656 | 100% |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `google_genai:gemini-3.8-flash` (từ `.env`), `LAB_TEMPERATURE=0`, `recursion_limit=60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, macOS 27.0.0 (Apple Silicon arm64), chạy trực tiếp
- Số lần chạy tác vụ đã dùng / ngân sách: 6 / 15 (3 baseline + 3 subagents trên tập learn)
- Commit của tag `freeze`: (chưa tạo tag freeze)

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
| `python-code-maintenance` | **Tổng quát**: Hướng dẫn quy trình bảo trì gói Python (type hints cho mọi public function, tạo `tests/test_regressions.py` có >= 3 test, cập nhật `CHANGELOG.md` mục Unreleased). Không chứa task ID hay số liệu hardcode. | **Đúng**: Khớp chính xác với cả 3 quy ước house rules của họ tác vụ code. | 14 dòng; description kích hoạt rõ ràng ("Use when fixing bugs, refactoring, or preparing code changes for review in a Python package."); chờ đo ở Phần 3.4 |
| `log-triage-reporting` | **Tổng quát**: Checklist chuẩn hóa báo cáo phân loại log (schema_version 2, generated_by "log-triage", normalize service name snake_case, timestamp UTC, sort errors ascending). | **Đúng**: Khớp chính xác với cả 3 quy ước house rules của họ tác vụ logs. | 13 dòng; description kích hoạt chuẩn xác ("Use when parsing server logs to extract errors and generate structured JSON triage reports."); chờ đo ở Phần 3.4 |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
