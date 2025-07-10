# Pain Point to Solution Agent – Cách Hoạt Động & Giải Thích Code

## 1. Mục đích

Đây là agent nhận **pain point** liên quan đến trải nghiệm khách hàng/dịch vụ khách hàng, sau đó gợi ý các tính năng phù hợp của Filum.ai để giải quyết.

---
## Project Structure

```
PAIN-POINT-AGENT/
│
├── database/
│   └── features.json      # Knowledge base: List of feature descriptions for matching
│
├── output/
│   └── output.json        # Output file: Stores results (top solutions) generated after running the agent
│
├── scripts/
│   └── pain_point_agent.py # Main Python script: The agent logic for matching pain points to features
│
└── Readme.md              # This documentation file
```
---

## 2. Hướng dẫn chạy

- **Yêu cầu:** Python 3.x, file database `features.json` (chứa các thông tin về tính năng) phải đúng đường dẫn.
- **Chạy chương trình:**
  ```bash
  python pain_point_agent.py
  ```
- **Sửa input để test:**  
  Thay đổi nội dung biến `input_json` trong file để nhập pain point và context mong muốn.

---

## 3. Cách hoạt động & giải thích code

### a. Các bước tính điểm matching

**1. Tiền xử lý input (preprocess)**
- Tất cả pain point và context được đưa về chữ thường (lowercase), loại bỏ dấu câu, ký tự đặc biệt, và loại bỏ các từ vô nghĩa (stopwords) như "của", "là", "và", v.v.
- Sau đó tách thành tập hợp các từ khóa (từ/cụm từ quan trọng).

**2. Tiền xử lý context**
- Context (ví dụ channel: "email", customer_type: "B2C") cũng chuyển hết về chữ thường, gom thành tập từ khóa context.

**3. So khớp & tính điểm (hàm match_pain_point, match_score)**
- Với mỗi tính năng (feature) trong database:
  - So khớp từ khóa pain point với trường `keywords` của feature: **mỗi từ trùng +1 điểm**
  - So khớp pain point với `example_pain_points`: **mỗi từ trùng +2 điểm** (ưu tiên cao hơn vì đây là ví dụ thực tế)
  - So khớp context với `channels` và `customer_types`: **mỗi từ trùng +0.5 điểm**
  - Tổng điểm này là **relevance_score**
- Nếu tổng điểm > 0, feature được đưa vào danh sách kết quả.

**4. Sắp xếp kết quả**
- Kết quả được sắp xếp giảm dần theo `relevance_score`.
- Chỉ trả về tối đa top_n (mặc định 3) feature phù hợp nhất.

**5. Giải thích lý do matching (hàm explain_matching)**
- Mỗi feature được match sẽ kèm một chuỗi giải thích ngắn gọn:
  - Từ khóa nào trùng?
  - Pain point nào gần giống ví dụ?
  - Context nào khớp?

---

### b. Triển khai từng hàm chính

- **load_db(path):** Load file JSON database thành danh sách Python dict.
- **preprocess(text):** Chuẩn hóa, tách từ, loại stopword khỏi text, trả về tập từ khóa.
- **preprocess_context(context):** Gom các giá trị context thành tập từ khóa chuẩn hóa.
- **match_score(words, target_list):** Tính số từ trùng nhau giữa input và từng trường trong feature.
- **explain_matching(pain, context, feature):** Tạo chuỗi giải thích vì sao feature này được chọn.
- **match_pain_point(pain_point, features, context, top_n):** Hàm chính, xử lý toàn bộ logic matching như trên.

---

### c. Ví dụ kết quả output

```json
[
  {
    "feature_name": "AI Agent for FAQ & First Response",
    "category": "AI Customer Service - AI Inbox",
    "description": "AI tự động trả lời câu hỏi thường gặp.",
    "how_it_helps": "Giảm tải cho nhân viên, trả lời tự động các câu hỏi lặp lại.",
    "link": "https://docs.filum.ai/features/ai-inbox",
    "relevance_score": 27.0,
    "explanation": "Pain point gần giống ví dụ: Nhân viên hỗ trợ bị quá tải câu hỏi lặp lại, Khách hỏi lại nhiều câu giống nhau; Context trùng: email, b2c"
  },
  ...
]
```
- **relevance_score** càng cao, feature càng phù hợp.
- **explanation** giúp bạn hiểu vì sao agent chọn giải pháp này.

---

### d. Lưu ý

- Dễ dàng mở rộng: Có thể thêm/sửa tính năng mới vào `features.json` mà không cần sửa code.
- Nếu muốn nâng cấp logic (dùng AI, fuzzy matching, semantic search...), chỉ cần chỉnh lại hàm `match_score` hoặc thêm bước mới trong `match_pain_point`.

---

## 4. Tổng kết

- Agent này giúp tự động gợi ý giải pháp dựa trên mô tả pain point.
- Điểm matching giúp xác định mức độ phù hợp, tăng tính minh bạch nhờ trường giải thích.
- Đơn giản, dễ bảo trì, dễ mở rộng.
