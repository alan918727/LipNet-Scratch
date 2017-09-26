# LipNet-Scratch


## Connectionist temporal classification (CTC)

### Definition 

CTC is a method to solve the classification problem. It is based on neural network temporal classification.

When processing audio or video data, it is hard to extract the label for **single frame**. However, if we process the data with dozens of frames, the pronunciation labels are easy to be extracted. Thus, CTC is widely used in audio processing and video processing. 

For this lip reading project, this CTC method could be used to solve the classification problem. For video processing, it is not easy to align every single label and frame. When we introduce this method, we do not need to align every label and frame. Instead, we directly output the probability of prediction sequence.

Refer to the traditional Framewise training, we need to align every phoneme to frame. The CTC method introduce the blank. In other word, it does not care the length of each phoneme. Instead, the spike sequence of phoneme are the output of CTC. Hence, 

In the old days, everyone who wanted to train neural networks used a two step procedure: (1) initialize by pre-training your neural network and (2) fine-tune your algorithm through backpropagation. Rather, the CTC loss function operates under the assumption that we don’t need to do the first pre-training step. And this small, little cost function can do this because of a big thing called data.