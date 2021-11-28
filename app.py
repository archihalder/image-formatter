import cv2
import base64
import numpy as np
import streamlit as st
from io import BytesIO
from PIL import Image, ImageFilter, ImageOps


def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


# Title of the page
st.title('Image Formatter')

# Uploading an image file
uploaded_file = st.file_uploader(
    'Choose an image file', type=['jpg', 'jpeg', 'png'])


# this uploaded file is of 'streamlit.uploaded_file_manager.UploadedFile' class
# we have to convert that into a numpy array
if uploaded_file is not None:
    file_byte = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_byte, 1)
    st.image(img, channels='BGR')  # displaying the uploaded img
try:
    img_array = img
except:
    st.stop()

# Converting image array to PIL Image
photo = Image.fromarray(img_array)

# Properties of the uploaded image
st.header('Properties of the image')
st.write(f'The image size is {photo.size}')
st.write(f'The color mode is {photo.mode}')

# Sidebar title
st.sidebar.title('Tools')

# ------------------------------------------------------------
# FILTERS

st.sidebar.header('Filters')
filter = st.sidebar.selectbox('Choose from the below filters',
                              ('NONE', 'BLUR', 'SMOOTH', 'SHARPEN', 'GRAYSCALE'))

st.header('Filtered Image')

# 1. applying filter to the image
# 2. converting it to a numpy array
# 3. displaying the new image

if filter == 'BLUR':
    filtered_img = photo.filter(ImageFilter.BLUR)
    img = np.array(filtered_img)
    st.write('Image is blurred')
    st.image(img, channels='BGR')

elif filter == 'SMOOTH':
    filtered_img = photo.filter(ImageFilter.SMOOTH)
    img = np.array(filtered_img)
    st.write('Image is smoothened')
    st.image(img, channels='BGR')

elif filter == 'SHARPEN':
    filtered_img = photo.filter(ImageFilter.SHARPEN)
    img = np.array(filtered_img)
    st.write('Image is sharpened')
    st.image(img, channels='BGR')

elif filter == 'GRAYSCALE':
    filtered_img = ImageOps.grayscale(photo)
    img = np.array(filtered_img)
    st.write('Image is in grayscale')
    st.image(img)

else:
    img = np.array(photo)
    st.write('No filters are applied')
    st.image(img, channels='BGR')

# ---------------------------------------------------------
# ROTATE

# Converting image array to PIL Image
new_img = Image.fromarray(img)

st.header('Rotated Image')

# 1. rotating the image
# 2. converting it to numpy array
# 3. displaying the new image

st.sidebar.header('Rotate')
angle = st.sidebar.slider(
    'Select the angle of rotation', 0, 360)
r_image = new_img.rotate(angle, expand=True)
img1 = np.array(r_image)
st.write(f'Image is rotated by {angle} degrees in counterclockwise direction')
show = st.image(img1, channels='BGR')

# -------------------------------------------------------------
# RESIZE

# Converting image array to PIL Image
new_img = Image.fromarray(img1)

st.header('Resized Image')

# getting height and width as input
st.sidebar.header('Resize')
h = st.sidebar.number_input('Height', 0, 5000)
w = st.sidebar.number_input('Width', 0, 5000)

# using .thumbnail as it doesn't change the aspect ratio
#
if h != 0 and w != 0:
    st.write(f'The image is resized to {h}x{w} shape')
    temp_img = new_img
    temp_img.thumbnail((h, w))
    img2 = np.array(temp_img)
else:
    st.write('No adjustments done')
    img2 = np.array(new_img)

st.image(img2, channels='BGR')


# -------------------------------------------------------------
# EXTENSION

st.sidebar.header('Change extension')
ext = st.sidebar.selectbox('Choose from the below extensions',
                           ('.jpg', '.jpeg', '.png'))

# ------------------------------------------------------------
# DOWNLOAD

download = st.selectbox(
    'Do you want to download the image?', ('NO', 'YES'))

# Image downloader
if download == 'YES':
    result = Image.fromarray(img2)
    st.markdown(get_image_download_link(result, 'output'+ext,
                                        'Download '+'output'+ext), unsafe_allow_html=True)
