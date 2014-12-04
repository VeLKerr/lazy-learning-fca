#include "loader.h"


void SLoader::load_context(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const {
			
	char buf[100];
	std::ifstream ifile(_path);

	// skipping first line
	ifile.getline(buf, sizeof(buf) / sizeof(char) - 1);

	while(!ifile.eof()) {
		ifile.getline(buf, sizeof(buf) / sizeof(char) - 1);

		// last empty line
		if(ifile.gcount() == 0){
			break;
		}
		
		char *row = new char[num_attrs + 1];
		for(int i = 0; i < num_attrs; i++){
			row[i] = buf[2*i];
		}
		row[num_attrs] = '\0';

		if(buf[2*num_attrs] == 'p'){
			positive_context.push_back(row);
		} else {
			negative_context.push_back(row);
		}
	}

	ifile.close();
}

void SLoader::load_context(
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const {
	load_context(_path, num_attrs, positive_context, negative_context);
}

void SLoader::load_data(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &test_data,
		std::vector<const char*> &_answer) const {

	char buf[100];
	std::ifstream ifile(path);

	// skipping first line
	ifile.getline(buf, sizeof(buf) / sizeof(char) - 1);

	while(!ifile.eof()) {
		ifile.getline(buf, sizeof(buf) / sizeof(char) - 1);

		// last empty line
		if(ifile.gcount() == 0){
			break;
		}
		
		char *row = new char[num_attrs + 1];
		for(int i = 0; i < num_attrs; i++){
			row[i] = buf[2*i];
		}		
		row[num_attrs] = '\0';
		test_data.push_back(row);

		
		char *ch = new char[2];
		ch[1] = '\0';
		if(buf[2*num_attrs] == 'p'){
			ch[0] = POSITIVE_CHAR;
		} else {
			ch[0] = NEGATIVE_CHAR;
		}
		_answer.push_back(ch);
	}

	ifile.close();
}

void SLoader::load_data(
		const int num_attrs,
		std::vector<const char*> &test_data,
		std::vector<const char*> &answer) const{
	load_data(_path, num_attrs, test_data, answer);
}