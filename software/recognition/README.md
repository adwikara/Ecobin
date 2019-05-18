This is home to the machine learning code. Ecobin’s object detection algorithm, which uses Keras and Tensorflow, is trained and run on the SCC. The algorithm includes a neural network, based on the VGG16 pre-trained model, but differs from VGG16 in the last four layers:
1. Flatten
2. Dense (4096 nodes)
3. Dropout (80%)
4. Dense (12 nodes thus far)

### Quick Start
The workflow for these scripts are the following.

1. Train the model (very time consuming, please time accordingly):
```
$ python3 transfer_learn.py
```
2. Run the backend of Ecobin
```
$ python3 backend.py
```

After step 1, if you wish to test the model with an image and see the output 
```
$ python3 
Python 3.7.2 (default, Feb 12 2019, 08:15:36) 
[Clang 10.0.0 (clang-1000.11.45.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import ecobin_predict
>>> ecobin_predict.predict('<image_name>')
```
