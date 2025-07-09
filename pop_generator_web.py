import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")

with st.sidebar:
    st.header("🧱 Input Produk")
    nama_produk = st.text_input("Nama Produk", "GRANIT POLISHED 80X80")
    harga_awal = st.number_input("Harga Awal", min_value=0, value=269401)
    harga_promo = st.number_input("Harga Promo", min_value=0, value=249801)
    diskon_utama = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=5)

    uploaded_bg = st.file_uploader("Upload Background", type=["jpg", "png"])
    uploaded_logo = st.file_uploader("Upload Logo Produk", type=["jpg", "png"])
    uploaded_font = st.file_uploader("Upload Font (TTF/OTF)", type=["ttf", "otf"])

    generate = st.button("✨ Generate POP")

def format_rupiah(nilai):
    return "Rp{:,.0f}".format(nilai).replace(",", ".")

if generate and uploaded_bg and uploaded_logo and uploaded_font:
    bg = Image.open(uploaded_bg).convert("RGBA")
    logo = Image.open(uploaded_logo).convert("RGBA")
    logo.thumbnail((200, 200))

    font_bytes = io.BytesIO(uploaded_font.read())
    font_judul = ImageFont.truetype(font_bytes, size=60)
    font_harga = ImageFont.truetype(font_bytes, size=50)
    font_diskon = ImageFont.truetype(font_bytes, size=42)
    font_label = ImageFont.truetype(font_bytes, size=36)

    draw = ImageDraw.Draw(bg)

    # Posisi teks di dalam lingkaran
    center_x = bg.width // 2
    start_y = 380
    spacing = 75

    draw.text((center_x, start_y), nama_produk, font=font_judul, anchor="mm", fill="black")
    draw.text((center_x, start_y + spacing), format_rupiah(harga_awal), font=font_label, anchor="mm", fill="gray")
    draw.text((center_x, start_y + spacing * 2), format_rupiah(harga_promo), font=font_harga, anchor="mm", fill="red")
    draw.text((center_x, start_y + spacing * 3), f"DISKON {diskon_utama}%", font=font_diskon, anchor="mm", fill="red")
    draw.text((center_x, start_y + spacing * 4), f"MEMBER {diskon_member}%", font=font_diskon, anchor="mm", fill="blue")

    # Tempel logo di kanan atas
    bg.paste(logo, (bg.width - logo.width - 60, 40), logo)

    st.image(bg, caption="Hasil POP", use_column_width=True)

    img_bytes = io.BytesIO()
    bg.save(img_bytes, format="PNG")
    st.download_button("📥 Download POP", data=img_bytes.getvalue(), file_name="POP_MitraBangunan.png", mime="image/png")

elif generate:
    st.warning("Mohon upload background, logo, dan font terlebih dahulu.")
