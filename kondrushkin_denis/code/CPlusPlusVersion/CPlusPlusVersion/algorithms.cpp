#include "algorithms.h"


/* Base Algorithm Class */

Algorithm::Algorithm(const Context& context, const Data& test_data)
	:_num_attrs(context.get_num_attrs()), _context(context), _test_data(test_data){
}

Algorithm::~Algorithm(){}


/* SimpleLazyAlgorithm */

SimpleLazyAlgorithm::SimpleLazyAlgorithm(const Context& context, const Data& test_data)
	:Algorithm(context, test_data){}

void SimpleLazyAlgorithm::classify(std::vector<char*>& res) const {
	int n = _test_data.len();
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

		char *ch = new char[2];
		ch[1] = '\0';
		if(is_undefined){
			ch[0] = UNDEFINED_CHAR;
		}else{
			ch[0] = is_positive ? POSITIVE_CHAR : NEGATIVE_CHAR;
		}
		res.push_back(ch);
	}
}


/* FreqLazyAlgorithm */

FreqLazyAlgorithm::FreqLazyAlgorithm(const Context& context, const Data& test_data)
	:Algorithm(context, test_data){}

void FreqLazyAlgorithm::classify(std::vector<char*>& res) const {
	int n = _test_data.len();
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

		char *ch = new char[2];
		ch[1] = '\0';
		if(is_undefined){
			ch[0] = UNDEFINED_CHAR;
		}else{
			ch[0] = is_positive ? POSITIVE_CHAR : NEGATIVE_CHAR;
		}
		res.push_back(ch);
	}
}