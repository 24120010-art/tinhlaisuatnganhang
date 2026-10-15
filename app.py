import datetime
from google import genai
import streamlit as st
st.image("anh 1.webp")
# Thiết lập giao diện trang
st.set_page_config(
    page_title="Hệ Thống Tiết Kiệm & AI Tích Hợp", page_icon="🏦", layout="centered"
)

st.title("🏦 Ứng Dụng Tính Lãi Ngân Hàng & Chuyên Gia AI")
st.markdown(
    "Nhập thông tin tiết kiệm bên dưới. Hệ thống sẽ tính toán, xuất hóa đơn"
    " và tự động gửi phân tích từ Chuyên gia AI!"
)
st.markdown("---")

# Thanh bên (Sidebar) để nhập API Key của AI
with st.sidebar:
  st.subheader("⚙️ Cấu Hình AI")
  api_key = st.text_input(
      "Nhập Google Gemini API Key:", type="password", key="sidebar_api_key"
  )
  st.markdown(
      "*(Khóa này giúp AI tự động đọc kết quả và phân tích khoản gửi của bạn)*"
  )

# Dữ liệu biểu lãi suất các ngân hàng (%/năm)
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

# Khu vực nhập liệu giao dịch chung
st.subheader("📝 Nhập Thông Tin Gửi Tiết Kiệm")

col1, col2 = st.columns(2)
with col1:
  customer_name = st.text_input(
      "Họ và tên khách hàng:", placeholder="Ví dụ: Nguyễn Văn A"
  )
  selected_bank = st.selectbox(
      "Chọn Ngân Hàng:", list(BANK_INTEREST_RATES.keys())
  )
with col2:
  selected_term_name = st.selectbox("Chọn kỳ hạn gửi:", list(term_options.keys()))
  months = term_options[selected_term_name]

# Tự động đồng bộ lãi suất khi đổi ngân hàng hoặc kỳ hạn
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

col3, col4 = st.columns(2)
with col3:
  annual_rate = st.number_input(
      f"Lãi suất (%/năm) tại {selected_bank}:",
      min_value=0.1,
      max_value=30.0,
      value=st.session_state["rate_input"],
      step=0.1,
      key="rate_input",
  )
  principal = st.number_input(
      "Số tiền gửi (VNĐ):",
      min_value=1_000_000,
      step=1_000_000,
      value=50_000_000,
      format="%d",
  )
with col4:
  interest_type = st.radio("Chọn hình thức tính lãi:", ("Lãi đơn", "Lãi kép"))

# Nút tính toán chung
if st.button("🚀 Tính Toán, Xuất Hóa Đơn & Nhận Phân Tích AI", type="primary"):
  if not customer_name.strip():
    st.warning("⚠️ Vui lòng nhập họ và tên khách hàng trước khi tiếp tục!")
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

    # Tự động gọi AI phân tích dựa trên thông tin vừa nhập
    if api_key:
      try:
        client = genai.Client(api_key=api_key)
        prompt = (
            f"Khách hàng {customer_name} gửi tiết kiệm {principal:,.0f} VNĐ"
            f" tại ngân hàng {selected_bank} với kỳ hạn {selected_term_name}"
            f" ({months} tháng), lãi suất {annual_rate}%/năm theo hình thức"
            f" {interest_type}. Tổng lãi dự kiến là {total_interest:,.0f} VNĐ,"
            f" tổng nhận cuối kỳ là {final_amount:,.0f} VNĐ. Hãy đưa ra lời"
            f" khuyên tài chính ngắn gọn, chuyên nghiệp và đánh giá phương án"
            f" gửi này bằng tiếng Việt."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        st.session_state["ai_advice"] = response.text
      except Exception as e:
        st.session_state["ai_advice"] = (
            f"Không thể kết nối tới AI để phân tích: {e}"
        )
    else:
      st.session_state["ai_advice"] = (
          "⚠️ Bạn chưa nhập API Key ở thanh bên (Sidebar). Hãy nhập để nhận"
          " phân tích tự động từ Chuyên gia AI!"
      )

# Hiển thị kết quả, hóa đơn và phân tích AI trên cùng một dòng chảy trang web
if st.session_state.get("calculated", False):
  st.markdown("---")
  st.subheader("📊 Kết Quả Tính Toán")

  res_col1, res_col2 = st.columns(2)
  with res_col1:
    st.metric(
        label="Tổng Tiền Lãi Dự Kiến",
        value=f"{st.session_state['total_interest']:,.0f} VNĐ",
    )
  with res_col2:
    st.metric(
        label="Tổng Số Tiền Nhận Cuối Kỳ",
        value=f"{st.session_state['final_amount']:,.0f} VNĐ",
    )

  st.markdown("---")
  st.subheader("🧾 Hóa Đơn Giao Dịch Gửi Tiết Kiệm")

  # Hóa đơn thanh toán
  with st.container(border=True):
    st.markdown(
        f"### 🏦 HỆ THỐNG NGÂN HÀNG: {st.session_state['bank'].upper()}"
    )
    st.markdown(f"**Thời gian giao dịch:** {st.session_state['date']}")
    st.markdown("---")
    st.markdown(
        f"- **Họ tên khách hàng:** `{st.session_state['customer_name']}`"
    )
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
        f"Tạo sổ thành công cho **{st.session_state['customer_name']}** tại"
        f" **{st.session_state['bank']}**!"
    )

  # Phần Phân tích AI tự động hiển thị ngay dưới hóa đơn
  st.markdown("---")
  st.subheader("🤖 Phân Tích & Tư Vấn Từ Chuyên Gia AI")
  with st.chat_message("assistant"):
    st.markdown(st.session_state.get("ai_advice", "Chưa có phân tích."))
