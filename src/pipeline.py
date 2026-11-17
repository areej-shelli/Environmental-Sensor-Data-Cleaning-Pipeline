import sqlite3
import numpy as np
import pandas as pd

# ==========================================
# مشروع معالجة بيانات مستشعرات الطقس (IoT Telemetry)
# إعداد: أريج | Areej Alshelli
# الهدف: تنظيف قراءات الحرارة والرطوبة ومعالجة الفجوات
# ==========================================

print("-> جاري تحميل بيانات المستشعرات الخام...")

# بيانات افتراضية قادمة من المستشعر (تتضمن أخطاء واقعية: فجوة يوم 2 مارس، وقيمة شاذة 999.0)
raw_data = {
    "timestamp": [
        "2026-03-01 08:00:00",
        "2026-03-03 08:00:00",
        "2026-03-04 08:00:00",
        "2026-03-05 08:00:00",
        "2026-03-06 08:00:00",
    ],
    "temperature": [22.5, 23.0, 999.0, 21.8, 22.1],  # 999.0 هون خطأ فادح من المستشعر
    "humidity": [45.0, 46.5, 47.0, 44.2, 45.5],
}

df = pd.DataFrame(raw_data)
df["timestamp"] = pd.to_datetime(df["timestamp"])

print("\n[البيانات قبل التعديل]:")
print(df)
print("-" * 40)

# الخطوة 1: فحص واستبعاد القيم الشاذة للحرارة باستخدام طريقة IQR
q1 = df["temperature"].quantile(0.25)
q3 = df["temperature"].quantile(0.75)
iqr = q3 - q1

min_limit = q1 - 1.5 * iqr
max_limit = q3 + 1.5 * iqr

# تحويل القيمة الشاذة إلى NaN عشان نعرف نعالجها
df.loc[
    (df["temperature"] < min_limit) | (df["temperature"] > max_limit),
    "temperature",
] = np.nan

# الخطوة 2: ترتيب الجدول وسد الفجوات الزمنية (مثل يوم 2 مارس الناقص)
df = df.set_index("timestamp").resample("D").mean()

# تعبئة الفراغات بطريقة الاستيفاء (Interpolation) لحساب قيمة منطقية قريبة للواقع
df["temperature"] = df["temperature"].interpolate(method="linear")
df["humidity"] = df["humidity"].interpolate(method="linear")

df = df.reset_index()

print("\n[البيانات بعد التنظيف وملء الفجوات]:")
print(df)
print("-" * 40)

# الخطوة 3: تخزين البيانات في SQLite وتطبيق SQL Window Functions للحصول على المتوسط المتحرك
db_name = "weather_sensors.db"
conn = sqlite3.connect(db_name)

df.to_sql("sensor_logs", conn, if_exists="replace", index=False)

# استعلام SQL بيحسب المتوسط المتحرك لآخر 3 أيام عشان نغطي التذبذب
query = """
    SELECT 
        timestamp,
        temperature,
        humidity,
        AVG(temperature) OVER (
            ORDER BY timestamp 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS temp_rolling_avg
    FROM sensor_logs
"""

result_df = pd.read_sql(query, conn)
conn.close()

print("\n[النتائج النهائية مع المتوسط المتحرك عبر SQL]:")
print(result_df)

