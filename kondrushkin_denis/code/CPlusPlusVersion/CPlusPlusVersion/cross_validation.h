#pragma once


#include <vector>
#include <fstream>
#include "data.h"
#include "context.h"
#include "defines.h"
#include "algorithms.h"


class CrossValidator {

private:
	const Data& _data;							// data for cross-validation
	const int _k;								// number of k-folds
	std::vector<const Context*> _contexts;		// array of k contexts
	std::vector<const Data*> _tests;			// array of k tests

public:
	CrossValidator(const Data& input_data, const int k);	// splits data into k folds
	~CrossValidator();										// frees memory

public:
	void validate(const char* path, const std::vector<Algorithm*>& algorithms);						// process validation

};