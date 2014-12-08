#include "algorithms.h"


/************************************** Base Algorithm Class **************************************/

Algorithm::Algorithm(){}

Algorithm::Algorithm(const Context* context, const Data* test_data)
	: _context(context), _test_data(test_data){
}

Algorithm::~Algorithm(){}

/**
	Description:
		Sets context for learning and data for classifying.
*/
void Algorithm::set(const Context* context, const Data* test_data){
	_context = context;
	_test_data = test_data;
}


//************************************** StupidLazyAlgorithm Class **************************************/

StupidLazyAlgorithm::StupidLazyAlgorithm(){}

StupidLazyAlgorithm::StupidLazyAlgorithm(const Context* context, const Data* test_data)
	:Algorithm(context, test_data){}

void StupidLazyAlgorithm::classify(std::vector<char*>& res) const {

	const int n = _test_data->len();
	for(int  i = 0; i < n; i++){
		bool is_positive = true;
		bool is_negative = true;
		bool is_undefined = false;

		const int positive_len = _context->positive_len();
		const int negative_len = _context->negative_len();

		// gets current sample's intent
		const char* test_intent = _test_data->at(i);

		// checks on inclusion into any negative training sample
		for(int positive_intent_index = 0; positive_intent_index < positive_len; positive_intent_index++){
			const char* intersect = _context->positive_intersect(positive_intent_index, test_intent);
			if(_context->check_any_negative_inclusion(test_intent)){
				is_positive = false;
				delete[] intersect;
				break;
			}
			delete[] intersect;
		}

		// checks on inclusion into any positive training sample
		for(int negative_intent_index = 0; negative_intent_index < negative_len; negative_intent_index++){
			const char* intersect = _context->negative_intersect(negative_intent_index, test_intent);
			if(_context->check_any_positive_inclusion(test_intent)){
				is_negative = false;
				delete[] intersect;
				break;
			}
			delete[] intersect;
		}

		// checks whether testing sample leads to contrudiction
		if((is_positive && is_negative) || (!is_positive && !is_negative)){
			is_undefined = true;
		}

		// sets answer for giving sample
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


//************************************** HammingDistanceLazyAlgorithm Class **************************************/

HammingDistanceLazyAlgorithm::HammingDistanceLazyAlgorithm(const Context* context, const Data* test_data)
	:Algorithm(context, test_data){}

HammingDistanceLazyAlgorithm::HammingDistanceLazyAlgorithm(){}

void HammingDistanceLazyAlgorithm::classify(std::vector<char*>& res) const {
	
	// gets number of attributes in given data
	const int _num_attrs = _test_data->get_num_attrs();		

	const int n = _test_data->len();
	for(int  i = 0; i < n; i++){
		bool is_positive = true;
		bool is_negative = true;
		bool is_undefined = false;

		const int positive_len = _context->positive_len();
		const int negative_len = _context->negative_len();

		// gets current sample's intent
		const char* test_intent = _test_data->at(i);
		
		// sets arrays for storing frequencies
		int positive_freqs[100]; 
		int negative_freqs[100]; 
		for(int j = 0; j < _num_attrs; j++){
			positive_freqs[j] = 0;
			negative_freqs[j] = 0;
		}

		// aggregates frequencies for positive training samples
		for(int positive_intent_index = 0; positive_intent_index < positive_len; positive_intent_index++){
			const char* positive_intent = _context->positive_at(positive_intent_index);
			for(int j = 0; j < _num_attrs; j++){
				if(test_intent[j] == positive_intent[j]){
					positive_freqs[j]++;
				}
			}
		}

		// aggregates frequencies for negative training samples
		for(int negative_intent_index = 0; negative_intent_index < negative_len; negative_intent_index++){
			const char* negative_intent = _context->negative_at(negative_intent_index);
			for(int j = 0; j < _num_attrs; j++){
				if(test_intent[j] == negative_intent[j]){
					negative_freqs[j]++;
				}
			}
		}

		// cumulates positive and negative significance
		double positive_significance = 0;
		double negative_significance = 0;
		for(int j = 0; j < _num_attrs; j++){
			positive_significance += positive_freqs[j] * positive_freqs[j] / ((positive_len + 1.0) * (positive_len + 1.0));
			negative_significance += negative_freqs[j] * negative_freqs[j] / ((negative_len + 1.0) * (negative_len + 1.0));
		}
		positive_significance = sqrt(positive_significance);
		negative_significance = sqrt(negative_significance);

		if(positive_significance > negative_significance){
			is_negative = false;
		} else {
			is_positive = false;
		}

		// checks whether testing sample leads to contrudiction
		if((is_positive && is_negative) || (!is_positive && !is_negative)){
			is_undefined = true;
		}

		// sets answer for giving sample
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


//************************************** HammingDistanceLazyAlgorithm Class **************************************/

HammDistWeightedAlgorithm::HammDistWeightedAlgorithm(){}

HammDistWeightedAlgorithm::HammDistWeightedAlgorithm(const Context* context, const Data* test_data)
	:Algorithm(context, test_data){}

void HammDistWeightedAlgorithm::classify(std::vector<char*>& res) const{

	// gets number of attributes in given data
	const int num_attrs = _test_data->get_num_attrs();		
	
	// sets weights for each size of inclusion
	double weights[100];
	for(long long i = 0; i < num_attrs; i++){
		if(i < 1){
			weights[i] = 0;
		} else {
			weights[i] =  pow((double)i, 45);
		}
	}

	const int n = _test_data->len();
	for(int  i = 0; i < n; i++){
		bool is_positive = true;
		bool is_negative = true;
		bool is_undefined = false;

		const int positive_len = _context->positive_len();
		const int negative_len = _context->negative_len();

		// gets current sample's intent
		const char* test_intent = _test_data->at(i);
		
		// sets arrays for storing frequencies
		double positive_freqs[100]; 
		double negative_freqs[100]; 
		for(int j = 0; j < num_attrs; j++){
			positive_freqs[j] = 0;
			negative_freqs[j] = 0;
		}

		// aggregates frequencies for positive training samples
		for(int positive_intent_index = 0; positive_intent_index < positive_len; positive_intent_index++){
			const char* positive_intent = _context->positive_at(positive_intent_index);

			int num_matches = 0;
			for(int j = 0; j < num_attrs; j++){
				if(test_intent[j] == positive_intent[j]){
					num_matches++;
				}
			}

			for(int j = 0; j < num_attrs; j++){
				if(test_intent[j] == positive_intent[j]){
					positive_freqs[j]+= num_matches * weights[num_matches];
				}
			}

		}

		// aggregates frequencies for negative training samples
		for(int negative_intent_index = 0; negative_intent_index < negative_len; negative_intent_index++){
			const char* negative_intent = _context->negative_at(negative_intent_index);

			int num_matches = 0;
			for(int j = 0; j < num_attrs; j++){
				if(test_intent[j] == negative_intent[j]){
					num_matches++;
				}
			}

			for(int j = 0; j < num_attrs; j++){
				if(test_intent[j] == negative_intent[j]){
					negative_freqs[j]+= num_matches * weights[num_matches];
				}
			}
		}

		// cumulates positive and negative significance
		double positive_significance = 0;
		double negative_significance = 0;
		for(int j = 0; j < num_attrs; j++){
			positive_significance += positive_freqs[j] * positive_freqs[j] / ((positive_len + 1.0) * (positive_len + 1.0));
			negative_significance += negative_freqs[j] * negative_freqs[j] / ((negative_len + 1.0) * (negative_len + 1.0));
		}
		positive_significance = sqrt(positive_significance);
		negative_significance = sqrt(negative_significance);

		if(positive_significance > negative_significance){
			is_negative = false;
		} else {
			is_positive = false;
		}

		// checks whether testing sample leads to contrudiction
		if((is_positive && is_negative) || (!is_positive && !is_negative)){
			is_undefined = true;
		}

		// sets answer for giving sample
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


//************************************** HypothesisTestingAlgorithm Class **************************************/

HypothesisTestingAlgorithm::HypothesisTestingAlgorithm(){}

HypothesisTestingAlgorithm::HypothesisTestingAlgorithm(const Context* context, const Data* test_data)
	:Algorithm(context, test_data){}

void HypothesisTestingAlgorithm::classify(std::vector<char*>& res) const{

	// gets number of attributes in given data
	const int num_attrs = _test_data->get_num_attrs();	

	// sets weights for each size of inclusion
	double weights[100];
	for(long long i = 0; i < num_attrs; i++){
		if(i < 1){
			weights[i] = 0;
		} else {
			weights[i] =  pow((double)i, 5);
		}
	}

	const int n = _test_data->len();
	for(int  i = 0; i < n; i++){
		bool is_positive = true;
		bool is_negative = true;
		bool is_undefined = false;

		const int positive_len = _context->positive_len();
		const int negative_len = _context->negative_len();

		// cumulates positive and negative significance
		double positive_significance = 0;
		double negative_significance = 0;

		// gets current sample's intent
		const char* test_intent = _test_data->at(i);

		// takes into account support from positive samples
		for(int positive_intent_index = 0; positive_intent_index < positive_len; positive_intent_index++){
			const char* intersect = _context->positive_intersect(positive_intent_index, test_intent);			
			int num_matches = (int)strlen(intersect);

			double positive_support = _context->positive_support(intersect);
			double negative_support = _context->negative_support(intersect);
			
			positive_support *= _context->len();
			positive_support /= _context->positive_len();

			negative_support *= _context->positive_len();
			negative_support /= _context->negative_len();			

			positive_significance += positive_support * (1 - negative_support) * weights[num_matches];

			delete[] intersect;
		}

		// takes into account support from negative samples
		for(int negative_intent_index = 0; negative_intent_index < negative_len; negative_intent_index++){
			const char* intersect = _context->negative_intersect(negative_intent_index, test_intent);
			int num_matches = (int)strlen(intersect);

			double positive_support = _context->positive_support(intersect); 
			double negative_support = _context->negative_support(intersect);
			
			positive_support *= _context->len();
			positive_support /= _context->positive_len();

			negative_support *= _context->positive_len();
			negative_support /= _context->negative_len();			

			negative_significance += negative_support * (1 - positive_support) * weights[num_matches];			

			delete[] intersect;
		}

		if(positive_significance > negative_significance){
			is_negative = false;
		} else {
			is_positive = false;
		}

		// checks whether testing sample leads to contrudiction
		if((is_positive && is_negative) || (!is_positive && !is_negative)){
			is_undefined = true;
		}

		// sets answer for giving sample
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