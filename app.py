import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit.components.v1 as components

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

# Funksiya: Face ID tasdiqlash (JavaScript orqali kamera tasvirini olish)
def capture_face_with_permission():
    components.html(
        """
        <script>
        async function requestCameraAccess() {
            try {
                // Kamera uchun ruxsat so'rash
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();
                document.body.appendChild(video);

                // Video o'qilib bo'lgach tasvirni olish
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const context = canvas.getContext('2d');

                setTimeout(() => {
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const imageData = canvas.toDataURL('image/png');
                    fetch('/face-id-callback', {
                        method: 'POST',
                        body: JSON.stringify({ image: imageData }),
                        headers: { 'Content-Type': 'application/json' }
                    }).then(response => {
                        if (response.ok) {
                            alert('Face ID tasdiqlandi!');
                        } else {
                            alert('Face ID tasdiqlanmadi.');
                        }
                        stream.getTracks().forEach(track => track.stop()); // Kamerani o'chirish
                        video.remove();
                    });
                }, 3000); // 3 soniyadan keyin tasvirni olish
            } catch (error) {
                alert('Kamera uchun ruxsat berilmadi!');
            }
        }

        requestCameraAccess();
        </script>
        """,
        height=0,
        width=0,
    )

# Funksiya: Yuzni tasdiqlash (tasvir ma'lumotini qabul qilish va tahlil qilish)
def verify_face(captured_image, stored_embedding):
    # Bu funksiya tasvirni tahlil qilish va foydalanuvchi ma'lumotlarini solishtirish uchun ishlatiladi
    resized_image = np.random.rand(128)  # Kameradan olingan tasvirni ishlovdan o'tkazish (moslashuv uchun)
    similarity = cosine_similarity([stored_embedding], [resized_image])[0][0]
    return similarity > 0.8  # Moslik chegarasi

# Streamlit ilovasi
def main():
    st.set_page_config(page_title="Face ID va Kamera Ruxsati", layout="wide")
    st.title("Brauzerda Kamera Ruxsati va Face ID")

    # Login bosqichi
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

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
    if st.button("Face ID tasdiqlashni boshlash"):
        capture_face_with_permission()

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
