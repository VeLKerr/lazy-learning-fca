#include "context.h"

/* constructors & destructors */

Context::Context(
	const int num_attrs,
	const std::vector<const char*>& positive_context,
	const std::vector<const char*>& negative_context)
	: _num_attrs(num_attrs), _positive_context(positive_context), _negative_context(negative_context){}

Context::Context(const int num_attrs, Loader& loader)
	:_num_attrs(num_attrs){
	loader.load_context(num_attrs, _positive_context, _negative_context);
}

Context::~Context(){
	for each(const char* ch in _positive_context){
		delete[] ch;
	}
	for each(const char* ch in _negative_context){
		delete[] ch;
	}
}


/* private */

int Context::len(bool positive) const{
	if(positive){
		return (int)_positive_context.size();
	} else {
		return (int)_negative_context.size();
	}
}

const char* Context::at(bool positive, const int index) const{
	if(positive){
		return _positive_context.at(index);
	} else {
		return _negative_context.at(index);
	}
}

const char* Context::intersect(bool positive, const int index, const char* object_intent) const{
	const char* ref_intent;
	if(positive){
		ref_intent = _positive_context.at(index);
	} else {
		ref_intent = _negative_context.at(index);
	}

	char* intersection = new char[_num_attrs + 1];
	for(int i = 0; i < _num_attrs; i++){
		char och = object_intent[i];
		char rch = ref_intent[i];
		intersection[i] = (och == rch) ? och : MISS_CHAR;
	}
	intersection[_num_attrs] = '\0';

	return intersection;
}

bool Context::check_inclusion(bool positive, const int index, const char* intent) const{
	const char* ref_intent;
	if(positive){
		ref_intent = _positive_context.at(index);
	} else {
		ref_intent = _negative_context.at(index);
	}
	
	int missed_num = 0;
	for(int i = 0; i < _num_attrs; i++){
		if(intent[i] == MISS_CHAR){
			missed_num++;
			continue;
		} else if(intent[i] != ref_intent[i]){
			return false;
		}
	}

	return missed_num != _num_attrs;
}

bool Context::check_any_inclusion(bool positive, const char* intent) const{
	int n = len(positive);
	for(int i = 0; i < n; i++){
		if(check_inclusion(positive, i, intent)){
			return true;
		}
	}

	return false;
}

int Context::score(bool positive, const char* intent) const{
	int score = 0;
	int n = len(positive);
	for(int i = 0; i < n; i++){
		score += check_inclusion(positive, i, intent) ? 1 : 0;
	}

	return score;
}

double Context::support(bool positive, const char* intent) const{
	double n = len(positive);
	return score(positive, intent) / n;
}


/* public */

int Context::get_num_attrs() const
{
	return _num_attrs;
}

int Context::positive_len() const{
	return len(true);
}

int Context::negative_len() const{
	return len(false);
}

const char* Context::positive_at(const int index) const
{
	return at(true, index);
}

const char* Context::negative_at(const int index) const {
	return at(false, index);
}

const char* Context::positive_intersect(const int index, const char* object_intent) const{
	return intersect(true, index, object_intent);
}

const char* Context::negative_intersect(const int index, const char* object_intent) const{
	return intersect(false, index, object_intent);
}

bool Context::check_positive_inclusion(const int index, const char* intent) const {
	return check_inclusion(true, index, intent);
}

bool Context::check_negative_inclusion(const int index, const char* intent) const {
	return check_inclusion(false, index, intent);
}

bool Context::check_any_positive_inclusion(const char* intent) const{
	return check_any_inclusion(true, intent);
}

bool Context::check_any_negative_inclusion(const char* intent) const{
	return check_any_inclusion(false, intent);
}

int Context::positive_score(const char* intent) const{
	return score(true, intent);
}

int Context::negative_score(const char* intent) const{
	return score(false, intent);
}

double Context::positive_support(const char* intent) const{
	return support(true, intent);
}

double Context::negative_support(const char* intent) const{
	return support(false, intent);
}