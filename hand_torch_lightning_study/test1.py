import os
import urllib.request

mnist_url = "https://github.com/mnielsen/neural-networks-and-deep-learning/raw/master/data/mnist.pkl.gz"
mnist_filename = "mnist.pkl.gz"

if not os.path.exists(mnist_filename):
    print("Downloading MNIST data...")
    urllib.request.urlretrieve(mnist_url, mnist_filename)
    print("Download complete.")
else:
    print("MNIST data already exists.")

import gzip
import pickle   
import numpy as np

np.random.seed(42)

def load_data():

    with gzip.open("mnist.pkl.gz", "rb") as f:
        training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    return (training_data, validation_data, test_data)


def one_hot(j):
 
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

def data_builder():

  
    tr_d, va_d, te_d = load_data()

    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [one_hot(y) for y in tr_d[1]]
    training_data = list(zip(training_inputs, training_results))

    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = list(zip(validation_inputs, va_d[1]))

    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = list(zip(test_inputs, te_d[1]))

    return (training_data, validation_data, test_data)

def forward_pass(sample,W1,W2,B1,B2):

    z1 = (W1 @ sample) + B1
    a1 = a1 = 1.0 / (1.0 + np.exp(-z1)) 

    z2 = (W2 @ a1) + B2
    a2 = a2 = 1.0 / (1.0 + np.exp(-z2))

    return (a2,a1,z2,z1)

def backward_pass(cost,a2,a1,sample,W2):

    sigmoid_derivative_2 = a2 * (1 - a2)

    Delta_2 = cost*sigmoid_derivative_2 #(10,1)

    Nabla_B2 = Delta_2
    Nabla_W2 = Delta_2 @ a1.T  #(10,100)

    sigmoid_derivative_1 = a1 * (1- a1)

    Delta_1 = (W2.T @ Delta_2) * sigmoid_derivative_1 #(100,1)

    Nabla_B1 = Delta_1
    Nabla_W1 = Delta_1 @ sample.T #(100,784)

    return (Nabla_W1,Nabla_W2,Nabla_B1,Nabla_B2)

def batch_update(W1,W2,B1,B2,Nabla_W1,Nabla_W2,Nabla_B1,Nabla_B2,Learn_rate):

    W2 = W2 - Learn_rate * Nabla_W2
    B2 = B2 - Learn_rate * Nabla_B2
    W1 = W1 - Learn_rate * Nabla_W1
    B1 = B1 - Learn_rate * Nabla_B1

    return (W1,W2,B1,B2)

def Network(input_layer,hidden_layer,output_layer):
    training_data, validation_data, test_data = data_builder()
    W1 = np.random.randn(hidden_layer,input_layer)
    W2 = np.random.randn(output_layer,hidden_layer)
    B1 = np.random.randn(hidden_layer,1)
    B2 = np.random.randn(output_layer,1)
    #print(W1.shape)
    #print(B1.shape)
    #print(W2.shape)
    #print(B2.shape)

    Batch_Nabla_W1 = np.zeros_like(W1)
    Batch_Nabla_W2 = np.zeros_like(W2)
    Batch_Nabla_B1 = np.zeros_like(B1)
    Batch_Nabla_B2 = np.zeros_like(B2)

    """
    weights and biases have a mean = 0 and variance = 1
    """

    Epochs = 60
    Learn_rate = 2

    Batch_size = 16

    counter = 1

    val_counter = 0

    correct = 0
    no_improvement = 0
    patience = 8
    cost_scalar = 0
    cost_val = 0
    
    cost_max = float('inf')
    cost_min = float('inf')

    for epoch in range(Epochs):

        np.random.shuffle(training_data)

        for sample , output in training_data : 

            counter+=1
            
            a2,a1,z2,z1 = forward_pass(sample,W1,W2,B1,B2)

            cost = a2 - output

            if np.argmax(a2) == np.argmax(output) :
                correct += 1
            

            cost_scalar = + cost_scalar + 0.5 * np.linalg.norm(a2 - output)**2

            Nabla_W1,Nabla_W2,Nabla_B1,Nabla_B2 = backward_pass(cost,a2,a1,sample,W2)

            Batch_Nabla_W1 = Batch_Nabla_W1 + Nabla_W1
            Batch_Nabla_W2 = Batch_Nabla_W2 + Nabla_W2
            Batch_Nabla_B1 = Batch_Nabla_B1 + Nabla_B1
            Batch_Nabla_B2 = Batch_Nabla_B2 + Nabla_B2


            if counter % Batch_size == 0 :

                W1,W2,B1,B2 = batch_update(W1,W2,B1,B2,(Batch_Nabla_W1/Batch_size) ,(Batch_Nabla_W2/Batch_size), (Batch_Nabla_B1/Batch_size) , (Batch_Nabla_B2 /Batch_size),Learn_rate)

                Batch_Nabla_W1.fill(0)
                Batch_Nabla_W2.fill(0)
                Batch_Nabla_B1.fill(0)
                Batch_Nabla_B2.fill(0)

        
        if len(training_data) - counter != 0 :

            rem = len(training_data) - counter

            W1,W2,B1,B2 = batch_update(W1,W2,B1,B2,(Batch_Nabla_W1/rem) ,(Batch_Nabla_W2/rem), (Batch_Nabla_B1/rem) , (Batch_Nabla_B2 /rem),Learn_rate)

            Batch_Nabla_W1.fill(0)
            Batch_Nabla_W2.fill(0)
            Batch_Nabla_B1.fill(0)
            Batch_Nabla_B2.fill(0)
        
        counter = 0

        cost_scalar = cost_scalar/len(training_data)

        print(f"cost = {cost_scalar}")
        
        print(f"epoch  = {epoch} - Accuracy = {((correct/50000)*100):.2f} % ")
        correct = 0

        for val_image , val_label in validation_data:

            v2,v1,z2,z1 = forward_pass(val_image,W1,W2,B1,B2)

            if np.argmax(v2) == val_label:

                val_counter +=1

            cost_val_mat = v2 - one_hot(val_label)

            cost_val = cost_val + 0.5 * np.linalg.norm(cost_val_mat)**2
        

        val_mean = cost_val/len(validation_data)
        
        print(f"  Validation accuracy = {((val_counter/10000)*100) : .5f} % ")
        print(f"  Validation cost = {val_mean : .5f}  ")
       

        
        if val_mean < cost_min:

            print(f" Cost improved from {cost_min:.5f} to {val_mean:.5f} \n ")

            cost_min = val_mean
            no_improvement = 0
        
        else :

            print(f" Cost didnt improve from {cost_min:.5f} \n ")
            no_improvement += 1
        
        if no_improvement == patience:

            print("Early stopping")

            break
        
        cost_scalar = 0
        val_counter = 0
        cost_val = 0
        val_mean = 0

if __name__ == "__main__":
    Network(784,50,10)




