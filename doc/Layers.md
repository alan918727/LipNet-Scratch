# LipNet-Scratch



## LipNet Layers Build


## Input data

The input data is the image data numpy arrays, with 4-dimesion array, **(frames,width,heights,channels)**. For lips reading, the frames are cropped into 100*50 size.

## Network Layers
Generally, the lip reading network are build by these layers:

1. Convolutional Neural Networks(CNN) *3
2. Gated Recurrent Unit(GRU) *2
3. Linear Fully Connected Neural Networks.

The first convolutional neural network is for image processing. The CNN contains stacked convolutions operating spatially over an image. In this project, we are doing the video processing, hence the spatiotemporal Convolutions is used to implement a 4-d array with t,c,i,j

The second GRU is a type of RNN(Recuurent Neural Network). It is a simple model which is similar to LSTM(Long Short-Term Memory)	


###CNN
	 self.input_data = Input(name='the_input', shape=input_shape, dtype='float32')
	 self.zero1 = ZeroPadding3D(padding=(1, 2, 2), name='zero1')(self.input_data)
	 self.conv1 = Conv3D(32, (3, 5, 5), strides=(1, 2, 2), kernel_initializer='he_normal', name='conv1')(self.zero1)
	 self.batc1 = BatchNormalization(name='batc1')(self.conv1)
	 self.actv1 = Activation('relu', name='actv1')(self.batc1)
	 self.drop1 = SpatialDropout3D(0.5)(self.actv1)
	 self.maxp1 = MaxPooling3D(pool_size=(1, 2, 2), strides=(1, 2, 2), name='max1')(self.drop1)


self.input (75,100,50,3) -> self.zero1 (75,100,50,3) -> 

_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
the_input (InputLayer)       (None, 75, 100, 50, 3)    0         
_________________________________________________________________
zero1 (ZeroPadding3D)        (None, 77, 104, 54, 3)    0         
_________________________________________________________________
conv1 (Conv3D)               (None, 75, 50, 25, 32)    7232      
_________________________________________________________________
batc1 (BatchNormalization)   (None, 75, 50, 25, 32)    128       
_________________________________________________________________
actv1 (Activation)           (None, 75, 50, 25, 32)    0         
_________________________________________________________________
spatial_dropout3d_7 (Spatial (None, 75, 50, 25, 32)    0         
_________________________________________________________________
max1 (MaxPooling3D)          (None, 75, 25, 12, 32)    0         
_________________________________________________________________
zero2 (ZeroPadding3D)        (None, 77, 29, 16, 32)    0         
_________________________________________________________________
conv2 (Conv3D)               (None, 75, 25, 12, 64)    153664    
_________________________________________________________________
batc2 (BatchNormalization)   (None, 75, 25, 12, 64)    256       
_________________________________________________________________
actv2 (Activation)           (None, 75, 25, 12, 64)    0         
_________________________________________________________________
spatial_dropout3d_8 (Spatial (None, 75, 25, 12, 64)    0         
_________________________________________________________________
max2 (MaxPooling3D)          (None, 75, 12, 6, 64)     0         
_________________________________________________________________
zero3 (ZeroPadding3D)        (None, 77, 14, 8, 64)     0         
_________________________________________________________________
conv3 (Conv3D)               (None, 75, 12, 6, 96)     165984    
_________________________________________________________________
batc3 (BatchNormalization)   (None, 75, 12, 6, 96)     384       
_________________________________________________________________
actv3 (Activation)           (None, 75, 12, 6, 96)     0         
_________________________________________________________________
spatial_dropout3d_9 (Spatial (None, 75, 12, 6, 96)     0         
_________________________________________________________________
max3 (MaxPooling3D)          (None, 75, 6, 3, 96)      0         
_________________________________________________________________
time_distributed_3 (TimeDist (None, 75, 1728)          0         
_________________________________________________________________
bidirectional_5 (Bidirection (None, 75, 512)           3048960   
_________________________________________________________________
bidirectional_6 (Bidirection (None, 75, 512)           1181184   
_________________________________________________________________
dense1 (Dense)               (None, 75, 28)            14364     
_________________________________________________________________
softmax (Activation)         (None, 75, 28)            0         
=================================================================
Total params: 4,572,156
Trainable params: 4,571,772
Non-trainable params: 384