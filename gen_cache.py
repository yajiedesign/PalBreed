import json

from breed import Breed
from find import dfs


def main():
    bread = Breed()

    for i in bread.id:
        print(i)
        root_node = dfs(i, 0, bread, 10, i)
        json_text = json.dumps(root_node, ensure_ascii=False)
        with open(f'./data/{i}.json', 'w', encoding='utf-8') as f:
            f.write(json_text)

    pass


if __name__ == '__main__':
    main()
