#include "cross_validation.h"


/**
	Description:
		Splits data into k folds.
*/
CrossValidator::CrossValidator(const Data& input_data, const int k)
	: _data(input_data), _k(k){

	// gets number of attributes and cardinality of given data
	int num_attrs = input_data.get_num_attrs();
	int n = input_data.len();

	// creates k-folds
	for(int i = 0; i < k; i++){

		std::vector<const char*>* positive_context = new std::vector<const char*>();
		std::vector<const char*>* negative_context = new std::vector<const char*>();
		
		// fills current context for learning and sets current data for testing
		for(int j = 0; j < k; j++){

			// size of one fold: last fold has some riminder data
			int block_length = (j != k - 1) ? n / k : n - (k - 1) * (n / k);
			
			// start sample index in the current j-th block
			int start_index = j * (n / k);

			// sets current data for testing for i-fold
			if(i == j){

				std::vector<const char*>* data = new std::vector<const char*>();
				std::vector<const char*>* answer = new std::vector<const char*>();

				// fetchs data and answers for samples from current block
				for(int t = 0; t < block_length; t++){
					const char *ref_test = input_data.at(start_index + t);
					char *test = new char[num_attrs + 1];
					strcpy(test, ref_test);
					data->push_back(test);

					const char *ref_ans = input_data.answer_at(start_index + t);
					char *ans = new char[2];
					strcpy(ans, ref_ans);
					answer->push_back(ans);
				}

				Data *test_data = new Data(num_attrs, *data, *answer);
				_tests.push_back(test_data);

			} else {

				// fetches data for learning from current block
				for(int t = 0; t < block_length; t++){
					const char *ref_input = input_data.at(start_index + t);
					char *input = new char[num_attrs + 1];
					strcpy(input, ref_input);

					if(input_data.answer_at(start_index + t)[0] == POSITIVE_CHAR){
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


/**
	Description:
		Frees memory.
*/
CrossValidator::~CrossValidator(){
	for each(const Context* context in _contexts){
		delete context;
	}

	for each(const Data* test in _tests){
		delete test;
	}
}


/**
	Description:
		Process validation and stores results at given path.
*/
void CrossValidator::validate(const char* path, const std::vector<Algorithm*>& algorithms){
	
	// prints header into file
	std::ofstream ofile(path);
	for each(Algorithm* alg in algorithms){
		ofile << typeid(*alg).name() + strlen("class ") << ' ';
	}
	ofile << std::endl;

	// sets initial rates for each algorithm
	std::vector<double> total_rates = std::vector<double>();
	for each(Algorithm* alg in algorithms){
		total_rates.push_back(0);
	}

	// processes k-fold validation
	for(int i = 0; i < _k; i++){
		std::vector<char*> res;

		// validates each algorithm
		for (int j = 0; j < algorithms.size(); j++){
			algorithms[j]->set(_contexts.at(i), _tests.at(i));
			algorithms[j]->classify(res);

			double rate = 0;
			for(int t = 0; t < _tests.at(i)->len(); t++){
				if(strcmp(res.at(t), _tests.at(i)->answer_at(t)) == 0){
					rate++;
				}
			}
			rate /= _tests.at(i)->len();
			total_rates[j] += rate;

			ofile << rate << '\t';
			res.clear();
		}

		ofile << std::endl;
	}

	// prints average rate for each algorithm
	ofile << std::endl;
	for each(double rate in total_rates){
		ofile << rate / _k << '\t';
	}

	ofile.close();
}