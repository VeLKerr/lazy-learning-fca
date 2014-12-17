#include "Element.h"

struct ElementClassifierResult
{
    size_t unacc_in_unacc_amount;
    size_t unacc_in_acc_amount;
    size_t unacc_in_good_amount;
    size_t unacc_in_vgood_amount;

    size_t acc_in_unacc_amount;
    size_t acc_in_acc_amount;
    size_t acc_in_good_amount;
    size_t acc_in_vgood_amount;

    size_t good_in_unacc_amount;
    size_t good_in_acc_amount;
    size_t good_in_good_amount;
    size_t good_in_vgood_amount;

    size_t vgood_in_unacc_amount;
    size_t vgood_in_acc_amount;
    size_t vgood_in_good_amount;
    size_t vgood_in_vgood_amount;
};

class Classifier
{
private:
    std::vector<Element> train_data_unacc_;
    std::vector<Element> train_data_acc_;
    std::vector<Element> train_data_good_;
    std::vector<Element> train_data_vgood_;

    bool isEqual(const std::vector<size_t>& first,
        const std::vector<size_t>& second,
        const std::vector<bool>& is_occured) const
    {
        if (first.size() != second.size() || first.size() != is_occured.size()) {
            return false;
        }
        for (size_t index = 0; index < first.size(); ++index) {
            if (first[index] != second[index] && is_occured[index]) {
                return false;
            }
        }
        return true;
    }

    void calculateClassifierResult(const std::vector<Element>& train_data,
        const Element& elem,
        const std::vector<bool>& is_occured,
        size_t& counter) const
    {
        for (const Element& cur_elem : train_data) {
            if (isEqual(elem.getAttributes(), cur_elem.getAttributes(), is_occured)) {
                ++counter;
            }
        }
    }

    std::vector<bool> getSubSetIndexes(const Element& first,
        const Element& second) const
    {
        std::vector<bool> answer = std::vector<bool>(6, false);
        std::vector<size_t> first_attrs = first.getAttributes();
        std::vector<size_t> second_attrs = second.getAttributes();
        for (size_t index = 0; index < first_attrs.size(); ++index) {
            if (first_attrs[index] == second_attrs[index]) {
                answer[index] = true;
            }
        }
        return answer;
    }

public:
    Classifier(const std::vector<Element>& train_data)
    {
        train_data_unacc_ = std::vector<Element>();
        train_data_acc_ = std::vector<Element>();
        train_data_good_ = std::vector<Element>();
        train_data_vgood_ = std::vector<Element>();
        for (const Element& elem : train_data) {
            if (elem.getQuality() == 0) {
                train_data_unacc_.push_back(elem);
            } else if (elem.getQuality() == 1) {
                train_data_acc_.push_back(elem);
            } else if (elem.getQuality() == 2) {
                train_data_good_.push_back(elem);
            } else if (elem.getQuality() == 3) {
                train_data_vgood_.push_back(elem);
            } else {
                assert(false);
            }
        }
    }

    size_t classify(const Element& elem, double param) const
    {
        ElementClassifierResult classifier_result = ElementClassifierResult();
        for (const Element& cur_elem : train_data_unacc_) {
            std::vector<bool> is_occured = getSubSetIndexes(cur_elem, elem);
            calculateClassifierResult(train_data_unacc_, elem, is_occured,
                classifier_result.unacc_in_unacc_amount);
            calculateClassifierResult(train_data_acc_, elem, is_occured,
                classifier_result.unacc_in_acc_amount);
            calculateClassifierResult(train_data_good_, elem, is_occured,
                classifier_result.unacc_in_good_amount);
            calculateClassifierResult(train_data_vgood_, elem, is_occured,
                classifier_result.unacc_in_vgood_amount);
        }
        for (const Element& cur_elem : train_data_acc_) {
            std::vector<bool> is_occured = getSubSetIndexes(cur_elem, elem);
            calculateClassifierResult(train_data_unacc_, elem, is_occured,
                classifier_result.acc_in_unacc_amount);
            calculateClassifierResult(train_data_acc_, elem, is_occured,
                classifier_result.acc_in_acc_amount);
            calculateClassifierResult(train_data_good_, elem, is_occured,
                classifier_result.acc_in_good_amount);
            calculateClassifierResult(train_data_vgood_, elem, is_occured,
                classifier_result.acc_in_vgood_amount);
        }
        for (const Element& cur_elem : train_data_good_) {
            std::vector<bool> is_occured = getSubSetIndexes(cur_elem, elem);
            calculateClassifierResult(train_data_unacc_, elem, is_occured,
                classifier_result.good_in_unacc_amount);
            calculateClassifierResult(train_data_acc_, elem, is_occured,
                classifier_result.good_in_acc_amount);
            calculateClassifierResult(train_data_good_, elem, is_occured,
                classifier_result.good_in_good_amount);
            calculateClassifierResult(train_data_vgood_, elem, is_occured,
                classifier_result.good_in_vgood_amount);
        }
        for (const Element& cur_elem : train_data_vgood_) {
            std::vector<bool> is_occured = getSubSetIndexes(cur_elem, elem);
            calculateClassifierResult(train_data_unacc_, elem, is_occured,
                classifier_result.vgood_in_unacc_amount);
            calculateClassifierResult(train_data_acc_, elem, is_occured,
                classifier_result.vgood_in_acc_amount);
            calculateClassifierResult(train_data_good_, elem, is_occured,
                classifier_result.vgood_in_good_amount);
            calculateClassifierResult(train_data_vgood_, elem, is_occured,
                classifier_result.vgood_in_vgood_amount);
        }

        /*
        std::cout << classifier_result.unacc_in_unacc_amount / static_cast<double>(train_data_unacc_.size()) << " "
        << classifier_result.unacc_in_acc_amount / static_cast<double>(train_data_acc_.size()) << " "
        << classifier_result.unacc_in_good_amount / static_cast<double>(train_data_good_.size()) << " "
        << classifier_result.unacc_in_vgood_amount / static_cast<double>(train_data_vgood_.size()) << std::endl;

        std::cout << classifier_result.acc_in_unacc_amount / static_cast<double>(train_data_unacc_.size()) << " "
        << classifier_result.acc_in_acc_amount / static_cast<double>(train_data_acc_.size()) << " "
        << classifier_result.acc_in_good_amount / static_cast<double>(train_data_good_.size()) << " "
        << classifier_result.acc_in_vgood_amount / static_cast<double>(train_data_vgood_.size()) << std::endl;

        std::cout << classifier_result.good_in_unacc_amount / static_cast<double>(train_data_unacc_.size()) << " "
        << classifier_result.good_in_acc_amount / static_cast<double>(train_data_acc_.size()) << " "
        << classifier_result.good_in_good_amount / static_cast<double>(train_data_good_.size()) << " "
        << classifier_result.good_in_vgood_amount / static_cast<double>(train_data_vgood_.size()) << std::endl;

        std::cout << classifier_result.vgood_in_unacc_amount / static_cast<double>(train_data_unacc_.size()) << " "
        << classifier_result.vgood_in_acc_amount / static_cast<double>(train_data_acc_.size()) << " "
        << classifier_result.vgood_in_good_amount / static_cast<double>(train_data_good_.size()) << " "
        << classifier_result.vgood_in_vgood_amount / static_cast<double>(train_data_vgood_.size()) << std::endl << std::endl;
        */

        size_t pp_unacc = classifier_result.unacc_in_unacc_amount;
        size_t pt_unacc = classifier_result.unacc_in_acc_amount +
            classifier_result.unacc_in_good_amount +
            classifier_result.unacc_in_vgood_amount;
        size_t tp_unacc = classifier_result.acc_in_unacc_amount +
            classifier_result.good_in_unacc_amount +
            classifier_result.vgood_in_unacc_amount;
        size_t tt_unacc = classifier_result.acc_in_acc_amount +
            classifier_result.good_in_acc_amount +
            classifier_result.vgood_in_acc_amount +
            classifier_result.acc_in_good_amount +
            classifier_result.good_in_good_amount +
            classifier_result.vgood_in_good_amount +
            classifier_result.acc_in_vgood_amount +
            classifier_result.good_in_vgood_amount +
            classifier_result.vgood_in_vgood_amount;

        size_t pp_acc = classifier_result.acc_in_acc_amount;
        size_t pt_acc = classifier_result.acc_in_good_amount +
            classifier_result.acc_in_vgood_amount;
        size_t tp_acc = classifier_result.good_in_acc_amount +
            classifier_result.vgood_in_acc_amount;
        size_t tt_acc = classifier_result.good_in_good_amount +
            classifier_result.vgood_in_good_amount +
            classifier_result.good_in_vgood_amount +
            classifier_result.vgood_in_vgood_amount;

        size_t pp_good = classifier_result.good_in_good_amount;
        size_t pt_good = classifier_result.good_in_vgood_amount;
        size_t tp_good = classifier_result.vgood_in_good_amount;
        size_t tt_good = classifier_result.vgood_in_vgood_amount;


        if (pp_unacc / static_cast<double>(pt_unacc) > param) {
            return 0;
        } else {
            if (classifier_result.unacc_in_unacc_amount / static_cast<double>(train_data_unacc_.size()) >
                classifier_result.unacc_in_acc_amount / static_cast<double>(train_data_acc_.size())) {
                return 0;
            }
            if (pp_acc / static_cast<double>(pt_acc) > param) {
                return 1;
            } else if (pp_good / static_cast<double>(pt_good) > param) {
                return 2;
            } else {
                return 3;
            }
        }
    }
};

