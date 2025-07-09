import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="POP Generator Mitra Bangunan", layout="centered")

with st.sidebar:
    st.header("🛠️ Input Produk")
    nama_produk    = st.text_input("Nama Produk", "TRISENSA CERAMICS 80X80")
    harga_awal     = st.number_input("Harga Awal", min_value=0, value=269401)
    harga_promo    = st.number_input("Harga Promo", min_value=0, value=249801)
    diskon_utama   = st.number_input("Diskon Utama (%)", min_value=0, value=5)
    diskon_member  = st.number_input("Diskon Member (%)", min_value=0, value=3)
    bg_file        = st.file_uploader("Upload Background", type=["jpg","jpeg","png"])
    logo_file      = st.file_uploader("Upload Logo", type=["png","jpg","jpeg"])
    go             = st.button("🎯 Generate POP")

def format_rp(x):
    return f"Rp{x:,.0f}".replace(",", ".")

def load_font(sz):
    try: return ImageFont.truetype("arial.ttf", sz)
    except: return ImageFont.load_default()

if go and bg_file:
    bg = Image.open(bg_file).convert("RGBA")
    W,H = bg.size
    draw = ImageDraw.Draw(bg)
    cx, cy = W//2, int(H*0.55)

    # Logo
    if logo_file:
        logo = Image.open(logo_file).convert("RGBA")
        logo.thumbnail((180,180))
        bg.paste(logo, (W-logo.width-40,40), logo)

    # Fonts
    f_prod = load_font(60)
    f_small= load_font(40)
    f_big  = load_font(100)
    f_num  = load_font(80)
    f_lbl  = load_font(30)

    # Produk
    w,h = draw.textsize(nama_produk, f_prod)
    draw.text((cx-w//2, cy-260), nama_produk, font=f_prod, fill="black")

    # Harga awal (coret)
    t0 = format_rp(harga_awal)
    w,h= draw.textsize(t0, f_small)
    draw.text((cx-w//2, cy-180), t0, font=f_small, fill="gray")
    draw.line([(cx-w//2,cy-160),(cx+w//2,cy-160)], fill="gray", width=4)

    # Harga promo
    t1 = format_rp(harga_promo)
    w,h= draw.textsize(t1, f_big)
    draw.text((cx-w//2, cy-90), t1, font=f_big, fill="red")

    # Diskon utama circle
    r=120; dx=-50; dy=20
    draw.ellipse([cx+r*dx//abs(dx)-r, cy+dy-r, cx+dx+r, cy+dy+r], fill="red")
    txt=f"{diskon_utama}%"
    w,h=draw.textsize(txt,f_num)
    draw.text((cx+dx-w//2, cy+dy-h//2), txt, font=f_num, fill="white")
    lbl="DISKON"; w2,h2=draw.textsize(lbl,f_lbl)
    draw.text((cx+dx-w2//2, cy+dy+r-h2-10), lbl, font=f_lbl, fill="white")

    # Diskon member circle
    r2=100; dx2=50; dy2=30
    draw.ellipse([cx+dx2-r2, cy+dy2-r2, cx+dx2+r2, cy+dy2+r2], fill="blue")
    txt2=f"+{diskon_member}%"
    w,h=draw.textsize(txt2,f_num)
    draw.text((cx+dx2-w//2, cy+dy2-h//2), txt2, font=f_num, fill="white")
    lbl2="MEMBER"; w2,h2=draw.textsize(lbl2,f_lbl)
    draw.text((cx+dx2-w2//2, cy+dy2+r2-h2-10), lbl2, font=f_lbl, fill="white")

    # Show & download
    st.image(bg, use_column_width=True)
    buf=io.BytesIO(); bg.save(buf,"PNG")
    st.download_button("⬇️ Download POP", buf.getvalue(), "POP.png", "image/png")
else:
    st.info("Upload background & klik Generate POP.")
