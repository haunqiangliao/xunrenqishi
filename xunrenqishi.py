import streamlit as st
from datetime import datetime
import pandas as pd

# 页面设置
st.set_page_config(
    page_title="寻人启事互助平台",
    page_icon="🔍",
    layout="centered"
)

# 初始化数据（简化版使用session_state）
if 'posts' not in st.session_state:
    st.session_state.posts = pd.DataFrame(columns=[
        "姓名", "性别", "年龄", "特征描述", 
        "失踪时间", "失踪地点", "联系人", 
        "联系方式", "发布时间", "图片"
    ])

# 主界面
st.title("🔍 寻人启事互助平台")
st.write("用技术传递温暖，让爱回家")

# 功能导航
tab1, tab2 = st.tabs(["发布寻人启事", "浏览寻人信息"])

with tab1:
    # 发布新寻人启事
    st.subheader("发布新的寻人信息")
    
    with st.form("missing_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("姓名*", max_chars=20)
            gender = st.selectbox("性别*", ["男", "女", "其他"])
            age = st.number_input("年龄", min_value=0, max_value=120)
        with col2:
            missing_date = st.date_input("失踪时间*", max_value=datetime.today())
            missing_location = st.text_input("失踪地点*", max_chars=50)
        
        features = st.text_area("特征描述*", 
                              help="请详细描述衣着、体貌特征等",
                              max_chars=500)
        
        col3, col4 = st.columns(2)
        with col3:
            contact_person = st.text_input("联系人*", max_chars=20)
        with col4:
            contact_info = st.text_input("联系方式*", 
                                       help="电话/微信/邮箱等",
                                       max_chars=50)
        
        image = st.file_uploader("上传照片", type=["jpg", "png"])
        
        if st.form_submit_button("发布信息"):
            if name and gender and missing_location and contact_person and contact_info:
                new_post = {
                    "姓名": name,
                    "性别": gender,
                    "年龄": age,
                    "特征描述": features,
                    "失踪时间": missing_date.strftime("%Y-%m-%d"),
                    "失踪地点": missing_location,
                    "联系人": contact_person,
                    "联系方式": contact_info,
                    "发布时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "图片": image.getvalue() if image else None
                }
                st.session_state.posts = st.session_state.posts.append(new_post, ignore_index=True)
                st.success("信息发布成功！")
            else:
                st.error("请填写带*的必填项")

with tab2:
    # 浏览寻人信息
    st.subheader("浏览寻人信息")
    
    # 搜索筛选
    search_col1, search_col2 = st.columns(2)
    with search_col1:
        search_name = st.text_input("按姓名搜索")
    with search_col2:
        search_location = st.text_input("按地点搜索")
    
    # 显示信息卡片
    filtered_posts = st.session_state.posts
    if search_name:
        filtered_posts = filtered_posts[filtered_posts["姓名"].str.contains(search_name, na=False)]
    if search_location:
        filtered_posts = filtered_posts[filtered_posts["失踪地点"].str.contains(search_location, na=False)]
    
    if not filtered_posts.empty:
        for idx, row in filtered_posts.iterrows():
            with st.expander(f"{row['姓名']} ({row['性别']}, {row['年龄']}岁) - 失踪于{row['失踪时间']}"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    if row["图片"]:
                        st.image(row["图片"], width=150)
                    else:
                        st.info("暂无照片")
                with col2:
                    st.write(f"**失踪地点**: {row['失踪地点']}")
                    st.write(f"**特征描述**: {row['特征描述']}")
                    st.write(f"**联系人**: {row['联系人']} ({row['联系方式']})")
                    st.caption(f"发布时间: {row['发布时间']}")
    else:
        st.info("暂无匹配的寻人信息")

# 页脚
st.divider()
st.write("""
**使用须知**:
1. 请确保信息真实准确
2. 发现线索请及时联系发布者
3. 拒绝虚假信息传播
""")
