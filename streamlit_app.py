import streamlit as st 
import streamlit.components.v1 as stc
import os
from datetime import datetime
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr

TITLE = """
	<div style="background-color:#464e5e;padding:10px;border-radius:10px">
	<h1 style="color:white;text-align:center;">Planetoid's OCR</h1>
	</div>
	"""

@st.cache
def save_image(file):
	#if file is too large then return
	if file.size > 209715200: # 200 MB
		return 1
	
	folder = "public_images"
	datetoday = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	try:
		with open("log0.txt", "a") as f:
			f.write(f"{file.name} - {file.size} - {datetoday};\n")
	except:
		pass

	with open(os.path.join(folder, file.name), "wb") as f:
		f.write(file.getbuffer())
	return 0

@st.cache(suppress_st_warning=True, allow_output_mutation=True) 
def load_model():
	ocr = PaddleOCR(use_angle_cls=True, lang='en') 
	return ocr

def perform_ocr():

	#menu = ["Home","Scan "]
	#choice = st.sidebar.selectbox("Options",menu)
	stc.html(TITLE)
	path = None
	st.sidebar.image("planetoid.png", use_column_width=True)
	st.subheader("Scan your image")
	image_file = st.file_uploader("Upload receipt image file", type=['jpg', 'png', 'jpeg'])
	if image_file is not None:

		if not os.path.exists("public_images"):
			os.makedirs("public_images")
		path = os.path.join("public_images", image_file.name)
		if_save_image = save_image(image_file)
		if if_save_image == 1:
			st.warning("File size is too large. Try another file with lower size.")
		
		# elif if_save_image == 0:
			
		# 	# display receipt
		# 	try:
		# 		st.image(image_file, use_column_width=True)
		# 	except Exception as e:
		# 		st.error(f"Error {e} - wrong format of the file. Try another .jpg file.")
		# 	else:
		# 		st.error("Unknown error")
		
	else:
		if st.button("Try test file"):
			st.image("1.jpeg", use_column_width=True)
			path = "1.jpeg"

	if path is not None:

		ocr = load_model()
		#img_path = '1.jpeg'
		result = ocr.ocr(path, cls=True)
		#for line in result:
		#print(line)

		image = Image.open(path).convert('RGB')
		boxes = [line[0] for line in result]
		txts = [line[1][0] for line in result]
		scores = [line[1][1] for line in result]
		im_show = draw_ocr(image, boxes, txts, scores, font_path='Roboto-Black.ttf')
		st.image(im_show, use_column_width=True)
		st.image(image_file, use_column_width=True)
		#im_show = Image.fromarray(im_show)

if __name__ == "__main__":
	perform_ocr()
