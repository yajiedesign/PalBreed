import inspect
import textwrap

import streamlit as st
from pyecharts.charts import Tree
from streamlit_echarts import st_pyecharts

from breed import Breed
from ui import PalOption


def main():
    breed = Breed()

    with st.sidebar:
        st.header("设置")
        pal_options = [PalOption(pal_id, name) for (pal_id, name) in breed.id_with_name]
        selected_api = st.selectbox(
            label="选择目标帕鲁",
            options=pal_options,
        )
    from pyecharts.charts import Graph
    from pyecharts import options as opts
    max_depth = 3
    data = []
    tree_root = {}

    def dfs(tree_root, pal_id, depth):
        if depth > max_depth:
            return
        tree_root["name"] = breed.id_2_name[pal_id]
        tree_root["children"] = []
        if pal_id in breed.combine_with_child:
            for parent_a, parent_b in breed.combine_with_child[pal_id]:
                child_a = {}
                dfs(child_a, parent_a, depth + 1)
                tree_root["children"].append(child_a)
                child_b = {}
                dfs(child_b, parent_b, depth + 1)
                tree_root["children"].append(child_b)

    dfs(tree_root, selected_api.pal_id, 0)
    data.append(tree_root)


    c = (
        Tree()
        .add("", data, orient="BT", edge_shape="polyline")
        .set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例"),
                         datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100))
        .set_series_opts(label_opts=opts.LabelOpts(position="left", vertical_align="middle", ))

    )

    st_pyecharts(c, height="800px")


if __name__ == "__main__":
    main()
