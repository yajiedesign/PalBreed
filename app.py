import streamlit as st
from pyecharts.charts import Tree
from streamlit_echarts import st_pyecharts

from breed import Breed
from find import Find, FindWithCache
from ui import PalOption

from pyecharts.charts import Graph
from pyecharts import options as opts


@st.cache_data
def get_breed():
    return Breed()


def main():
    breed = get_breed()

    with st.sidebar:
        st.header("设置")
        mode_labels = ["目标帕鲁", ]
        mode_keys = ["TargetPal", ]

        mode = st.radio(
            "选择模式",
            options=range(len(mode_labels)),
            format_func=mode_labels.__getitem__,
        )
        mode = mode_keys[mode]
        if mode == "TargetPal":
            pal_options = [PalOption(pal_id, name) for (pal_id, name) in breed.id_with_name]
            target_pal = st.selectbox(
                label="选择目标帕鲁",
                options=pal_options,
            )

            known_pal = st.selectbox(
                label="已知父母(可选)",
                options=pal_options,
                index=None
            )

            #max_depth = st.slider(
            #    label="最大深度",
            #    min_value=1,
            #    max_value=3,
            #    value=1,
            #)
            max_depth = 1

    if mode == "TargetPal":
        data = []

        root_pal_id = target_pal.pal_id
        known_pal_id = known_pal.pal_id if known_pal is not None else None
        find = FindWithCache(breed, max_depth, known_pal_id, root_pal_id)

        tree_root = find.scan(root_pal_id, 0)
        data.append(tree_root)

        c = (
            Tree()
            .add("", data, orient="LR", edge_shape="polyline")
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(position="top", vertical_align="middle", ))

        )

        st_pyecharts(c, height="2800px")


if __name__ == "__main__":
    main()
