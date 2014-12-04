#pragma once
#include <iostream>
#include <fstream>
#include <vector>


class Loader {
public:
	virtual void load_context(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const = 0;

	virtual void load_test_data(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &test_data) const = 0;

};


class LoaderA : public Loader {

public:
	void load_context(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const;

	void load_test_data(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &test_data) const;
};