# cloud_class
A webapp for classifying pictures of clouds. The website is built in Flask and employs deep neural networks for classifying cloud types. The webapp used to host it is in progress.

# Dataset
A dataset of 10 cloud types was cultvated from the internet using googleimagesdownload https://github.com/hardikvasa/google-images-download and chromedriver. See scripts/download.sh for the method used. These classes were then grouped into 5 types based only on form omitting classifications that relied on elevation. Manual pruning was conducted to remove illustrations or unclear images. Duplicates were not accounted for.

# Model
The model is based on the ResNet architecture via the use of transfer learning. It is trained using the fastai api, which itself is partially built upon pytorch. The model was trained on a computer with the following specs:
* i7-4790k
* 16 GB RAM
* NVIDIA GTX 1070

**installation of GPU drivers for training the model**
https://medium.com/@pierre_guillou/how-to-install-fastai-v1-on-windows-10-ca1bc370dce4

# Webapp
The webapp is built in Flask and is designed to allow for user to submit pictures of clouds and run inferences on them. The users are able to choose from various models for their classifications.

**Instructions**
* register as a user
* make a new post and ensure to upload a picture of a cloud. Please type the name of the cloud in the post description.
* run the desired model on the photo to obtain the model's classification
