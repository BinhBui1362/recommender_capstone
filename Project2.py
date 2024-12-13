import streamlit as st
import pandas as pd
import pickle
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random

st.set_page_config(layout="wide")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('./background.jpg')

st.logo("./hasaki.png", size='large')

# Add content to the sidebar
st.sidebar.title(f"DEMO VERSION")
st.sidebar.write("Xây dựng hệ thống đề xuất sản phẩm cho website HASAKI.vn.")
st.sidebar.markdown(
    """
    - **Theo mức độ tương đồng của sản phẩm.**
    - **Theo đánh giá của người dùng.**
    """
)

# Main content
menu = ["Giới thiệu", "Đề xuất theo sản phẩm", "Đề xuất theo khách hàng"]
choice = st.sidebar.selectbox('Menu', menu)

st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.title("THÀNH VIÊN THỰC HIỆN")
st.sidebar.markdown(
    """
    :blue[**Bùi Văn Bình**]\t:man:
    \n\n
     :blue[**Lê Thị Thanh Trúc**]\t:woman:
    """
)
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")


if choice == "Giới thiệu":

    st.markdown("<h1 style='text-align: center; color:#404040; font-family:verdana;'>CAPSTONE PROJECT</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color:#2e8f58; font-family:verdana;'>Product Recommender System</h2><br>", unsafe_allow_html=True)
    st.image("./banner.jpg",use_container_width=True)
    st.write("")
    st.markdown("<h3 style='color:#2e8f58;'>Khách hàng</h3>", unsafe_allow_html=True)
    st.markdown("""
                <p style='color:#000000; font-size: 22px;'><b>Hasaki.vn</b> là hệ thống cửa hàng mỹ phẩm chính hãng và dịch vụ chăm sóc sắc đẹp chuyên sâu.
                <b>Hasaki.vn</b> đang mong muốn xây dựng một hệ thống đề xuất sản phẩm, hỗ trợ người dùng nhanh chóng chọn được sản phẩm phù hợp.
                </p>
                """,  unsafe_allow_html=True)
    st.markdown("<h3 style='color:#2e8f58;'>Dữ liệu</h3>", unsafe_allow_html=True)
    st.markdown("""
            <p style='color:#000000; font-size: 22px;'>Dữ liệu được thu thập từ website <b>Hasaki.vn</b>, với danh mục là các sản phẩm <i>Chăm sóc da mặt</i> và được phân chia thành 3 bảng:<br>
            </p>
            """,  unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='text-align: center; color:#404040;'>SẢN PHẨM</h4>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h4 style='text-align: center; color:#404040;'>ĐÁNH GIÁ</h4>", unsafe_allow_html=True)
    with col3:
        st.markdown("<h4 style='text-align: center; color:#404040;'>KHÁCH HÀNG</h4>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#2e8f58;'>Giải pháp</h3>", unsafe_allow_html=True)
    st.markdown("""
            <p style='color:#000000; font-size: 22px;'>
                Các mô hình sử dụng để giải quyết bài toán lần lượt là <i><b>Cosine Similarity</b></i> cho việc đề xuất sản phẩm tương tự, và <i><b>SVDpp</b></i> 
                trong thư viện Surprise cho việc đề xuất sản phẩm dựa trên đánh giá của khách hàng.
            </p>
            """,  unsafe_allow_html=True)
elif choice == "Đề xuất theo sản phẩm":
    # Load the saved data
    with open('./content_based.pkl', 'rb') as f:
        saved_data = pickle.load(f)

    # Extract components
    tfidf_matrix = saved_data['tfidf_matrix']
    cosine_sim = saved_data['cosine_similarity']
    df = saved_data['df']

    def get_recommendations(sp_id, cosine_sim=cosine_sim, nums=5):
        idx = df.index[df['ma_san_pham'] == sp_id][0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        indices = []
        for i in range(nums+1):
            if len(indices) == nums: break
            if sim_scores[i][0] == idx:
                pass
            else:
                indices.append(sim_scores[i])
        sp_indices = [i[0] for i in indices]
        recs = df.iloc[sp_indices, :-1].sort_values(by=['diem_trung_binh'], ascending=False).head(3)
        return recs

    # Example usage
    
    st.image("./content-based.png",use_container_width=True)
    sample = pd.read_csv("./sample_product.csv")
    product_dict = sample.set_index('ten_san_pham')['ma_san_pham'].to_dict()
    st.markdown("<h2 style='text-align: center; color:#2e8f58; font-family:verdana;'>ĐỀ XUẤT SẢN PHẨM TƯƠNG ĐỒNG</h2>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")

    st.markdown("<h5 style='color:#2e8f58;'>Chọn sản phẩm:</h5>", unsafe_allow_html=True)

    current_product = st.selectbox("",
        list(product_dict.keys()),
    placeholder="Chọn sản phẩm")

    st.write("")
    example_id = product_dict[current_product]

    st.markdown(f"<h4 style='color:#404040;'>Sản phẩm đang chọn: <span style='color: green;'><i>{current_product}</i></span> </h4>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    col1, col2 = st.columns([0.3,0.7])
    with col1:
        random_pic = random.randint(1,8)
        st.image(f'./prod{random_pic}.png')
    with col2: 
        st.markdown(f"""
        <p style='color:#000000; font-size: 18px;'>
            Mã sản phẩm: <span style='color: green;'><b>{example_id}</b></span>
        </p>
        """,  unsafe_allow_html=True)

        st.markdown(f":grey[{(sample[sample['ma_san_pham']==example_id]['diem_trung_binh'].values[0])}]:star:")

        st.markdown(f"""
        <p style='color:#000000; font-size: 15px;'>
            {(sample[sample['ma_san_pham']==example_id]['mo_ta'].values[0]).strip()}
        </p>
        """,  unsafe_allow_html=True)

    
    recommendations = get_recommendations(example_id)   
    recommendations['ma_san_pham'] = recommendations['ma_san_pham'].astype(str)
    st.write("")
    st.write("")
    st.write(":red[Các sản phẩm tương tự:]")
    item1, item2, item3 = st.columns(3)
    with item1:
        st.markdown(f"""
                    <p style='color:#2e8f58; font-size: 18px;text-align: center;'>
                    <b>{recommendations.iloc[0,:]['ten_san_pham']}</b>
                    </p>
                    """,  unsafe_allow_html=True)
        st.markdown(f"""
        <p style='color:#1f1d1d; font-size: 18px;text-align: center;'>
        <b> Mã sản phẩm: {recommendations.iloc[0,:]['ma_san_pham']}</b>
        </p>
        """,  unsafe_allow_html=True)
        with st.expander(":grey[\t\tThông tin chi tiết]", icon="👉"):
            random_pic = random.randint(1,8)
            st.image(f'./prod{random_pic}.png')
            st.markdown(f"""
                    <p style='color:#1f1d1d; font-size: 15px;text-align: left;'>
                    <i>{recommendations.iloc[0,:]['mo_ta']}</i>
                    </p>
                    """,  unsafe_allow_html=True)
            st.markdown(f":grey[Điểm đánh giá: {recommendations.iloc[0,:]['diem_trung_binh']}]:star:")

    with item2:
        st.markdown(f"""
            <p style='color:#2e8f58; font-size: 18px;text-align: center;'>
            <b>{recommendations.iloc[1,:]['ten_san_pham']}</b>
            </p>
            """,  unsafe_allow_html=True)
        st.markdown(f"""
            <p style='color:#1f1d1d; font-size: 18px;text-align: center;'>
            <b>Mã sản phẩm: {recommendations.iloc[1,:]['ma_san_pham']}</b>
            </p>
            """,  unsafe_allow_html=True)
        with st.expander(":grey[\t\tThông tin chi tiết]", icon="👉"):
            random_pic = random.randint(1,8)
            st.image(f'./prod{random_pic}.png')
            st.markdown(f"""
                    <p style='color:#1f1d1d; font-size: 15px;text-align: left;'>
                    <i>{recommendations.iloc[1,:]['mo_ta']}</i>
                    </p>
                    """,  unsafe_allow_html=True)
            st.markdown(f":grey[Điểm đánh giá: {recommendations.iloc[1,:]['diem_trung_binh']}]:star:")
    with item3:
        st.markdown(f"""
            <p style='color:#2e8f58; font-size: 18px;text-align: center;'>
            <b>{recommendations.iloc[2,:]['ten_san_pham']}</b>
            </p>
            """,  unsafe_allow_html=True)
        st.markdown(f"""
                    <p style='color:#1f1d1d; font-size: 18px;text-align: center;'>
                    <b> Mã sản phẩm: {recommendations.iloc[2,:]['ma_san_pham']}</b>
                    </p>
                    """,  unsafe_allow_html=True)
        with st.expander(":grey[\t\tThông tin chi tiết]", icon="👉"):
            random_pic = random.randint(1,8)
            st.image(f'./prod{random_pic}.png')
           
            st.markdown(f"""
                    <p style='color:#1f1d1d; font-size: 15px;text-align: left;'>
                    <i>{recommendations.iloc[2,:]['mo_ta']}</i>
                    </p>
                    """,  unsafe_allow_html=True)
            st.markdown(f":grey[Điểm đánh giá: {recommendations.iloc[1,:]['diem_trung_binh']}]:star:")
else:
    # Load the saved data

    with open('./collaborative.pkl', 'rb') as f:
        saved_data = pickle.load(f)

    # Extract components
    model = saved_data['model']
    df = saved_data['df']
    
    st.image("./collaborative_filtering.png")
    st.markdown("<h2 style='text-align: center; color:#2e8f58; font-family:verdana;'>ĐỀ XUẤT SẢN PHẨM PHÙ HỢP VỚI KHÁCH HÀNG</h2>", unsafe_allow_html=True)

    customer = pd.read_csv("./Cung_cap_HV/data/Khach_hang.csv")
    customer_dict = customer.set_index('ho_ten')['ma_khach_hang'].to_dict()
    
    product = pd.read_csv("./Cung_cap_HV/data/San_pham.csv")


    name = st.selectbox("",
        list(customer_dict.keys())
    )
     
    st.write("")
    df = pd.merge(df,product,how='left',on="ma_san_pham")

    try:
        cmt1,cmt_mid,cmt2  = st.columns([0.3,0.01,0.59])
        user_id = customer_dict[name]
        with cmt1:
            st.markdown(f"<h6 style='color:#404040;'>Đang hiển thị: <span style='color: green;'><i>{name}</i></span> </h6>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#1f1d1d;'>Mã khách hàng: {user_id}:key:</span>", unsafe_allow_html=True)
            cmt_list = df[df['ma_khach_hang']==user_id]['noi_dung_binh_luan'].tolist()
            st.markdown(f"<span style='color:#1f1d1d;'><b>Số bình luận đã đăng: {len(cmt_list)}</b></span>", unsafe_allow_html=True)
            try:
                cmt_id = random.sample(range(0, len(cmt_list)), 3)
            except:
                cmt_id = list(range(0,len(cmt_list)))
            for i in cmt_id:
                st.markdown(f"<span style='color:#1f1d1d;'><b>Sản phẩm: {df[df['ma_khach_hang']==user_id]['ten_san_pham'].tolist()[i]}</b> </br> <i>{cmt_list[i]}</i> </br> {df[df['ma_khach_hang']==user_id]['so_sao'].tolist()[i]}:star:</span>", unsafe_allow_html=True)

        with cmt2:
            df_score = df[["ma_san_pham","ten_san_pham", "diem_trung_binh"]]
            df_score['EstimateScore'] = df_score['ma_san_pham'].apply(lambda x: model.predict(user_id, x).est) # est: get EstimateScore
            df_score = df_score.sort_values(by=['EstimateScore'], ascending=False)
            df_score['ma_san_pham'] = df_score['ma_san_pham'].astype(str)
            df_score = df_score.drop_duplicates()
            st.markdown(f":grey[Các sản phẩm mà :blue[**{name}**] có thể sẽ thích:]")
            #st.write(df_score.sort_values(by=['diem_trung_binh'], ascending=False).head(3))
            item1, item2, item3 = st.columns(3)
            with item1:
                st.markdown(f"""
                            <p style='color:#2e8f58; font-size: 18px;text-align: center;'>
                            <b>{df_score.iloc[0,:]['ten_san_pham']}</b>
                            </p>
                            """,  unsafe_allow_html=True)
                random_pic = random.randint(1,8)
                st.image(f'./prod{random_pic}.png')
                st.markdown(f":grey[Điểm đánh giá: {df_score.iloc[0,:]['diem_trung_binh']}]:star:")

            with item2:
                st.markdown(f"""
                    <p style='color:#2e8f58; font-size: 18px;text-align: center;'>
                    <b>{df_score.iloc[1,:]['ten_san_pham']}</b>
                    </p>
                    """,  unsafe_allow_html=True)
                random_pic = random.randint(1,8)
                st.image(f'./prod{random_pic}.png')

                st.markdown(f":grey[Điểm đánh giá: {df_score.iloc[1,:]['diem_trung_binh']}]:star:")
            with item3:
                st.markdown(f"""
                    <p style='color:#2e8f58; font-size: 18px;text-align: center;'>
                    <b>{df_score.iloc[2,:]['ten_san_pham']}</b>
                    </p>
                    """,  unsafe_allow_html=True)
            
                random_pic = random.randint(1,8)
                st.image(f'./prod{random_pic}.png')
                
                st.markdown(f":grey[Điểm đánh giá: {df_score.iloc[1,:]['diem_trung_binh']}]:star:")

    except:
        st.write(":red[Vui lòng chọn tên đăng nhập!]")
