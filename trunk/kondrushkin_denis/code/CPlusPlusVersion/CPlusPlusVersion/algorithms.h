#pragma once
#include <vector>
#include <math.h>
#include "context.h"
#include "loader.h"


#define POSITIVE_CHAR '+'
#define NEGATIVE_CHAR '-'
#define UNDEFINED_CHAR '?'


class Algorithm{

protected:
	std::vector<const char*> _test_data;
	const Context& _context;
	const int _num_attrs;

public:
	Algorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context);
	virtual ~Algorithm();
	virtual void classify(std::vector<char>& res) const = 0;
};

class SimpleLazyAlgorithm : public Algorithm {
public:
	SimpleLazyAlgorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context);
	void classify(std::vector<char>& res) const;
};

class FreqLazyAlgorithm : public Algorithm {
public:
	FreqLazyAlgorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context);
	void classify(std::vector<char>& res) const;
};


