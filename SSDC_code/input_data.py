
import tensorflow as tf
import numpy as np
import scipy.io as io


""" Functions for handling data"""
class DataSet(object):

    def __init__(self, images, labels, dtype=tf.float32):


        #Convert the shape from [num_exmaple,channels, height, width]
        #to [num_exmaple, height, width, channels]
        images = np.transpose(images,(0,2,3,1))
        labels = np.transpose(labels)
        
        
        dtype = tf.as_dtype(dtype).base_dtype
        if dtype not in (tf.uint8, tf.float32):
            raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                          dtype)


        assert images.shape[0] == labels.shape[0], (
            'images.shape: %s labels.shape: %s' % (images.shape, labels.shape))
        self._num_examples = images.shape[0]

        # Convert shape from [num examples, rows, columns, depth]
        # to [num examples, rows*columns*depth] 
        images = images.reshape(images.shape[0],images.shape[1] * images.shape[2] * images.shape[3])
            
        self._images = images
        self._labels = labels
        self._epochs_completed = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = np.arange(self._num_examples)
            np.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], np.reshape(self._labels[start:end],len(self._labels[start:end]))




def read_data_sets(directory,value, dtype=tf.float32):

    images = io.loadmat(directory)[value+'_patch']
    labels = io.loadmat(directory)[value+'_labels']

    data_sets = DataSet(images, labels, dtype=dtype)

    return data_sets

