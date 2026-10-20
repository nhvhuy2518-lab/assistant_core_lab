# Architecture Note: assistant_core

## 1. Module Responsibilities
- `config.py`: Đọc cấu hình từ biến môi trường qua Pydantic Settings, ẩn secret bằng `repr=False`.
- `errors.py`: Định nghĩa cây phân cấp ngoại lệ (`AssistantError`, `ConfigError`, `DataError`, `InvalidRequest`, `ProviderError`).
- `models.py`: Định nghĩa hợp đồng dữ liệu công khai (`Message`, `Response`, `Intent`, `Source`).
- `router.py`: Phân loại ý định người dùng (Intent) theo quy tắc tĩnh.
- `knowledge.py`: Tải và truy xuất dữ liệu danh bạ phòng ban (`OfficeDirectory`) và sổ tay sinh viên (`Handbook`).
- `tools.py`: Các hàm tính toán thuần túy (pure functions) tính học phí tất định.
- `responder.py`: Interface Protocol phân tách tầng sinh câu trả lời (`TemplateResponder`, `StubLLMResponder`).
- `service.py`: Cổng giao tiếp duy nhất (`AssistantService.handle`) tiếp nhận `Message` và trả về `Response`.
- `logging_setup.py`: Cấu hình log có cấu trúc dạng JSON ra stderr, bảo vệ secret.
- `__main__.py`: Giao diện dòng lệnh (CLI).

## 2. Service Interface
- **Method**: `AssistantService.handle(msg: Message) -> Response`
- **Input**: `Message(text: str [1-2000 chars], session_id: str)`
- **Output**: `Response(answer: str, intent: Intent, sources: list[Source], degraded: bool)`
- **Error Handling**: Input không hợp lệ bị chặn bởi `ValidationError`; lỗi hạ tầng LLM được bắt lại và chuyển sang template fallback với cờ `degraded=True`.

## 3. Architectural Decisions
1. **Học phí được tính toán bằng pure functions trong `tools.py`**: Tránh việc LLM bị ảo giác (hallucination) khi tính toán số học; đảm bảo kết quả tất định và có thể unit test độc lập.
2. **LLM được đặt sau interface `Responder` (Adapter pattern)**: Cho phép sử dụng `StubLLMResponder` trong kiểm thử và CI hoàn toàn offline mà không tốn chi phí gọi API hay làm lộ API key.
3. **Cấu hình tuân thủ The Twelve-Factor App Factor III**: Toàn bộ tham số được đọc từ môi trường/`.env`; tệp `.env.example` cung cấp tài liệu cấu hình mà không chứa khóa bí mật thực tế.