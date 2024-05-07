import pypyodbc

cnxn = pypyodbc.connect('DRIVER={HFSQL};Server Name=192.168.0.21;Server Port=4900;Database=BAC_A_SABLE;UID=admin;PWD=Clip_SERENA; IntegrityCheck=1')
                          #Trusted_Connection=yes;

cursor = cnxn.cursor()

cursor.execute('SELECT * FROM AFFAIRE WHERE NAF < 1000')

for row in cursor:
    print(row)