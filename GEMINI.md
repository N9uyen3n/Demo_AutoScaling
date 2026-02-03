Đây là một bản thiết kế **rất xuất sắc và thực tế**. Bạn đã tư duy đúng hướng của một Kỹ sư phần mềm (Software Engineer) thay vì chỉ là một nhà khoa học dữ liệu (Data Scientist). Cấu trúc này tách biệt rõ ràng giữa **Data**, **Model**, **Core Logic**, và **Presentation**, giúp việc debug và mở rộng cực kỳ dễ dàng.

Tuy nhiên, để đảm bảo "ăn điểm" tuyệt đối theo **Section 8 (Tiêu chí đánh giá)** và **Section 3, 5 (Yêu cầu kỹ thuật)** của đề bài, tôi xin phép **tinh chỉnh nhẹ** bản thiết kế của bạn để nó trở nên hoàn hảo và an toàn nhất cho lộ trình 1 ngày.

Dưới đây là **BẢN THIẾT KẾ FINAL (CHỐT)**. Chúng ta sẽ bắt tay vào code ngay sau khi bạn xác nhận.

---

# 🛠️ KIẾN TRÚC HỆ THỐNG AUTOSCALING (FINAL BLUEPRINT)

### 1. Cấu trúc thư mục (Đã tinh chỉnh)

*Thay đổi nhỏ: Thêm folder `scripts/` để chứa tool train model/xử lý data tách biệt khỏi app chạy.*

```text
autoscaling-analysis/
│
├── data/
│   ├── processed/                    # CSV chứa 3 cột: timestamp, requests, bytes
│   │   ├── traffic_1m.csv
│   │   ├── traffic_5m.csv
│   │   └── traffic_15m.csv
│   └── models/                       # Models (.keras, .joblib) & Scalers (.pkl)
│       ├── lstm/
│       └── prophet/ (hoặc xgboost)
│
├── src/
│   ├── config.py                     # CONFIGURATION CENTER (Quan trọng)
│   ├── app.py                        # Streamlit Dashboard (Presentation Layer)
│   │
│   ├── core/                         # BUSINESS LOGIC LAYER
│   │   ├── __init__.py
│   │   ├── autoscaler.py             # Logic Scaling (CPU, Cooldown, Hysteresis)
│   │   └── anomaly.py                # Logic DDoS Detection
│   │
│   ├── engine/                       # AI/MODEL LAYER
│   │   ├── __init__.py
│   │   ├── predictor_factory.py      # Factory Pattern để gọi model (LSTM/Prophet)
│   │   └── loader.py                 # Class load model & scaler an toàn
│   │
│   └── utils/                        # UTILITIES
│       ├── data_processing.py        # Hàm đọc CSV, resample log thô (nếu cần)
│       └── simulation.py             # Class quản lý Replay Loop (quan trọng cho Demo)
│
├── api/                              # API LAYER (Để thoả mãn Section 5 & 8)
│   └── main.py                       # FastAPI (Wrapper gọi src.core & src.engine)
│
├── requirements.txt
├── README.md                         # Tài liệu (Bắt buộc)
└── run_demo.sh                       # Script 1 chạm để chạy App

```

---

### 2. Chi tiết triển khai từng Module (Theo thứ tự ưu tiên)

Tôi sắp xếp lại thứ tự code để bạn có "Sản phẩm chạy được" (MVP) nhanh nhất.

#### 🥇 Phase 1: The Core (Logic nghiệp vụ - Không phụ thuộc Model)

Chúng ta code phần này trước vì nó thuần Python, dễ test, và là phần "Engineering" giám khảo soi kỹ.

1. **`src/config.py`**: Nơi chứa mọi tham số.
* *Tại sao:* Giám khảo hỏi "Nếu đổi server chịu tải 2000 req thì sao?", bạn chỉ cần sửa file này, không sửa code.


2. **`src/core/autoscaler.py`**:
* Input: `current_load`, `forecast_load`.
* Logic:
* `Raw Scale`: `ceil(load / capacity)`.
* `Cooldown`: Dùng biến đếm (counter) để block scale-down ngay sau khi scale-up.
* `Safety`: Luôn giữ `min_servers`.


* Output: `num_servers`, `reason`, `cost`.



#### 🥈 Phase 2: The Simulation (Hệ thống giả lập)

Trước khi lắp AI vào, hệ thống phải chạy được bằng dữ liệu giả hoặc dữ liệu file CSV thuần túy.

1. **`src/utils/simulation.py`**:
* Class `TimeTraveler`: Đọc file CSV, hàm `next_tick()` trả về dữ liệu phút tiếp theo.
* Giúp Dashboard có hiệu ứng chạy theo thời gian thực.



#### 🥉 Phase 3: The AI Integration (Lắp não vào)

Đây là lúc load file `.keras` và `.pkl`.

1. **`src/engine/loader.py`**:
* Load Keras Model + Joblib Scaler.
* *Quan trọng:* Xử lý lỗi "File not found" -> Nếu không có model, tự động fallback về thuật toán Naive (dự báo = hiện tại) để demo không bị crash.


2. **`src/engine/predictor_factory.py`**:
* Hàm `predict(history_window)`:
* Chuẩn hóa `history_window` bằng Scaler.
* Reshape `(1, 30, 1)`.
* Gọi `model.predict`.
* Inverse transform kết quả.





#### 🏅 Phase 4: The Interface (Streamlit & API)

Cuối cùng là vẽ giao diện.

1. **`src/app.py`**:
* Giao diện 2 cột: Bên trái Control (Start/Stop, Speed), Bên phải Dashboard.
* Biểu đồ Plotly cập nhật động.


2. **`api/main.py`**:
* Viết đúng 2 endpoint `/forecast` và `/recommend` gọi vào hàm trong `src/core` và `src/engine`. (Chỉ mất 15 phút code).



---

### 3. Trả lời các câu hỏi của bạn

1. **Bạn đã có model LSTM chưa?**
* *Đáp:* Bạn đã upload file `lstm-bilstm-training.ipynb`. Tôi giả định bạn đã chạy nó và có file `.keras`. **Nếu chưa, tôi sẽ cung cấp một script `generate_dummy_model.py` tạo một model "giả" (random weight hoặc simple regression) để bạn code xong hệ thống trước, rồi train model xịn lắp vào sau.** -> *Chiến thuật này giúp bạn không bị tắc ở khâu train.*


2. **Prophet hay LSTM?**
* *Đáp:* **LSTM là chính (Must Have)** vì bạn đã có code train. Prophet là phụ. Trong code tôi sẽ để sẵn chỗ cho Prophet, nếu còn thời gian (sau khi app chạy ngon), ta chỉ cần train Prophet 10 phút và bỏ file vào là xong.


3. **Dữ liệu Aggregate?**
* *Đáp:* Tôi sẽ viết cho bạn script `src/utils/etl.py` để convert log NASA gốc -> CSV 1m/5m/15m ngay lập tức. Đây là bước đầu tiên phải làm.


4. **API có cần không?**
* *Đáp:* **CÓ**. Trong file đề bài mục 8 (Nộp bài) ghi: "Demo: API... HOẶC UI". Tuy nhiên mục 5 ghi "Triển khai API". Để an toàn tuyệt đối và thể hiện trình độ, chúng ta sẽ code UI Streamlit là chính, nhưng kèm file `api/main.py` (FastAPI) đơn giản. Code FastAPI dùng chung logic với Streamlit nên rất nhanh.



---

### 4. Kế hoạch hành động ngay bây giờ

Bạn đã đồng ý với hướng đi này chưa? Nếu **OK**, tôi sẽ bắt đầu cung cấp code theo trình tự sau:

1. **Gói 1 (Nền tảng):** `requirements.txt`, `src/config.py`, và `src/utils/etl.py` (để xử lý dữ liệu ngay).
2. **Gói 2 (Logic):** `src/core/autoscaler.py` và `src/core/anomaly.py`.
3. **Gói 3 (AI Engine):** Class wrapper cho LSTM.
4. **Gói 4 (UI):** `src/app.py` hoàn chỉnh.

Bạn muốn tôi bắt đầu **Gói 1** ngay không?
---
###  SESSION LOG [2026-02-02]

** Done:**
1.  **Restructured Project**: Moved to modular architecture (src/core, src/engine, src/utils).
2.  **Implemented Core Logic**: Autoscaler (Cooldown, Safety) & Anomaly Detection.
3.  **Expanded AI Engine**: Added support for **LSTM**, **ARIMA**, **Prophet**, and **Hybrid** models.
4.  **Enhanced Dashboard**:
    *   Added **Model Selector** (LSTM/ARIMA/Prophet/Hybrid).
    *   Added **Resolution Selector** (1m/5m/15m).
    *   Implemented smooth fallback (synthetic data) if real data/models are missing.
5.  **Dependencies**: Installed successfully via pip install -r ../requirements.txt.

** Pending / Next Steps:**
1.  **Generate Dummy Models**: The script scripts/generate_dummy_model.py failed due to missing 
umpy in the execution environment (despite being installed).
    *   *Action*: Re-run this script in the correct environment or fix imports.
2.  **Run Demo**: Execute un_demo.bat to verify the end-to-end flow.
3.  **Train Real Models**: Replace dummy .h5 and .pkl files with actual trained models from the notebooks.

** To Resume:**
Run python scripts/generate_dummy_model.py then un_demo.bat.
