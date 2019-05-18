# Ecobin
This is a repository for Team 9- Ecobin, for our senior year capstone project at Boston University's Department of Electrical and Computer Engineering.

## Introduction
Mission: Our project aims to develop a smart Internet-of-Things (IoT) device which can automate recycling by employing Computer Vision and a Raspberry Pi 3+. 
 
## Architecture
![Architecture](https://user-images.githubusercontent.com/33497234/56839341-04e06d00-6850-11e9-8a4e-8f2f3e5c4723.png)

## Getting Started
In order to install the dependencies required, run
```
pip3 install -r requirements.txt

```

## Deployment
The two major depositories, hardware/ and software/, contain code and instructions on how each module works. 

Overall tech stack includes
```
Raspberry Pi 3 B+
MongoDB Atlas
Keras/ Tensorflow
Flask
Swift/XCode for iOS application development
```
## Addendum
This Github is a general introduction to Ecobin and its current state as of April 26, 2019. Any further question could be addressed to the developers. 

At the curent state, most requirements were satisfied in the final demo. 
* We have to make a minor adjustment during testing to the motion sensor due to loose wires. 
* The latest object recognition algorithm achieves upward 85% accuracy, and the client gave very positive remarks for this achievement. 
* The sorting mechanical component could sweep the 1kg food can smoothly into the recycling bin. 
* In addition, any object below a threshold of 60% accuracy was successfully categorized as trash in order to prevent false positives. 
* The capacity sensor  sends correct measurements to the database and API and the information was displayed on the iOS application
* The API, database and iOS application were able to display and update the correct information with fail-proof mechanism


## Authors
* ECE TEAM: Charles Thao @thaorell, Aditya Wikara @adityawikara, Shree Jayaram @ShreeJayaram, Hayato Nakamura @hayatonakamura, Kevin Sinaga @ksinaga
* ME TEAM: Esther Huynh, Yuzi Li, Jiaqian Wu, Qianqian Guo

## Acknowledgments
* Professor Alan Pisano
* Professor Osama AlShaykh
* Professor Michael Hirsch
* All EC463/464 TAs
