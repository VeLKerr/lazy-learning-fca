#include "loader.h"
#include "context.h"
#include "algorithms.h"

const char* path_train = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\train1.csv";
const char* path_test = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\test1.csv";
const char* path_save = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\results.csv";
const int num_attrs = 9;

int main(){

	
	Context context(path_train, 9, LoaderA());
	SimpleLazyAlgorithm algorithm = SimpleLazyAlgorithm(path_test, num_attrs, LoaderA(), context);
	std::vector<char> res = std::vector<char>();
	algorithm.classify(res);


	std::ofstream ofile(path_save);
	for(int i = 0; i < res.size(); i++){
		ofile << res.at(i) << std::endl;
	}

	return 0;
}