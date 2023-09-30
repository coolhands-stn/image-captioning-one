# Flickr8K Dataset

We are using the  Flickr8k dataset. ( https://www.ijcai.org/Proceedings/15/Papers/593.pdf )
The Flickr8k is a good choice because it contains 5-captions per image, more data for a smaller download.
The dataset consists of ( image, caption )  pairs

The dataset returns (input, label) pairs suitable for training with keras.
The inputs are (images, input_tokens) pairs. The images have been processed with the feature-extractor model.
For each location in the input_tokens the model looks at the text so far and tries to predict the next which is lined up at the same location in the labels.
