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

    # Estimasi posisi tengah lingkaran
    center_x = bg.width // 2
    center_y = int(bg.height * 0.53)

    # Font besar default
    def get_font(size):
        try:
            return ImageFont.truetype("arial.ttf", size=size)
        except:
            return ImageFont.load_default()

    # Tulisan Harga Awal (Coret)
    harga_awal_text = format_rupiah(harga_awal)
    font_awal = get_font(40)
    harga_awal_size = draw.textlength(harga_awal_text, font=font_awal)
    draw.text((center_x - harga_awal_size // 2, center_y - 180), harga_awal_text, fill="black", font=font_awal)
    draw.line([(center_x - harga_awal_size // 2, center_y - 165), (center_x + harga_awal_size // 2, center_y - 165)], fill="black", width=3)

    # Harga Promo
    harga_promo_text = format_rupiah(harga_promo)
    font_promo = get_font(70)
    promo_width = draw.textlength(harga_promo_text, font=font_promo)
    draw.text((center_x - promo_width // 2, center_y - 120), harga_promo_text, fill="red", font=font_promo)

    # Diskon Utama
    diskon_utama_text = f"DISKON {diskon_utama}%"
    font_diskon = get_font(50)
    diskon_utama_width = draw.textlength(diskon_utama_text, font=font_diskon)
    draw.text((center_x - diskon_utama_width // 2, center_y - 40), diskon_utama_text, fill="red", font=font_diskon)

    # Diskon Member
    diskon_member_text = f"MEMBER +{diskon_member}%"
    font_member = get_font(45)
    member_width = draw.textlength(diskon_member_text, font=font_member)
    draw.text((center_x - member_width // 2, center_y + 20), diskon_member_text, fill="blue", font=font_member)

    # Logo di atas tengah
    bg.paste(logo, (center_x + 100, 80), mask=logo)

    # Preview
    st.image(bg, caption="Hasil POP", use_column_width=True)

    # Download
    img_bytes = io.BytesIO()
    bg.save(img_bytes, format="PNG")
    st.download_button("⬇️ Download POP", data=img_bytes.getvalue(), file_name="POP_MitraBangunan.png", mime="image/png")

elif generate:
    st.warning("Mohon upload background dan logo terlebih dahulu.")
