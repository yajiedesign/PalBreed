import copy






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
