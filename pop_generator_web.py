import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")

with st.sidebar:
    st.header("📦 Input Produk")
    nama_produk = st.text_input("Nama Produk", "GRANIT POLISHED 80X80")
    harga_awal = st.number_input("Harga Awal", min_value=0, value=269401)
    harga_promo = st.number_input("Harga Promo", min_value=0, value=249801)
    diskon_utama = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=5)

    uploaded_bg = st.file_uploader("Upload background", type=["jpg", "png"])
    uploaded_logo = st.file_uploader("Upload Logo Produk", type=["jpg", "png"])
    uploaded_font = st.file_uploader("Upload Font (TTF/OTF)", type=["ttf", "otf"])

    generate = st.button("⚡ Generate POP")

def format_rupiah(nilai):
    return f"Rp{nilai:,}".replace(",", ".")

if generate and uploaded_bg and uploaded_logo and uploaded_font:
    bg = Image.open(uploaded_bg).convert("RGBA")
    logo = Image.open(uploaded_logo).convert("RGBA")
    logo.thumbnail((250, 250))

    font_bytes = io.BytesIO(uploaded_font.read())
    font = ImageFont.truetype(font_bytes, size=85)

    draw = ImageDraw.Draw(bg)
    bg.paste(logo, (bg.width - logo.width - 60, 40), logo)

    draw.text((130, 60), nama_produk, font=font, fill="black")
    draw.text((130, 200), f"{format_rupiah(harga_awal)}", font=font, fill="gray")
    draw.text((130, 340), f"{format_rupiah(harga_promo)}", font=font, fill="red")
    draw.text((130, 480), f"DISKON {diskon_utama}%", font=font, fill="red")
    draw.text((130, 620), f"MEMBER {diskon_member}%", font=font, fill="blue")

    st.image(bg, caption="Hasil POP", use_column_width=True)

    img_bytes = io.BytesIO()
    bg.save(img_bytes, format="PNG")
    st.download_button("⬇️ Download PNG", data=img_bytes.getvalue(), file_name="POP_MitraBangunan.png", mime="image/png")

elif generate:
    st.warning("Mohon upload background, logo, dan font terlebih dahulu.")
