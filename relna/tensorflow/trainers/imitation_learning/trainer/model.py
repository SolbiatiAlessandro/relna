import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import logging
import os

class Model():
    """
    """

    def _create_model(self):
        """
        main tensorflow model
        returns: input placeholder, output placeholder, output prediction
        """
        input_ph = tf.placeholder(dtype=tf.float32, shape=[None, 44]) # [None, 1] is because is 1D array
        output_ph = tf.placeholder(dtype=tf.float32, shape=[None, 17])
        
        W0 = tf.get_variable(name='W0', shape=[44, 30], initializer = tf.contrib.layers.variance_scaling_initializer())
        W1 = tf.get_variable(name='W1', shape=[30, 23], initializer = tf.contrib.layers.variance_scaling_initializer())
        W2 = tf.get_variable(name='W2', shape=[23, 17], initializer = tf.contrib.layers.variance_scaling_initializer())
        
        
        b0 = tf.get_variable(name='b0', shape=[30], initializer = tf.constant_initializer(0))
        b1 = tf.get_variable(name='b1', shape=[23], initializer = tf.constant_initializer(0))
        b2 = tf.get_variable(name='b2', shape=[17], initializer = tf.constant_initializer(0))
        
        weights = [W0, W1, W2]
        biases = [b0, b1, b2]
        activations = [tf.nn.relu, tf.nn.relu, None]
        
        layer = input_ph
        for W, b, activation in zip(weights, biases, activations):
            layer = tf.matmul(layer, W) + b
            if activation is not None:
                layer = activation(layer)
                
        output_pred = layer
        return input_ph, output_ph, output_pred

    def _new_tf_session(self):
        """
        reset tf session, returns new session
        """
        try:
            sess.close()
        except:
            pass
        tf.reset_default_graph()
        return tf.Session()

    def train(self, 
            X_train, 
            y_train, 
            steps=10000, 
            batch_size=32, 
            save_folder='/tmp/'
            ):
        """
        train and save model
        returns: train_mse
        """
        save_folder = os.path.join(save_folder, "model.ckpt")
        sess = self._new_tf_session()
        input_ph, output_ph, output_pred = self._create_model()

        # this is the mean square error
        mse = tf.reduce_mean(0.5 * tf.square(output_pred - output_ph)) 

        # this is an operation that pereform gradient descent
        opt = tf.train.AdamOptimizer().minimize(mse) 

        sess.run(tf.global_variables_initializer())

        # save weight as the training goes on
        saver = tf.train.Saver() 

        #training
        training_mse = []
        for training_step in range(steps):
            #random batch
            indices = np.random.randint(low = 0, high = len(X_train), size = batch_size)
            input_batch = X_train[indices]
            output_batch = y_train[indices]
            
            # run optimizer and get mse
            _, mse_run = sess.run([opt, mse], feed_dict={input_ph: input_batch, output_ph: output_batch})
            
            training_mse.append(mse_run)
            if training_step % 1000 == 0:
                logging.warning('[model.py]:train - {0:04d} mse : {1:.3f}'.format(training_step, mse_run))
                # saver.save(sess, save_folder)

        logging.warning('[model.py]:train - training complete')
        saver.save(sess, save_folder)
        logging.warning('[model.py]:train - model saved to {}'.format(save_folder))
        return training_mse

    @staticmethod
    def visualize_train_mse(training_mse):
        plt.figure(figsize=(15,10))
        plt.plot(training_mse)
        plt.show()

    def predict(self,
            X_predict,
            save_folder="/tmp/",
            ):
        """
        predict loading model from save_folder
        """
        save_folder = os.path.join(save_folder, "model.ckpt")
        sess = self._new_tf_session()
        input_ph, output_ph, output_pred = self._create_model()
        saver = tf.train.Saver() 
        logging.warning('[model.py]:predict - loading model from {}'.format(save_folder))
        saver.restore(sess, save_folder)

        output_pred_run = sess.run(output_pred, feed_dict={input_ph: X_predict[0].reshape((1,44))})
        return output_pred_run

    @staticmethod
    def evaluate_predictions(
            y_predict,
            y_labels
            ):
        mse = ((y_predict - y_labels)**2).mean(axis=None)
        return mse
