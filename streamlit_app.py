import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import glob
import seaborn as sns

# Memanggil fungsi read_csv
air_quality = pd.read_csv("./dataset/Air_Quality.csv")

st.write('''# Selamat Datang di Dashboard Kualitas Udara 🌬️
Halo! Siapa yang suka nafas segar? Kita semua, kan? Nah, dashboard ini adalah tempat yang tepat untuk memantau seberapa "segar" udara di sekitar kita! 🌿
Di sini, kamu akan menemukan data tentang kualitas udara dari berbagai stasiun. Mulai dari tarikan napas dalam-dalam hingga "Woah, mungkin aku harus tetap di dalam ruangan hari ini!" 😷
Mari kita jelajahi bersama-sama dan lihat apakah kita bisa menemukan udara yang benar-benar "Instagrammable" di luar sana! 💨
Selamat menjelajah! 🚀''')

with st.container():
    st.write('''
         ## Explanatory Data Analysis
         Selamat datang di bagian EDA dari dashboard kualitas udara. Di sini, kami melakukan analisis eksploratif terhadap data kualitas udara untuk memahami karakteristiknya lebih dalam.
         ''')

    # Menampilkan kolom informasi
    col1, col2 = st.columns([1,2])
    info = pd.DataFrame(air_quality.isnull().sum().sort_values(ascending=False), columns=['Missing_Values'])
    info.index.name = 'Feature'

    with col1:
        st.subheader("Missing Value")
        st.write(info)

    with col2:
        st.subheader("Missing Value in Percentage")
        st.bar_chart(info['Missing_Values'] / air_quality.shape[0] * 100)

    # Memisahkan dengan garis horizontal
    st.markdown("---")

with st.container():
    st.subheader('Data Distribution & Outlier')
    st.write('Mari kita jelajahi keindahan distribusi data dan cari tahu cerita menarik di balik outlier! 😄✨')
    tab1, tab2 = st.tabs(["Data Distribution", "Data Outliers"])
    clean_data = air_quality.copy()
    clean_data['date'] = pd.to_datetime(clean_data[['year', 'month', 'day']])
    clean_data.interpolate(inplace=True)
    clean_data.drop_duplicates(inplace=True)
    
    with tab1:
        col3,col4 = st.columns([1,1])
        with col3:
            feature = st.selectbox(
                label="Choose the feature!",
                options=air_quality.columns[5:-1],
                key="feature_selectbox"  
            )
        with col4:
            station = st.selectbox(
                label="Choose the station!",
                options=clean_data['station'].unique(),
                key="station_selectbox" )

        plot = sns.histplot(clean_data.loc[clean_data['station'] == station][feature],kde=True)
            
        if clean_data.loc[clean_data['station'] == station][feature].dtype == 'object':
            plot.tick_params(axis='x', rotation=45)
            
        st.pyplot(plot.get_figure())
        
    with tab2:
        col5,col6 = st.columns([1,1])
        with col5:
            feature = st.selectbox(
                label="Choose the feature!",
                options=air_quality.columns[5:-1],
                key="feature_selectbox_2"  
            )
        
        with col6:
            station = st.selectbox(
                label="Choose the station!",
                options=clean_data['station'].unique(),
                key="station_selectbox_2" )
        
        data = clean_data.loc[clean_data['station'] == station]
        
        if clean_data[feature].dtype == 'float64' or clean_data[feature].dtype == 'int64': 
            col7,col8 = st.columns([2,1])
            with col7:  
                    fig, ax = plt.subplots()
                    ax.boxplot(x=clean_data.loc[clean_data['station'] == station][feature],vert=False)
                    ax.set_title(f'Boxplot for {feature} at {station}')
                    ax.set_ylabel('Values')
                    st.pyplot(fig)
                
            with col8:
                columns = [i for i in clean_data.select_dtypes(include=['int64', 'float64']).columns][5:]
                outlier = [data.loc[(data[i] < data[i].quantile(0.25) - 1.5 * (data[i].quantile(0.75) - data[i].quantile(0.25))) | (data[i] > data[i].quantile(0.75) + 1.5 * (data[i].quantile(0.75) - data[i].quantile(0.25))),i].size for i in columns]
                outlier = pd.Series(data=outlier,index = columns,name=f'all feature outliers size')
                st.write(outlier)
        else:
            columns = [i for i in clean_data.select_dtypes(include=['int64', 'float64']).columns][5:]
            outlier = [data.loc[(data[i] < data[i].quantile(0.25) - 1.5 * (data[i].quantile(0.75) - data[i].quantile(0.25))) | (data[i] > data[i].quantile(0.75) + 1.5 * (data[i].quantile(0.75) - data[i].quantile(0.25))),i].size for i in columns]
            outlier = pd.Series(data=outlier,index = columns,name=f'all feature outliers size')
            st.write(outlier)

with st.container():
    st.subheader("Data Correlation")
    
    tab3,tab4 = st.tabs(['All Feature','Choose Feature'])
    
    with tab3:
        plt.figure(figsize=(10, 8))
        plot = sns.heatmap(clean_data.select_dtypes('float64').corr(),annot=True)
        st.pyplot(plot.get_figure())
        
    with tab4:
        features = st.multiselect(
    label="Choose two feature!",
    options=(air_quality.columns[5:-1]),max_selections=2)

    if len(features) != 0:
        fig,ax = plt.subplots()
        plt.ylabel(features[1])
        plt.xlabel(features[0])
        ax.scatter(x=air_quality[features[0]],y=air_quality[features[1]],alpha=0.5)
        st.pyplot(fig)

with st.container():
    min_date = clean_data['date'].min().date()
    max_date = clean_data['date'].max().date()
    
    st.subheader("Data Visualization by Time and Station")
    col9, col10, col11 = st.columns([1, 1, 1])
      
    with col9:
        station = st.selectbox(label="Choose the station!", options=clean_data['station'].unique(), key='station_selectbox_3')
    with col10:
        date = st.date_input(label='Choose the date!', min_value=min_date)
    with col11:
        feature = st.selectbox(
            label="Choose the feature!",
            options=air_quality.columns[5:-1],
            key="feature_selectbox_3"  
        )
    

    filtered_data = clean_data.loc[(clean_data['date'] == str(date)) & (clean_data['station'] == station)]
    filtered_data = filtered_data.set_index('hour')[[feature]]
    st.line_chart(filtered_data)

    
with st.container():
    st.subheader("Trend Visualization")
    
    col12, col13, col14 = st.columns([1, 1, 1])
      
    with col12:
        station2 = st.selectbox(label="Choose the station!", options=clean_data['station'].unique(), key='station_selectbox_4')
    with col13:
        date2 = st.date_input(label='Choose the date!', min_value=min_date,key='select_date_2')
    with col14:
        feature2 = st.selectbox(
            label="Choose the feature!",
            options=air_quality.columns[5:-1],
            key="feature_selectbox_5"  
        )
        
    filtered_data = clean_data.loc[(clean_data['date'] == str(date2))]
    
    plt.figure(figsize=(10,5))
    plt.title(f"Trend of {feature2} at {station2}")
    plot = sns.lineplot(y=filtered_data[feature2], x=filtered_data['hour'], hue=filtered_data['station'])
    plt.xticks(rotation=45)
    st.pyplot(plot.get_figure())

    

    

    