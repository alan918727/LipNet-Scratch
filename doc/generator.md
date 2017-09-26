# LipNet-Scratch



## Generator Loading data

### Build Video list and align hash

 After build dataset, the training list and validation list are stored in an array.

	self.train_list = self.enumerate_videos(os.path.join(self.train_path, '*', '*'))
	self.val_list   = self.enumerate_videos(os.path.join(self.val_path, '*', '*'))

each time we shuffle the video list

	 np.random.shuffle(self.train_list)
also we got all the align hash

		def get_align(self, _id):
	        return self.align_hash[_id]



### Select batch of videos to train

There are thousands of video in the GRID corpus, which is considered as a very large dataset. Hence, we cannot load all the data at one time, it will cause memory error. In order to avoid this memory issue, we write the loading function to get batch of the data to train once.

	def get_list_safe(l, index, size):
	    ret = l[index:index+size]
	
	    # while the index+size is over the length of array, it back to the first of array and append.
	    while size - len(ret) > 0:
	        ret += l[0:size - len(ret)]
	                 
	    return ret
    
First, we try to get the training list from the dataset. These lines are to get the list of videos which are loaded to extract the video data. The size here is the batch size we choose to load each time.

    X_data_path = get_list_safe(video_list, index, size)


### Load video data from video
After we decide the list of videos to load data, we could import the video class to carry out the video data extract. The list of video data is stored in the Xdata, the padded label from align is stored in Ydata. The Xdata is normalized to range [0,1]. 

At last, this function returns the training data, which is a tuple of inputs and outputs. There are multiple inputs, which are the Xdata, Ydata, input length and label length. The output data is the dummy ctc data for dummy loss function.


 	for path in X_data_path:

            video = Video(face_predictor_path=self.face_predictor_path).from_frames(path)
            align = self.get_align(path.split('\\')[-1])
            video_unpadded_length = video.length
            X_data.append(video.data)
            Y_data.append(align.padded_label)
            label_length.append(align.label_length) 
            input_length.append(video.length) 
            source_str.append(align.sentence) # CHANGED [A] -> A, CHECK!

        source_str = np.array(source_str)
        label_length = np.array(label_length)
        input_length = np.array(input_length)
        Y_data = np.array(Y_data)
        X_data = np.array(X_data).astype(np.float32) / 255 # Normalize image data to [0,1], TODO: mean normalization over training data

        inputs = {'the_input': X_data,
                  'the_labels': Y_data,
                  'input_length': input_length,
                  'label_length': label_length,
                  'source_str': source_str  # used for visualization only
                  }
        outputs = {'ctc': np.zeros([size])}  


### Main training Fuction
In the main train code
we load the data step by step. At each iteration, we load a batch of data from the training list. Then we fit the model with our training data loaded. 

After each iteration, we clear the training data to save the memory. Hence we could load the next batch of data to train.
	
	for itr in range(0,3):
	    print('iteration {}'.format(itr))
	    data=lip_gen.get_batch(20*itr,20,train=True)
        %at here, the function get_list_safe is executed, which load the list index to index+size
	    lipnet.model.fit(x=data[0],y=data[1],batch_size=6,epochs=2,verbose=1,
	                validation_split=0.0, validation_data=None, shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0)
	    del data
