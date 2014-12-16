#include <iostream>
#include <cstring>
#include <vector>


#include "loader.h"
#include "context.h"
#include "data.h"
#include "algorithms.h"
#include "cross_validation.h"


int main(){

	const char* path_res = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\results.txt"; 

	const char* path = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\tic-tac-toe.data.txt"; 
	const int num_attrs = 9;

	//const char* path = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\connect-4.data"; 
	//const int num_attrs = 42;

	const int k = 30;

	// loads data for validation
	Data input_data = Data(num_attrs, SLoader(path));	

	// set algorithms for validation
	std::vector<Algorithm*> algorithms = std::vector<Algorithm*>();
	algorithms.push_back(new HammingDistanceLazyAlgorithm());
	algorithms.push_back(new HammDistWeightedAlgorithm());
	algorithms.push_back(new HypothesisTestingAlgorithm());
	algorithms.push_back(new HypothesisTestingWeightedAlgorithm());
	
	// validates
	CrossValidator cross_validator = CrossValidator(input_data, k);
	cross_validator.validate(path_res, algorithms);

	// frees memory
	for each (Algorithm* alg in algorithms){
		delete alg;
	}

	return 0;
}