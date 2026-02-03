# 🛡️ DEFENSE Q&A: AUTOSCALING SYSTEM ANALYSIS

Tài liệu này dùng để trả lời phản biện, dựa trên **Code thật** và **Kết quả Benchmark thật** của dự án.

---

### 1. ❓ Vì sao các bạn chọn những mô hình này (LSTM, Prophet, Hybrid) làm ứng viên ban đầu?
**Trả lời:** Chúng tôi chọn mô hình dựa trên đặc thù của dữ liệu Web Traffic (NASA Logs):
*   **Prophet:** Được chọn vì khả năng bắt **Seasonality** (chu kỳ ngày/tuần) cực tốt và chịu được nhiễu (outliers). NASA logs có xu hướng truy cập mạnh vào ban ngày và giảm vào ban đêm (Diurnal pattern).
*   **LSTM (Long Short-Term Memory):** Là mạng Deep Learning chuyên trị các chuỗi thời gian phi tuyến tính phức tạp, học được các phụ thuộc ngắn hạn (Short-term dependencies) mà Prophet có thể bỏ sót.
*   **Hybrid (Prophet + LSTM):** (Mô hình chính) Chúng tôi kết hợp sức mạnh của cả hai: Prophet bắt trend/seasonality (phần tĩnh), LSTM học phần dư (Residuals - phần lỗi mà Prophet chưa giải thích được). Đây là kiến trúc **Residual Learning**.

---

### 2. ❓ Best model được chọn dựa trên metric nào, trên tập nào?
**Trả lời:**
*   Dựa trên kết quả thực nghiệm tại file `comprehensive_comparison.csv`:
*   **Metric:** Chúng tôi ưu tiên **RMSE (Root Mean Square Error)** vì nó phạt nặng các sai số lớn (tránh dự báo sai lệch quá nhiều gây sập hệ thống).
*   **Kết quả (5min Resolution):**
    *   **Prophet:** RMSE = 86.99 (MAE = 60.3)
    *   **LSTM:** RMSE = 99.37 (MAE = 84.83)
    *   **Hybrid (Best):** **RMSE = 49.17** (MAE = 36.3).
    *   👉 **Kết luận:** Mô hình Hybrid giảm sai số **~43%** so với Prophet gốc.

---

### 3. ❓ Vì sao mô hình ở khung 5 phút (5min) lại phù hợp hơn 1 phút hoặc 15 phút?
**Trả lời:** Đây là bài toán **Trade-off (Đánh đổi)** giữa "Độ nhạy" (Sensitivity) và "Độ ổn định" (Stability):
*   **1 phút:** Dữ liệu quá nhiễu (Noisy). Dự báo sẽ dao động liên tục theo từng phút -> Gây ra hiện tượng **Flapping** (Scale out rồi lại Scale in liên tục), làm giảm tuổi thọ phần cứng và tăng latency khởi động.
*   **15 phút:** Quá thô (Coarse). Nếu có Spike xảy ra ở phút thứ 2, hệ thống phải đợi đến phút 15 mới phản ứng -> **Quá trễ**, user đã bị time-out.
*   **5 phút (Sweet Spot):** Đủ mịn để phản ứng kịp thời với thay đổi tải, nhưng cũng đủ mượt để loại bỏ nhiễu ngẫu nhiên.  

---

### 4. ❓ Nếu dự báo sai (underestimate hoặc overestimate), hệ thống autoscaling sẽ bị ảnh hưởng như thế nào?
**Trả lời:** Chúng tôi xử lý việc này bằng **Chiến lược phòng thủ 3 lớp (3-Layer Defense)** trong `src/core/autoscaler.py`:
*   **Trường hợp 1: Overestimate (Dự báo > Thực tế):**
    *   *Hậu quả:* Tốn chi phí tài nguyên (thừa server).
    *   *Xử lý:* Chấp nhận được để đảm bảo **Reliability**. Layer 1 (Predictive) sẽ scale dư một chút để an toàn (Over-provisioning).
*   **Trường hợp 2: Underestimate (Dự báo < Thực tế - Nguy hiểm):**
    *   *Hậu quả:* Thiếu server, sập hệ thống.
    *   *Xử lý:* **Layer 2 (Reactive Override)** sẽ kích hoạt ngay lập tức. Code dòng 37 (`autoscaler.py`): `if reactive_target > predictive_target: target = reactive_target`. Hệ thống tự động chuyển sang mode phản ứng nhanh, bỏ qua dự báo sai.

---

### 5. ❓ Tại sao autoscaling không nên phản ứng theo từng giây hoặc từng request?
**Trả lời:**
1.  **Cold Start Latency:** Một server/container mất từ 30s - 2 phút để khởi động và sẵn sàng nhận traffic. Scale theo giây là vô nghĩa vì server chưa kịp lên thì traffic đã đổi.
2.  **Thrashing/Flapping:** Nếu scale theo từng giây, số lượng replicas sẽ dao động cực mạnh (ví dụ: 10 -> 20 -> 10 -> 25), gây quá tải cho bộ điều khiển Cluster (Kubernetes Control Plane) và làm hệ thống mất ổn định.

---

### 6. ❓ Nếu bỏ cơ chế hysteresis và cooldown, điều gì sẽ xảy ra?
**Trả lời:**
*   Cơ chế này nằm ở **Layer 3 (Stability Rule)** trong code.
*   Nếu bỏ đi: Hệ thống sẽ bị **Flapping**.
    *   *Ví dụ:* Load đang ở ngưỡng 79% (Scale Out tại 80%). Tải dao động 79% -> 81% -> 79%.
    *   *Không có hysteresis:* Hệ thống Add Node -> Remove Node -> Add Node liên tục mỗi chu kỳ quét.
    *   *Có Cooldown (Code dòng 61):* Sau khi Scale Out, chúng tôi khóa Scale In trong `N` chu kỳ (`cooldown_counter`), bất kể tải giảm nhẹ, giữ cho hệ thống ổn định đường dài.

---

### 7. ❓ Việc phát hiện spike / bất thường trong bài này có phải là phát hiện DDoS thực sự không?
**Trả lời:**
*   Thực tế, đây là phát hiện **Traffic Spike (Volume-based Anomaly)** ở tầng ứng dụng (L7), chưa phải là giải pháp Anti-DDoS chuyên dụng (L3/L4 scrubbing).
*   Tuy nhiên, trong bối cảnh Autoscaling, chúng tôi quan tâm đến **Symptom (Triệu chứng)**: Liệu lượng request này có đánh sập server không?
*   Thuật toán **Z-Score** (Code: `anomaly.py`) giúp phân biệt:
    *   **Flash Crowd (Người dùng thật):** Tăng từ từ hoặc theo trend dự báo được.
    *   **DDoS/Anomaly:** Tăng đột biến vượt quá `Mean + 3*Sigma` trong thời gian ngắn. Hệ thống sẽ cảnh báo (Alert) để Admin can thiệp, thay vì chỉ mù quáng Scale out (tránh tốn chi phí cho traffic rác).

---

### 8. ❓ Chi phí được tối ưu trong bài toán này được định nghĩa như thế nào?
**Trả lời:** Chi phí trong bài toán là sự cân bằng giữa **Resource Cost** và **SLA Penalty Cost**:
*   **Resource Cost:** Số lượng Replicas * Đơn giá/giờ (định nghĩa trong `config.py` là `COST_PER_REPLICA_PER_TICK`).
*   **Mục tiêu:** Minimizing Cost nhưng ràng buộc là `Capacity >= Demand`.
*   Nhờ **Hybrid Model (RMSE thấp)**, chúng ta giảm được lượng "Buffer" (tài nguyên dự phòng thừa thãi) so với các phương pháp tĩnh, từ đó tiết kiệm tiền thật sự khi chạy trên Cloud (AWS/GCP).

---

### 9. ❓ Nếu áp dụng chiến lược này vào hệ thống thật, những rủi ro nào có thể xảy ra?
**Trả lời:**
1.  **Model Drift:** Sau vài tháng, hành vi người dùng thay đổi (Data Distribution Shift), mô hình cũ sẽ dự báo sai. -> Cần cơ chế **Retraining** định kỳ (MLOps pipeline).
2.  **Lag phản ứng:** Dù có Reactive Layer, vẫn luôn có độ trễ khi khởi tạo server vật lý. -> Cần kết hợp scale VM sẵn (Pre-warming) kỹ hơn trước các sự kiện lớn.

---

### 10. ❓ Nếu có thêm dữ liệu dài hơn (6–12 tháng), các bạn sẽ cải tiến mô hình hoặc chiến lược autoscaling như thế nào?
**Trả lời:**
1.  **Modeling Yearly Seasonality:** Với 12 tháng, Prophet có thể học được tính chu kỳ theo **Năm** (Lễ tết, Black Friday) -> Dự báo chính xác hơn cho các sự kiện đặc biệt.
2.  **Long-term Capacity Planning:** Không chỉ Autoscaling (ngắn hạn), mà có thể đưa ra khuyến nghị mua **Reserved Instances** (thuê server dài hạn giá rẻ) để tối ưu chi phí hạ tầng sâu hơn.
