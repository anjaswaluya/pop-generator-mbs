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
    logo.thumbnail((250, 250))

    draw = ImageDraw.Draw(bg)

    center_x = bg.width // 2
    center_y = int(bg.height * 0.54)  # tengah lingkaran putih

    # Font fallback helper
    def get_font(size):
        try:
            return ImageFont.truetype("arial.ttf", size=size)
        except:
            return ImageFont.load_default()

    # Tulis nama produk (besar)
    font_produk = get_font(60)
    text_produk = nama_produk.upper()
    w = draw.textlength(text_produk, font=font_produk)
    draw.text((center_x - w / 2, center_y - 250), text_produk, fill="black", font=font_produk)

    # Harga coret
    font_awal = get_font(45)
    harga_awal_text = format_rupiah(harga_awal)
    w = draw.textlength(harga_awal_text, font=font_awal)
    draw.text((center_x - w / 2, center_y - 150), harga_awal_text, fill="gray", font=font_awal)
    draw.line([(center_x - w / 2, center_y - 140), (center_x + w / 2, center_y - 140)], fill="gray", width=4)

    # Harga promo besar
    font_promo = get_font(100)
    harga_promo_text = format_rupiah(harga_promo)
    w = draw.textlength(harga_promo_text, font=font_promo)
    draw.text((center_x - w / 2, center_y - 60), harga_promo_text, fill="red", font=font_promo)

    # Diskon Utama
    font_diskon = get_font(65)
    diskon_text = f"DISKON {diskon_utama}%"
    w = draw.textlength(diskon_text, font=font_diskon)
    draw.text((center_x - w / 2, center_y + 70), diskon_text, fill="red", font=font_diskon)

    # Diskon Member
    font_member = get_font(55)
    member_text = f"MEMBER +{diskon_member}%"
    w = draw.textlength(member_text, font=font_member)
    draw.text((center_x - w / 2, center_y + 140), member_text, fill="blue", font=font_member)

    # Logo pojok kanan atas
    bg.paste(logo, (center_x + 100, 80), mask=logo)

    # Tampilkan & download
    st.image(bg, caption="Hasil POP", use_column_width=True)
    img_bytes = io.BytesIO()
    bg.save(img_bytes, format="PNG")
    st.download_button("⬇️ Download POP", data=img_bytes.getvalue(), file_name="POP_MitraBangunan.png", mime="image/png")

elif generate:
    st.warning("Mohon upload background dan logo terlebih dahulu.")
