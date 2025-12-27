import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
import time

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="JAI - رعاية مرضى القلب", page_icon="❤️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; color: black; }
    .stButton > button { border-radius: 10px; font-weight: bold; width: 100%; color: white; }
    .blue-btn { background-color: #007bff !important; }
    .green-btn { background-color: #28a745 !important; }
    .red-btn { background-color: #dc3545 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الحالة والبيانات ---
if 'page' not in st.session_state: st.session_state.page = "home"
if 'data_history' not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=['الوقت', 'النبض', 'الضغط', 'الأكسجين', 'الحالة'])

# محاكاة نموذج الذكاء الاصطناعي (نموذج بسيط للتنبؤ)
def predict_risk(heart_rate, bp, spo2):
    # بيانات تدريب وهمية بسيطة: 1 خطر، 0 طبيعي
    X = [[100, 150, 90], [70, 120, 98], [110, 160, 85], [60, 110, 99]]
    y = [1, 0, 1, 0]
    clf = RandomForestClassifier()
    clf.fit(X, y)
    prediction = clf.predict([[heart_rate, bp, spo2]])
    return "خطر" if prediction[0] == 1 else "طبيعي"

# --- 3. محتوى الصفحات ---

# الصفحة الرئيسية
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center;'>دور إنترنت الأشياء في رعاية مرضى القلب ❤️</h1>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/iot-concept-illustration_114360-1234.jpg", width=400) # رابط صورة تعبيرية عن IoT
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚀 بدء المحاكاة", key="start_btn"):
            st.session_state.page = "simulation"
            st.rerun()
    with col2:
        if st.button("📊 عرض بيانات المريض", key="data_btn"):
            st.session_state.page = "data"
            st.rerun()
    with col3:
        if st.button("⚠️ عرض التنبيهات", key="alert_btn"):
            st.session_state.page = "alerts"
            st.rerun()

# صفحة المحاكاة والبيانات (مدمجة للتحديث التلقائي)
elif st.session_state.page == "simulation" or st.session_state.page == "data":
    st.title("📟 مراقبة المؤشرات الحيوية (بث مباشر)")
    
    # توليد بيانات عشوائية تحاكي IoT
    hr = np.random.randint(60, 120)
    bp = np.random.randint(100, 160)
    spo2 = np.random.randint(88, 100)
    status = predict_risk(hr, bp, spo2)
    
    # إضافة البيانات للتاريخ
    new_data = pd.DataFrame({'الوقت': [time.strftime("%H:%M:%S")], 'النبض': [hr], 'الضغط': [bp], 'الأكسجين': [spo2], 'الحالة': [status]})
    st.session_state.data_history = pd.concat([st.session_state.data_history, new_data], ignore_index=True).tail(10)

    # عرض البطاقات
    c1, c2, c3 = st.columns(3)
    c1.metric("نبض القلب", f"{hr} bpm", delta="طبيعي" if hr < 100 else "مرتفع", delta_color="inverse")
    c2.metric("ضغط الدم", f"{bp} mmHg", delta="طبيعي" if bp < 140 else "مرتفع", delta_color="inverse")
    c3.metric("نسبة الأكسجين", f"{spo2} %", delta="طبيعي" if spo2 > 94 else "منخفض", delta_color="normal")

    # الرسوم البيانية
    st.subheader("📈 منحنى المتابعة الزمني")
    fig = px.line(st.session_state.data_history, x='الوقت', y=['النبض', 'الضغط', 'الأكسجين'], 
                  title="تغير المؤشرات الحيوية", color_discrete_sequence=["#00ff00", "#ffff00", "#ff0000"])
    st.plotly_chart(fig, use_container_width=True)

    # التنبؤ بالذكاء الاصطناعي
    if status == "خطر":
        st.error(f"🚨 تنبيه ذكي: JAI يتنبأ باحتمالية خطر نوبة قلبية بناءً على المؤشرات الحالية!")
    else:
        st.success("✅ حالة المريض مستقرة وفقاً لتحليل الذكاء الاصطناعي.")

    if st.button("العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()
    
    time.sleep(5)
    st.rerun()

# صفحة التنبيهات
elif st.session_state.page == "alerts":
    st.title("⚠️ سجل التنبيهات الصحية")
    alerts = st.session_state.data_history[st.session_state.data_history['الحالة'] == "خطر"]
    
    if not alerts.empty:
        for index, row in alerts.iterrows():
            st.markdown(f"<div style='padding:10px; background-color:#ffcccc; border-radius:5px; margin-bottom:5px;'>🚨 تنبيه خطير عند الساعة {row['الوقت']}: نبض {row['النبض']} وضغط {row['الضغط']}</div>", unsafe_allow_html=True)
    else:
        st.write("لا توجد تنبيهات حالية. المريض بخير.")
        
    if st.button("العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()

st.markdown("---")
st.markdown("<center><b>JAI: مساعدك الذكي لرعاية مرضى القلب | تطوير جوري 👑</b></center>", unsafe_allow_html=True)
