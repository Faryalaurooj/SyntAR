import cv2
import numpy as np
import os
import time
from PIL import Image


id_dict = {"su" : 0, "rafale" : 1, "miraje" : 2, "mig29" : 3}  #classes


def rgba2rgb( rgba, background=(0,0,0) ):
    row, col, ch = rgba.shape

    if ch == 3:
        return rgba

    assert ch == 4, 'RGBA image has 4 channels.' #make it transparent

    rgb = np.zeros( (row, col, 3), dtype='float32' )
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]

    a = np.asarray( a, dtype='float32' ) / 255.0

    R, G, B = background

    rgb[:,:,2] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,0] = b * a + (1.0 - a) * B

    return np.asarray( rgb, dtype='uint8' ), a

def get_objectname(f):  #pick the objects aircraft from the folder od all objects with their name
	name = ''
	if 'su' in f or 'Su' in f:
		name = 'su'
	elif 'Mig29' in f:
		name = 'mig29'
	elif 'Mirage2000' in f:
		name = 'miraje'
	elif 'Rafale' in f or 'rafale' in f:
		name = 'rafale'
	elif 'tejaas' in f or 'Tejas' in f:
		name = 'miraje'
	return name

try:
    from tkinter import Tk
    from tkFileDialog import askopenfilenames
except:
    from tkinter import Tk
    from tkinter import filedialog

def pascal_voc_to_yolo(x1, y1, x2, y2, image_w, image_h):
    return [((x2 + x1)/(2*image_w)), ((y2 + y1)/(2*image_h)), (x2 - x1)/image_w, (y2 - y1)/image_h] # normalize the bounding box values of the patch to feed to yolo between 0 - 1
    
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
path = filedialog.askdirectory()# show an "Open" dialog box and return the path to the selected file
path = path+'/'

def click_event(event, x, y, flags, params):   #we will click on any point on the background where automatically the object will be pasted
	global centre
	if event == cv2.EVENT_LBUTTONDOWN:
		centre = y,x
			
for model in os.listdir("Backgroundsdataset"):  # now select any backgrund
	background = "Backgroundsdataset/" + model
	sample = cv2.imread(background,-1)
	print (sample.shape)

	centre = (0,0)

	cv2.imshow('image', sample)
	cv2.setMouseCallback('image', click_event)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	training_image = (background).split('/')[-1]
	print ("-------------------------------------------------------------", training_image)
	b = False
	count = 0
	#path = "data/objects/"
	for objects in os.listdir(path):    # objects are pasted one by one on one background
		count = count+1
		sample = cv2.imread(background,-1)
		
		background_image = Image.open(background, 'r').convert('RGBA')
		img1 = sample
		
		img2 = Image.open(path+objects)
	
		mask = np.asarray(img2)
		img2 = img2.convert("RGBA")
	
		rgb, a = rgba2rgb ( mask )
	
		h,w = 0,0
	
		a = cv2.resize(a, (a.shape[1]+h,a.shape[0]+w), interpolation = cv2.INTER_AREA)

		ret,thresh1 = cv2.threshold(a,0.5,1,cv2.THRESH_BINARY)
		ret,thresh2 = cv2.threshold(a,0.5,1,cv2.THRESH_BINARY_INV)
	
		h, w, c = img1.shape
		h_m, w_m = thresh2.shape[0], thresh2.shape[1]
		
		result = np.zeros((h, w), np.uint8)
		
		cropped_out = img1[ int(centre[0]-(h_m/2)) : int(centre[0]+(h_m/2)) ,  int(centre[1]-(w_m/2)) : int(centre[1]+(w_m/2))]
		
		cropped_out[thresh2 < 0.05] = 0
		
		cropped_out = cropped_out + rgb
		rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR )
		
		white = np.ones(img1.shape) * 255
		white[ int(centre[0]-(h_m/2)) : int(centre[0]+(h_m/2)) ,  int(centre[1]-(w_m/2)) : int(centre[1]+(w_m/2)) ] = cropped_out
		img1 = img1*(white/255)
		img1[ int(centre[0]-(h_m/2)) : int(centre[0]+(h_m/2)) ,  int(centre[1]-(w_m/2)) : int(centre[1]+(w_m/2)) ] = cropped_out
		result[ int(centre[0]-(h_m/2)) : int(centre[0]+(h_m/2)) ,  int(centre[1]-(w_m/2)) : int(centre[1]+(w_m/2)) ] = thresh1
		
		
		top_left_x, top_left_y = int(centre[0]-(h_m/2)), int(centre[1]-(w_m/2))
		bottom_right_x, bottom_right_y = int(centre[0]+(h_m/2)), int(centre[1]+(w_m/2))
		
		bb = pascal_voc_to_yolo(top_left_x, top_left_y, bottom_right_x, bottom_right_y, w, h)
		
		result = result*255
	
		bg = background.split('/')[-1].split('.')[0]
		ob = objects.split('.')[0]
	
		generated_path = 'generated/'+ ob.split('_')[0] + '_' + bg.split('_')[0]  + str(count)   # so inside generated folder , for each background the objects are pasted 
		sample_path = generated_path+'/' + ob.split('_')[0] + '_' + bg  + '.png'
	
		mask_path = sample_path.split('.')[0] + '_mask'+"."+sample_path.split('.')[1]
		
		os.mkdir(generated_path)
	
		if result is not None:
			seg = np.where(result == 1)
			
		obg_img = Image.new('RGBA', (w_m, h_m), (0,0,0,0))
		obg_img.paste(img2, (0,0))
		
		background_image.paste(obg_img,  (int(centre[1]-(w_m/2))  ,  int(centre[0]-(h_m/2)) ), mask = img2)
		obg_img = np.array(obg_img)
		background_image = np.array(background_image)
		obg_img = cv2.cvtColor(obg_img, cv2.COLOR_RGB2BGR)
	
		result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
		cv2.imwrite(mask_path, result)
	
		background_image = cv2.cvtColor(background_image, cv2.COLOR_RGB2BGR)
		cv2.imwrite(sample_path, background_image)
		
		annotations_path = "Output/Harmonization/"+bg+'/'+sample_path.split('/')[1]+'.txt'  # harmonization is done and for each pasted object an output will be generated inside OUtput folder along with label
		ob_name = get_objectname(objects)
		print (annotations_path, ob_name)
		
		if not os.path.isdir("Output/Harmonization/"+bg):
			os.mkdir("Output/Harmonization/"+bg)
			
		with open(annotations_path, 'w') as f:
			if ob_name in id_dict.keys():
				f.write(str(id_dict[ob_name])+' '+str(bb[0])+' '+str(bb[1])+' '+str(bb[2])+' '+str(bb[3])+'\n')
				f.close()
		
		cmd = "python harmonization.py --input_name " + training_image + " --ref_name " + '/'.join(sample_path.split('/')[1:]) + " --harmonization 7"

		print ("Harmonization Command : ",cmd)
	
		if os.system(cmd) != 0:
 			print ("Failed command : ", cmd)

