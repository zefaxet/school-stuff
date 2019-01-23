package edward;

public class Util
{
	
	/**
	 * This method produces the 1D dot product of a 2D and a 1D vector
	 * @param weights Weight Vector
	 * @param inputs Input Vector
	 * @return The cross product result
	 * INNER IS PRIMARY
	 */
	static double[] dot(double[][] weights, double[] inputs)
	{
			
		double[] product = new double[weights.length];
		
		for(int i = 0; i < product.length; i++)
		{
			
			double[] vw = weights[i];
			product[i] = dot(vw, inputs);
		
		}
		
		return product;
	
	}
	
	/**
	 * This method produces the dot product resultant of a 1D weight vector and a 1D input vector
	 * @param weights Weight vector
	 * @param inputs Input vector
	 * @return The cross product result
	 */
	static double dot(double[] weights, double[] inputs)
	{
		
		if (weights.length != inputs.length)
			throw new RuntimeException(String.format("Arrays of different lengths: %d %d",weights.length,inputs.length));
		
		double result = 0;
		
		for(int i = 0; i < weights.length; i++)
		{
			
			result += weights[i] * inputs[i];
			
		}
		
		return result;
		
	}
	
	/**
	 * sigma function
	 * @param z
	 * @return
	 */
	static double sigma(double z)
	{
		
		return 1 / (1 + Math.exp(-z));
	
	}
	
	/**
	 * Perform the sigma function of an array of z-values
	 * @param z sigma function input
	 * @return sigma(z) for each element
	 */
	static double[] sigma(double[] z)
	{
		
		double[] result = new double[z.length];
		
		for (int i = 0; i < z.length; i++)
		{
			
			result[i] = sigma(z[i]);
			
		}
		
		return result;
		
	}
	
	/**
	 * Adds 2 1d arrays together
	 * @param a
	 * @param b
	 * @return the 1d sum
	 */
	static double[] add(double[] a, double[] b)
	{
		
		if (a == null)
		{
			
			a = new double[b.length];
			for (int i = 0; i < a.length; i++)
			{
				
				a[i] = 0;
				
			}
			
		}
		if (b == null)
		{
			
			b = new double[a.length];
			for (int i = 0; i < b.length; i++)
			{
				
				b[i] = 0;
				
			}
			
		}
		
		if (a.length != b.length)
			throw new RuntimeException("Arrays of different sizes.");
		
		//TODO maybe skip out on the new array creation to save some flops
		double[] result = new double[a.length];
		
		for (int i = 0; i < a.length; i++)
		{
			
			result[i] = a[i] + b[i];
			
		}
		
		return result;
		
	}
	
	/**
	 * Adds two 2-d arrays of the same size
	 * @param a
	 * @param b
	 * @return the 2d sum
	 */
	static double[][] add(double[][] a, double[][] b)
	{
		if (a == null)
		{
			
			a = b.clone();
			for (int y = 0; y < a[0].length; y++)
			{
				
				for (int x = 0; x < a.length; x++)
				{
					
					a[x][y] = 0;
					
				}
				
			}
			
		}
		
		if (b == null)
		{
			
			b = a.clone();
			for (int y = 0; y < b[0].length; y++)
			{
				
				for (int x = 0; x < b.length; x++)
				{
					
					b[x][y] = 0;
					
				}
				
			}
			
		}
		
		if (a.length != b.length)
			throw new RuntimeException(String.format("Arrays of different lengths: %d %d",a.length,b.length));
		
		double[][] result = a.clone();
		
		for (int i = 0; i < a.length; i++)
		{
			
			result[i] = add(a[i],b[i]);
			
		}
		
		return result;
		
	}
	
	/**
	 * this was just for getting the random numbers for weights and biases
	 * felt better to not type that out somewhere else
	 * @return
	 */
	static double rand()
	{
		
		return Math.random() * 2 - 1;
		
	}
	
	/**
	 * Computes the bias gradients for each neuron in the output layer
	 * @param activations actual values in the output layer
	 * @param expected expected values from the output layer
	 * @return the set of bias gradients for each neuron
	 */
	static double[] computeOutputBiasGradients(double[] activations, double[] expected)
	{
		
		double[] result = new double[activations.length];
		
		for (int i = 0; i < activations.length; i ++)
		{
		
			double activation = activations[i];
			result[i] = (activation - expected[i]) * activation * (1 - activation);
		
		}
		
		return result;
		
	}
	
	/**
	 * Computes the set of bias gradients for neurons in a hidden layer
	 * @param activations activations of the layer neurons
	 * @param weights set weights from this layer to the next
	 * @param biases bias gradients from the layer in front
	 * @return the set of bias gradients for an internal layer
	 */
	static double[] computeInnerBiasGradients(double[] activations, double[][] weights, double[] biases)
	{
		
		double[] result = new double[activations.length];
	
		double[] wbdot = dot(weights, biases);
		for (int i = 0; i < wbdot.length; i++)
		{
		
			result[i] = wbdot[i] * activations[i] * (1 - activations[i]);
		
		}
		
		return result;
	
	}
	
	/**
	 * Computes the set of weight gradients for a layer's nodes
	 * @param activations activations of the previous layer
	 * @param context used for debugging
	 * @param biasGradients the bias gradients for the neurons in the layer
	 * @return the set of weight gradients for each neuron in the layer
	 */
	static double[][] computeWeightGradients(double[] activations, Layer context, double[] biasGradients)
	{
		
		if (activations.length != context.neurons[0].getWeights().length)
			throw new RuntimeException("Arrays of different sizes.");
		
		//There should be a weight for every activation
		double[][] result = new double[activations.length][biasGradients.length];
		
		for (int y = 0 ; y < biasGradients.length; y++)
		{
			
			for (int x = 0; x < activations.length; x++)
			{
				
				result[x][y] = activations[x] * biasGradients.length;
				
			}
			
		}
		
		return result;
		
	}
	
}
