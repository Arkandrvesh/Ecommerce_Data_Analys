import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
# Load datasets from local directory
customers = pd.read_csv('/data/customers_dataset.csv', delimiter=",")
geolocation = pd.read_csv('/data/geolocation_dataset.csv', delimiter=",")
order_items = pd.read_csv('/data/order_items_dataset.csv', delimiter=",")
order_payments = pd.read_csv('/data/order_payments_dataset.csv', delimiter=",")
order_reviews = pd.read_csv('/data/order_reviews_dataset.csv', delimiter=",")
orders = pd.read_csv('/data/orders_dataset.csv', delimiter=",")
product_category_translation = pd.read_csv('/data/product_category_name_translation.csv', delimiter=",")
products = pd.read_csv('/data/products_dataset.csv', delimiter=",")
sellers = pd.read_csv('/data/sellers_dataset.csv', delimiter=",")

# Load datasets from link drive
# order_url='https://drive.google.com/drive/folders/1Bi4FOZmQBecizCP1Yk0AcvK8ENS4B4rL/view?usp=drive_link'
# order_url='https://drive.google.com/uc?id=' + order_url.split('/')[-2]
# customers = pd.read_csv(order_url)


# Page title
st.title('E-commerce Data Analysis Dashboard')

# Cleaning Data section
st.header('Cleaning Data')

# Display missing data in products dataset
st.subheader('Missing Data in Products Dataset')
md_products = products[products.isna().any(axis=1)]
st.write(md_products)

# Drop missing values in products dataset
st.subheader('Products Dataset after Dropping Missing Values')
products = products.dropna()
st.write(products)

# Top cities in datasets
st.header('Top Cities in Datasets')
city_counts = geolocation['geolocation_city'].value_counts().head(5)
cust_city = customers['customer_city'].value_counts().head(6)
seller_city = sellers['seller_city'].value_counts().head(5)

# Visualizing top cities
st.subheader('Visualization of Top Cities')
fig, axes = plt.subplots(2, 2, figsize=(15, 8))
sns.countplot(data=geolocation[geolocation['geolocation_city'].isin(city_counts.index)], x='geolocation_city', ax=axes[0, 0])
sns.countplot(data=customers[customers['customer_city'].isin(city_counts.index)], x='customer_city', ax=axes[0, 1])
sns.countplot(data=sellers[sellers['seller_city'].isin(city_counts.index)], x = 'seller_city', ax=axes[1,0])
plt.tight_layout()
st.pyplot(fig)

# # Merge data to get customer information for each order
# cust_order_data = pd.merge(orders, customers, on='customer_id', how='left').dropna()
# # Menggabungkan data pelanggan dengan data pesanan berdasarkan kunci customer_id
# cust_order_data = pd.merge(orders, customers, on='customer_id', how='left')

# cust_order_data.to_csv('cust_order_data.csv', index=False)

# Visualization & Explanatory Analysis section
st.header('Visualization & Explanatory Analysis')

# Merge data to get customer information for each order
cust_order_data = pd.merge(orders, customers, on='customer_id', how='left')

#buat file
cust_order_data.to_csv('cust_order_data.csv', index=False)

# Convert order_purchase_timestamp to datetime format
cust_order_data['order_purchase_timestamp'] = pd.to_datetime(cust_order_data['order_purchase_timestamp'])

# Extract year from order_purchase_timestamp
cust_order_data['year'] = cust_order_data['order_purchase_timestamp'].dt.year

# Question 1: Average repeat orders from monthly active consumers each year
st.subheader('Average Repeat Orders from Monthly Active Customers Each Year')
# Group data by customer and year to find the average number of repeat orders per year
repeat_orders_per_year = cust_order_data.groupby(['year', 'customer_unique_id'])['order_id'].count().reset_index()
repeat_orders_per_year = repeat_orders_per_year.groupby('year')['order_id'].mean()

# Visualization
plt.figure(figsize=(10, 6))
sns.barplot(x=repeat_orders_per_year.index, y=repeat_orders_per_year.values, color='skyblue')
plt.title('Average Repeat Orders from Monthly Active Customers Each Year')
plt.xlabel('Year')
plt.ylabel('Average Repeat Orders')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Displaying average repeat orders per year
st.write("Average number of repeat orders from monthly active consumers each year:")
st.write(repeat_orders_per_year)

# Display the plot using st.pyplot() with figure argument
st.pyplot(plt.gcf())

# Conclusion for Question 1
st.subheader('Conclusion for Question 1')
st.markdown("""
Rata-rata jumlah pesanan ulang dari konsumen aktif bulanan setiap tahun adalah sebagai berikut:

Tahun 2016: 1.009202  
Tahun 2017: 1.017209  
Tahun 2018: 1.011783  

Ini menunjukkan bahwa secara umum, jumlah pesanan ulang dari konsumen aktif bulanan setiap tahunnya cukup stabil, dengan variasi yang relatif kecil.

Dalam hal hubungannya dengan geolokasi, dapat diasumsikan bahwa terdapat kemungkinan perbedaan dalam kebiasaan pesanan ulang antara berbagai daerah atau lokasi geografis. Variasi ini bisa dipengaruhi oleh berbagai faktor seperti preferensi konsumen lokal, ketersediaan produk, layanan pengiriman, dan faktor-faktor ekonomi regional.

Misalnya, area perkotaan mungkin memiliki kecenderungan pesanan ulang yang lebih tinggi karena aksesibilitas yang lebih baik terhadap berbagai macam produk dan layanan, sementara daerah pedesaan mungkin memiliki pola pembelian yang lebih jarang karena keterbatasan aksesibilitas atau pilihan produk yang lebih terbatas.

Oleh karena itu, untuk memahami hubungan antara rata-rata pesanan ulang konsumen dan geolokasi, perlu untuk melakukan analisis lebih lanjut dengan mempertimbangkan data geografis yang lebih spesifik dan faktor-faktor lain yang mungkin memengaruhi kebiasaan pembelian konsumen di setiap wilayah.
""")



# Question 2: Effect of cities on orders
st.subheader('Effect of Cities on Orders')
# Visualizing effect of cities on orders
plt.figure(figsize=(10, 6))
sns.countplot(data=cust_order_data, x='customer_city', order=cust_order_data['customer_city'].value_counts().index[:5])
plt.title('Effect of Cities on Orders')
plt.xlabel('City')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()

# Displaying top 5 cities with highest number of customers
st.write("Top 5 cities with the highest number of customers:")
st.write(customers['customer_city'].value_counts().head(5))

# Display the plot using st.pyplot() with figure argument
st.pyplot(plt.gcf())


# Conclusion for Question 1
st.subheader('Conclusion for Question 2')
st.markdown("""Dari hasil analisis data yang saya lakukan dan visualisasi nya menunjukan bahwasannya pengaruh lokasi sangat penting, dimana saya melakukan penyocokan grafik lokasi antar customer dan seller. Hasil daripada itu, order dari lokasi konsummennya menunjukan bahwa kota bernama sao paulo memiliki paling banyak sesuai dengan rata-rata lokasi dari customer dan seller.

Geolokasi dapat memiliki beberapa pengaruh yang signifikan:

Personalisasi Pengalaman Pengguna: Dengan menggunakan data geolokasi, platform e-commerce dapat menyajikan pengalaman yang lebih personal kepada pengguna. Misalnya, mereka dapat menyesuaikan tampilan situs web atau aplikasi dengan informasi lokal, seperti menampilkan harga dalam mata uang lokal, menyesuaikan penawaran promosi berdasarkan lokasi pengguna, atau menampilkan produk yang lebih relevan berdasarkan preferensi pembelian lokal.

Penyesuaian Logistik: Informasi geolokasi dapat membantu dalam manajemen rantai pasok dan logistik. Platform e-commerce dapat menggunakan data geolokasi untuk mengoptimalkan rute pengiriman, memperkirakan waktu pengiriman yang lebih akurat, atau menyesuaikan inventarisasi berdasarkan permintaan lokal.

Penargetan Geografis: Data geolokasi dapat digunakan untuk melakukan penargetan iklan yang lebih efektif. Platform e-commerce dapat menyesuaikan kampanye pemasaran mereka berdasarkan lokasi pengguna, memastikan bahwa iklan ditampilkan kepada audiens yang paling mungkin tertarik dengan produk atau layanan yang mereka tawarkan di wilayah tertentu.

Analisis Pasar Lokal: Data geolokasi dapat membantu dalam memahami perilaku pembelian konsumen di berbagai wilayah geografis. Ini dapat membantu platform e-commerce untuk mengidentifikasi tren pasar lokal, menyesuaikan strategi penjualan, dan mengoptimalkan portofolio produk mereka untuk memenuhi kebutuhan konsumen di setiap wilayah.

Keamanan Transaksi: Penggunaan data geolokasi dapat membantu dalam mengidentifikasi aktivitas penipuan atau transaksi mencurigakan. Dengan memeriksa apakah lokasi pengguna sesuai dengan alamat pengiriman atau lokasi transaksi sebelumnya, platform e-commerce dapat meningkatkan keamanan transaksi dan melindungi pelanggan mereka dari penipuan.

Dengan memanfaatkan data geolokasi dengan bijak, platform e-commerce dapat meningkatkan pengalaman pengguna, meningkatkan efisiensi operasional, dan meningkatkan kesuksesan bisnis secara keseluruhan. Namun, penting juga untuk memperhatikan privasi dan keamanan data pengguna saat menggunakan informasi geolokasi dalam konteks e-commerce.
""")
