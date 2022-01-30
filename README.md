# Semantic segmentation with UNET(Tensorflow 2) and Deploy on FPGA with Vitis AI

## 1. Introduction

UNET is one of the most popular, simple and effective neurtal network model for Semantic segmentation. In this project UNET model with Tensorflow 2 has been developed for road scene segmentation. Then the model was deployed to FPGA. Vitis AI 1.4 has been used to accelerate DPU on ZCU 104 FPGA. Follwoing the process will be presented step by step in details.

## 2. OS, Tools and hardware used

* Ubuntu 20.04.3, Vitis AI 1.4
* ZCU 104
* Docker

## 3. Connection between Host(Ubuntu) and Taregt(ZCU104)

  - ### 1.1 Wire connection for ZCU104
   ![alt text](https://github.com/Zaman32/vitis_fpga_semantic_seg/blob/main/vitis_doc_png/zcu104_set.png?raw=true)
   
  - ### 1.2 Flashing the OS Image to the SD Card
     - Download and install Etcher :point_right: https://etcher.io/
     - Download the ZCU104 system images :point_right: https://www.xilinx.com/member/forms/download/design-license-xef.html?filename=xilinx-zcu104-dpu-v2021.1-v1.4.0.img.gz
     - Flash the ZCU104 images to the SD card

   - ### 1.3 Booting the Evaluation Board and Login through UART port
     - Connect the power supply (12V ~ 5A).
     - Connect the UART debug interface to the host and other peripherals as required.
     - Check which tty port is connected with the board using the following command
       ```
       $ dmesg | grep tty
       ```
       ** In my case its ttyUSB1
     - Install(if not installed) and configure minicom :point_right: https://wiki.emacinc.com/wiki/Getting_Started_With_Minicom
       * For zcu104, settings will be
           * baud rate: 115200 bps
           * data bit: 8
           * top bit: 1
           * no parity
     - Now insert the SD card and power up the board, you can see the booting from the host terminal using the following command(replace ttyXXX with your tty port name. )
       ```
       $ sudo minicom -D /dev/ttyXXX
       ```
       Log in to the system with username “root” and password “root.”
     
   - ### 1.4 Configure Ethernet port
      To exchange file from host to zcu104, connect the Ethernet cable with the board and your PC. Configure host and target static IP address to communicate between host and target. I used the following network configuration. Process is following
      - Configure host IP address
           * IP address: 10.42.0.42
           * Gateway: 10.42.0.1
           * Netmask: 255.255.255.0
             
          You can do it from the top right corner in Ubuntu -> Wired Settings -> Network -> Wired -> Settings -> IPv4 -> Netmask
      - Configure ZCU104 IP address
           * IP address: 10.42.0.42
           * Gateway: 10.42.0.1
           * Netmask: 255.255.255.0
           
         Login to zcu104 from host with UART and minicom. In the terminal implement the following command. Check with which port ethernet is connected. View network interface card command
         ```
         $ ip l show
         ```
         In my case it is eth0. Write the following command to set up zcu104 network
         ```
         $ ifconfig eth0 10.42.0.100 netmask 255.255.255.0 up
         $ route add default gw 10.42.0.1
         ```
      
## 4. Setting up Vitis AI 1.4
- ### 1.1 Setting up Host - Install docker and Configure IP address 
  - #### 1.1.1 Install Docker
     * Install docker. :point_right: https://docs.docker.com/engine/install/ubuntu/
     * Do the Post-installation steps for Linux to ensure that your Linux user is in the group docker. Do the first step(Manage Docker as a non-root user)            :point_right: https://docs.docker.com/engine/install/linux-postinstall/
     * Clone the Vitis AI repository to obtain the examples, reference code, and scripts. 
     ``` 
     $ git clone --recurse-submodules https://github.com/Xilinx/Vitis-AI 
     $ cd Vitis-AI 
    ```
    * Pull latest CPU docker container 
     ```
     $ docker pull xilinx/vitis-ai
     ```
     * Run docker container
     
       Run the following command from home directory to run docker container 
       ```
       $ cd Vitis-AI 
       $ ./docker_run.sh xilinx/vitis-ai
       ```
     
     
## 4. The Main Flow
The full work flow can be devided into 5 part mentioned following. The 1st and 2nd part is done outside Vitis AI container and the rest is done on the Vitis AI container. 

 ***1. Process Image:*** For each dataset, organize the data into proper folders, such as train (for training), val (for validation during the training phase), test (for testing during the inference/prediction phase) and calib (for calibration during the quantization phase). See Organize the Data for more information.
 
 ***2. Train model:*** Train the CNNs in Keras on Host platform(outside ) with GPU and generate the HDF5 weights model. See Train the CNN for more information.
 
 ***3. Quantize model:*** Quantize from 32-bit floating point to 8-bit fixed point and evaluate the prediction accuracy of the quantized CNN. See Quantize the Frozen Graphs for more information.
 
 ***4. Compile the model:*** Run the compiler to generate the xmodel file for the target board from the quantized pb file. See Compile the Quantized Models for more information.
 
 ***5. Deploy and Run the model on ZCU104:*** Deploy the model and accelerate on FPGA with C++ code
 
 ## 5. Process Image: 
Create a project folder for the project. If the folder is outside Vitis AI folder, after training it needs to be moved to the project folder Vitis AI folder(where Vitis AI were cloned). Download the dataset from :point_right: [link](https://drive.google.com/file/d/0B0d9ZiqAgFkiOHR1NTJhWVJMNEU/view) .The folder name is ```dataset1```. The code ```unet_config.py``` contains all the directory path and constants definition. The code ```unet_utils.py``` contains all the utility functions. 
The code ```1_preprocess_data.py``` does the first part. 
 1. Read the images from ```images_prepped_train``` and split and store them in new seperate folder named ```train_img```, ```valid_img``` and ```calib_img```.
 2. Read the images from ```annotations_prepped_train``` and split and store them in new seperate folder named ```train_seg```, ```valid_seg``` and ```calib_seg```.
 3. Read the images from ```images_prepped_test``` and split and store them in new seperate folder named ```test_img```.
 4. Read the images from ```annotations_prepped_test``` and split and store them in new seperate folder named ```test_seg```.
 

## 6. Train model: 
The code ```2_train_model.py``` normalize the training and validation images and train the model. After training the best model will be saved as Hierarchical Data Format(.h5). This file need to be quantized.

## 7. Quantize the model: 
Create a folder in Vitis-AI folder. Move your project folder in the new folder.
1. Open a terminal in Vitis-AI folder. Run the following command to start the Vitis AI docker.
   ```
    $ ./docker_run.sh
    ```
2. activate the conda tensorflow 2 environment with following command
   ```
   $ conda activate vitis-ai-tensorflow2
   ``` 
3. Go to your project folder from this terminal. For my case its the following.
   ```
   $ cd test-model/road_scene
   ```
4. Run the ```3_quantize_model.py``` code with the following command. It will quantize the 32-bit floating point model to 8-bit fixed point model. For quantizetion some sample image, on which the main model were trained, need to be provided. This images used to calibrate the quantized model. 
   ```
   $ python 3_quantize_model.py 
   ```
   
5. Evaluate the the non-quantized and quantized model prediction with the following code
   ```
   $ python eval_quantized_model.py
   ```
   
![alt text](https://github.com/Zaman32/vitis_fpga_semantic_seg/blob/main/vitis_doc_png/doc_pred_com.png?raw=true) 
Prediction comparison of non-quantized and quantized model  



     
![alt text](https://github.com/Zaman32/vitis_fpga_semantic_seg/blob/main/vitis_doc_png/doc_iou.png?raw=true) 

IoU comparison of non-quantized and quantized model    
     
## 8. Compile the model:
The command compile the model. It needs to be run from the project directory in docker.
  ```
  $ vai_c_tensorflow2 -m /workspace/test-model/road_scene/quantized_model/quantized_model.h5 -a /opt/vitis_ai/compiler/arch/DPUCZDX8G/ZCU104/arch.json -o /workspace/test-model/road_scene/compiled_model -n compiled_unet -e "{'mode':'normal'}"
  ```
Breakdown of the command

 - ``` -m ``` the location of the quantized model
 - ``` -a ``` arch option supplies the specific configuration of the DPU Architecture.
 - ``` -o ``` output directory
 - ``` -n ``` net name
 - ``` -o ``` options

## 9. Deploy and Run on FPGA:
Create a deployment folder(in my case road_scene_target_zcu104) that we will put on the FPGA. 
The folder will contain the following files and folder.
- ```test.tar.gz``` will contain test images and segmentation image
    ```
    # copy test images into target board
    $ tar -cvf "test.tar" ${DATASET_DIR}/img_test ${DATASET_DIR}/seg_test
    $ gzip test.tar
    $ cp test.tar.gz ${TARGET_104}
    ```
- ```unet``` contain .xmodel and .json file
-  ```rpt``` contain the log file
-  ```png_unet``` it will store the predicted image
-  ```code``` contains all the code. It will contain the following folders and files 
    * ```build_app.sh```
    * ```build_get_dpu_fps.sh```
    * ```run_cnn_fps.sh```
    * ```src``` contains ```get_dpu_fps.cc``` and ```main_mt_int8.cc```
    * ```common``` contains ```common.cpp``` and ```common.h```

Copy the folder(road_scene_target_zcu104) to the FPGA using following command. 

  ```
  $ scp <project-directory-path>/road_scene_target_zcu104 root@10.42.0.100:~/
  ```
  
From the FPGA terminal connected with minicom from FPGA enter into the road_scene_target_zcu104 and run the ```run_all_target.sh``` with the following command. 
  ```
  $ ./run_all_target.sh
  ```
  ![alt text](https://github.com/Zaman32/vitis_fpga_semantic_seg/blob/main/vitis_doc_png/out_000.png?raw=true)
  
  Inference by FPGA on a test image
  

 
