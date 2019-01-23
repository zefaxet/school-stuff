package edward;

class Neuron
{
	
	private double[] weights;
	private double bias;
	private double activation;
	
	void setWeights(double[] weights)
	{
		
		this.weights = weights;
		
	}
	
	double[] getWeights()
	{
		
		return this.weights;
		
	}
	
	void setActivation(double activation)
	{
		
		this.activation = activation;
		
	}
	
	double getActivation()
	{
		
		return this.activation;
		
	}
	
	void setBias(double bias)
	{
		
		this.bias = bias;
		
	}
	
	double getBias()
	{

		return this.bias;
		
	}
	
}
