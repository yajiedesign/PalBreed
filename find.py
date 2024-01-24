def dfs(pal_id, depth, breed, max_depth, root_pal_id):
    if depth > max_depth:
        return None
    node = {}
    node["name"] = breed.id_2_name[pal_id]
    if pal_id == root_pal_id and depth != 0:
        return node

    node["children"] = []
    if pal_id in breed.combine_with_child:
        for parent_a, parent_b in breed.combine_with_child[pal_id]:
            parent_node = {}
            parent_node["name"] = breed.id_2_name[parent_a] + " + " + breed.id_2_name[parent_b]
            node["children"].append(parent_node)
            parent_node["children"] = []
            child_a = dfs(parent_a, depth + 1, breed, max_depth, root_pal_id)
            if child_a is not None:
                parent_node["children"].append(child_a)

            child_b = dfs(parent_b, depth + 1, breed, max_depth, root_pal_id)
            if child_b is not None:
                parent_node["children"].append(child_b)
    return node
