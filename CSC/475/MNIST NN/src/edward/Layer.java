package edward;

class Layer
{
	
	Neuron[] neurons;
	
	public Layer(int size)
	{
		
		this.neurons = new Neuron[size];
		for (int i = 0; i < size; i++)
		{
			
			neurons[i] = new Neuron();
			
		}
		
	}
	
	/**
	 * hold the activations of the neurons in the layer for reference in the backprop pass
	 * @param activations
	 */
	void setActivations(double[] activations)
	{
		
		if (activations.length != neurons.length)
			throw new RuntimeException(String.format("Got %d activations for %d neurons.",activations.length,neurons.length));
		
		for (int i = 0; i < neurons.length; i++)
		{
			
			neurons[i].setActivation(activations[i]);
			
		}
		
	}
	
	/**
	 * Fires the neuron
	 * @param inputs the neurons' inputs
	 * @return the activations of the neurons in the layer
	 */
	double[] activate(double[] inputs)
	{
		
		double[][] weights = new double[neurons.length][inputs.length];
		for (int x = 0; x < inputs.length; x++)
		{
			
			for (int y = 0; y < neurons.length; y++)
			{
				
				double w = neurons[y].getWeights()[x];
				weights[y][x] = w;
				
			}
			
		}
		
		//A = sigma(W . X + B)
		double[] results = Util.dot(weights, inputs);
		results = Util.sigma(Util.add(results, getBiases()));
		
		//Store activations for backprop
		setActivations(results);
		
		return results;
		
	}
	
	double[] getActivations()
	{
		
		double[] activations = new double[neurons.length];
		
		for (int i = 0; i < neurons.length; i++)
		{
			
			activations[i] = neurons[i].getActivation();
			
		}
		
		return activations;
		
	}
	
	double[] getBiases()
	{
		
		double[] biases = new double[neurons.length];
		
		for (int i = 0; i < neurons.length; i++)
		{
			
			biases[i] = neurons[i].getActivation();
			
		}
		
		return biases;
		
	}
	
	/**
	 * apply weight and bias gradients to each neuron in the layer
	 * @param biasGradientSums the vector of bias gradients
	 * @param weightGradientSums the vector of weight gradients
	 * @param eta learning rate
	 * @param batchSize
	 */
	void applyGradients(double[] biasGradientSums, double[][] weightGradientSums, float eta, int batchSize)
	{
		
		for (int i = 0; i < neurons.length ; i++)
		{
			
			Neuron neuron = neurons[i];
			double newBias = neuron.getBias() - (eta/batchSize) * biasGradientSums[i];
			neuron.setBias(newBias);
			
			double[] oldweights = neuron.getWeights();
			double[] newWeights = new double[oldweights.length];
			for (int j = 0; j < oldweights.length; j++)
			{
				
				double newWeight = oldweights[j] - (eta/batchSize) * weightGradientSums[j][i];
				newWeights[j] = newWeight;
				
			}
			
			neuron.setWeights(newWeights);
			
		}
		
	}
	
}