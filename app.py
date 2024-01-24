import streamlit as st
from pyecharts.charts import Tree
from streamlit_echarts import st_pyecharts

from breed import Breed
from find import dfs
from ui import PalOption


@st.cache_data
def get_breed():
    return Breed()


def main():
    breed = get_breed()

    with st.sidebar:
        st.header("设置")
        pal_options = [PalOption(pal_id, name) for (pal_id, name) in breed.id_with_name]
        selected_api = st.selectbox(
            label="选择目标帕鲁",
            options=pal_options,
        )

        max_depth = st.slider(
            label="最大深度",
            min_value=1,
            max_value=3,
            value=2,
        )
    from pyecharts.charts import Graph
    from pyecharts import options as opts

    data = []

    root_pal_id = selected_api.pal_id

    tree_root = dfs(root_pal_id, 0, breed, max_depth, root_pal_id)
    data.append(tree_root)

    c = (
        Tree()
        .add("", data, orient="LR", edge_shape="polyline")
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
        .set_series_opts(label_opts=opts.LabelOpts(position="top", vertical_align="middle", ))

    )

    st_pyecharts(c, height="800px")


if __name__ == "__main__":
    main()
