#include "loader.h"
#include "context.h"
#include "algorithms.h"

const char* path_train = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\train9.csv";
const char* path_test = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\test7.csv";
const char* path_save = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\results_simple.csv";
const char* path_save_freq = "D:\\COURSES\\HSE\\Ordered Sets\\HW\\lazy-learning-fca\\kondrushkin_denis\\data\\results_freq.csv";
const int num_attrs = 9;

void read_correct_answer(const char* path, const int num_attrs, std::vector<char> &answer){
	char buf[100];
	std::ifstream ifile(path);

	// skipping first line
	ifile.getline(buf, sizeof(buf) / sizeof(char) - 1);

	while(!ifile.eof()) {
		ifile.getline(buf, sizeof(buf) / sizeof(char) - 1);

		// last empty line
		if(ifile.gcount() == 0){
			break;
		}

		if(buf[2*num_attrs] == 'p'){
			answer.push_back(POSITIVE_CHAR);
		} else {
			answer.push_back(NEGATIVE_CHAR);
		}
	}

	ifile.close();
}

int main(){
	std::vector<char> res = std::vector<char>();
	std::vector<char> ans = std::vector<char>();
	Context context(path_train, 9, LoaderA());
	read_correct_answer(path_test, num_attrs, ans);

	
	Algorithm& algorithm = SimpleLazyAlgorithm(path_test, num_attrs, LoaderA(), context);
	algorithm.classify(res);
	std::ofstream ofile(path_save);
	for(int i = 0; i < res.size(); i++){
		ofile << res.at(i) << std::endl;
	}
	

	res.clear();
	Algorithm& algorithm_freq = FreqLazyAlgorithm(path_test, num_attrs, LoaderA(), context);
	algorithm_freq.classify(res);
	std::ofstream ofile_freq(path_save_freq);
	double rate = 0;
	for(int i = 0; i < res.size(); i++){
		ofile_freq << res.at(i) << ' ' << ans.at(i) <<std::endl;
		if(res.at(i) == ans.at(i)){
			rate++;
		}
	}
	rate /= ans.size();
	ofile_freq << rate;

	return 0;
}