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
        fecundity = pd.read_csv('data/fecundity.csv', header=None)
        self.id_2_fecundity = dict(zip(fecundity[0], fecundity[1]))
        self.fecundity_2_id = dict(zip(fecundity[1], fecundity[0]))
        self.fecundity = fecundity[1].tolist()
        name = pd.read_csv(f'data/name_{language}.csv', header=None)
        self.id_2_name = dict(zip(name[0], name[1]))
        self.id = list(name[0])
        self.id.sort()
        self.id_with_name = [(i, self.id_2_name[i]) for i in self.id]

        fixed = pd.read_csv('data/fixed.csv', header=None)
        # fixed col 1 col 2 is key col3 is value
        self.fixed = dict(zip(zip(fixed[0], fixed[1]), fixed[2]))
        self.combine = {}
        self.combine_with_child = {}
        self.create_bread()

    def create_bread(self):
        for key in self.fixed:
            parent_a, parent_b = key
            child = self.fixed[key]
            self.combine[CombineKey(parent_a, parent_b)] = child

        for parent_a in self.id:
            for parent_b in self.id:
                key = CombineKey(parent_a, parent_b)
                if key in self.combine:
                    continue
                if parent_a == parent_b:
                    continue

                fecundity = self.id_2_fecundity[parent_a] + self.id_2_fecundity[parent_b]
                fecundity = round(fecundity / 2)
                # find the closest fecundity
                child = self.fecundity[0]
                for f in self.fecundity:
                    if abs(fecundity - f) < abs(fecundity - child):
                        child = f

                self.combine[CombineKey(parent_a, parent_b)] =  self.fecundity_2_id[child]

        for key in self.combine:
            parent_a, parent_b = key.parent_a, key.parent_b
            child = self.combine[key]
            if child not in self.combine_with_child:
                self.combine_with_child[child] = []
            self.combine_with_child[child].append((parent_a, parent_b))


if __name__ == '__main__':
    breed = Breed()
    print(breed.fecundity)
