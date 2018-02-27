import pymssql
if __name__ == "__main__":
    conn = pymssql.connect(host='127.0.0.1', user='sa', password='0000', database='QIDATA')
    cur = conn.cursor()
    sql = "CREATE TABLE  stock_basics(stockcode NVARCHAR(25) PRIMARY KEY, name VARCHAR(25),industry  VARCHAR(25)" \
        ", area VARCHAR(25),pe float, outstanding float, totals float, totalAssets float, liquidAssets float," \
        "fixedAssets float,  " \
        "reserved float,reservedPerShare float,esp float,bvps float,pb float,timeToMarket VARCHAR(50)," \
        "undp float,perundp float,rev float," \
        "profit float,gpr float,npr float,holders bigint)"
    cur.execute(sql)
    conn.commit()
    cur.close()
    print('build success')
