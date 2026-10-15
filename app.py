import datetime
import streamlit as st
st.image("anh 1.webp")
# Thiết lập giao diện trang
st.set_page_config(
    page_title="Tính Lãi Tiết Kiệm Theo Ngân Hàng", page_icon="🏦", layout="centered"
)

# Tiêu đề ứng dụng
st.title("🏦 Ứng Dụng Tính Lãi Tiết Kiệm Đa Ngân Hàng")
st.markdown(
    "Chọn ngân hàng, kỳ hạn và hình thức gửi để tính lãi chính xác và xuất"
    " hóa đơn."
)
st.markdown("---")

# Dữ liệu biểu lãi suất tham khảo của các ngân hàng lớn (%/năm)
# Cấu trúc: { "Tên Ngân Hàng": { số_tháng: lãi_suất } }
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

# Form nhập liệu
with st.form("savings_form"):
  st.subheader("📝 Thông Tin Gửi Tiết Kiệm")

  # 1. Chọn ngân hàng
  selected_bank = st.selectbox(
      "Chọn Ngân Hàng:", list(BANK_INTEREST_RATES.keys())
  )

  # 2. Nhập số tiền gửi
  principal = st.number_input(
      "Nhập số tiền gửi (VNĐ):",
      min_value=1_000_000,
      step=1_000_000,
      value=50_000_000,
      format="%d",
  )

  # 3. Chọn hình thức tính lãi
  interest_type = st.radio("Chọn hình thức tính lãi:", ("Lãi đơn", "Lãi kép"))

  # 4. Chọn kỳ hạn gửi
  term_options = {
      "1 Tháng": 1,
      "3 Tháng": 3,
      "6 Tháng": 6,
      "9 Tháng": 9,
      "12 Tháng": 12,
      "24 Tháng": 24,
      "36 Tháng": 36,
  }
  selected_term_name = st.selectbox("Chọn kỳ hạn gửi:", list(term_options.keys()))
  months = term_options[selected_term_name]

  # Lấy lãi suất mặc định từ biểu lãi suất của ngân hàng đã chọn tương ứng với kỳ hạn
  default_rate = BANK_INTEREST_RATES[selected_bank].get(months, 5.0)

  # 5. Lãi suất (%/năm) - Tự động điền theo ngân hàng, cho phép người dùng sửa đổi nếu cần
  annual_rate = st.number_input(
      f"Lãi suất (%/năm) tại {selected_bank} cho kỳ hạn {selected_term_name}:",
      min_value=0.1,
      max_value=30.0,
      value=float(default_rate),
      step=0.1,
  )

  # Nút submit form
  submit_btn = st.form_submit_button("Tính Toán & Xem Hóa Đơn")

# Xử lý tính toán khi người dùng bấm nút
if submit_btn:
  st.session_state["calculated"] = True
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
    # Công thức lãi đơn: Tiền lãi = P * r * t
    total_interest = principal * r * t
    final_amount = principal + total_interest
  else:
    # Công thức lãi kép theo tháng: A = P * (1 + r/12)^months
    final_amount = principal * ((1 + (r / 12)) ** months)
    total_interest = final_amount - principal

  st.session_state["total_interest"] = total_interest
  st.session_state["final_amount"] = final_amount
  st.session_state["date"] = datetime.datetime.now().strftime(
      "%d/%m/%Y %H:%M:%S"
  )

# Hiển thị kết quả và Hóa đơn nếu đã tính toán
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
    st.markdown(f"- **Ngân hàng giao dịch:** `{st.session_state['bank']}`")
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
        f"Tạo sổ tiết kiệm điện tử tại {st.session_state['bank']} thành công!"
    )
