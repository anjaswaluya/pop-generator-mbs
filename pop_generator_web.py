import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")

with st.sidebar:
    st.header("🛠️ Input Produk")
    nama_produk   = st.text_input("Nama Produk", "TRISENSA CERAMICS 80X80")
    harga_awal    = st.number_input("Harga Awal", min_value=0, value=269401)
    harga_promo   = st.number_input("Harga Promo", min_value=0, value=249801)
    diskon_utama  = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member = st.number_input("Diskon Member (%)", min_value=0, value=3)
    bg_file       = st.file_uploader("Upload Background", type=["jpg","jpeg","png"])
    logo_file     = st.file_uploader("Upload Logo (PNG)", type=["png"])
    go            = st.button("🎯 Generate POP")

def format_rp(x):
    return f"Rp{x:,.0f}".replace(",", ".")

def load_font(sz):
    try:
        return ImageFont.truetype("arial.ttf", sz)
    except:
        return ImageFont.load_default()

if go and bg_file:
    bg = Image.open(bg_file).convert("RGBA")
    W,H = bg.size
    draw = ImageDraw.Draw(bg)
    cx,cy = W//2, int(H*0.55)

    # Logo pojok kanan atas
    if logo_file:
        logo = Image.open(logo_file).convert("RGBA")
        logo.thumbnail((180,180))
        bg.paste(logo, (W-logo.width-40, 40), logo)

    # Fonts
    f_prod = load_font(60)
    f_small= load_font(40)
    f_big  = load_font(100)
    f_num  = load_font(80)
    f_lbl  = load_font(30)

    # Helper center text
    def center_text(text, font, y, fill):
        w,h = font.getsize(text)
        draw.text((cx - w//2, y), text, font=font, fill=fill)

    # 1) Produk
    center_text(nama_produk, f_prod, cy-260, "black")

    # 2) Harga awal (coret)
    t0 = format_rp(harga_awal)
    w0,_ = f_small.getsize(t0)
    draw.text((cx - w0//2, cy-180), t0, font=f_small, fill="gray")
    draw.line([(cx - w0//2, cy-160),(cx + w0//2, cy-160)], fill="gray", width=4)

    # 3) Harga promo
    t1 = format_rp(harga_promo)
    center_text(t1, f_big, cy-90, "red")

    # 4) Diskon Utama (lingkaran merah)
    r,dx,dy = 120, -50, 20
    draw.ellipse([cx+dx-r, cy+dy-r, cx+dx+r, cy+dy+r], fill="red")
    txt = f"{diskon_utama}%"
    center_text(txt, f_num, cy+dy - f_num.getsize(txt)[1]//2, "white")
    lbl="DISKON"
    center_text(lbl, f_lbl, cy+dy + r - f_lbl.getsize(lbl)[1] - 10, "white")

    # 5) Diskon Member (lingkaran biru)
    r2,dx2,dy2 = 100, 50, 30
    draw.ellipse([cx+dx2-r2, cy+dy2-r2, cx+dx2+r2, cy+dy2+r2], fill="blue")
    txt2 = f"+{diskon_member}%"
    center_text(txt2, f_num, cy+dy2 - f_num.getsize(txt2)[1]//2, "white")
    lbl2="MEMBER"
    center_text(lbl2, f_lbl, cy+dy2 + r2 - f_lbl.getsize(lbl2)[1] - 10, "white")

    # Tampilkan + Download
    st.image(bg, use_column_width=True)
    buf = io.BytesIO(); bg.save(buf,"PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP_MitraBangunan.png", "image/png")
else:
    st.info("Upload background dan klik Generate POP.")
