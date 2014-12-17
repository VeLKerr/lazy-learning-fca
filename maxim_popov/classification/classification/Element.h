#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <cassert>

class Element
{
private:
    size_t quality_;
    std::vector<size_t> attributes_;
public:
    Element() : attributes_(std::vector<size_t>(6)) {}

    void setBuying(const std::string& str)
    {
        if (str == "low") {
            attributes_[0] = 0;
        } else if (str == "med") {
            attributes_[0] = 1;
        } else if (str == "high") {
            attributes_[0] = 2;
        } else if (str == "vhigh") {
            attributes_[0] = 3;
        } else {
            assert(false);
        }
    }

    void setMaint(const std::string& str)
    {
        if (str == "low") {
            attributes_[1] = 0;
        } else if (str == "med") {
            attributes_[1] = 1;
        } else if (str == "high") {
            attributes_[1] = 2;
        } else if (str == "vhigh") {
            attributes_[1] = 3;
        } else {
            assert(false);
        }
    }

    void setDoors(const std::string& str)
    {
        if (str == "2") {
            attributes_[2] = 0;
        } else if (str == "3") {
            attributes_[2] = 1;
        } else if (str == "4") {
            attributes_[2] = 2;
        } else if (str == "5more") {
            attributes_[2] = 3;
        } else {
            assert(false);
        }
    }

    void setPersons(const std::string& str)
    {
        if (str == "2") {
            attributes_[3] = 0;
        } else if (str == "4") {
            attributes_[3] = 1;
        } else if (str == "more") {
            attributes_[3] = 2;
        } else {
            assert(false);
        }
    }

    void setLugBoot(const std::string& str)
    {
        if (str == "small") {
            attributes_[4] = 0;
        } else if (str == "med") {
            attributes_[4] = 1;
        } else if (str == "big") {
            attributes_[4] = 2;
        } else {
            assert(false);
        }
    }

    void setSafety(const std::string& str)
    {
        if (str == "low") {
            attributes_[5] = 0;
        } else if (str == "med") {
            attributes_[5] = 1;
        } else if (str == "high") {
            attributes_[5] = 2;
        } else {
            assert(false);
        }
    }

    void setQuality(const std::string& str)
    {
        if (str == "unacc") {
            quality_ = 0;
        } else if (str == "acc") {
            quality_ = 1;
        } else if (str == "good") {
            quality_ = 2;
        } else if (str == "vgood") {
            quality_ = 3;
        } else {
            assert(false);
        }
    }

    size_t getQuality() const
    {
        return quality_;
    }

    std::vector<size_t> getAttributes() const
    {
        return attributes_;
    }

};

std::vector<std::string> parseLine(const std::string& line, char letter)
{
    std::vector<std::string> storage = std::vector<std::string>();
    size_t position = 0;
    size_t previous_position = 0;
    while ((position = line.find(letter, previous_position)) != std::string::npos) {
        storage.push_back(line.substr(previous_position, position - previous_position));
        previous_position = position + 1;
    }
    storage.push_back(line.substr(previous_position, line.size() - previous_position));
    return storage;
}

bool getElementFromLine(std::istream& input, Element& elem)
{
    std::string line;
    if (std::getline(input, line)) {
        std::vector<std::string> datas = parseLine(line, ',');
        assert(datas.size() == 7);
        elem.setBuying(datas[0]);
        elem.setMaint(datas[1]);
        elem.setDoors(datas[2]);
        elem.setPersons(datas[3]);
        elem.setLugBoot(datas[4]);
        elem.setSafety(datas[5]);
        elem.setQuality(datas[6]);
        return true;
    }
    return false;
}

