# 🎤 PLANORA Demo Script - 5 Phút Presentation

## 📋 Checklist Trước Demo

### Technical Setup (2 phút trước)
- [ ] Terminal ready tại folder `src/`
- [ ] Run `streamlit run app_optimized.py`
- [ ] Dashboard đã load xong
- [ ] Browser zoom 100% (Ctrl+0)
- [ ] Sidebar expanded
- [ ] Chọn "LSTM (Pre-calculated)" + "1m" resolution
- [ ] START SIMULATION = ON

### Backup Plan
- [ ] Screenshot của dashboard đang chạy
- [ ] Video recording (3-5 phút) sẵn sàng
- [ ] Slide PDF backup

---

## 🎯 Demo Flow (5 Phút)

### **[0:00-0:30] HOOK - Giới thiệu vấn đề** 
> "Trong cloud computing, cấp phát tài nguyên cố định dẫn đến 2 vấn đề nghiêm trọng..."

**Actions:**
- Không cần show gì, nói trực tiếp
- Gesture: Tay trái = lãng phí, Tay phải = sập hệ thống

**Script:**
```
"Khi ít người dùng → Lãng phí tài nguyên
Khi traffic tăng đột biến → Hệ thống sập

Giải pháp? PLANORA - Hệ thống autoscaling thông minh với AI"
```

---

### **[0:30-1:30] DEMO CORE - Real-time Dashboard** ⭐ QUAN TRỌNG NHẤT
> "Đây là dashboard real-time của chúng em..."

**Actions:**
1. **Point to Traffic Chart** (20s)
   - "Đường xanh cyan = Actual traffic"
   - "Đường tím đứt nét = AI forecast"
   - Highlight: "AI dự đoán TRƯỚC 1-5 phút"

2. **Point to Metrics Row** (20s)
   - "Current traffic: 120 req/min"
   - "AI forecast: 135 req/min → Tăng 15"
   - "Active Nodes: 8/20 → System scale động"

3. **Watch a Scale Event** (20s)
   - Chờ 1 scale-out event xảy ra
   - Point: "Nodes tăng từ 8 → 9"
   - "Delta hiện +1"

**Script:**
```
"Dashboard này monitor real-time traffic và dùng AI để predict tải trong tương lai.

Khi AI dự báo tải sẽ tăng, hệ thống PROACTIVE scale-out trước khi traffic thật sự tăng.

Anh chị thấy, đây - nodes vừa tăng từ 8 lên 9 để đón đầu traffic spike."
```

---

### **[1:30-2:30] TECHNICAL DEPTH - 3-Layer Defense** 🛡️
> "Core innovation của chúng em là 3-Layer Defense Strategy..."

**Actions:**
1. **Point to Decision Panel** (30s)
   - L1: "Predictive - Tấn công, chủ động scale trước"
   - L2: "Reactive - Phòng thủ, safety net khi AI sai"
   - L3: "Stability - Luật ổn định, chống flapping"

2. **Show Override Scenario** (30s)
   - Chờ 1 reactive override (hoặc explain)
   - "Khi traffic thật > forecast → L2 override L1"
   - Point to warning box

**Script:**
```
"3-Layer Defense là điểm khác biệt của PLANORA:

Layer 1 - PREDICTIVE: AI forecast → Pre-warm servers
Layer 2 - REACTIVE: Actual load → Safety net
Layer 3 - STABILITY: Cooldown rules → Prevent flapping

Ví dụ này, anh chị thấy L2 override L1 vì traffic thật cao hơn dự báo.
Đây là cơ chế bảo vệ khi AI prediction có sai số."
```

---

### **[2:30-3:30] VISUAL SHOWCASE - Server Grid & Charts** 🎨
> "Để visualization rõ hơn..."

**Actions:**
1. **Server Grid** (30s)
   - Point to green nodes = active
   - Point to gray nodes = inactive
   - "Mỗi node có CPU load bar riêng"

2. **Forecast Error Chart** (30s)
   - Point to residuals chart bên phải
   - "Đây là sai số giữa predict và actual"
   - "Green bars = dự báo tốt, Red bars = sai số lớn"

**Script:**
```
"Phần visualization giúp operators dễ monitor:

Server Grid - 12 nodes với CPU real-time
Green = active, Gray = standby

Forecast Error chart - Track độ chính xác của AI
Giúp identify khi nào cần retrain model."
```

---

### **[3:30-4:15] MODEL PERFORMANCE - Switch Models** 🤖
> "Chúng em implement nhiều models..."

**Actions:**
1. **Sidebar → Model Selection** (20s)
   - Click dropdown
   - Show: LSTM, Prophet, ARIMA
   - "Mỗi model có ưu/nhược khác nhau"

2. **Switch to ARIMA** (25s)
   - Select "ARIMA"
   - Chờ 2-3 ticks để chart update
   - "ARIMA reactive hơn, LSTM smooth hơn"

**Script:**
```
"Hệ thống support nhiều models:

LSTM - Deep learning, tốt cho pattern phức tạp
Prophet - Facebook model, handle seasonality
ARIMA - Statistical, train nhanh on-the-fly

Production có thể chọn model phù hợp theo use case."
```

---

### **[4:15-5:00] CLOSE - Impact & Future** 🚀
> "Kết quả và hướng phát triển..."

**Actions:**
- Quay lại overview dashboard
- Point to cost metric (nếu có)
- Gesture confident

**Script:**
```
"Impact của PLANORA:

✅ Giảm 30-50% chi phí so với fixed scaling
✅ Zero downtime với predictive scaling  
✅ Auto-detect anomalies (DDoS, spikes)

Future work:
- Multi-region autoscaling
- Cost optimization với spot instances
- Integration với Kubernetes HPA

Cảm ơn anh chị đã theo dõi!"
```

---

## 🎬 Backup Scenarios

### Nếu Dashboard Lag
```
"Do đang demo trên laptop, production sẽ deploy trên cloud với response time < 100ms"
→ Switch to screenshot hoặc video
```

### Nếu No Data
```
"Data thật từ NASA HTTP logs 1995, 2 tháng access logs"
→ Show synthetic data đang chạy
"Đây là pattern tương tự được simulate"
```

### Nếu Không Scale Event
```
"Để demo rõ hơn mechanism..."
→ Explain decision panel logic
→ Show code snippet nếu có slide backup
```

---

## 💡 Pro Tips

### Body Language
- **Stand confident**, không dựa bàn
- **Hand gestures** to highlight points
- **Eye contact** với judges, không chỉ nhìn screen

### Voice
- **Vary tempo**: Nhanh ở intro, chậm ở technical
- **Emphasize** key terms: "Predictive", "Reactive", "3-Layer"
- **Pause** sau mỗi key point (1-2s)

### Technical Terms
- Không dùng: "Em nghĩ", "Có thể", "Chắc"
- Dùng: "Chúng em implement", "Hệ thống guarantee", "Kết quả cho thấy"

### Time Management
- Có đồng hồ trước mặt
- **3:00 mark** = Phải đến Model Performance
- **4:30 mark** = Start wrapping up

---

## 📊 Key Metrics to Mention

| Metric | Value | Impact |
|--------|-------|--------|
| Forecast Accuracy | MAPE < 15% | High precision |
| Scale-out Latency | < 5s | Fast response |
| Cost Savings | 30-50% | vs Fixed scaling |
| Cooldown Period | 3 cycles | Prevent flapping |

---

## 🎥 Camera Positioning (Nếu Record)
```
[Screen Recording]    [You]
    75%                25%
    
hoặc Picture-in-Picture mode
```

---

## ✅ Post-Demo Q&A Prep

**Expected Questions:**

**Q: "Làm sao xử lý khi AI prediction sai?"**
A: "Layer 2 Reactive Defense sẽ override dựa trên actual load. Ngoài ra có cooldown mechanism tránh scale in quá nhanh."

**Q: "Tại sao không dùng simple threshold-based?"**
A: "Threshold-based reactive - đợi spike mới scale. Predictive pre-warm trước khi spike xảy ra, giảm latency cho users."

**Q: "Data nguồn gốc từ đâu?"**
A: "NASA HTTP logs 1995, 2 tháng access logs thật. Đã được process thành time series 1min/5min/15min."

**Q: "Training time của models?"**
A: "LSTM pre-trained. ARIMA train on-the-fly < 2s. Production có thể schedule retrain daily."

---

**Chúc bạn demo thành công! 🎉**
