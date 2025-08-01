
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")
st.title("🔧 POP Generator - Mitra Bangunan")

with st.sidebar:
    st.header("📷 Input Produk")
    nama_produk = st.text_input("Nama Produk", "GRANIT POLISHED 80X160")
    harga_awal = st.number_input("Harga Awal", min_value=0, value=269141)
    harga_promo = st.number_input("Harga Promo", min_value=0, value=248013)
    diskon_utama = st.number_input("Diskon Utama (%)", min_value=0, max_value=100, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, max_value=100, value=3)

    uploaded_bg = st.file_uploader("Upload Background", type=["jpg", "jpeg", "png"])
    uploaded_logo = st.file_uploader("Upload Logo Produk", type=["jpg", "jpeg", "png"])
    font_file = st.file_uploader("Upload Font (TTF/OTF)", type=["ttf", "otf"])

    if st.button("🚀 Generate POP"):
        if uploaded_bg and uploaded_logo and font_file:
            # Baca semua resource dari upload
            bg = Image.open(uploaded_bg).convert("RGBA")
            logo = Image.open(uploaded_logo).convert("RGBA")
            logo.thumbnail((250, 250))

            font_bytes = BytesIO(font_file.read())

            font_judul = ImageFont.truetype(font_bytes, size=95)
            font_harga = ImageFont.truetype(BytesIO(font_bytes.getvalue()), size=85)
            font_promo = ImageFont.truetype(BytesIO(font_bytes.getvalue()), size=85)
            font_diskon = ImageFont.truetype(BytesIO(font_bytes.getvalue()), size=65)
            font_diskon_member = ImageFont.truetype(BytesIO(font_bytes.getvalue()), size=65)

            draw = ImageDraw.Draw(bg)
            logo_position = (bg.width - logo.width - 60, 40)
            bg.paste(logo, logo_position, logo)

            draw.text((130, 360), nama_produk, font=font_judul, fill="black")
            draw.text((130, 600), f"Rp. {harga_awal:,.0f}".replace(",", "."), font=font_harga, fill="gray")
            draw.line([(130, 660), (130 + 420, 660)], fill="gray", width=5)
            draw.text((130, 700), f"Rp. {harga_promo:,.0f}".replace(",", "."), font=font_promo, fill="red")
            draw.text((130, 840), f"DISKON {diskon_utama}%", font=font_diskon, fill="red")
            draw.text((500, 840), f"MEMBER +{diskon_member}%", font=font_diskon_member, fill="blue")

            # Preview hasil
            st.subheader("📸 Hasil POP")
            img_bytes = BytesIO()
            bg.save(img_bytes, format="PNG")
            st.image(img_bytes.getvalue(), caption="POP Mitra Bangunan", use_column_width=True)
            st.download_button("📥 Download PNG", data=img_bytes.getvalue(), file_name="POP_MitraBangunan.png", mime="image/png")

        else:
            st.warning("Mohon upload background, logo, dan font terlebih dahulu.")
