package edward;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.*;


public class SigNet
{
	
	private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) throws IOException, URISyntaxException
	{
		
		SigNet network = new SigNet(2);
		network.train();
    
    }
    
    final float ETA = 3F; //TODO changing this was suggested (0.3)
    final int BATCH_SIZE = 10;
    final int EPOCHS = 3;
    
    private Layer[] layers;
    
    private SigNet(int nLayers)
	{
		
		layers = new Layer[nLayers];
		
		layers[0] = new Layer(30);
		layers[1] = new Layer(10);
		
	}
	
	/**
	 * Completes a full feed-forward pass of the network
	 * @param inputs the activations of the first (input) layer
	 * @return the activations of the last (output) layer
	 */
	double[] feedForward(double[] inputs)
	{

		//Simply takes the results of one layer and passes it to the next
		for (Layer layer: layers)
		{
			
			inputs = layer.activate(inputs);
			
		}
		
		return inputs;
		
	}
	
	/**
	 * Trains the network using the mnist training data set
	 */
	private void train() throws IOException, URISyntaxException
	{
		
		//Load the list of training samples
		URL url = getClass().getClassLoader().getResource("resources/mnist_train.csv");
		FileReader reader = new FileReader(url.toURI().getPath());
		BufferedReader buffer = new BufferedReader(reader);
		List<double[]> images = new ArrayList<>();
		//Read all lines into an arraylist
		while (buffer.ready())
		{
			
			String image = buffer.readLine();
			String[] bytes = image.split(",");
			double[] conversion = new double[785];
			//then resolve the numerical values
			for (int i = 0; i < bytes.length; i++)
			{
				
				conversion[i] = Double.valueOf(bytes[i]);
				
				if (i != 0)
					conversion[i] = conversion[i] / 255;
				
			}
			
			images.add(conversion);
			
		}
		//
		
		setRandomWeights();
		
		//Begin epochs
		for (int i = 0; i < EPOCHS; i++)
		{
			
			int correct = 0;
			
			System.out.println(String.format("Beginning epoch %d",i+1));
			
			int index = 0;
			while (index < images.size())
			{
				
				double[] outerBiasGradientSum = null;
				double[][] outerWeightGradientSum = null;
				double[] innerBiasGradientSum = null;
				double[][] innerWeightGradientSum = null;
			
				Collections.shuffle(images);
				int curri = index;
				//go through the data a batch at a atime
				while(index < curri + BATCH_SIZE)
				{
					
					double[] image = images.get(index);
					int expectation = (int) image[0];
					//prepare the one-hot vector with the expected value
					double[] onehot = {0,0,0,0,0,0,0,0,0,0}; onehot[expectation] = 1; //TODO try doing error with onehot and raw result
					//strip out the leading entry, the identifier
					image = Arrays.copyOfRange(image, 1, image.length); //TODO this is wasteful, figure something better out
					//feed forward pass
					double[] result = feedForward(image);
					
					//check if network chose correctly for stats
					double max = -1;
					int maxindex = 0;
					for (int j = 0; j < result.length; j++)
					{
						
						if (result[j] > max)
						{
							
							max = result[j];
							maxindex = j;
							
						}
						
					}
					
					//tick stats
					if (maxindex == expectation)
						correct += 1;
					
					//begin backprop
					double[][] weights = new double[layers[0].neurons.length][layers[1].neurons.length];
					//get weights for inner layer bias gradient calculation
					for (int x = 0; x < layers[0].neurons.length; x++)
					{
						
						for (int y = 0; y < layers[1].neurons.length; y++)
						{
							
							weights[x][y] = layers[1].neurons[y].getWeights()[x];
							
						}
						
					}
					
					//find bias gradients of inner and outer layers
					double[] outputBiasGradients = Util.computeOutputBiasGradients(result, onehot);
					double[] innerBiasGradients = Util.computeInnerBiasGradients(layers[0].getActivations(),
							weights, outputBiasGradients);
					
					//find weight gradients of inner and outer layers
					double[][] outputWeightGradients = Util.computeWeightGradients(layers[0].getActivations(), layers[1], outputBiasGradients);
					double[][] internalWeightGradients = Util.computeWeightGradients(image, layers[0], innerBiasGradients);
					//contribute to sum for after mini-batch
					outerBiasGradientSum = Util.add(outerBiasGradientSum,outputBiasGradients);
					innerBiasGradientSum = Util.add(innerBiasGradientSum,innerBiasGradients);
					outerWeightGradientSum = Util.add(outputWeightGradients, outerWeightGradientSum);
					innerWeightGradientSum = Util.add(innerWeightGradientSum, internalWeightGradients);
					
					index++;
					
				}
				
				System.out.println(String.format("Current index is %d", index));
				
				//apply weight and bias gradients
				layers[0].applyGradients(innerBiasGradientSum, innerWeightGradientSum, ETA, BATCH_SIZE);
				layers[1].applyGradients(outerBiasGradientSum, outerWeightGradientSum, ETA, BATCH_SIZE);
				
			}
			
			double accuracy = (double) correct /  (double) images.size();
			System.out.print("EPOCH ACCURACY: ");
			System.out.println(accuracy);
			System.out.println(correct);
			
		}
		
	}
	
	/**
	 * Crawl through the network and set every weight and bias to a value between -1 and 1
	 */
	void setRandomWeights()
	{
		
		//TODO this entire process needs to be generified
		for (Layer layer: layers)
		{
			
			for (Neuron neuron: layer.neurons)
			{
				
				double[] weights;
				int in;
				
				neuron.setBias(Util.rand());
				if (layer.equals(layers[0]))
					in = 784;
				else
					in = 30;
				weights = new double[in];
				for (int i = 0; i < in; i ++)
				{
					
					weights[i] = Util.rand();
					
				}
				
				neuron.setWeights(weights);
			}
			
		}
		
	}
	
}

