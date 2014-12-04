#include "cross_validation.h"


CrossValidator::CrossValidator(const Data& input_data, const int k)
	: _data(input_data), _k(k){

	int num_attrs = input_data.get_num_attrs();
	int n = input_data.len();
	for(int i = 0; i < k; i++){

		std::vector<const char*>* positive_context = new std::vector<const char*>();
		std::vector<const char*>* negative_context = new std::vector<const char*>();
		
		for(int j = 0; j < k; j++){
			int block_length = (j != k - 1) ? n / k : n - (k - 1) * (n / k);

			if(i == j){

				std::vector<const char*>* data = new std::vector<const char*>();
				std::vector<const char*>* answer = new std::vector<const char*>();

				for(int t = 0; t < block_length; t++){
					const char *ref_test = input_data.at(j * (n / k) + t);
					char *test = new char[num_attrs + 1];
					strcpy(test, ref_test);
					data->push_back(test);

					const char *ref_ans = input_data.answer_at(j * (n / k) + t);
					char *ans = new char[2];
					strcpy(ans, ref_ans);
					answer->push_back(ans);
				}

				Data *test_data = new Data(num_attrs, *data, *answer);
				_tests.push_back(test_data);
			} else {
				for(int t = 0; t < block_length; t++){
					const char *ref_input = input_data.at(j * (n / k) + t);
					char *input = new char[num_attrs + 1];
					strcpy(input, ref_input);

					if(input_data.answer_at(j * (n / k ) + t)[0] == POSITIVE_CHAR){
						positive_context->push_back(input);
					} else {
						negative_context->push_back(input);
					}
				}
			}
		}

		Context *context = new Context(num_attrs, *positive_context, *negative_context);
		_contexts.push_back(context);
	}
}

CrossValidator::~CrossValidator(){
	for each(const Context* context in _contexts){
		delete context;
	}

	for each(const Data* test in _tests){
		delete test;
	}
}

void CrossValidator::validate(const char* path){
	std::ofstream ofile(path);
	std::vector<char*> res;

	for(int i = 0; i < _k; i++){
		SimpleLazyAlgorithm alg1 = SimpleLazyAlgorithm(*_contexts.at(i), *_tests.at(i));
		alg1.classify(res);
		double rate1 = 0;
		for(int j = 0; j < _tests.at(i)->len(); j++){
			if(strcmp(res.at(j), _tests.at(i)->answer_at(j)) == 0){
				rate1++;
			}
		}
		rate1 /= _tests.at(i)->len();
		ofile << rate1 << '\t';
		res.clear();

		FreqLazyAlgorithm alg2 = FreqLazyAlgorithm(*_contexts.at(i), *_tests.at(i));
		alg2.classify(res);
		double rate2 = 0;
		for(int j = 0; j < _tests.at(i)->len(); j++){
			if(strcmp(res.at(j), _tests.at(i)->answer_at(j)) == 0){
				rate2++;
			}
		}
		rate2 /= _tests.at(i)->len();
		ofile << rate2 << std::endl;
		res.clear();
	}

	ofile.close();
}