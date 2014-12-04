#pragma once

#include <vector>
#include "loader.h"


#define MISS_CHAR '.'


class Context {

private:
	std::vector<const char*> _positive_context;
	std::vector<const char*> _negative_context;
	int _num_attrs;

public:
	Context(const char* path, const int num_attrs, Loader& load_contexter);
	~Context();

private:
	int len(bool positive) const;
	const char* at(bool positive, const int index) const;

	const char* intersect(bool positive, const int index, const char* object_intent) const;
	bool check_inclusion(bool positive, const int index, const char* intent) const;
	bool check_any_inclusion(bool positive, const char* intent) const;

	int score(bool positive, const char* intent) const;
	double support(bool positive, const char* intent) const;


public:
	int get_num_attrs() const;

	int positive_len() const;
	int negative_len() const;

	const char* positive_at(const int index) const;
	const char* negative_at(const int index) const;

	const char* positive_intersect(const int index, const char* object_intent) const;
	const char* negative_intersect(const int index, const char* object_intent) const;

	bool check_positive_inclusion(const int index, const char* intent) const;
	bool check_negative_inclusion(const int index, const char* intent) const;

	bool check_any_positive_inclusion(const char* intent) const;
	bool check_any_negative_inclusion(const char* intent) const;

	int positive_score(const char* intent) const;
	int negative_score(const char* intent) const;

	double positive_support(const char* intent) const;
	double negative_support(const char* intent) const;
};