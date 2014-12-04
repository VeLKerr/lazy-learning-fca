#pragma once


#include <vector>
#include <fstream>
#include "data.h"
#include "context.h"
#include "defines.h"
#include "algorithms.h"


class CrossValidator {

private:
	const Data& _data;
	const int _k;
	std::vector<const Context*> _contexts;
	std::vector<const Data*> _tests;

public:
	CrossValidator(const Data& input_data, const int k);
	~CrossValidator();

public:
	void validate(const char* path);

};