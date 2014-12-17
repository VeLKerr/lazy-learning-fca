#define _CRT_SECURE_NO_WARNINGS
#include "CrossValidation.h"


std::vector<Element> readElements()
{
    std::vector<Element> elements = std::vector<Element>();
    Element elem = Element();
    while (getElementFromLine(std::cin, elem)) {
        elements.push_back(elem);
    }
    return elements;
}

std::vector<Element> getRandomElements(const std::vector<Element>& elements, size_t size)
{
    std::vector<int> indexes = std::vector<int>();
    for (size_t index = 0; index < elements.size(); ++index) {
        indexes.push_back(index);
    }
    std::random_device rd;
    std::mt19937 generator(rd());
    std::shuffle(indexes.begin(), indexes.end(), generator);
    std::vector<Element> answer = std::vector<Element>();
    for (size_t index = 0; index < size; ++index) {
        answer.push_back(elements[indexes[index]]);
    }
    return answer;
}


int main()
{
    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);

    std::vector<Element> elements = readElements();
    double best_param = 0;
    double best_average_proportion = 0;
    for (size_t index = 0; index < 10; ++index) {
        double param = 0.5 * index;
        std::vector<Element> rand_elements = getRandomElements(elements, 300);
        CrossValidation<Classifier> cv = CrossValidation<Classifier>(rand_elements, param);
        double average_proportion = cv.process(10, 0.8);
        std::cout << "Parameter = " << param << std::endl;
        std::cout << "Average correct proportion via CV = " << average_proportion << std::endl;
        std::cout << std::endl;
        if (average_proportion > best_average_proportion) {
            best_average_proportion = average_proportion;
            best_param = param;
        }
    }

    std::cout << "Current best parameter = " << best_param << std::endl;
    std::cout << "Current best correct proportion = " << best_average_proportion << std::endl;
    std::cout << std::endl;

    std::cout << "----------------------------------------" << std::endl;

    double new_best_param = 0;
    double new_best_average_proportion = 0;
    for (size_t index = 0; index < 25; ++index) {
        double param = best_param - 0.25 + index * 0.02;
        std::vector<Element> rand_elements = getRandomElements(elements, 300);
        CrossValidation<Classifier> cv = CrossValidation<Classifier>(rand_elements, param);
        double average_proportion = cv.process(10, 0.8);
        std::cout << "Parameter = " << param << std::endl;
        std::cout << "Average correct proportion via CV = " << average_proportion << std::endl;
        std::cout << std::endl;
        if (average_proportion > new_best_average_proportion) {
            new_best_average_proportion = average_proportion;
            new_best_param = param;
        }
    }

    std::cout << "Total best parameter = " << new_best_param << std::endl;
    std::cout << "Total best correct proportion = " << new_best_average_proportion << std::endl;
    std::cout << std::endl;
    return 0;
}

