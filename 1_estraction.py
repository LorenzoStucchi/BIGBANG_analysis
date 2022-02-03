import geopandas as gpd
import rasterstats as rs
import pandas as pd

def merge_months(df, f):
    temp = pd.read_csv(f)
    temp.drop("DEN_REG",inplace=True, axis=1)
    df = df.merge(temp, on="COD_REG", how="left")
    return df

resource = "ae"
variable_path = "input/BIGBANG/" + resource + "/" + resource + "_YYYY_MMc.asc"
regions_path = "input/regions/regioni.gpkg"

regioni = gpd.read_file(regions_path)
regioni.drop(["Shape_Leng", "Shape_Area", "geometry", "COD_RIP"], inplace=True, axis=1)

for month in range(1,13):
    m = "0" + str(month) if month < 10 else str(month)
    f = variable_path.replace("MM", m)
    f_ = f.replace("YYYY", "2019")
    results = pd.DataFrame(rs.zonal_stats(regions_path, f_, stats="mean"))
    results["COD_REG"] = results.index + 1 
    meanyear = "2019_" + m
    results = results.rename(columns={"mean": meanyear})
    results = results.merge(regioni, on="COD_REG", how="left")
    print("done month: " + m + " of year: 2019")

    for i in range(1951,2019):
        f_ = f.replace("YYYY", str(i))
        temp = pd.DataFrame(rs.zonal_stats(regions_path, f_, stats="mean"))
        temp["COD_REG"] = temp.index + 1 
        meanyear = str(i) + "_" + m
        temp = temp.rename(columns={"mean": meanyear})
        results = results.merge(temp, on="COD_REG", how="left")
        print("done month: " + m + " of year: " + str(i))

    results.to_csv("output/" + resource + "/" + m + ".csv")
    print("done month: " + m)

m_01 = pd.read_csv("output/" + resource + "/01.csv")
y = m_01

for month in range(2,13):
    m = "0" + str(month) if month < 10 else str(month)
    y = merge_months(y, "output/" + resource + "/" + m + ".csv")

y.drop("Unnamed: 0_x", inplace=True, axis=1)
y.drop("Unnamed: 0_y", inplace=True, axis=1)
y.drop(["COD_REG"], inplace=True, axis=1)

y_T = y.T
y_T.columns = y_T.loc["DEN_REG", :]
y_T.drop(["DEN_REG"], inplace=True, axis=0)
y_T["month"] = pd.to_datetime(y_T.index, format="%Y_%m")
y_T = y_T.sort_values(by="month")
y_T.set_index('month',inplace=True)

y_T.to_csv("output/" + resource + ".csv")

# y_T["Piemonte"].to_csv("output/" + resource + "_Piemonte.csv")
# y_T["Emilia-Romagna"].to_csv("output/" + resource + "_ER.csv")
# y_T["Umbria"].to_csv("output/" + resource + "_Umbria.csv")
# y_T["Puglia"].to_csv("output/" + resource + "_Puglia.csv")
# y_T["Sicilia"].to_csv("output/" + resource + "_Sicilia.csv")
# y_T["Sardegna"].to_csv("output/" + resource + "_Sardegna.csv")
