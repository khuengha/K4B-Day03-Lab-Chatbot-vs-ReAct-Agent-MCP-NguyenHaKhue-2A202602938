# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Hà Khuê
> **Mã Sinh Viên / Mã Học viên:** 2A202602938  
> **Chủ đề Lựa chọn:** Trợ lý Dịch vụ Khách hàng VinBus 

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Nhiều yêu cầu của khách hàng không thể trả lời trong một bước mà phải trải qua chuỗi suy luận nối tiếp: hiểu ý định → trích xuất tham số (mã tuyến, mã KH, ngày) → gọi tool → đọc Observation → tổng hợp câu trả lời. Ví dụ điển hình: khách muốn đăng ký vé tháng nhưng chưa biết giá vé, Agent phải `route_query` trước để báo giá, chờ khách xác nhận rồi mới `register_monthly_ticket`. Tuy nhiên phần lớn test case trong phạm vi lab chỉ cần 1–2 bước suy luận, chưa có ca bắt buộc chuỗi phân nhánh phức tạp nhiều tầng, nên trừ 1 điểm. |
| **2. Tool Interaction** | 5 / 5 | Đây là tiêu chí cốt lõi của bài lab: hệ thống bắt buộc phải kết nối LLM với MCP Server để gọi tool thật (`route_query`, `register_monthly_ticket`) thao tác trên "cơ sở dữ liệu" tuyến xe VinBus. Không có tool, Agent hoàn toàn không thể tra cứu lộ trình hay đăng ký vé — mô hình không có dữ liệu này trong kiến thức nền. Mọi hành động tạo tác dụng phụ (booking_id) đều đi qua lớp MCP, đúng tinh thần Function Calling + MCP của bài lab. |
| **3. Dynamic Decision** | 4 / 5 | Bước tiếp theo của Agent phụ thuộc hoàn toàn vào kết quả Observation bước trước: nếu `route_query` trả về `NOT_FOUND`, Agent phải chuyển hướng gợi ý tuyến khác hoặc xin khách cung cấp lại mã tuyến thay vì gọi tool đăng ký; nếu tra cứu thành công mới tiến hành đăng ký. Vòng lặp ReAct (Thought → Action → Observation) trong `app.py` thể hiện rõ việc quyết định động này. Điểm chưa tối đa vì dữ liệu mock đơn giản, ít ca test đòi hỏi Agent phải "quay lui" (backtrack) nhiều vòng hoặc xử lý lỗi phức tạp. |
| **4. Long Horizon Goal** | 3 / 5 | Agent có System Prompt quy định vai trò và mục tiêu xuyên suốt (giải đáp & hỗ trợ đăng ký vé tháng VinBus) trong suốt hội thoại nhiều lượt, và phải nhớ ngữ cảnh khách hàng (mã KH, tuyến quan tâm) qua các bước. Tuy nhiên phạm vi bài lab là các request ngắn, hoàn thành trong 1 phiên xử lý duy nhất — không có mục tiêu dài hạn kéo dài qua nhiều phiên/phút giờ như đặt vé nhiều chặng hay theo dõi đơn hàng nhiều ngày, nên chỉ đạt mức trung bình khá. |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Đăng ký vé tháng tuyến OCT1 cho khách hàng KH202602938 từ ngày 13/09/2026",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "register_monthly_ticket",
    "arguments": {
      "customer_id": "KH202602938",
      "route_code": "OCT1",
      "start_date": "13/09/2026"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "TK-KH202602938-OCT1",
      "customer_id": "KH202602938",
      "route_code": "OCT1",
      "start_date": "13/09/2026",
      "message": "Đăng ký vé tháng thành công cho khách hàng KH202602938 trên tuyến OCT1 từ ngày 13/09/2026."
    },
    "latency_ms": 1706.19
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
