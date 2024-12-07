import streamlit as st
import pandas as pd
import pickle
import base64

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

st.logo("./hasaki.png")

# Add content to the sidebar
st.sidebar.title(f"DEMO VERSION v0.2")
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
if choice == "Giới thiệu":
    pass
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
    sample = pd.read_csv("./sample_product.csv")
    product_dict = sample.set_index('ten_san_pham')['ma_san_pham'].to_dict()
    current_product = st.selectbox(
        ":red[Vui lòng chọn sản phẩm:]",
        list(product_dict.keys())
    )
    example_id = product_dict[current_product]

    st.write(f":grey[Sản phẩm đang chọn:] :blue[{current_product}]")
    st.write(f":grey[Mã sản phẩm:] :blue[{example_id}]")

    st.write(f":grey[Thông tin chi tiết:]")
    st.write(f":blue[{(sample[sample['ma_san_pham']==example_id]['mo_ta'].values[0]).strip()}]")
    
    recommendations = get_recommendations(example_id)   
    recommendations['ma_san_pham'] = recommendations['ma_san_pham'].astype(str)
    st.write(":grey[Các sản phẩm tương tự:]")
    st.write(recommendations)
else:
    # Load the saved data
    with open('./collaborative.pkl', 'rb') as f:
        saved_data = pickle.load(f)

    # Extract components
    model = saved_data['model']
    df = saved_data['df']
    

    with st.popover("Đăng nhập"):
        name = st.text_input("Tên đăng nhập")
        
    customer = pd.read_csv("./Cung_cap_HV/data/Khach_hang.csv")
    product_dict = customer.set_index('ho_ten')['ma_khach_hang'].to_dict()

    product = pd.read_csv("./Cung_cap_HV/data/San_pham.csv")
    df = pd.merge(df,product,how='left',on="ma_san_pham")

    try:
        user_id = product_dict[name]
        st.write(f":grey[Đang hiển thị: {name}]")
        st.write(":grey[Mã khách hàng:]",user_id)
        st.write(':grey[Các bình luận đã đăng:')
        st.write(df[df['ho_ten']==name].head(5))


        df_score = df[["ma_san_pham","ten_san_pham", "diem_trung_binh"]]
        df_score['EstimateScore'] = df_score['ma_san_pham'].apply(lambda x: model.predict(user_id, x).est) # est: get EstimateScore
        df_score = df_score.sort_values(by=['EstimateScore'], ascending=False)
        df_score['ma_san_pham'] = df_score['ma_san_pham'].astype(str)
        df_score = df_score.drop_duplicates()
        st.write(df_score.sort_values(by=['diem_trung_binh'], ascending=False).head(5))
    except:
        st.write(":red[Vui lòng nhập tên đăng nhập!]")
