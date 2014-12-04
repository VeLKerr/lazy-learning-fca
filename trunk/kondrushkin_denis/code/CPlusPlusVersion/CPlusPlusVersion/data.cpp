#include "data.h"


Data::Data(const int num_attrs, const std::vector<const char*>& data, const std::vector<const char*>& answer)
	: _num_attrs(num_attrs), _data(data), _answer(answer){}

Data::Data(const int num_attrs, Loader& loader)
	:_num_attrs(num_attrs){
	loader.load_data(num_attrs, _data, _answer);
}

Data::~Data(){
	for each(const char* ch in _data){
		delete[] ch;
	}

	for each(const char* ch in _answer){
		delete[] ch;
	}
}

int Data::get_num_attrs() const {
	return _num_attrs;
}

int Data::len() const{
	return (int)_data.size();
}

const char* Data::at(int index) const{
	return _data.at(index);
}

const char* Data::answer_at(int index) const{
	return _answer.at(index);
}