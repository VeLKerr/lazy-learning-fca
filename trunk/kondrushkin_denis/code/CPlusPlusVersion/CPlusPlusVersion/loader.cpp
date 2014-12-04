#include "loader.h"



void LoaderA::load_context(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &positive_context,
		std::vector<const char*> &negative_context) const {
			
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

		if(buf[2*num_attrs] == 'p'){
			positive_context.push_back(row);
		} else {
			negative_context.push_back(row);
		}
	}

	ifile.close();
}


void LoaderA::load_test_data(
		const char* path,
		const int num_attrs,
		std::vector<const char*> &test_data) const{

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
	}

	ifile.close();
}