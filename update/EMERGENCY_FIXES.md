# 🚨 EMERGENCY FIXES - Khi Demo Gặp Vấn Đề

## ⏰ Dành cho bạn khi chỉ còn < 30 phút trước demo!

---

## 🔥 TOP 5 Lỗi Thường Gặp

### 1️⃣ ImportError: No module named 'X'

**Lỗi:**
```
ImportError: No module named 'config'
ImportError: No module named 'core'
```

**Fix Nhanh (10 giây):**
```bash
# Make sure you're in src/ folder
cd src
python -c "import sys; print(sys.path)"

# If not in src/, run:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Fix Tốt Hơn (30 giây):**
```python
# Add to top of app_optimized.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

---

### 2️⃣ FileNotFoundError: Data files not found

**Lỗi:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/test_1min.csv'
```

**Fix Nhanh (1 phút):**
```python
# Dashboard sẽ TỰ ĐỘNG generate synthetic data
# Just let it run, no action needed!
```

**Hoặc tạo data ngay:**
```bash
cd src
python generate_demo_data.py
```

---

### 3️⃣ Dashboard chạy CHẬM/LAG

**Symptoms:**
- Update > 2 seconds per tick
- Browser freezing
- Charts not rendering

**Emergency Fix (5 giây):**
```python
# In sidebar:
Update Interval: Tăng lên 1.5 - 2.0s
```

**Better Fix (30 giây):**
```python
# Edit config.py
HISTORY_WINDOW = 30  # Giảm từ 60 xuống 30
MAX_CHART_POINTS = 50  # Limit chart points
```

**Nuclear Option:**
```python
# Comment out Forecast Error chart
# In app_optimized.py, line ~550
# with c_res:
#     # st.plotly_chart(fig2, ...)
```

---

### 4️⃣ Streamlit KHÔNG MỞ Browser

**Lỗi:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
(But browser doesn't open)
```

**Fix:**
```bash
# Manual open
# Windows:
start http://localhost:8501

# Mac:
open http://localhost:8501

# Linux:
xdg-open http://localhost:8501
```

**Or thử port khác:**
```bash
streamlit run app_optimized.py --server.port 8502
```

---

### 5️⃣ Charts KHÔNG HIỂN THỊ

**Symptoms:**
- Blank white space where charts should be
- "Failed to fetch" errors

**Fix Nhanh:**
```python
# Restart Streamlit
# Ctrl+C in terminal
# Run again: streamlit run app_optimized.py
```

**If still broken:**
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Or in Windows:
# Delete C:\Users\YourName\.streamlit\cache
```

---

## 🔧 Quick Diagnostics

### Test 1: Check Imports (15 seconds)
```bash
cd src
python -c "
import config
from core.autoscaler import Autoscaler
from engine.loader import ModelLoader
from utils.simulation import TimeTraveler
print('✅ All imports OK')
"
```

### Test 2: Check Data Loading (20 seconds)
```bash
cd src
python -c "
import pandas as pd
import os

for res in ['1min', '5min', '15min']:
    path = f'../data/test_{res}.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f'✅ {res}: {len(df)} rows')
    else:
        print(f'⚠️ {res}: NOT FOUND (will use synthetic)')
"
```

### Test 3: Check Streamlit (10 seconds)
```bash
streamlit --version
# Should show: Streamlit, version 1.x.x
```

---

## 🆘 Last Resort Solutions

### If EVERYTHING Fails (2 minutes)

**Plan A: Use Screenshots**
1. Take screenshots of dashboard running
2. Present screenshots trong slide
3. Walk through như đang live demo

**Plan B: Use Video**
1. Record demo trước (5 phút)
2. Play video trong presentation
3. Pause để giải thích

**Plan C: Code Walkthrough**
1. Open VS Code
2. Explain architecture từ code
3. Show 3-Layer Defense logic

---

## 🎬 Demo Recovery Strategies

### If Lag During Demo

**Say:**
```
"Do đang demo trên laptop local, có thể hơi chậm.
Production version deploy trên cloud sẽ có response time < 100ms."
```

**Action:**
- Pause simulation
- Show specific features (server grid, charts)
- Resume nếu đủ smooth

---

### If Data Not Loading

**Say:**
```
"Data thật là NASA HTTP logs 1995.
Để demo nhanh, em đang dùng synthetic data với pattern tương tự."
```

**Action:**
- Let synthetic data generate
- Continue demo normally
- Highlight that algorithm works với bất kỳ data nào

---

### If Model Prediction Fails

**Say:**
```
"Đây là pre-calculated predictions từ model đã train.
Nếu train live, ARIMA mất ~2s, LSTM mất ~5s."
```

**Action:**
- Switch to "LSTM (Pre-calculated)"
- Show forecast từ CSV
- Explain training process từ slides

---

### If Charts Not Updating

**Say:**
```
"Để dễ quan sát, em sẽ tạm dừng simulation và
highlight từng component của hệ thống."
```

**Action:**
- Pause simulation
- Point to metrics
- Explain 3-Layer Defense
- Resume nếu fix được

---

## 📱 Backup Materials Checklist

Chuẩn bị SẴN trước khi demo:

- [ ] **Screenshots** của dashboard (5-10 ảnh)
- [ ] **Video recording** (3-5 phút) backup
- [ ] **Slide PDF** với system architecture
- [ ] **Code snippets** (autoscaler.py, ARIMA logic)
- [ ] **Metrics table** (RMSE, MAE results)
- [ ] **Paper printout** của slides (just in case)

---

## 🎯 5-Minute Pre-Demo Checklist

**T-minus 5 minutes:**

```bash
# 1. Navigate to src/
cd path/to/project/src

# 2. Test imports
python -c "import config; print('OK')"

# 3. Start dashboard
streamlit run app_optimized.py

# 4. Wait for browser to open

# 5. Check:
✓ Sidebar loads
✓ Charts render
✓ Simulation starts
✓ Metrics update

# 6. Ready? Take deep breath 🧘
```

---

## 💡 Pro Tips

### Terminal Setup
```bash
# Split terminal window:
# Left: Running Streamlit
# Right: Backup Python shell for quick tests
```

### Browser Setup
```bash
# Open 2 tabs:
# Tab 1: Dashboard (localhost:8501)
# Tab 2: Backup dashboard (just in case)
```

### Zoom Level
```bash
# Set browser zoom to 100% (Ctrl+0)
# Or 90% nếu màn hình nhỏ
```

---

## 🔍 Debug Commands

### If you need to debug FAST:

```python
# Add to any file to print debug info
import sys
print(f"DEBUG: {variable}", file=sys.stderr)

# In Streamlit:
st.write(f"DEBUG: {variable}")  # Shows on dashboard

# Check session state:
st.write(st.session_state)
```

### Find where code is failing:

```python
# Wrap in try-except
try:
    # Your code
    result = function_call()
except Exception as e:
    st.error(f"Error: {e}")
    import traceback
    st.code(traceback.format_exc())
```

---

## 📞 Emergency Contacts (Figurative)

### Streamlit Issues
- Docs: https://docs.streamlit.io
- Forum: https://discuss.streamlit.io
- Quick search: "streamlit [your error]"

### Python Issues
- Stack Overflow: https://stackoverflow.com
- Quick search: "python [your error]"

---

## 🎪 Demo Mindset

### Remember:
1. **Judges care about IDEA**, not perfect execution
2. **Your explanation > Flashy demo**
3. **Backup plan > No plan**
4. **Stay calm > Panic**

### If something breaks:
```
❌ DON'T: Panic, apologize nhiều lần, stop presenting
✅ DO: Acknowledge briefly, pivot to backup, continue confident
```

---

## ✅ Final Pre-Demo Command

**Run this 30 seconds trước khi present:**

```bash
cd src
python quick_setup.py  # Checks everything
streamlit run app_optimized.py  # Start dashboard
```

**If any error appears:**
1. Screenshot error message
2. Check this file for fix
3. Apply fix
4. Re-run

---

## 🚀 You Got This!

**Remember:**
- Code ≠ Product
- Demo ≠ Competition
- Confidence > Perfection

**Worst case scenario:**
- Dashboard fails completely
- You still có slides
- You still có idea
- You still có presentation skills

**Best case scenario:**
- Everything works smooth
- Judges impressed
- You win 🏆

---

**Good luck! Breathe. You prepared well. Now go show them! 💪**

---

## 📋 Print This Section

```
═══════════════════════════════════════
    EMERGENCY DEMO COMMAND CARD
═══════════════════════════════════════

1. START DASHBOARD:
   cd src
   streamlit run app_optimized.py

2. IF IMPORTS FAIL:
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"

3. IF TOO SLOW:
   Sidebar → Update Interval: 2.0s

4. IF CHARTS BLANK:
   Ctrl+C → Restart → Refresh browser

5. IF DATA MISSING:
   Let it generate synthetic (auto)

6. NUCLEAR OPTION:
   Show screenshots/video instead

═══════════════════════════════════════
```

**Cut this out, keep on desk during demo!**
