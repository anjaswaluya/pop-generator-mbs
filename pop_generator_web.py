import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")

# Sidebar Input
with st.sidebar:
    st.header("🛠️ Input Produk")
    nama_produk = st.text_input("Nama Produk", "GRANIT POLISHED 80X160")
    harga_awal   = st.number_input("Harga Awal", min_value=0, value=269141)
    harga_promo  = st.number_input("Harga Promo", min_value=0, value=248013)
    diskon_utama = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member= st.number_input("Diskon Member (%)", min_value=0, value=3)
    bg_file      = st.file_uploader("Upload Background", type=["jpg","jpeg","png"])
    logo_file    = st.file_uploader("Upload Logo", type=["png","jpg","jpeg"])
    ok           = st.button("🎯 Generate POP")

# Rupiah formatter
def format_rp(x):
    return f"Rp{x:,.0f}".replace(",", ".")

# Fallback font loader
def load_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

if ok and bg_file:
    bg = Image.open(bg_file).convert("RGBA")
    W, H = bg.size
    draw = ImageDraw.Draw(bg)

    # center of white circle (manual tune if perlu)
    cx, cy = W//2, int(H*0.55)

    # Draw Logo
    if logo_file:
        logo = Image.open(logo_file).convert("RGBA")
        logo.thumbnail((180,180))
        bg.paste(logo, (W - logo.width - 40, 40), logo)

    # Text sizes
    f_prod  = load_font(60)
    f_price_small = load_font(40)
    f_price_big   = load_font(100)
    f_disc_num    = load_font(80)
    f_disc_lbl    = load_font(30)

    # 1) Nama Produk
    w,h = draw.textsize(nama_produk, font=f_prod)
    draw.text((cx - w//2, cy - 260), nama_produk, font=f_prod, fill="black")

    # 2) Harga Awal (coret)
    t_awal = format_rp(harga_awal)
    w,h = draw.textsize(t_awal, font=f_price_small)
    draw.text((cx - w//2, cy - 180), t_awal, font=f_price_small, fill="gray")
    draw.line([(cx - w//2, cy - 160),(cx + w//2, cy - 160)], fill="gray", width=4)

    # 3) Harga Promo
    t_promo = format_rp(harga_promo)
    w,h = draw.textsize(t_promo, font=f_price_big)
    draw.text((cx - w//2, cy - 90), t_promo, font=f_price_big, fill="red")

    # 4) Lingkaran Diskon Utama
    radius = 120
    x0,y0 = cx - radius - 50, cy + 20 - radius
    x1,y1 = cx - 50 + radius, cy + 20 + radius
    draw.ellipse([x0,y0,x1,y1], fill="red")
    txt = f"{diskon_utama}%"
    w,h = draw.textsize(txt, font=f_disc_num)
    draw.text((cx - 50 - w//2, cy + 20 - h//2), txt, font=f_disc_num, fill="white")
    lbl = "DISKON"
    w2,h2 = draw.textsize(lbl, font=f_disc_lbl)
    draw.text((cx - 50 - w2//2, cy + 20 + radius - h2 - 10), lbl, font=f_disc_lbl, fill="white")

    # 5) Lingkaran Diskon Member
    radius2 = 100
    x0,y0 = cx + 50 - radius2, cy + 30 - radius2
    x1,y1 = cx + 50 + radius2, cy + 30 + radius2
    draw.ellipse([x0,y0,x1,y1], fill="blue")
    txt2 = f"+{diskon_member}%"
    w,h = draw.textsize(txt2, font=f_disc_num)
    draw.text((cx + 50 - w//2, cy + 30 - h//2), txt2, font=f_disc_num, fill="white")
    lbl2 = "MEMBER"
    w2,h2 = draw.textsize(lbl2, font=f_disc_lbl)
    draw.text((cx + 50 - w2//2, cy + 30 + radius2 - h2 - 10), lbl2, font=f_disc_lbl, fill="white")

    # Show & Download
    st.image(bg, use_column_width=True)
    buf = io.BytesIO(); bg.save(buf,"PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_MitraBangunan.png", "image/png")

else:
    st.info("Upload background dulu, lalu klik Generate POP.")
