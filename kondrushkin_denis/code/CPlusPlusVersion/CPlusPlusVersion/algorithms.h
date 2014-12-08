#pragma once


#include <vector>
#include <math.h>
#include "context.h"
#include "data.h"


class Algorithm{

protected:
	const Context* _context;	// context for learning
	const Data* _test_data;		// data for testing

public:
	Algorithm();
	Algorithm(const Context* context, const Data* test_data);
	virtual ~Algorithm();

public:
	void set(const Context* context, const Data* test_data);	// sets context for learning and data for classifying.
	virtual void classify(std::vector<char*>& res) const = 0;	// classifies test data
};


class StupidLazyAlgorithm : public Algorithm {

public:
	StupidLazyAlgorithm();
	StupidLazyAlgorithm(const Context* context, const Data* test_data);
	void classify(std::vector<char*>& res) const;
};


class HammingDistanceLazyAlgorithm : public Algorithm {

public:
	HammingDistanceLazyAlgorithm();
	HammingDistanceLazyAlgorithm(const Context* context, const Data* test_data);
	void classify(std::vector<char*>& res) const;
};


class HammDistWeightedAlgorithm : public Algorithm {

public:
	HammDistWeightedAlgorithm();
	HammDistWeightedAlgorithm(const Context* context, const Data* test_data);
	void classify(std::vector<char*>& res) const;
};


