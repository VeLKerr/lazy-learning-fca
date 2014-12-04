#pragma once

#include <vector>
#include  "loader.h"


class Data {

private:
	std::vector<const char*> _data;
	std::vector<const char*> _answer;
	const int _num_attrs;

public:
	Data(const int num_attrs, const std::vector<const char*>& data, const std::vector<const char*>& answer);
	Data(const int num_attrs, Loader& loader);
	~Data();

public:
	int get_num_attrs() const;
	int len() const;
	const char* at(int index) const;
	const char* answer_at(int index) const;
};