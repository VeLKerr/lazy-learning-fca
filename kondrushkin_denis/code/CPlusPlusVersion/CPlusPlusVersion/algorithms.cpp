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

void SimpleLazyAlgorithm::classify(std::vector<char>& res) const {
	size_t n = _test_data.size();
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

/* FreqLazyAlgorithm */

FreqLazyAlgorithm::FreqLazyAlgorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context)
	:Algorithm(path, num_attrs, loader, context){}

void FreqLazyAlgorithm::classify(std::vector<char>& res) const {
	size_t n = _test_data.size();
	for(int  i = 0; i < n; i++){
		bool is_positive = true;
		bool is_negative = true;
		bool is_undefined = false;

		int positive_len = _context.positive_len();
		int negative_len = _context.negative_len();

		const char* test_intent = _test_data.at(i);
		
		int positive_freqs[100]; 
		int negative_freqs[100]; 
		for(int j = 0; j < _num_attrs; j++){
			positive_freqs[j] = 0;
			negative_freqs[j] = 0;
		}

		for(int positive_intent_index = 0; positive_intent_index < positive_len; positive_intent_index++){
			const char* positive_intent = _context.positive_at(positive_intent_index);
			for(int j = 0; j < _num_attrs; j++){
				if(test_intent[j] == positive_intent[j]){
					positive_freqs[j]++;
				}
			}
		}

		for(int negative_intent_index = 0; negative_intent_index < negative_len; negative_intent_index++){
			const char* intersect = _context.negative_intersect(negative_intent_index, test_intent);
			const char* negative_intent = _context.positive_at(negative_intent_index);
			for(int j = 0; j < _num_attrs; j++){
				if(test_intent[j] == negative_intent[j]){
					negative_freqs[j]++;
				}
			}
		}

		double positive_freq_vector[100];
		double negative_freq_vector[100];
		for(int j = 0; j < _num_attrs; j++){
			positive_freq_vector[j] = positive_freqs[j] / (positive_len + 1.0);
			negative_freq_vector[j] = negative_freqs[j] / (negative_len + 1.0);
		}

		double positive_significance = 0;
		double negative_significance = 0;
		for(int j = 0; j < _num_attrs; j++){
			positive_significance += positive_freq_vector[j] * positive_freq_vector[j];
			negative_significance += negative_freq_vector[j] * negative_freq_vector[j];
		}
		positive_significance = sqrt(positive_significance);
		negative_significance = sqrt(negative_significance);

		if(positive_significance > negative_significance){
			is_negative = false;
		} else {
			is_positive = false;
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