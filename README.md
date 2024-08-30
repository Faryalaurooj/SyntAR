# SyntAR
Synthetic data generation for Aircraft detection and recognition 

# Code
Create an environmnet and activate it

`conda create -n hor python=3.9`


 `conda activate hor`


## Install dependencies
`python -m pip install -r requirements.txt`

## Train
To train SinGAN model on your background satellite images, crop the image to get 512 × 512 pixels images . Put the desired training images under Input/Images, and run

``python main_train.py --input_name <input_file_name>``

To run this code on a cpu machine, specify 
`--not_cuda when calling main_train.py`

To harmonize a pasted aircraft into an image (See Fig. 6 in our paper), please first train SinGAN model on the desired background satellite image (as described above), then save the naively pasted reference image and it's binary mask under "Input/Harmonization" (see saved images for an example). Run the command

``python harmonization.py --input_name <training_image_file_name> --ref_name <naively_pasted_reference_image_file_name> --harmonization_start_scale <scale to inject>``

Please note that different injection scale will produce different harmonization effects. The coarsest injection scale equals 1.

## Test
To test and generate the harmonized SyntAR images against all provided backgrounds and for all the aircraft patches , we have a script which is automated method to pick backgrounds one by one from the backgrounds folder , place objects one by one on the backgrounds where the user clicks on the background and generates the naively pasted aircraft images for the backgrounds inside "generated" folder. Then the scrip automatically runs the harmonization pipeline to create SyntAR images for all the generated images and save them inside "Output" folder.

Run this cmd 

`python ScriptForMaskingAllbg_Finalized.py `


choose directory box opens , select folder named data with double click, aall_objects double click, ok. THen first background will open , click wherever you want to place aircraft and enter. THe harmonization code will start for all objects on that background one by one. 



## User Study

The data used for the user study can be found in the Downloads folder.

backgrounds folder: 5 real images which can serve as backgrounds, randomly picked from the places database

For additional details please see subsection 3.1 in our paper
