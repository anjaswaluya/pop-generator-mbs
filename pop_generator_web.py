import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")

with st.sidebar:
    st.header("🛠️ Input Produk")
    nama_produk   = st.text_input("Nama Produk", "TRISENSA CERAMICS 80X80")
    harga_awal    = st.number_input("Harga Awal", min_value=0, value=269141)
    harga_promo   = st.number_input("Harga Promo", min_value=0, value=248013)
    diskon_utama  = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=3)
    bg_file       = st.file_uploader("Upload Background (JPG/PNG)", type=["jpg", "jpeg", "png"])
    logo_file     = st.file_uploader("Upload Logo Produk (PNG)", type=["png"])
    go            = st.button("🎯 Generate POP")

def format_rupiah(nilai):
    return f"Rp{nilai:,.0f}".replace(",", ".")

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def center_draw(draw, text, font, center_x, y, fill):
    # Mengukur teks pakai bbox (lebih aman)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = center_x - text_width // 2
    draw.text((x, y), text, font=font, fill=fill)

if go and bg_file:
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)
    cx, cy = W // 2, int(H * 0.55)

    # Font
    f_prod = get_font(60)
    f_price = get_font(100)
    f_disc = get_font(80)
    f_label = get_font(30)
    f_strike = get_font(40)

    # Logo pojok kanan atas
    if logo_file:
        logo = Image.open(logo_file).convert("RGBA")
        logo.thumbnail((180,180))
        bg.paste(logo, (W - logo.width - 40, 40), logo)

    # Nama produk
    center_draw(draw, nama_produk, f_prod, cx, cy - 260, "black")

    # Harga awal (coret)
    text_awal = format_rupiah(harga_awal)
    bbox = draw.textbbox((0, 0), text_awal, font=f_strike)
    tw = bbox[2] - bbox[0]
    tx = cx - tw // 2
    ty = cy - 180
    draw.text((tx, ty), text_awal, font=f_strike, fill="gray")
    draw.line([(tx, ty + 20), (tx + tw, ty + 20)], fill="gray", width=3)

    # Harga promo
    center_draw(draw, format_rupiah(harga_promo), f_price, cx, cy - 90, "red")

    # Lingkaran diskon utama (merah)
    r = 130
    dx, dy = -100, 100
    draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill="red")
    center_draw(draw, f"{diskon_utama}%", f_disc, cx + dx, cy + dy - 20, "white")
    center_draw(draw, "DISKON", f_label, cx + dx, cy + dy + 60, "white")

    # Lingkaran diskon member (biru)
    r2 = 100
    dx2, dy2 = 100, 100
    draw.ellipse([cx + dx2 - r2, cy + dy2 - r2, cx + dx2 + r2, cy + dy2 + r2], fill="blue")
    center_draw(draw, f"+{diskon_member}%", f_disc, cx + dx2, cy + dy2 - 20, "white")
    center_draw(draw, "MEMBER", f_label, cx + dx2, cy + dy2 + 50, "white")

    # Output dan download
    st.image(bg, use_column_width=True)
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_MitraBangunan.png", "image/png")

else:
    st.info("Silakan upload background lalu klik Generate POP.")
