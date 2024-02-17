import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu

@st.cache_data
#Load Data CSV
def load_data(url) :
    missing_value_format = ['N.A', 'na', 'n.a.','n/a','?','-']
    df = pd.read_csv(url, na_values = missing_value_format)
    return df


def udaraBuruk(allData):
    
    #Menampilkan Data 2016
    datamentah = allData[allData['year'] == 2016]

    #Sorting untuk udara terkotor
    data2016 = datamentah.sort_values(by = ['PM2.5', 'PM10', "SO2", "NO2", "CO", "O3"], ascending = False)

    #Menampilkan Stasiun Mana Yang Mempunyai Udara Buruk
    cuacaBuruk = (data2016['PM2.5'] >= 65) | (data2016['PM10'] >= 150) | (data2016['SO2'] > 350) | (data2016['NO2'] > 400) | (data2016['CO'] > 30000) |(data2016['O3'] > 235)
    Udaraburuk2016 = data2016.drop(["TEMP", "PRES", "DEWP", "RAIN", "wd", "WSPM", "year", "month", "day", "hour"], axis = 1)[cuacaBuruk] 

    station = Udaraburuk2016['station']
    rekapstation = {}

    for data in station:
        if data in rekapstation:
            rekapstation[data] += 1
        else:
            rekapstation[data] = 1

    #Memanggil 5 Station Terburuk
    df_rekapstation = pd.DataFrame(rekapstation.values(), index = rekapstation.keys())
    df_rekapstation = df_rekapstation.sort_values(by=0, ascending = False)
    stationburuk = df_rekapstation.head(5)
    
    #Pengiriman Tepat Waktu dan Terlambat
    nama_station = ['Gucheng', 'Wanshouxigong', 'Dongsi', 'Guanyuan', 'Tiantan']
    data_udara_buruk = pd.DataFrame({
        'Jumlah': stationburuk[0]
    })

    #Menampilkan Pie Chart
    col1, col2 = st.columns([3,1])

    with col1:
        warna = ['#1068c9', '#03396c', '#005b96','#6497b1', '#b3cde0']
        fig, ax = plt.subplots()
        ax.pie(
            stationburuk[0],
            labels=nama_station,
            autopct='%1.1f%%',
            colors=warna,
        )
        ax.axis('equal')
        st.pyplot(fig)

    with col2:
        st.dataframe(data_udara_buruk)

    #Expander Grafik
    with st.expander("Mengapa 5 Station itu mendapatkan Kualitas udara Terburuk pada Tahun 2016?") :
        st.write("Dikarenakan Partikel PM2.5 dan PM10 serta Senyawa SO2, NO2, CO, O3 selalu naik melebihi batas normal sampai 65 µgram/m^3 dan 150 µgram/m^3 bagi PM2.5 dan PM10. Penyebab dari Partikel udara dan Senyawa tersebut meningkat yaitu udara panas, kebakaran dan polusi lingkungan. Jadi alangkah baiknya untuk menjaga lingkungan station tetap bersih, menanam lebih banyak tanaman dan vegetasi di sekitar area station untuk membantu menyaring udara dan menyerap polutan, mengurangi penggunaan kendaraan di area station, serta mengedukasi masyarakat untuk menggunakan kendaraan ramah lingkungan seperti sepeda atau minimal menghimbau kepada calon penumpang untuk menggunakan kendaraan umum ketika datang station sehingga kedua Partikel udara dan Senyawa tersebut tidak meningkat sampai melebihi batas normalnya.")


def partikel_berpengaruh(allData):

    #Menghitung data udara yang melebihi batas amannya
    partikelPM25 = allData[allData['PM2.5'] >= 66]
    udaraBurukPM25 = partikelPM25.groupby(['station', 'year'])[['PM2.5']].count().reset_index()

    partikelPM10 = allData[allData['PM10'] >= 150]
    udaraBurukPM10 = partikelPM10.groupby(['station', 'year'])[['PM10']].count().reset_index()

    partikelSO2 = allData[allData['SO2'] >= 350]
    udaraBurukSO2 = partikelSO2.groupby(['station', 'year'])[['SO2']].count().reset_index()

    partikelNO2 = allData[allData['NO2'] >= 400]
    udaraBurukNO2 = partikelNO2.groupby(['station', 'year'])[['NO2']].count().reset_index()

    partikelCO = allData[allData['CO'] >= 3000]
    udaraBurukCO = partikelCO.groupby(['station', 'year'])[['CO']].count().reset_index()

    partikelO3 = allData[allData['O3'] >= 235]
    udaraBurukO3 = partikelO3.groupby(['station', 'year'])[['O3']].count().reset_index()   

    #menggabungkan data udara yang yang melebihi batas aman
    rangeUdaraBurukMerger1 = pd.merge(udaraBurukPM25, udaraBurukPM10, how = 'left')
    rangeUdaraBurukMerger2 = pd.merge(udaraBurukSO2, udaraBurukNO2, how = 'left')
    rangeUdaraBurukMerger3 = pd.merge(udaraBurukCO, udaraBurukO3, how = 'left')
    rangeUdaraBurukMerger4 = pd.merge(rangeUdaraBurukMerger1, rangeUdaraBurukMerger2, how = 'left')
    dataUdaraBuruk = pd.merge(rangeUdaraBurukMerger4, rangeUdaraBurukMerger3, how = 'left') 

    # Mengganti NaN Menjadi 0 Karena NaN Merupakan Data Partikel Yang Tidak Melewati Ambang Batas Aman Maka Dihitung Menjadi 0 
    dataUdaraBuruk.fillna(0, inplace = True)

    #memisahkan data berdasarkan stasiunnya
    stations = dataUdaraBuruk['station'].unique()
    polutans = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    for stasiun in stations:
        perStationData = dataUdaraBuruk[dataUdaraBuruk['station'] == stasiun]
        perStationData.set_index('year')
        print(f'Data Udara Buruk Station {stasiun}')
    
    stations = dataUdaraBuruk['station'].unique()
    polutans = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    tahun = [2013, 2014, 2015, 2016, 2017]

    getStation = dataUdaraBuruk[dataUdaraBuruk['station'] == station]
    getStation.set_index('year')

    x = np.arange(len(tahun))
    w = 0.17
    fig, ax = plt.subplots(figsize=(14,10))
    
    barplotPM25 = ax.bar(x-w*2, getStation['PM2.5'], w, label="PM2.5")
    barplotPM10 = ax.bar(x-w, getStation['PM10'], w, label="PM10")
    barplotSO2 = ax.bar(x, getStation['SO2'], w, label="SO2")
    barplotNO2 = ax.bar(x+w*0.5, getStation['NO2'], w, label="NO2")
    barplotCO = ax.bar(x+w*1.5, getStation['CO'], w, label="CO")

    ax.bar_label(barplotPM25, labels=getStation['PM2.5'].astype(int))
    ax.bar_label(barplotPM10, labels=getStation['PM10'].astype(int))
    ax.bar_label(barplotSO2, labels=getStation['SO2'].astype(int))
    ax.bar_label(barplotNO2, labels=getStation['NO2'].astype(int))
    ax.bar_label(barplotCO, labels=getStation['CO'].astype(int))

    plt.title(f'Data Perhitungan Polutan Yang Melebihi Batas Aman Di Station {station}')
    plt.ylabel('Perhitungan Polutan Yang Melebihi Batas Aman')
    plt.legend()
    plt.xticks(x, tahun)
    st.pyplot(fig)
    
    st.write(f'Terlihat pada Grouped Bar Chart diatas bahwa partikel udara yang paling sering mempengaruhi di station {station} adalah partikel PM2.5.')
    st.write('Yaitu: ')
    for i in range(len(tahun)):
        st.write(f'- Pada tahun {tahun[i]} sebanyak {getStation["PM2.5"].reset_index()["PM2.5"][i]} kali melebihi ambang batas')
    

def arah_angin(allData):

    #filter data berdasarkan partikel yang melebihi ambang batas aman yang tersebar di udara pada semua stasiun
    udaraBuruk = (allData['PM2.5'] >= 66) | (allData['PM10'] >= 150) | (allData['SO2'] > 350) | (allData['NO2'] > 400) | (allData['CO'] > 30000) |(allData['O3'] > 235)
    dfUdaraBuruk = allData[udaraBuruk]

    arahAngin = list(dfUdaraBuruk['wd'])
    rekapArahAngin = {}
    for data in arahAngin:
        if data in rekapArahAngin:
            rekapArahAngin[data] += 1
        else:
            rekapArahAngin[data] = 1

    sortArahAngin = dict(sorted(rekapArahAngin.items(), key = lambda item: item[1], reverse = True))

    keys = sortArahAngin.keys()
    values = sortArahAngin.values()

    # Buat plot menggunakan Matplotlib
    fig, ax = plt.subplots()
    ax.bar(keys, values)

    ax.set_xticklabels(sortArahAngin.keys(), rotation=90)
    ax.set_xlabel('Arah Angin')
    ax.set_ylabel('Banyaknya Terjadi')
    ax.set_title('Arah Angin Saat Terjadinya Udara Buruk di 12 stasiun dari Tahun 2013-2017')
    st.pyplot(fig)
    
    #Expander Grafik
    with st.expander("Arah angin yang paling sering mempengaruhi kualitas udara di semua stasiun") :
        st.write(f'Dari bar chart di atas terlihat bahwa ketika arah angin mengarah di antara Timur hingga Utara kualitas udara sering menurun. Maka dari itu ketika arah angin terasa mengarah ke sana di himbau untuk semua stasiun untuk bersiap untuk melakukan pencegahan menurunnya kualitas udara di stasiun.')

def pengaruh_hujan(sub_menu):
    #Filter Data Rata-Rata Tidak Hujan Setiap tahun
    notRainyYear = allData[allData['RAIN'] == 0 ]
    meanNotRainyYear = notRainyYear.groupby(['year', 'station'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

    #Filter Data Rata-Rata Hujan Setiap tahun
    rainyYear = allData[allData['RAIN'] > 0 ]
    meanRainyYear = rainyYear.groupby(['year','station'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

    #Filter Data Rata-Rata Tidak Hujan Setiap Bulan
    notRainyMonth = allData[allData['RAIN'] == 0 ]
    meanNotRainyMonth = notRainyMonth.groupby(['year', 'month', 'station'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

    #Filter Data Rata-Rata Hujan Setiap Bulan
    rainyMonth = allData[allData['RAIN'] > 0 ]
    meanRainyMonth = rainyMonth.groupby(['year', 'month', 'station'])[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

    #bahan untuk melakukan analisis lebih lanjut terkait pengaruh hujan
    resultMeanNotRainyYear = meanNotRainyYear.reset_index()
    resultMeanRainyYear    = meanRainyYear.reset_index()
    resultMeanNotRainyMonth = meanNotRainyMonth.reset_index()
    resultMeanRainyMonth = meanRainyMonth.reset_index()

    # Ambil unik stasiun dari data yang telah di filter
    stations = resultMeanNotRainyYear['station'].unique()
    years = resultMeanNotRainyYear['year'].unique()

    pollutants = ['PM2.5', 'PM10','SO2', 'NO2','CO' , 'O3']
    
    if (sub_menu == 'Pengaruh Hujan Per Tahun') or (sub_menu== 'Pengaruh Hujan Per Bulan'):
        station = st.selectbox (label = "Pilih Stasiun",
        options = (
                    "Aotizhongxin",
                    "Changping",
                    "Dingling", 
                    "Dongsi",
                    "Guanyuan", 
                    "Gucheng", 
                    "Huairou", 
                    "Nongzhanguan", 
                    'Shunyi',
                    "Tiantan", 
                    'Wanliu', 
                    'Wanshouxigong'
                )
        )
    else:

        if not sub_menu == 'Kesimpulan':
            arrayStationCountRainy = np.array([], dtype=int)

            for station in stations:
                allDataPerStation = rainyYear[rainyYear['station'] == station].shape[0]
                arrayStationCountRainy = np.append(arrayStationCountRainy, allDataPerStation)

            if sub_menu == 'Persentase tingkat polutan setiap tahunnya pada saat hujan di station yang per sedikit turun hujan' :
                st.markdown(f'Stasiun yang paling sedikit turun hujan adalah **{stations[arrayStationCountRainy.argmin()]}** dengan jumlah {arrayStationCountRainy.min()} kali', )
            else:
                st.markdown(f'Stasiun yang paling sering turun hujan adalah **{stations[arrayStationCountRainy.argmax()]}** dengan jumlah {arrayStationCountRainy.max()} kali', )
            
            st.markdown('''
            **Catatan :**
            - Persentase > 0 artinya penurunan tingkat partikel
            - Persentase < 0 artinya kenaikan tingkat partikel
            ''')

            # Mengambil data rerata hari-hari hujan dan tidak hujan station Nongzhanguan
            resultRainyNongzhanguan = resultMeanRainyYear[resultMeanRainyYear['station'] == 'Nongzhanguan']
            resultNotRainyNongzhanguan = resultMeanNotRainyYear[resultMeanNotRainyYear['station'] == 'Nongzhanguan']

            # Mengambil data hujan dan tidak hujan station Shunyi
            resultRainyShunyi = resultMeanRainyYear[resultMeanRainyYear['station'] == 'Shunyi']
            resultNotRainyShunyi = resultMeanNotRainyYear[resultMeanNotRainyYear['station'] == 'Shunyi']

            #Menghitung persentase penurunan atau kenaikan tingkat polutan pada saat hujan
            rainyPolutanNongzhanguan = resultRainyNongzhanguan[pollutants]
            notRainyPolutanNongzhanguan = resultNotRainyNongzhanguan[pollutants]

            reductionNongzhanguan = ((notRainyPolutanNongzhanguan - rainyPolutanNongzhanguan) / notRainyPolutanNongzhanguan) * 100

            rainyPolutanShunyi = resultRainyShunyi[pollutants]
            notRainyPolutanShunyi = resultNotRainyShunyi[pollutants]

            reductionShunyi = ((notRainyPolutanShunyi - rainyPolutanShunyi) / notRainyPolutanShunyi) * 100

    if sub_menu == 'Pengaruh Hujan Per Tahun':

        tab1,tab2 = st.tabs(["Visualisasi", "Keterangan"])
        with tab1 :
            stationDataNotRainyYear = resultMeanNotRainyYear[resultMeanNotRainyYear['station'] == station]
            stationDataRainyYear = resultMeanRainyYear[resultMeanRainyYear['station'] == station]
            
            stationDataMerge = pd.merge(stationDataNotRainyYear, stationDataRainyYear, on='year', suffixes=('_tidak_hujan', '_hujan'))
            
            selectedColumns = [f'{pollutant}_{condition}' for condition in ['tidak_hujan', 'hujan'] for pollutant in pollutants]
            dataToPlot = stationDataMerge.set_index('year')[selectedColumns]

            fig = plt.figure(figsize=(16,8))

            sns.heatmap(dataToPlot.T, cmap='coolwarm', annot=True, fmt=".2f", linewidths=0.5, annot_kws={"fontsize":14})
            plt.title(f'Perbandingan Tingkat Polutan (Hujan vs Tidak Hujan) di Stasiun {station}')
            plt.xlabel('Tahun')
            plt.ylabel('Polutan')
            st.pyplot(fig)
        with tab2 :
            st.write('Dari hasil visualisasi tersebut berdasarkan data tahunan tingkat polutan pada saat hujan dan tidak hujan menunjukan bahwa hujan itu cukup mempengaruhi terhadap kualitas udara. Dapat dilihat tingkat partikel-partikel pada saat hujan turun beberapa persen dibandingkan pada saat tidak hujan. Tapi, jika dilihat dari partikel CO pada tahun 2013 selalu mengalami kenaikan pada saat hujan.')

    elif sub_menu == 'Pengaruh Hujan Per Bulan':

        tab1,tab2 = st.tabs(["Visualisasi", "Keterangan"])
        with tab1 :
            stationDataNotRainyMonth = resultMeanNotRainyMonth[resultMeanNotRainyMonth['station'] == station]
            stationDataRainyMonth = resultMeanRainyMonth[resultMeanRainyMonth['station'] == station]

            stationDataMerge = pd.merge(stationDataNotRainyMonth, stationDataRainyMonth, on=['year', 'month'], suffixes=('_tidak_hujan', '_hujan'))

            selectedData = [f'{pollutant}_{condition}' for condition in ['tidak_hujan', 'hujan'] for pollutant in pollutants]
            dataToPlot = stationDataMerge.set_index(['year','month'])[selectedData]

            fig = plt.figure(figsize=(18,18))
            
            sns.heatmap(dataToPlot, cmap="coolwarm", annot=True ,fmt=".2f", linewidth=0.8, annot_kws={"fontsize":14})
            plt.title(f'Perbandingan Tingkat Polutan (Hujan vs Tidak Hujan) di Stasiun {station}')
            plt.xlabel("Polutan")
            plt.ylabel("Tahun dan Bulan")
            st.pyplot(fig)
        with tab2 :
            st.write('Jika dilihat dari heatmap tersebut menunjukan bahwa tingkat polutan setiap bulannya tidak selalu signifikan menurun untuk beberapa jenis partikel di setiap stasionnya. Terutama pada tahun 2014 bulan ke 11 (2014-11), pada saat hujan terutama partikel PM2.5, PM10, dan CO mengalami lonjakan yang cukup tinggi. Mungkin untuk suatu kondisi hujan bisa saja memperburuk kondisi udara.')

    elif sub_menu == 'Persentase tingkat polutan per tahunnya pada saat hujan di station yang paling sering turun hujan':
        
        tab1,tab2 = st.tabs(["Visualisasi", "Keterangan"])
        with tab1 :
            for pollutant in pollutants:
                fig, ax = plt.subplots()
                barplot = ax.bar(years, round(reductionNongzhanguan[pollutant], 2), label=pollutant, data=reductionNongzhanguan[pollutant])

                # Tambahkan label ke setiap bar
                for bar in barplot:
                    yval = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', va='bottom', ha='center')

                ax.set_xlabel('Tahun')
                ax.set_ylabel('Persentase Polutan')
                ax.set_title(f'Persentase Penurunan Tingkat Polutan {pollutant} Setiap Tahunnya pada saat hujan di Stasion Nongzhanguan', fontdict={'fontsize':10})
                ax.legend()

                st.pyplot(fig)
        with tab2 :
            st.write('Dari visualisasi tersebut menunjukan bahwa yang paling signifikan mengalami penurunan pada saat hujan adalah partikel _SO2, PM10,_ dan _NO2_ karena dilihat dari persentasenya yang dominan. Hujan masih cukup berpengaruh untuk 3 partikel lainnya yaitu _PM2.5, CO,_ dan _O3_. Namun, tidak sesignifikan _SO2, PM10,_ dan _NO2_. Bahkan, untuk partikel _CO_ mengalami kenaikan di tahun 2013 dan _O3_ mengalami kenaikan di tahun 2014.')

    elif sub_menu == 'Persentase tingkat polutan setiap tahunnya pada saat hujan di station yang per sedikit turun hujan':
        tab1,tab2 = st.tabs(["Visualisasi", "Keterangan"])
        with tab1 :
            for pollutant in pollutants:
                
                fig, ax = plt.subplots()
                barplot = ax.bar(years, round(reductionShunyi[pollutant], 2), label=pollutant, color='orange', data=reductionShunyi[pollutant])

                # Tambahkan label ke setiap bar
                for bar in barplot:
                    yval = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', va='bottom', ha='center')
                
                ax.set_xlabel('Tahun')
                ax.set_ylabel('Persentase Polutan')
                ax.set_title(f'Persentase Penurunan Tingkat Polutan {pollutant} Setiap Tahunnya pada saat hujan di Stasion Shunyi', fontdict={'fontsize':10})
                ax.legend()

                st.pyplot(fig)
            with tab2 :
                st.write('Jika dilihat dari hasil visualisasi diatas menunjukan bahwa pada station yang paling jarang turun hujan sekalipun, hujan sangat baik dalam mengurai partikel _PM10_ dan _SO2_. Hal tersebut ditunjukan dengan persentase penurunan yang sangat baik dari tahun ke tahun. Namun, untuk suatu kondisi hujan tidak dapat mengurai dengan baik seperti _PM2.5_ di tahun 2013, _NO2_ di tahun 2017, _CO_ di tahun 2013 dan 2015, _O3_ di tahun 2014.')
    else:
        st.write(
            '''
            **Bagaimana pengaruh hujan terhadap kualitas udara? apa pengaruh nya? Jika partikel polutan mengalami penurunan partikel mana yang mengalami penurunan secara signifikan pada saat hujan ?**

            Tentu, dari hasil analisis bahwa hujan berpengaruh terhadap kualitas udara. Dimana seperti yang ditunjukan pada diagram station Nongzhanguan (station sering turun hujan) semakin sering hujan maka dapat menurunkan kadar/tingkat polutan dengan cukup sangat baik untuk mengurai partikel _PM2.5, PM10, SO2,_ dan _NO2_ tanpa adanya kenaikan kadar/tingkat polutan di tahun-tahun tertentu. Namun, semakin jarang adanya hujan maka ada kemungkinan besar kadar polutan meningkat. Ditunjukan pada diagram station shunyi (station yang jarang hujan) terlihat bahwa ditahun tertentu partikel polutan seperti _PM2.5, NO2, CO,_ dan _O3_ meningkat, tetapi partikel _PM10_ dan _SO2_ setiap tahunnya selalu ada penurunan pada saat hujan.

            Artinya dari hal tersebut sudah cukup membuktikan bahwa hujan mampu untuk mengurai/membersihkan kadar/tingkat polutan terutama partikel _PM10_ dan _SO2_. Mungkin terdapat alasan untuk beberapa kondisi mengapa hujan dapat menyebabkan meningkatnya beberapa partikel polutan di udara. Jadi, agar lebih efektif dalam penurunan tingkat polutan alangkah baiknya station selalu menjaga kebersihan udara terutama pada saat hujan dan lebih baik lagi jika pihak station bekerjasama dengan pemerintah setempat untuk mengedukasi masyarakat sekitar station untuk turut membantu menjaga kebersihan udara.
            '''
        )

def pengaruh_temp():
    # data from https://allisonhorst.github.io/palmerpenguins/

    partikel = ("2013", "2014", "2015", '2016')
    Temp_Tinggi = {
        'PM2.5': (17.0, 25.0, 81.0, 16.00),						 											
        'PM10': (33.0, 33.0, 81.0, 19.0),
        'S02': (4.0, 4.0, 4.0, 4.0),
        'NO2': (9.0, 14.0, 20.0, 4.0),
        'CO' : (200.0, 400.0, 700.0, 400.0),
        'O3' : (178.0, 226.0, 325.0, 189.0)
    }

    x = np.arange(len(partikel))  # the label locations
    width = 0.1  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in Temp_Tinggi.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Length (mm)')
    ax.set_title('Temp Tinggi')
    ax.set_xticks(x + width, partikel)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 800)

    st.pyplot(fig)


    # data from https://allisonhorst.github.io/palmerpenguins/

    partikel = ("2013", "2014", "2015", '2016')
    Temp_Rendah = {
        'PM2.5': (56.0, 95.0, 95.0, 8.0),						 											
        'PM10': (67.0, 100.0, 98.0, 19.0),
        'S02': (34.0, 33.0, 32.0, 6.0),
        'NO2': (49.0, 82.0, 75.0, 16.0),
        'CO' : (1300.0, 3200.0, 2700.0, 600.0),
        'O3' : (2.0, 4.0, 6.0, 60.0)
    }

    x = np.arange(len(partikel))  # the label locations
    width = 0.1  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in Temp_Rendah.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Length (mm)')
    ax.set_title('Temp Rendah')
    ax.set_xticks(x + width, partikel)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 3500)

    st.pyplot(fig)

    with st.expander("Apakah di Station Tiantan Temp mempengaruhi kualitas udara?") :
        st.write(f'Terlihat bahwa Temp tidak terlalu mempengaruhi partikel PM2.5 dan PM10 pada tahun 2015 dan 2016. Tetapi, jika dilihat dari visualisasi diatas menunjukan bahwa pada suhu dingin tingkat polutan mengalami lebih banyak peningkatan yang melebihi ambang batas terutama partikel CO. Namun, khusus partikel O3 pada suhu tinggi justru mengalami peningkatan yang jauh lebih tinggi dibandingkan suhu rendah. Pada musim dingin, polusi udara dapat menjadi masalah karena dapat menyebabkan penumpukan partikel polutan di udara. Oleh karena itu, melakukan pembersihan dan perawatan berkala pada peralatan di sekitar stasiun kereta untuk mengurangi debu dan partikel lain yang dapat menyebabkan polusi udara serta untuk pihak station agar menghimbau calon penumpangnya khususnya pada musim dingin agar tidak membawa kendaraan pribadi ke area station (untuk kondisi tertentu seperti kepadatan station) atau pihak station membatasi jumlah kendaraan pribadi calon penumpang.')



df_aotizhongxin  = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Aotizhongxin_20130301-20170228.csv')
df_changping     = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Changping_20130301-20170228.csv')
df_dingling      = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Dingling_20130301-20170228.csv')
df_dongsi        = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Dongsi_20130301-20170228.csv')
df_guanyuan      = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Guanyuan_20130301-20170228.csv')
df_gucheng       = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Gucheng_20130301-20170228.csv')
df_huairou       = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Huairou_20130301-20170228.csv')
df_nongzhanguan  = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Nongzhanguan_20130301-20170228.csv')
df_shunyi        = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Shunyi_20130301-20170228.csv')
df_tiantan       = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Tiantan_20130301-20170228.csv')
df_wanliu        = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Wanliu_20130301-20170228.csv')
df_wanshouxigong = load_data('https://raw.githubusercontent.com/Hathappend/StreamlitDashboard-PSD/master/PRSA_Data_Wanshouxigong_20130301-20170228.csv')

#Cleaning data
df_aotizhongxin.dropna(axis=0, inplace=True)
df_aotizhongxin.reset_index(drop=True, inplace=True)

df_changping.dropna(axis=0, inplace=True)
df_changping.reset_index(drop=True, inplace=True)

df_dingling.dropna(axis=0, inplace=True)
df_dingling.reset_index(drop=True, inplace=True)

df_dongsi.dropna(axis=0, inplace=True)
df_dongsi.reset_index(drop=True, inplace=True)

df_guanyuan.dropna(axis=0, inplace=True)
df_guanyuan.reset_index(drop=True, inplace=True)

df_gucheng.dropna(axis=0, inplace=True)
df_gucheng.reset_index(drop=True, inplace=True)

df_huairou.dropna(axis=0, inplace=True)
df_huairou.reset_index(drop=True, inplace=True)

df_nongzhanguan.dropna(axis=0, inplace=True)
df_nongzhanguan.reset_index(drop=True, inplace=True)

df_shunyi.dropna(axis=0, inplace=True)
df_shunyi.reset_index(drop=True, inplace=True)

df_tiantan.dropna(axis=0, inplace=True)
df_tiantan.reset_index(drop=True, inplace=True)

df_wanliu.dropna(axis=0, inplace=True)
df_wanliu.reset_index(drop=True, inplace=True)

df_wanshouxigong.dropna(axis=0, inplace=True)
df_wanshouxigong.reset_index(drop=True, inplace=True)

#Data Join
allData = pd.concat([df_aotizhongxin, df_changping, df_dingling, df_dongsi, df_guanyuan, df_gucheng, df_huairou, df_nongzhanguan, df_shunyi, df_tiantan, df_wanliu, df_wanshouxigong])

#Style CSS Custom
card_style = """
    <style>
        .card {
            border: 1px solid #e6e6e6;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            
        }
        .card-header{
            height:220px;
        }
        .card-header img {
            display: block;
            max-height: 100%; /* Atur tinggi maksimum gambar di sini */
            max-width: 100%; /* Pastikan gambar tidak melebihi lebar kartu header */
            object-fit: contain; /* Menjaga proporsi gambar */
            margin: 0 auto;
        }

        .card-content{
            width:100%;
            height:230px;
            text-align:center;
            margin-top:20px;
        }

        .card-content p{
            padding:20px;
        }
    
    </style>
    """

with st.sidebar :
    selected = option_menu('Menu',['Beranda', 'Udara Buruk','Pengaruh Suhu', 'Pengaruh Polutan', 'Arah Angin', 'Pengaruh Hujan'],
    icons =["easel2"],
    menu_icon="cast",
    default_index=0)

if (selected == 'Beranda') :
    st.header(f"Analisis Kualitas Udara")
    st.markdown("***")
    st.write('Pada analisis ini akan mencari dan menemukan insight dari beberapa **pertanyaan bisnis** dibawah ini:')
    st.markdown(
        '''
        - Bagaimana pengaruh hujan terhadap kualitas udara? apa pengaruh nya? Jika partikel polutan mengalami penurunan partikel mana yang mengalami penurunan secara signifikan pada saat hujan ? - 10122004 - Asep Yaman Suryaman
        - Cari 5 station dengan Kualitas udara terburuk di tahun 2016 - 10122027 - Bambang Firman
        - Apakah di station Tiantan temp mempengaruhi kualitas udara - 10122024 - Dzaky Farras Fauzan
        - Partikel apa yang paling sering mempengaruhi kualitas udara menjadi buruk di setiap station pertahunya? - 10122035 - Dendi Ramdhani
        - Arah angin yang paling sering mempengaruhi kualitas udara di semua stasiun - 10122010 - Tito Muhammad Athoriq
        '''
    )
    st.markdown("***")
    st.markdown('##### Team Contributor : ')
    col1, col2 = st.columns([2,2])
    # Tambahkan CSS ke aplikasi Streamlit
    col1.markdown(card_style, unsafe_allow_html=True)
    col2.markdown(card_style, unsafe_allow_html=True)

    # Membuat card
    with col1:
        st.markdown(
            '''
            <div class='card'>
                <div class='card-header'>
                    <img class="image" src='https://github.com/Hathappend/StreamlitDashboard-PSD/blob/master/img-profile/tito.png?raw=true'>
                </div>
                <div class='card-content'>
                    <h5>10122010  <br>Tito Muhammad Athoriq</h5> 
                    <p>
                    Menganalisis terkait <b>arah angin</b> untuk mencari tahu seberapa sering mempengaruhi kualitas udara di semua stasiun
                    </p>
                </div>
            </div>
            ''', 
            unsafe_allow_html=True)

        st.markdown(
            '''
            <div class='card'>
                <div class='card-header'>
                    <img class="image" src='https://github.com/Hathappend/StreamlitDashboard-PSD/blob/master/img-profile/dendi.png?raw=true'>
                </div>
                <div class='card-content'>
                    <h5>10122035  <br>Dendi Ramdhani</h5> 
                    <p>
                    Menganalisis terkait <b>pengaruh polutan</b> yang sering mempengaruhi kualitas udara di setiap stasiun nya
                    </p>
                </div>
            </div>
            ''', 
            unsafe_allow_html=True)
        
        st.markdown(
            '''
            <div class='card'>
                <div class='card-header'>
                    <img class="image" src='https://github.com/Hathappend/StreamlitDashboard-PSD/blob/master/img-profile/dzaky.png?raw=true'>
                </div>
                <div class='card-content'>
                    <h5>10122024  <br>Dzaky Farras Fauzan</h5> 
                    <p>
                    Menganalisis terkait <b>pengaruh suhu</b> Temperature yang fokus analisis nya hanya pada stasiun Tiantan
                    </p>
                </div>
            </div>
            ''', 
            unsafe_allow_html=True)
            
    with col2:
        st.markdown(
            '''
            <div class='card'>
                <div class='card-header'>
                    <img class="image" src='https://github.com/Hathappend/StreamlitDashboard-PSD/blob/master/img-profile/asep.png?raw=true'>
                </div>
                <div class='card-content'>
                    <h5>10122004  <br>Asep Yaman Suryaman</h5> 
                    <p>
                    Menganalisis terkait <b>pengaruh hujan</b> terhadap tingkat partikel polutan dan mengetahui partikel mana saja yang terpengaruh
                    </p>
                </div>
            </div>
            ''', 
            unsafe_allow_html=True)

        st.markdown(
            '''
            <div class='card'>
                <div class='card-header'>
                    <img class="image" src='https://github.com/Hathappend/StreamlitDashboard-PSD/blob/master/img-profile/bambang.png?raw=true'>
                </div>
                <div class='card-content'>
                    <h5>10122027  <br>Bambang Firman Fatoni</h5> 
                    <p>
                    Menganalisis terkait kualitas <b>udara buruk</b> di 5 Station yang mendapatkan Kualitas udara Terburuk pada Tahun 2016
                    </p>
                </div>
            </div>
            ''', 
            unsafe_allow_html=True)
            
elif(selected == "Udara Buruk"):
    st.header("5 Stasiun yang Sering Terjadi Udara Terburuk")
    st.write('by : 10122027 - Bambang Firman Fatoni')
    st.markdown("***")
    udaraBuruk(allData)
elif(selected == "Pengaruh Suhu"):
    st.header("Pengaruh Temperature Terhadap Kualitas Udara di Tiantan")
    st.write('by : 10122024 - Dzaky Farras Fauzan')
    st.markdown("***")
    pengaruh_temp()
elif(selected == "Pengaruh Polutan"):
    st.header("Partikel yang paling sering mempengaruhi kualitas udara menjadi buruk di setiap station pertahunya")
    st.write('by : 10122035 - Dendi Ramdhani')
    st.markdown("***")
    station = st.selectbox(
        label = "Pilih Stasiun",
        options = (
                    "Aotizhongxin",
                    "Changping",
                    "Dingling", 
                    "Dongsi",
                    "Guanyuan", 
                    "Gucheng", 
                    "Huairou", 
                    "Nongzhanguan", 
                    'Shunyi',
                    "Tiantan", 
                    'Wanliu', 
                    'Wanshouxigong'
                )
    )
    partikel_berpengaruh(allData)
elif(selected == "Arah Angin"):
    st.header("Arah Mata Angin yang Banyak Mempengaruhi Cuaca Buruk")
    st.write('by : 10122010 - Tito Muhammad Athoriq')
    st.markdown("***")
    arah_angin(allData)
elif(selected == "Pengaruh Hujan"):
    st.header("Pengaruh hujan terhadap tingkat partikel polutan")
    st.write('by : 10122004 - Asep Yaman Suryaman')
    st.markdown("***")
    sub_menu = st.selectbox('Pilih Submenu', ['Pengaruh Hujan Per Tahun', 'Pengaruh Hujan Per Bulan', 'Persentase tingkat polutan per tahunnya pada saat hujan di station yang paling sering turun hujan', 'Persentase tingkat polutan setiap tahunnya pada saat hujan di station yang per sedikit turun hujan', 'Kesimpulan'])
    pengaruh_hujan(sub_menu)