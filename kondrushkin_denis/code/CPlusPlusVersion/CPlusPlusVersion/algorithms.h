#pragma once
#include <vector>
#include "context.h"
#include "loader.h"


#define POSITIVE_CHAR '+'
#define NEGATIVE_CHAR '-'
#define UNDEFINED_CHAR '?'


class Algorithm{

protected:
	std::vector<const char*> _test_data;
	const Context& _context;
	int _num_attrs;

public:
	Algorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context);
	virtual ~Algorithm();
	virtual void classify(std::vector<char>& res) = 0;
};

class SimpleLazyAlgorithm : public Algorithm {
public:
	SimpleLazyAlgorithm(const char* path, const int num_attrs, const Loader& loader, const Context& context);
	void classify(std::vector<char>& res);
};


