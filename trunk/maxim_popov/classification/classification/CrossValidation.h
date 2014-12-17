#include "Classificator.h"
#include <random>
#include <algorithm> 

template <typename Classificator>
class CrossValidationIteration
{
private:
    std::vector<Element> train_data_;
    std::vector<Element> test_data_;
    double correct_proportion_;
    double param_;
public:
    CrossValidationIteration(const std::vector<Element>& elements,
        size_t train_data_size, double param) : param_(param)
    {
        std::vector<int> indexes = std::vector<int>();
        for (size_t index = 0; index < elements.size(); ++index) {
            indexes.push_back(index);
        }
        std::random_device rd;
        std::mt19937 generator(rd());
        std::shuffle(indexes.begin(), indexes.end(), generator);
        for (size_t index = 0; index < elements.size(); ++index) {
            if (index < train_data_size) {
                train_data_.push_back(elements[indexes[index]]);
            } else {
                test_data_.push_back(elements[indexes[index]]);
            }
        }
        Classificator classifier = Classificator(train_data_);
        size_t correct_amount = 0;
        for (const Element& elem : test_data_) {
            size_t type = classifier.classify(elem, param_);
            if (elem.getQuality() == type) {
                ++correct_amount;
            }
        }
        correct_proportion_ = correct_amount / static_cast<double>(test_data_.size());
    }

    double getCorrectProportion() const
    {
        std::cout << "Correct proportion via one iteration CV = " << correct_proportion_ << std::endl;
        return correct_proportion_;
    }

    double getIncorrectProportion() const
    {
        return 1 - correct_proportion_;
    }
};

template <typename Classificator>
class CrossValidation
{
private:
    std::vector<Element> elements_;
    double param_;
public:
    CrossValidation(const std::vector<Element>& elements, double param) :
        elements_(elements), param_(param) {}

    double process(size_t number, double train_proportion) const
    {
        double correct_proportion = 0;
        for (size_t index = 0; index < number; ++index) {
            CrossValidationIteration<Classificator> iteration =
                CrossValidationIteration<Classificator>(elements_,
                static_cast<int>(elements_.size() * train_proportion), param_);
            correct_proportion += iteration.getCorrectProportion();
        }
        return correct_proportion / static_cast<double>(number);
    }
};