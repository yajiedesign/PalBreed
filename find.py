import copy


class Find:
    def __init__(self,
                 breed,
                 max_depth,
                 known_parent,
                 root_pal_id):

        self.breed = breed
        self.max_depth = max_depth
        self.known_parent = known_parent
        self.root_pal_id = root_pal_id

    def scan(self, pal_id, depth, ):
        if depth > self.max_depth:
            return None
        node = {}
        node["name"] = f"{pal_id:03d} {self.breed.id_2_name[pal_id]}"
        if pal_id == self.root_pal_id and depth != 0:
            return node

        node["children"] = []
        if pal_id in self.breed.combine_with_child:
            for parent_a, parent_b in self.breed.combine_with_child[pal_id]:

                if self.known_parent is not None:
                    if parent_a != self.known_parent and parent_b != self.known_parent:
                        continue

                parent_node = {}
                name_a = f"{parent_a:03d} {self.breed.id_2_name[parent_a]}"
                name_b = f"{parent_b:03d} {self.breed.id_2_name[parent_b]}"
                parent_node["name"] = name_a + " + " + name_b
                parent_node["parent_a"] = parent_a
                parent_node["parent_b"] = parent_b
                node["children"].append(parent_node)
                parent_node["children"] = []
                child_a = self.scan(parent_a, depth + 1, )
                if child_a is not None:
                    parent_node["children"].append(child_a)

                child_b = self.scan(parent_b, depth + 1, )
                if child_b is not None:
                    parent_node["children"].append(child_b)
        return node


class FindWithCache:
    def __init__(self,
                 breed,
                 max_depth,
                 known_parent,
                 root_pal_id):

        self.breed = breed
        self.max_depth = max_depth
        self.known_parent = known_parent
        self.root_pal_id = root_pal_id

    def scan(self, pal_id, depth, ):
        if depth > self.max_depth:
            return None
        node = copy.deepcopy(self.breed.cache[pal_id])
        if pal_id == self.root_pal_id and depth != 0:
            return node

        for child in node["children"]:
            parent_a = child["parent_a"]
            parent_b = child["parent_b"]
            del child["parent_a"]
            del child["parent_b"]
            if self.known_parent is not None:
                if parent_a != self.known_parent and parent_b != self.known_parent:
                    continue

            child_a = self.scan(parent_a, depth + 1, )
            if child_a is not None:
                child["children"].append(child_a)

            child_b = self.scan(parent_b, depth + 1, )
            if child_b is not None:
                child["children"].append(child_b)

        return node
