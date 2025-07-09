import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")

with st.sidebar:
    st.header("🛠️ Input Produk")
    nama_produk = st.text_input("Nama Produk", "GRANIT POLISHED 80X160")
    harga_awal = st.number_input("Harga Awal", min_value=0, value=269141)
    harga_promo = st.number_input("Harga Promo", min_value=0, value=248013)
    diskon_utama = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=3)

    uploaded_bg = st.file_uploader("Upload Background", type=["jpg", "png"])
    uploaded_logo = st.file_uploader("Upload Logo Produk", type=["jpg", "png"])

    generate = st.button("🎯 Generate POP")

def format_rupiah(nilai):
    return f"Rp{nilai:,}".replace(",", ".")

if generate and uploaded_bg and uploaded_logo:
    bg = Image.open(uploaded_bg).convert("RGBA")
    logo = Image.open(uploaded_logo).convert("RGBA")
    logo.thumbnail((200, 200))

    draw = ImageDraw.Draw(bg)

    # Gunakan font default
    font_title = ImageFont.load_default()
    
    # Cari titik tengah dari lingkaran
    center_x = bg.width // 2
    center_y = int(bg.height * 0.53)  # sedikit lebih atas dari tengah penuh

    # Tulis Harga Awal (coret)
    harga_awal_text = format_rupiah(harga_awal)
    font_awal = ImageFont.load_default()
    draw.text((center_x - 100, center_y - 140), harga_awal_text, fill="black", font=font_awal)
    draw.line([(center_x - 100, center_y - 135), (center_x + 80, center_y - 135)], fill="black", width=2)

    # Tulis Harga Promo (besar)
    harga_promo_text = format_rupiah(harga_promo)
    draw.text((center_x - 80, center_y - 100), harga_promo_text, fill="red", font=font_awal)

    # Tulis Diskon Utama
    diskon_utama_text = f"DISKON {diskon_utama}%"
    draw.text((center_x - 90, center_y - 60), diskon_utama_text, fill="red", font=font_awal)

    # Tulis Diskon Member
    diskon_member_text = f"MEMBER +{diskon_member}%"
    draw.text((center_x - 90, center_y - 40), diskon_member_text, fill="blue", font=font_awal)

    # Tempel logo di atas
    bg.paste(logo, (center_x + 50, 80), mask=logo)

    # Preview
    st.image(bg, caption="Hasil POP", use_column_width=True)

    # Download tombol
    img_bytes = io.BytesIO()
    bg.save(img_bytes, format="PNG")
    st.download_button("⬇️ Download POP", data=img_bytes.getvalue(), file_name="POP_MitraBangunan.png", mime="image/png")

elif generate:
    st.warning("Mohon upload background dan logo terlebih dahulu.")
