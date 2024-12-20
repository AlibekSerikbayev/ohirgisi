import streamlit as st
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from fastai.vision.all import *
import plotly.express as px
import pathlib
from PIL import Image
import requests
from io import BytesIO

# PosixPath moslashuvi
pathlib.PosixPath = pathlib.Path

# Foydalanuvchi ma'lumotlar bazasi
users = {
    "admin": {
        "password": "password123",
        "face_embedding": np.random.rand(128)  # Oldindan olingan yuz vektori
    }
}

# Funksiya: Login va parolni tekshirish
def authenticate(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        return True
    return False

# Funksiya: Kamera orqali tasvir olish (kameraga ruxsat so‘raydi)
def capture_face_with_permission():
    st.write("Face ID uchun kameradan foydalanishga ruxsat bering...")

    # Kamera ochilishi va ishlashini tekshirish
    video_capture = cv2.VideoCapture(0)  # Web-kamerani ochish
    if not video_capture.isOpened():
        st.error("Kamera yoqilmadi. Iltimos, kameradan foydalanishga ruxsat bering yoki kamerani ulang.")
        return None

    st.info("Tasvir olinmoqda. Kamera oldida turing...")

    # Tasvir olish
    ret, frame = video_capture.read()
    if ret:
        video_capture.release()
        cv2.destroyAllWindows()
        return frame
    else:
        st.error("Tasvirni olishda muammo yuz berdi. Iltimos, qayta urinib ko'ring.")
        return None

# Funksiya: Face ID tasdiqlash
def verify_face(captured_image, stored_embedding):
    resized = cv2.resize(captured_image, (224, 224)).flatten()
    similarity = cosine_similarity([stored_embedding], [resized])[0][0]
    return similarity > 0.8  # Moslik chegarasi

# Streamlit sahifasi
def main():
    st.set_page_config(page_title="Tasvirlarni aniqlash", layout="wide")
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # Login bosqichi
    if not st.session_state.authenticated:
        st.title("Login sahifasi")
        username = st.text_input("Foydalanuvchi nomi")
        password = st.text_input("Parol", type="password")

        if st.button("Kirish"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login muvaffaqiyatli! Endi Face ID tasdiqlash.")
            else:
                st.error("Login yoki parol noto‘g‘ri.")
        st.stop()

    # Face ID bosqichi
    st.title("Face ID tasdiqlash")
    captured_image = None

    if st.button("Face ID olish"):
        # Kamera orqali tasvir olish
        captured_image = capture_face_with_permission()

        if captured_image is not None:
            st.image(captured_image, caption="Olingan tasvir", use_column_width=True)
            
            user_embedding = users[st.session_state.username]["face_embedding"]
            if verify_face(captured_image, user_embedding):
                st.success("Face ID muvaffaqiyatli tasdiqlandi!")
                st.session_state.face_authenticated = True
            else:
                st.error("Face ID tasdiqlanmadi. Iltimos, qayta urinib ko‘ring.")
        st.stop()

    # Asosiy kod
    st.markdown("# :rainbow[Tasvirlarni aniqlash]")
    st.write("Klasslar: Car, Airplane, Boat, Carnivore, Musical_instrument, Sports_equipment, Telephone, Office_supplies, Kitchen_utensil")

    # Rasmni yuklash - fayl yoki link orqali
    st.markdown("> :green[Rasmni ushbu qismga yuklang]")
    file_upload = st.file_uploader("Rasm yuklash (avif, png, jpeg, gif, svg)", type=["avif", "png", "jpeg", "gif", "svg"])
    url_input = st.text_input("Yoki rasmning URL manzilini kiriting")

    # Modelni yuklash
    try:
        model = load_learner('transport_model.pkl')
    except Exception as e:
        st.error(f"Modelni yuklashda xatolik: {e}")
        model = None

    # Rasm yuklash va ko'rsatish
    if file_upload or url_input:
        try:
            if file_upload:
                img = PILImage.create(file_upload)
                st.image(file_upload, caption="Yuklangan rasm")
            else:
                response = requests.get(url_input)
                img = PILImage.create(BytesIO(response.content))
                st.image(img, caption="URL orqali yuklangan rasm")
            
            if isinstance(img, PILImage) and model is not None:
                pred, pred_id, probs = model.predict(img)
                st.success(f"Bashorat: {pred}")
                st.info(f"Ehtimollik: {probs[pred_id] * 100:.1f}%")
                
                # Diagramma chizish
                fig = px.bar(x=probs * 100, y=model.dls.vocab, labels={'x': "Ehtimollik (%)", 'y': "Klasslar"}, orientation='h')
                st.plotly_chart(fig)
            else:
                st.error("Tasvirni yoki modelni yuklashda muammo bor.")
        except Exception as e:
            st.error(f"Bashorat qilishda xatolik: {e}")

    # Sidebar qo'shimchalar
    st.sidebar.header("Qo'shimcha ma'lumotlar")
    st.sidebar.write("Bizni ijtimoiy tarmoqlarda kuzatib boring:")
    st.sidebar.markdown("[Telegram](https://t.me/ali_bek_003)")
    st.sidebar.markdown("[Instagram](https://www.instagram.com/alib_ek0311/profilecard/?igsh=MWo5azN2MmM2cGs0aw==)")
    st.sidebar.markdown("[Github](https://github.com/AlibekSerikbayev)")
    st.write("Ushbu dastur Alibek Serikbayev tomonidan yaratildi")

if __name__ == "__main__":
    main()












# import streamlit as st
# from fastai.vision.all import *
# import plotly.express as px
# import pathlib
# from PIL import Image
# import requests
# from io import BytesIO

# # PosixPath moslashuvi
# pathlib.PosixPath = pathlib.Path

# # Sarlavha
# st.markdown("# :rainbow[Tasvirlarni aniqlash]")
# st.write("Klasslar: Car, Airplane, Boat, Carnivore, Musical_instrument, Sports_equipment, Telephone, Office_supplies, Kitchen_utensil")

# # Rasmni yuklash - fayl yoki link orqali
# st.markdown("> :green[Rasmni ushbu qismga yuklang]")
# file_upload = st.file_uploader("Rasm yuklash (avif, png, jpeg, gif, svg)", type=["avif", "png", "jpeg", "gif", "svg"])
# url_input = st.text_input("Yoki rasmning URL manzilini kiriting")

# # Modelni yuklash
# try:
#     model = load_learner('transport_model.pkl')
# except Exception as e:
#     st.error(f"Modelni yuklashda xatolik: {e}")
#     model = None

# # Rasm yuklash va ko'rsatish
# if file_upload or url_input:
#     try:
#         if file_upload:
#             img = PILImage.create(file_upload)
#             st.image(file_upload, caption="Yuklangan rasm")
#         else:
#             response = requests.get(url_input)
#             img = PILImage.create(BytesIO(response.content))
#             st.image(img, caption="URL orqali yuklangan rasm")
        
#         if isinstance(img, PILImage) and model is not None:
#             pred, pred_id, probs = model.predict(img)
#             st.success(f"Bashorat: {pred}")
#             st.info(f"Ehtimollik: {probs[pred_id] * 100:.1f}%")
            
#             # Diagramma chizish
#             fig = px.bar(x=probs * 100, y=model.dls.vocab, labels={'x': "Ehtimollik (%)", 'y': "Klasslar"}, orientation='h')
#             st.plotly_chart(fig)
#         else:
#             st.error("Tasvirni yoki modelni yuklashda muammo bor.")
#     except Exception as e:
#         st.error(f"Bashorat qilishda xatolik: {e}")

# # Sidebar qo'shimchalar
# st.sidebar.header("Qo'shimcha ma'lumotlar")
# st.sidebar.write("Bizni ijtimoiy tarmoqlarda kuzatib boring:")
# st.sidebar.markdown("[Telegram](https://t.me/ali_bek_003)")
# st.sidebar.markdown("[Instagram](https://www.instagram.com/alib_ek0311/profilecard/?igsh=MWo5azN2MmM2cGs0aw==)")
# st.sidebar.markdown("[Github](https://github.com/AlibekSerikbayev)")
# st.write("Ushbu dastur Alibek Serikbayev tomonidan yaratildi")
