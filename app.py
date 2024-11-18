import streamlit as st
from fastai.vision.all import *
import plotly.express as px
import pathlib
from PIL import Image
import requests
from io import BytesIO

# PosixPath moslashuvi
pathlib.PosixPath = pathlib.Path

# Sarlavha
st.markdown("# :rainbow[Tasvirlarni aniqlash]")
st.write("Klasslar: Car, Airplane, Boat, Carnivore, Musical_instrument, Sports_equipment, Telephone, Office_supplies, Kitchen_utensil")

# Rasmni yuklash - fayl yoki link orqali
st.markdown("> :green[Rasmni ushbu qismga yuklang]")
file_upload = st.file_uploader("Rasm yuklash (avif, png, jpeg, gif, svg)", type=["avif", "png", "jpeg", "gif", "svg"])
url_input = st.text_input("Yoki rasmning URL manzilini kiriting")

# Rasm yuklash va ko'rsatish
if file_upload or url_input:
    if file_upload:
        img = PILImage.create(file_upload)
        st.image(file_upload, caption="Yuklangan rasm")
    else:
        try:
            response = requests.get(url_input)
            img = PILImage.create(BytesIO(response.content))
            st.image(img, caption="URL orqali yuklangan rasm")
        except Exception as e:
            st.error("Rasmni yuklashda xatolik! Iltimos, URLni tekshiring.")

    # Modelni yuklash
    model = load_learner('transport_model.pkl')

    # Bashorat qilish
    pred, pred_id, probs = model.predict(img)
    st.success(f"Bashorat: {pred}")
    st.info(f"Ehtimollik: {probs[pred_id] * 100:.1f}%")

    # Diagramma chizish
    fig = px.bar(x=probs * 100, y=model.dls.vocab, labels={'x': "Ehtimollik (%)", 'y': "Klasslar"}, orientation='h')
    st.plotly_chart(fig)

# Sidebar qo'shimchalar
st.sidebar.header("Qo'shimcha ma'lumotlar")
st.sidebar.write("Bizni ijtimoiy tarmoqlarda kuzatib boring:")
st.sidebar.markdown("[Telegram](https://t.me/ali_bek_003)")
st.sidebar.markdown("[Instagram](https://www.instagram.com/alib_ek0311/profilecard/?igsh=MWo5azN2MmM2cGs0aw==)")
st.sidebar.markdown("[Github](https://github.com/AlibekSerikbayev)")
st.write("Ushbu dastur Alibek Serikbayev tomonidan yaratildi")
