#! coding: utf-8
import re
import copy
import math

class ID3:
    def __init__(self):
        self.nrow = 0
        self.ncol = 0
        self.labels   = []
        self.datasets = []
        self.set_data_sets()
        tree_tmp = self.id3_algorithm(copy.deepcopy(self.datasets), copy.deepcopy(self.labels))
        print(tree_tmp)
        self.puts_node(tree_tmp)

    def check_all_label(self, category, datasets):
        for data in datasets:
            if data[self.decision] != category:
                return False
        return True

    def count_vec(self, category, decision_c, label, datasets):
        count = 0
        for data in datasets:
            # if data[self.decision] == v:
            if data[label] == category and data[self.decision] == decision_c:
                count += 1
        return count


    def get_category(self, label, datasets):
        return [v for v in {eff_data:None for eff_data in [data[label] for data in datasets]}.keys()]

    def get_effective_label(self, datasets, labels):
        all_e = 0  # entropy
        for count in [self.count_vec(v, v, self.decision, datasets)
                for v in self.get_category(self.decision, datasets)]:
            # print(count)
            all_e += -1*(count/len(datasets)*math.log2(count/len(datasets)))

        # print(all_e)

        _max = 0
        _max_label = ""
        for label in labels:
            label_data = []
            sum_of_count = 0
            for category in self.get_category(label, datasets):
                sub_e = 0
                counts = [self.count_vec(category, v, label, datasets)
                    for v in self.get_category(self.decision, datasets)]
                count += sum(counts)
                for count in counts:
                    if count != 0:
                        sub_e -= count/sum(counts)*math.log2(count/sum(counts))
                label_data.append({"count":sum(counts),"entropy":sub_e})
                sum_of_count += sum(counts)

            # Gain calculation
            gained = all_e
            for data in label_data:
                gained -= (data["count"]/sum_of_count)*data["entropy"]

            print(label)
            print(gained)
            _max = max(_max, gained)
            if _max == gained:
                # print("temporary", label)
                _max = gained
                _max_label = label
        # print("MAX LABEL", _max_label)
        return _max_label

    def get_subset(self, v, eff, datasets):
        d = []
        for data in datasets:
            if data[eff] == v:
                d.append(data)
        return d

    def remove_list(self, lst, attr):
        return list(filter(lambda x : x != attr, lst))

    def get_mode_category(self):
        count = {}
        for data in self.datasets:
            if count[data[self.decision]] != None:
                count[data[self.decision]] += 1
            else:
                count[data[self.decision]] = 1
        return label


    def id3_algorithm(self, datasets, labels):
        for v in {eff_data:None for eff_data in [data[self.decision] for data in datasets]}.keys():
            if self.check_all_label(v, datasets) == True:
                return v
        else:
            tree = {}
            effective_label = self.get_effective_label(datasets, labels)
            tree[effective_label] = {}
            for v in {eff_data:None for eff_data in [data[effective_label] for data in datasets]}.keys():
                # print(v)
                d = self.get_subset(v, effective_label, datasets)
                if d == []:
                    return self.get_mode_category()
                else:
                    tree[effective_label].update({v: self.id3_algorithm(d, self.remove_list(labels, effective_label))})
            # print("Returned")
            # print(tree)
            return tree

    def puts_node(self, tree):
        if type(tree) is str:
            print(tree)
        else:
            for branch in tree.keys():
                print("node", branch)
                self.puts_branch(tree[branch])
                print("Return")

    def puts_branch(self, tree):
        for node in tree.keys():
            print("branch", node)
            self.puts_node(tree[node])

    def set_data_sets(self):
        first = 0
        for line in open("input.dat", "r"):
            line = re.sub(r'\n', '', line)
            if first == 0:
                self.labels = line.split(",")
                self.labels
                first = 1
            else:
                i = 0
                self.datasets.append({})
                for vec in line.split(","):
                    self.datasets[-1][self.labels[i]] = vec
                    i += 1
        self.decision = self.labels.pop()

id3 = ID3()

