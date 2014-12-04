#include "algorithms.h"


/* Base Algorithm Class */

Algorithm::Algorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context)
	:_num_attrs(num_attrs), _context(context){
	loader.load_test_data(path, num_attrs,_test_data);
}

Algorithm::~Algorithm(){
	for each(const char* ch in _test_data){
		delete[] ch;
	}
}

/* SimpleLazyAlgorithm */

SimpleLazyAlgorithm::SimpleLazyAlgorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context)
	:Algorithm(path, num_attrs, loader, context){}

void SimpleLazyAlgorithm::classify(std::vector<char>& res) {
	int n = _test_data.size();
	for(int  i = 0; i < n; i++){
		bool is_positive = true;
		bool is_negative = true;
		bool is_undefined = false;

		int positive_len = _context.positive_len();
		int negative_len = _context.negative_len();

		const char* test_intent = _test_data.at(i);

		for(int positive_intent_index = 0; positive_intent_index < positive_len; positive_intent_index++){
			const char* intersect = _context.positive_intersect(positive_intent_index, test_intent);
			if(_context.check_any_negative_inclusion(test_intent)){
				is_positive = false;
				delete[] intersect;
				break;
			}
			delete[] intersect;
		}

		for(int negative_intent_index = 0; negative_intent_index < negative_len; negative_intent_index++){
			const char* intersect = _context.negative_intersect(negative_intent_index, test_intent);
			if(_context.check_any_positive_inclusion(test_intent)){
				is_negative = false;
				delete[] intersect;
				break;
			}
			delete[] intersect;
		}

		if((is_positive && is_negative) || (!is_positive && !is_negative)){
			is_undefined = true;
		}

		if(is_undefined){
			res.push_back(UNDEFINED_CHAR);
		}else{
			res.push_back((is_positive) ? POSITIVE_CHAR : NEGATIVE_CHAR);
		}
	}
}