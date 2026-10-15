import datetime
import streamlit as st
st.image("anh 1.webp")
# Thiết lập giao diện trang
st.set_page_config(
    page_title="Tính Lãi Tiết Kiệm Đa Ngân Hàng", page_icon="🏦", layout="centered"
)

# Tiêu đề ứng dụng
st.title("🏦 Ứng Dụng Tính Lãi Tiết Kiệm Đa Ngân Hàng")
st.markdown(
    "Nhập thông tin khách hàng, chọn ngân hàng và kỳ hạn để tự động cập"
    " nhật lãi suất."
)
st.markdown("---")

# Dữ liệu biểu lãi suất tham khảo của các ngân hàng (%/năm)
BANK_INTEREST_RATES = {
    "Vietcombank": {1: 1.6, 3: 1.9, 6: 2.9, 9: 2.9, 12: 4.6, 24: 4.7, 36: 4.7},
    "BIDV": {1: 1.7, 3: 2.0, 6: 3.0, 9: 3.0, 12: 4.7, 24: 4.8, 36: 4.8},
    "Agribank": {1: 1.7, 3: 2.0, 6: 3.0, 9: 3.0, 12: 4.7, 24: 4.8, 36: 4.8},
    "VietinBank": {1: 1.7, 3: 2.0, 6: 3.0, 9: 3.0, 12: 4.7, 24: 4.8, 36: 4.8},
    "Techcombank": {1: 2.5, 3: 2.8, 6: 3.8, 9: 3.8, 12: 5.0, 24: 5.2, 36: 5.2},
    "MB Bank": {1: 2.3, 3: 2.6, 6: 3.6, 9: 3.8, 12: 5.1, 24: 5.4, 36: 5.4},
    "VPBank": {1: 2.4, 3: 2.7, 6: 3.7, 9: 3.9, 12: 5.2, 24: 5.5, 36: 5.5},
    "ACB": {1: 2.2, 3: 2.5, 6: 3.5, 9: 3.7, 12: 4.9, 24: 5.1, 36: 5.1},
    "TPBank": {1: 2.4, 3: 2.7, 6: 3.8, 9: 4.0, 12: 5.3, 24: 5.6, 36: 5.6},
}

term_options = {
    "1 Tháng": 1,
    "3 Tháng": 3,
    "6 Tháng": 6,
    "9 Tháng": 9,
    "12 Tháng": 12,
    "24 Tháng": 24,
    "36 Tháng": 36,
}

# Khu vực nhập liệu
st.subheader("📝 Thông Tin Giao Dịch")

# 1. Nhập họ tên khách hàng
customer_name = st.text_input(
    "Họ và tên khách hàng:",
    value="",
    placeholder="Ví dụ: Nguyễn Văn A",
)

# 2. Chọn Ngân Hàng
selected_bank = st.selectbox(
    "Chọn Ngân Hàng:", list(BANK_INTEREST_RATES.keys())
)

# 3. Chọn kỳ hạn gửi
selected_term_name = st.selectbox("Chọn kỳ hạn gửi:", list(term_options.keys()))
months = term_options[selected_term_name]

# Tự động cập nhật lãi suất khi đổi Ngân hàng hoặc Kỳ hạn
default_rate = BANK_INTEREST_RATES[selected_bank].get(months, 5.0)

if (
    "last_bank" not in st.session_state
    or st.session_state["last_bank"] != selected_bank
    or "last_term" not in st.session_state
    or st.session_state["last_term"] != selected_term_name
):
  st.session_state["rate_input"] = float(default_rate)
  st.session_state["last_bank"] = selected_bank
  st.session_state["last_term"] = selected_term_name

# 4. Lãi suất (%/năm) - Tự động thay đổi theo ngân hàng & kỳ hạn chọn (có thể sửa thủ công nếu muốn)
annual_rate = st.number_input(
    f"Lãi suất (%/năm) tại {selected_bank} ({selected_term_name}):",
    min_value=0.1,
    max_value=30.0,
    value=st.session_state["rate_input"],
    step=0.1,
    key="rate_input",
)

# 5. Nhập số tiền gửi
principal = st.number_input(
    "Nhập số tiền gửi (VNĐ):",
    min_value=1_000_000,
    step=1_000_000,
    value=50_000_000,
    format="%d",
)

# 6. Chọn hình thức tính lãi
interest_type = st.radio("Chọn hình thức tính lãi:", ("Lãi đơn", "Lãi kép"))

# Nút tính toán
submit_btn = st.button("Tính Toán & Xem Hóa Đơn", type="primary")

# Xử lý tính toán khi bấm nút
if submit_btn:
  if not customer_name.strip():
    st.warning("⚠️ Vui lòng nhập họ và tên khách hàng trước khi tính toán!")
  else:
    st.session_state["calculated"] = True
    st.session_state["customer_name"] = customer_name
    st.session_state["bank"] = selected_bank
    st.session_state["principal"] = principal
    st.session_state["interest_type"] = interest_type
    st.session_state["term_name"] = selected_term_name
    st.session_state["months"] = months
    st.session_state["annual_rate"] = annual_rate

    # Tính toán tiền lãi
    t = months / 12
    r = annual_rate / 100

    if interest_type == "Lãi đơn":
      total_interest = principal * r * t
      final_amount = principal + total_interest
    else:
      final_amount = principal * ((1 + (r / 12)) ** months)
      total_interest = final_amount - principal

    st.session_state["total_interest"] = total_interest
    st.session_state["final_amount"] = final_amount
    st.session_state["date"] = datetime.datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

# Hiển thị kết quả và Hóa đơn chi tiết
if st.session_state.get("calculated", False):
  st.markdown("---")
  st.subheader("📊 Kết Quả Tính Toán")

  col1, col2 = st.columns(2)
  with col1:
    st.metric(
        label="Tổng Tiền Lãi Dự Kiến",
        value=f"{st.session_state['total_interest']:,.0f} VNĐ",
    )
  with col2:
    st.metric(
        label="Tổng Số Tiền Nhận Cuối Kỳ",
        value=f"{st.session_state['final_amount']:,.0f} VNĐ",
    )

  st.markdown("---")
  st.subheader("🧾 Hóa Đơn Giao Dịch Gửi Tiết Kiệm")

  # Khu vực hiển thị hóa đơn thanh toán
  invoice_container = st.container(border=True)
  with invoice_container:
    st.markdown(
        f"### 🏦 HỆ THỐNG NGÂN HÀNG: {st.session_state['bank'].upper()}"
    )
    st.markdown(f"**Thời gian giao dịch:** {st.session_state['date']}")
    st.markdown("---")
    st.markdown(
        f"- **Họ tên khách hàng:** `{st.session_state['customer_name']}`"
    )
    st.markdown(
        f"- **Ngân hàng giao dịch:** `{st.session_state['bank']}`"
    )
    st.markdown(
        f"- **Số tiền gửi gốc:** `{st.session_state['principal']:,.0f} VNĐ`"
    )
    st.markdown(
        f"- **Hình thức tính lãi:** `{st.session_state['interest_type']}`"
    )
    st.markdown(f"- **Kỳ hạn gửi:** `{st.session_state['term_name']}`")
    st.markdown(
        f"- **Lãi suất áp dụng:** `{st.session_state['annual_rate']}%/năm`"
    )
    st.markdown(
        f"- **Tiền lãi dự kiến:** `{st.session_state['total_interest']:,.0f} VNĐ`"
    )
    st.markdown("---")
    st.markdown(
        f"### **Tổng số tiền nhận cuối kỳ:**"
        f" `{st.session_state['final_amount']:,.0f} VNĐ`"
    )
    st.success(
        f"Tạo sổ tiết kiệm điện tử thành công cho khách hàng"
        f" **{st.session_state['customer_name']}** tại"
        f" **{st.session_state['bank']}**!"
    )
