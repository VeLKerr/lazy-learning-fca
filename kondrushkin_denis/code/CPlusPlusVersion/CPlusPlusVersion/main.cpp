#include <iostream>
#include <cstring>
#include "loader.h"
#include "context.h"
#include "data.h"
#include "algorithms.h"
#include "cross_validation.h"


int main(){
	const char* path = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\tic-tac-toe.data.txt"; 
	const char* path_res = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\results.txt"; 
	const int num_attrs = 9;
	const int k = 30;

	Data input_data = Data(num_attrs, SLoader(path));
	
	CrossValidator cross_validator = CrossValidator(input_data, k);

	cross_validator.validate(path_res);


	return 0;
}