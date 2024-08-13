import pandas as pd

#.xlsx dosyayı oku
df = pd.read_excel('C:/Users/ersin/Desktop/webserver_log_files/0_all/all_bad_good_0_1_real.xlsx')

#.csv dosyaya kaydet
df.to_csv('C:/Users/ersin/Desktop/webserver_log_files/0_all/all_bad_good_0_1_real.csv', index=False)