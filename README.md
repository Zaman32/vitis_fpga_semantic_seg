# vitis_fpga_semantic_seg

In this project UNET with Tensorflow 2, for road scene segmentation has been implemented on FPGA with Vitis AI 1.4 tool. Follwoing the process will be presented step by step in details

## 0. OS, Tools and hardware used

* Ubuntu 20.04.3, Vitis AI 1.4
* ZCU 104
* Docker

## 1. Connection between Host(Ubuntu) and Taregt(ZCU104)

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
      
## 1. Setting up Host and Target
- ### 1.1 Setting up Host - Install docker and Configure IP address 
  - #### 1.1.1 Install Docker
     * Install docker. :point_right: https://docs.docker.com/engine/install/ubuntu/
     * Do the Post-installation steps for Linux to ensure that your Linux user is in the group docker. Do the first step(Manage Docker as a non-root user)            :point_right: https://docs.docker.com/engine/install/linux-postinstall/
     * Clone the Vitis AI repository to obtain the examples, reference code, and scripts. 
     ``` 
     $ git clone --recurse-submodules https://github.com/Xilinx/Vitis-AI 
     $ cd Vitis-AI 
     ```
     * Run docker container 
     ```
     $ docker pull xilinx/vitis-ai
     $ ./docker_run.sh xilinx/vitis-ai
     ```
     
     



   
     
     

