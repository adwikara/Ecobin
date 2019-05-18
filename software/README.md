# Welcome to Ecobin's software repository
This directory contains multiple modules, and they interact as follow
![Untitled document (1)](https://user-images.githubusercontent.com/25762021/56843652-41709080-6871-11e9-9e20-c71807463858.jpg)

## iOS/
#### Dependencies
* xcode 4.2
* IOS 12.0+
* Cocoapods

#### User Guide
![IMG_7575](https://user-images.githubusercontent.com/33381712/56838467-17f13e00-684c-11e9-8487-18cd88a7c244.PNG)

#### Page 1:  (Latest Information)
![IMG_7576](https://user-images.githubusercontent.com/33381712/56840348-18420700-6855-11e9-8b62-eb8640499f91.PNG) <br/>
This page displays the last processed waste information which includes the object type, object description, accuracy value as well as the capacity buildup for both types of waste. By clicking on the refresh button on the top left, the application will update the latest waste values. Additionally, if the application will auto-update the information every 10 seconds as long as the user remains on this page.

#### Page 2: (Overall Analytics)
![IMG_7577](https://user-images.githubusercontent.com/33381712/56840354-209a4200-6855-11e9-97fa-5b27728d6ef1.PNG) <br/>
The analytics page will display the total average accuracy measured over time, as well as the total number of general trash and recyclable trash recorded. 

#### Page 3: (Help Page)
![IMG_7577](https://user-images.githubusercontent.com/33381712/56840354-209a4200-6855-11e9-97fa-5b27728d6ef1.PNG) <br/>
On this page, the user is able to read useful information on how to navigate through the application.

## Recognition/
This is where the object recognition algorithms lie. 
#### Hardware 
The training of this neural network occurred on BU SCC, with the following specifications in the node and Linux Centos 6: 
1. 2 NVIDIA P100 GPUs with 16GB DDR4 memory
2. 128 GB memory
3. 2 fourteen-core 2.4 GHz Intel Xeon E5-2680v4

#### Dependencies
Software-wise, the following dependencies are needed:
```
keras >= 0.9.2
python >= 3.6.2
tensorflow==1.10
cuda==9.1
cudnn==7.1
```

This mechanism is based on a VGG-16, a convolutional neural networks. However, the basic configuration of VGG-16, consisting of 1000 classes, are not neccessary for the project. In this projects, we strived to classify the following classes:
* Category 1: Recyclable 
bottles
```
cups
metal cans
glass
general plastic containers
utensils
carton/cardboard
general recyclable items
```
* Category 2: Trash 
```
food
fruit
compostable containers
leafy green
general trash items 
```
This model has flavors of transfer learning and fine tuning using VGG16. 

The primary files in this directory is **transfer_learn.py**, **classes.json** **resize.py**

transfer_learn.py contains the machine learning code with Keras and Tensorflow. It requires data/, a directory for training and validation data. In order to use the dataset, unzip using the following command
```
unzip data.zip
```
The data/ direcoty contains two sub-directories: train/ and validation/, corresponding to the validation dataset and training dataset. We split our dataset into 80% training/20% validation. In order to train a more specialized model, the last four layers of VGG-16 frozen and modified into the following:
```
Convoluted (512 nodes)
Flatten
Dense (4096 nodes)
Dropout (80%)
Dense (12 layers)
```
To run trasnfer_learn.py and train a new model
```
python3 transfer_learn.py
```

With the above hardware configurations, it takes roughly 45-60 minutes. At the end, it will output ecobin.h5, which is the model that contains weights for all the convoluted layers. An example use of this file could be seen in ecobin_predict.py. 


If you wish to test the model with an image and see the output 
```
$ python3 
Python 3.7.2 (default, Feb 12 2019, 08:15:36) 
[Clang 10.0.0 (clang-1000.11.45.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import ecobin_predict
>>> ecobin_predict.predict('<image_name>')
```


classes.json contains the json-ified format of the classes and resize.py was used in order to make sure every image is of size (224,224), the required resolution.

## API/ and backend

Ecobin's backend is supported by the API and the database. It is the primary tool for Raspberry Pi, iOS application and the backend to communicate. The REST API is implemented in python using Flask and is hosted on a cloud instance at http://128.31.22.22:8080/ecobinC/api/v1.0/classify/1

#### Cloud specs
This cloud instance has the following specifications:
```
16GB DDR Memory
2 eight-core CPUs with AX1 support
1TB storage
```

#### Dependencies
```
python >= 3.6.2
Flask >=1.0.0
HTTPBasicAuth >=1.000 
Requests==2.2.1
```
The API also requires ecobin.h5, which is an output from **transfer_learn.py** from the recognition module. The back_end.py, update_database_new.py scripts have to be on the same directory as app.py 

A architectural diagram of the API is as follows: 

![APIdiagram](https://user-images.githubusercontent.com/28953941/56838583-7cac9880-684c-11e9-8162-be6b68d9b76c.png)



The API functions in this order: 

1. The Raspberry Pi takes a picture of an object placed in the bin and converts the .jpg into a base64 encoded string that can be stored in the API using a PUT request. 
2. The API features an authentication method implemented with ‘HTTPAUTH’. It requires a username and password in order to be able to access and store information from and to the API. 
3. The machine learning code then pulls the encoded string information from the API using a GET request. 
4. In the backend, the machine learning code then processes the image and returns a dictionary with key value pairs holding attributes: object name, accuracy, its classification type. The backend also updates the API with the processed information using a PUT request.  
5. The backend file connects to the Mongo Atlas database and stores the classification and accuracy information processed from the Machine Learning code.
6. The RasPi receives information from the API, whether the object is ‘trash’ or ‘recyclable’.
7. The RasPi outputs this signal to the stepper motor, which sorts the object.
8. The API then sends the information to the iOS application which  presents interactive results to the user. 

In order to run the API, simply run this command
```
python3 app.py
```

The API architecture for the key value pairs is as follows: 

```
classify = [
    {
        'id': 1,
        'name': 'nameholder',
        'string': 'stringplaceholder',
        'type': 'Trash',
        'accuracy': 80,
        'recyclable': 0,
        'trash': 0,
        'accuracyavg': 0,
        'capacityTrash': 0,
        'capacityRecycle': 0
    }
   ```
   
A brief description of each of the initialized key-value pairs is as follows:

1. ‘name’ : Name of object identified
2. ‘string’ : Base64 encoded image string
3. ‘type’ : whether it’s Trash or Recyclable
4. ‘accuracy’: Probability percentage of prediction accuracy
5. ‘recyclable’ : Total count of Recyclables
6. ‘trash’ : Total count of trash
7. ‘accuracyavg’ : Average of “Accuracy” 
8. ‘CapacityRecycle’ : Capacity limit of Recyclable Bin
9. ‘CapacityTrash’ : Capacity limit of Trash Bin

Ecobin also has a MongoDB Atlas Database which stores information communicated from the API and also to generate Ecobin user information summary to display on the iOS application.The Database functions as follows: 

1. Creates a “document” in a “collection called “test” in a database called “ecobin-results” to store the classified attributes of each object tested in the ecobin

2. To perform database ‘aggregate’ functions using pipeline in order to be able summarize information stored in the database and automatically update the summary  with each tested object. This information is queried by the API using the PUT request so that the iOS application can access it. The aggregate function performs two functions: 
    1. Counts and number of  “Trash” and “Recyclable” objects store their frequencies  in a list 
    2. Perform the average of accuracies of the probability percentages of images identified and classified to provide an estimation for the rate of success of the classification. 
    
This is how data is stored in the database after it is processed in the update_database_new.py file in the API folder:

![idj](https://user-images.githubusercontent.com/28953941/56840126-d6fd2780-6853-11e9-9a2c-d82794414b6a.png)

Three key pieces of information are stored in the database as seen above: 
1. 'Accuracy': Percentage probability  of correct object detection
2. 'Name': Name of the object identified
3. 'Type': Recyclable or Trash

## GUI/
This directory contains outdated code used to display GUI and debugging information from the Raspberry Pi to an LCD screen.
The GUI is enabled to work Tkinter python library which can be run by executing this command on the kivy.py file in the GUI folder. 

```
python3 kivy.py

```

The dependencies of this are: 

```
tkinter >= 8.0.0
PySimpleGUI >= 3.29.0
tk_tools == 0.11.0
Pillow == 6.0.0

```

## Webscraper/ 
Credits: https://github.com/hardikvasa/google-images-download
```
This is a command line python program to search keywords/key-phrases on Google Images and optionally download images to your computer. You can also invoke this script from another python file.

This is a small and ready-to-run program. No dependencies are required to be installed if you would only want to download up to 100 images per keyword. If you would want more than 100 images per keyword, then you would need to install Selenium library along with chromedriver. Detailed instructions in the troubleshooting section.
```

#### Usage
In order to use this webscraper, the user needs to specify options and keywords (or URL) of the desired Google Images. 
```
python3 google_images_download.py -l <number of imges> -cd <directory for Chrome Driver if more than 200 images> -nn --url <specify URL>
```
An example of this, where we are requiring 200 images from the URL https://www.google.com/search?biw=1378&bih=659&tbm=isch&sa=1&ei=fcukXKvoBs6Kggft3ID4DQ&q=glass+jars+in+black+background&oq=glass+jars+in+black+background&gs_l=img.3...11991.15759..15911...0.0..0.112.1564.19j1......1....1..gws-wiz-img.......0j0i8i30j0i24.0Mip6LQyMyA

```
python3 google_images_download.py   -l 200 -cd ~/Downloads/chromedriver -nn --url 'https://www.google.com/search?biw=1378&bih=659&tbm=isch&sa=1&ei=fcukXKvoBs6Kggft3ID4DQ&q=glass+jars+in+black+background&oq=glass+jars+in+black+background&gs_l=img.3...11991.15759..15911...0.0..0.112.1564.19j1......1....1..gws-wiz-img.......0j0i8i30j0i24.0Mip6LQyMyA'
```
The team pulls around 10000 images from Google Images for our datasets, which is sufficient, on top of other free datasets on the Internet. In addition, the team also incorporate datasets from trashnet and image-net.org 
