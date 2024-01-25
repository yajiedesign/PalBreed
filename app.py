import streamlit as st
from pyecharts.charts import Tree
from streamlit.components.v1 import components
from streamlit_echarts import st_pyecharts

from breed import Breed, CombineKey
from find import FindWithCache
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
        mode_labels = ["目标帕鲁", "已知父母"]
        mode_keys = ["TargetPal", "KnownParents"]

        mode = st.radio(
            "选择模式",
            options=range(len(mode_labels)),
            format_func=mode_labels.__getitem__,
        )
        mode = mode_keys[mode]
        if mode == "TargetPal":
            pal_options = [PalOption(key, breed.key_2_no[key], breed.key_2_name[key]) for key in breed.key]
            target_pal = st.selectbox(
                label="选择目标帕鲁",
                options=pal_options,
            )

            known_pal = st.selectbox(
                label="已知父母(可选)",
                options=pal_options,
                index=None
            )

            # max_depth = st.slider(
            #    label="最大深度",
            #    min_value=1,
            #    max_value=3,
            #    value=1,
            # )
            max_depth = 0

        elif mode == "KnownParents":
            pal_options = [PalOption(key, breed.key_2_no[key], breed.key_2_name[key]) for key in breed.key]
            known_pal_a = st.selectbox(
                label="已知父母 a",
                options=pal_options,
            )
            known_pal_b = st.selectbox(
                label="已知父母 b",
                options=pal_options,
            )

    if mode == "TargetPal":
        data = []

        root_key = target_pal.key
        known_key = known_pal.key if known_pal is not None else None
        find = FindWithCache(breed, max_depth, known_key, root_key)

        tree_root = find.scan(root_key, 0)
        data.append(tree_root)

        child_count = len(tree_root["children"]) * 40

        c = (
            Tree()
            .add("", data, orient="LR", edge_shape="polyline", pos_top="20px")
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(position="top", vertical_align="middle", ))

        )

        st_pyecharts(c, height=f"{child_count}px")
    elif mode == "KnownParents":

        parent_a = known_pal_a.key
        parent_b = known_pal_b.key

        if parent_a == parent_b:
            child = parent_a
        else:
            child = breed.combine[CombineKey(parent_a, parent_b)]

        st.write(f"{breed.key_2_no[child]:03d} {breed.key_2_name[child]}")

    st.components.v1.html(
        """
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?9c55a9e81830f138ba5b9af774c71fe4";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
        """,
        height=0,
    )


if __name__ == "__main__":
    main()
