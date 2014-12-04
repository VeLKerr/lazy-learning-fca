#pragma once


#include <iostream>
#include <fstream>
#include <vector>
#include "defines.h"


class Loader {

protected:
	const char* _path;

public:
	Loader(){};
	Loader(const char* path) : _path(path){}

public:
	virtual void load_context(
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const = 0;

	virtual void load_context(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const = 0;

	virtual void load_data(
		const int num_attrs,
		std::vector<const char*> &test_data,
		std::vector<const char*> &_answer) const = 0;
	
	virtual void load_data(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &test_data,
		std::vector<const char*> &_answer) const = 0;

};


class SLoader : public Loader {

public:
	SLoader(){};
	SLoader(const char* path) : Loader(path){}

public:
	void load_context(
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const;

	void load_context(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const;

	void load_data(
		const int num_attrs,
		std::vector<const char*> &test_data,
		std::vector<const char*> &answer) const;
	
	void load_data(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &test_data,
		std::vector<const char*> &answer) const;
};