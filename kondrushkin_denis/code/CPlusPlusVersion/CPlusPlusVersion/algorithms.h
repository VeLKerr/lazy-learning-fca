#pragma once


#include <vector>
#include <math.h>
#include "context.h"
#include "data.h"


class Algorithm{

protected:
	const Data& _test_data;
	const Context& _context;
	const int _num_attrs;

public:
	Algorithm(const Context& context, const Data& test_data);
	virtual ~Algorithm();
	virtual void classify(std::vector<char*>& res) const = 0;
};


class SimpleLazyAlgorithm : public Algorithm {

public:
	SimpleLazyAlgorithm(const Context& context, const Data& test_data);
	void classify(std::vector<char*>& res) const;
};


class FreqLazyAlgorithm : public Algorithm {

public:
	FreqLazyAlgorithm(const Context& context, const Data& test_data);
	void classify(std::vector<char*>& res) const;
};


