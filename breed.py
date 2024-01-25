import math

import pandas as pd


class CombineKey:
    def __init__(self, parent_a, parent_b):
        if parent_a > parent_b:
            parent_a, parent_b = parent_b, parent_a
        self.parent_a = parent_a
        self.parent_b = parent_b

    def __eq__(self, other):
        return self.parent_a == other.parent_a and self.parent_b == other.parent_b

    def __hash__(self):
        return hash((self.parent_a, self.parent_b))

    def __str__(self):
        return f'{self.parent_a} {self.parent_b}'


class Breed:
    def __init__(self):
        language = 'zh_cn'
        # read fecundity csv file and store in a dictionary
        breed_power = pd.read_csv('data/breed_power.csv', header=0)
        self.key_2_power = dict(zip(breed_power['Key'], breed_power['BreedPower']))
        self.power_2_key = dict(zip(breed_power['BreedPower'], breed_power['Key']))
        self.power_list = breed_power['BreedPower'].tolist()
        self.key = breed_power['Key'].tolist()

        name = pd.read_csv(f'data/name_{language}.csv', header=0)

        self.key_2_no = dict(zip(name['Key'], name['No']))
        self.key_2_name = dict(zip(name['Key'], name['Name']))

        fixed = pd.read_csv('data/fixed.csv', header=0)
        # fixed col 1 col 2 is key col3 is value
        self.fixed = dict(zip(zip(fixed['ParentAKey'], fixed['ParentBKey']), fixed['ChildKey']))

        only_same = pd.read_csv('data/only_same.csv', header=0)

        self.only_same = set(only_same['Key'])

        self.combine = {}
        self.combine_from_child = {}
        self.cache = None

        self.create_combine()
        self.create_cache()

    def create_combine(self):
        for key in self.fixed:
            parent_a, parent_b = key
            child = self.fixed[key]
            self.combine[CombineKey(parent_a, parent_b)] = child
        # self.fecundity

        for parent_a in self.key:
            for parent_b in self.key:
                key = CombineKey(parent_a, parent_b)
                if key in self.combine:
                    continue
                if parent_a == parent_b:
                    continue

                child_target_power = self.key_2_power[parent_a] + self.key_2_power[parent_b] + 1
                child_target_power = math.floor(child_target_power / 2)
                # find the closest fecundity
                min_diff_key = self.key[0]
                mim_diff = abs(child_target_power - self.key_2_power[min_diff_key])
                for k in self.key:
                    p = self.key_2_power[k]
                    diff = abs(child_target_power - p)
                    if diff < mim_diff:
                        min_diff_key = k
                        mim_diff = diff

                if min_diff_key in self.only_same:
                    continue
                self.combine[CombineKey(parent_a, parent_b)] = min_diff_key

        for key in self.combine:
            parent_a, parent_b = key.parent_a, key.parent_b
            child = self.combine[key]
            if child not in self.combine_from_child:
                self.combine_from_child[child] = []
            self.combine_from_child[child].append((parent_a, parent_b))

    def scan(self, pal_id):
        node = {"name": f"{self.key_2_no[pal_id]:03d} {self.key_2_name[pal_id]}", "children": []}

        if pal_id in self.combine_from_child:
            for parent_a, parent_b in self.combine_from_child[pal_id]:
                parent_node = {}
                name_a = f"{self.key_2_no[parent_a]:03d} {self.key_2_name[parent_a]}"
                name_b = f"{self.key_2_no[parent_b]:03d} {self.key_2_name[parent_b]}"
                parent_node["name"] = name_a + " + " + name_b
                parent_node["parent_a"] = parent_a
                parent_node["parent_b"] = parent_b
                node["children"].append(parent_node)
                parent_node["children"] = []

        return node

    def create_cache(self):
        cache = {}
        for i in self.key:
            root_node = self.scan(i)
            cache[i] = root_node
        self.cache = cache


if __name__ == '__main__':
    breed = Breed()
    print(breed.power_list)
