import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Demo Data Dashboard", page_icon="📊", layout="wide")

st.title("📊 Demo Data Dashboard")
st.caption("Tải CSV/Excel lên để xem KPI, biểu đồ và dữ liệu. Dữ liệu mẫu có sẵn để bạn thử ngay.")

@st.cache_data
def load_sample():
    return pd.DataFrame({
        "Ngày": pd.date_range("2026-01-01", periods=12, freq="MS"),
        "Danh mục": ["SEO", "Content", "Technical", "SEO", "Content", "Technical",
                     "SEO", "Content", "Technical", "SEO", "Content", "Technical"],
        "Chiến dịch": ["Từ khóa A", "Bài viết B", "Audit C", "Từ khóa D", "Bài viết E", "Audit F",
                       "Từ khóa G", "Bài viết H", "Audit I", "Từ khóa J", "Bài viết K", "Audit L"],
        "Lượt truy cập": [1200, 900, 700, 1500, 1100, 850, 1800, 1300, 950, 2100, 1550, 1200],
        "Chuyển đổi": [24, 18, 12, 31, 22, 15, 38, 27, 19, 45, 32, 24],
        "Chi phí": [300000, 180000, 120000, 350000, 210000, 130000,
                    390000, 230000, 140000, 420000, 250000, 160000]
    })

def normalize_columns(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df

with st.sidebar:
    st.header("⚙️ Dữ liệu")
    uploaded = st.file_uploader("Tải file CSV hoặc Excel", type=["csv", "xlsx"])
    st.caption("File cần có các cột: Ngày, Danh mục, Lượt truy cập, Chuyển đổi, Chi phí.")
    use_sample = st.toggle("Dùng dữ liệu mẫu", value=uploaded is None)

if uploaded is not None:
    try:
        if uploaded.name.lower().endswith(".csv"):
            data = pd.read_csv(uploaded)
        else:
            data = pd.read_excel(uploaded)
        data = normalize_columns(data)
        source_name = uploaded.name
    except Exception as e:
        st.error(f"Không đọc được file: {e}")
        st.stop()
elif use_sample:
    data = load_sample()
    source_name = "Dữ liệu mẫu"
else:
    st.info("Hãy tải file CSV/Excel ở thanh bên trái hoặc bật dữ liệu mẫu.")
    st.stop()

required = ["Ngày", "Danh mục", "Lượt truy cập", "Chuyển đổi", "Chi phí"]
missing = [c for c in required if c not in data.columns]
if missing:
    st.error("File thiếu cột bắt buộc: " + ", ".join(missing))
    st.write("Các cột hiện có:", list(data.columns))
    st.stop()

data["Ngày"] = pd.to_datetime(data["Ngày"], errors="coerce")
for col in ["Lượt truy cập", "Chuyển đổi", "Chi phí"]:
    data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
data = data.dropna(subset=["Ngày"])

if data.empty:
    st.warning("Không có dòng dữ liệu hợp lệ sau khi đọc file.")
    st.stop()

with st.sidebar:
    st.divider()
    categories = sorted(data["Danh mục"].dropna().astype(str).unique().tolist())
    selected = st.multiselect("Lọc danh mục", categories, default=categories)
    min_date = data["Ngày"].min().date()
    max_date = data["Ngày"].max().date()
    date_range = st.date_input("Khoảng ngày", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = data[data["Danh mục"].astype(str).isin(selected)].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[(filtered["Ngày"] >= start) & (filtered["Ngày"] <= end)]

st.caption(f"Nguồn dữ liệu: **{source_name}** · {len(filtered):,} dòng sau lọc")

visits = int(filtered["Lượt truy cập"].sum())
conversions = int(filtered["Chuyển đổi"].sum())
cost = float(filtered["Chi phí"].sum())
rate = conversions / visits * 100 if visits else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Lượt truy cập", f"{visits:,}")
c2.metric("Chuyển đổi", f"{conversions:,}")
c3.metric("Tỷ lệ chuyển đổi", f"{rate:.2f}%")
c4.metric("Tổng chi phí", f"{cost:,.0f} đ")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Lượt truy cập theo thời gian")
    trend = filtered.groupby(pd.Grouper(key="Ngày", freq="MS"), as_index=False)["Lượt truy cập"].sum()
    fig = px.line(trend, x="Ngày", y="Lượt truy cập", markers=True)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Hiệu quả theo danh mục")
    by_cat = filtered.groupby("Danh mục", as_index=False)[["Lượt truy cập", "Chuyển đổi"]].sum()
    fig2 = px.bar(by_cat, x="Danh mục", y=["Lượt truy cập", "Chuyển đổi"], barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📋 Bảng dữ liệu")
st.dataframe(filtered.sort_values("Ngày", ascending=False), use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ Tải dữ liệu sau lọc (CSV)", data=csv, file_name="dashboard_data_export.csv", mime="text/csv")

with st.expander("Hướng dẫn định dạng file tải lên"):
    st.write("Tên cột cần đúng như sau:")
    st.code("Ngày,Danh mục,Lượt truy cập,Chuyển đổi,Chi phí")
    st.write("Ví dụ: 2026-01-01,SEO,1200,24,300000")
