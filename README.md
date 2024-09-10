# SyntAR
Synthetic data generation for Aircraft detection and recognition 

# Code
Create an environmnet and activate it

`conda create -n hor python=3.9`


 `conda activate hor`

## Install dependencies
`python -m pip install -r requirements.txt`

## Train
### Training on background

To train SinGAN model on your background satellite images, crop the image to get 512 × 512 pixels images . For generating the crops , use this script

``python crop.py ``

Put the desired background training images crops under Backgroundsdataset folder, and run

``python train_all.py ``

This will call other files "main_train.py" and from there it will run the harmonization command for all the images one by one for all the scale 0 to 7 

To run this code on a cpu machine, specify 
`--not_cuda when calling main_train.py`


This is what runs with this command on terminal :

Harmonization Command :  python main_train.py --input_name slice_langleyairbase_x7247_y2386.png
Random Seed:  8158
GeneratorConcatSkip2CleanAdd(
  (head): ConvBlock(
    (conv): Conv2d(3, 32, kernel_size=(3, 3), stride=(1, 1))
    (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    (LeakyRelu): LeakyReLU(negative_slope=0.2)
  )
  (body): Sequential(
    (block1): ConvBlock(
      (conv): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
      (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (LeakyRelu): LeakyReLU(negative_slope=0.2)
    )
    (block2): ConvBlock(
      (conv): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
      (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (LeakyRelu): LeakyReLU(negative_slope=0.2)
    )
    (block3): ConvBlock(
      (conv): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
      (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (LeakyRelu): LeakyReLU(negative_slope=0.2)
    )
  )
  (tail): Sequential(
    (0): Conv2d(32, 3, kernel_size=(3, 3), stride=(1, 1))
    (1): Tanh()
  )
)
WDiscriminator(
  (head): ConvBlock(
    (conv): Conv2d(3, 32, kernel_size=(3, 3), stride=(1, 1))
    (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    (LeakyRelu): LeakyReLU(negative_slope=0.2)
  )
  (body): Sequential(
    (block1): ConvBlock(
      (conv): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
      (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (LeakyRelu): LeakyReLU(negative_slope=0.2)
    )
    (block2): ConvBlock(
      (conv): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
      (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (LeakyRelu): LeakyReLU(negative_slope=0.2)
    )
    (block3): ConvBlock(
      (conv): Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1))
      (norm): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (LeakyRelu): LeakyReLU(negative_slope=0.2)
    )
  )
  (tail): Conv2d(32, 1, kernel_size=(3, 3), stride=(1, 1))
)



### Harmonize the synthetic patches on trained backgrounds

To harmonize a pasted aircraft into an image (See Fig. 6 in our paper), please first train SinGAN model on the desired background satellite image (as described above), we run this command 

``python ScriptForMaskingAllbg_Finalized.py``

when we run this command dialog box will open , we select data then all_objects . It contains patches of all aircraft that we want to paste on our background. we click ok. Then the first background image will open and we click anywhere on the image and press enter. The harmonization code will now run and it will generate naively  pasted aircraft image and mask that i will used for harmonization. THese will be saved inside folder Generated/ 

Inside harmonization command there is one provision for scale of injection: 

``python harmonization.py --input_name <training_image_file_name> --ref_name <naively_pasted_reference_image_file_name> --harmonization_start_scale <scale to inject>``

Please note that different injection scale will produce different harmonization effects. The coarsest injection scale equals 1.

After harmonization the images are automatically saved inside Output/Harmonization folder

## Test
To test and generate the harmonized SyntAR images against all provided backgrounds and for all the aircraft patches , we have a script which is automated method to pick backgrounds one by one from the backgrounds folder , place objects one by one on the backgrounds where the user clicks on the background and generates the naively pasted aircraft images for the backgrounds inside "generated" folder. Then the scrip automatically runs the harmonization pipeline to create SyntAR images for all the generated images and save them inside "Output" folder.

Run this cmd 

``python ScriptForMaskingAllbg_Finalized.py ``

choose directory box opens , select folder named data with double click, aall_objects double click, ok. Then first background will open , click wherever you want to place aircraft and enter. The harmonization code will start for all objects on that background one by one. 


## User Study

The data used for the user study can be found in the Downloads folder.

backgrounds folder: 5 real images which can serve as backgrounds, randomly picked from the places database

For additional details please see subsection 3.1 in our paper
