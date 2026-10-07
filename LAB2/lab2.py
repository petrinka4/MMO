# Лабораторная работа №2. Разведочный и предиктивный анализ данных
# Запуск: python lab2.py (из папки LAB2, рядом с папкой marketing_data)


# ============================================================
# 1. Импорт библиотек и датасета
# ============================================================
import os
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import OneHotEncoder, Binarizer, StandardScaler, MinMaxScaler

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 40)
sns.set_theme(style="whitegrid")
os.makedirs("figures", exist_ok=True)

def save(name):
    plt.tight_layout()
    plt.savefig(f"figures/{name}.png", dpi=150, bbox_inches="tight")
    plt.show()

df = pd.read_csv("marketing_data/marketing_data.csv")
print("Размер датасета:", df.shape)
print(df.head())

df.info()


# ============================================================
# 2. Приведение типов
# ============================================================
# в названии столбца Income есть лишние пробелы, а сам доход записан строкой вида "$84,835.00"
df.columns = df.columns.str.strip()
df["Income"] = df["Income"].str.replace(r"[$,\s]", "", regex=True).astype(float)
df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], format="%m/%d/%y")
print(df[["Income", "Dt_Customer"]].dtypes)


# ============================================================
# 3. Проверка на пропуски и дубликаты
# ============================================================
missing = df.isna().sum()
print("Пропуски по столбцам:")
print(missing[missing > 0])
print("Доля пропусков в Income: {:.2%}".format(df["Income"].isna().mean()))

plt.figure(figsize=(12, 5))
sns.heatmap(df.isna(), cbar=False, cmap="viridis", yticklabels=False)
plt.title("Карта пропусков (до обработки)")
save("01_missing_before")

dup_full = df.duplicated().sum()
dup_no_id = df.drop(columns="ID").duplicated().sum()
print("Полных дубликатов:", dup_full)
print("Дубликатов без учета ID:", dup_no_id)
df = df.drop_duplicates(subset=df.columns.drop("ID")).reset_index(drop=True)
print("Размер после удаления дубликатов:", df.shape)


# ============================================================
# 4. Анализ категориальных признаков
# ============================================================
cat_cols = ["Education", "Marital_Status", "Country"]
for col in cat_cols:
    print(df[col].value_counts(), "\n")

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
for ax, col in zip(axes, cat_cols):
    order = df[col].value_counts().index
    sns.countplot(data=df, x=col, order=order, ax=ax, color="#4C72B0")
    ax.set_title(col)
    ax.tick_params(axis="x", rotation=45)
save("02_categorical_before")

# редкие и некорректные значения семейного положения относим к Single,
# 2n Cycle по смыслу соответствует магистратуре
df["Marital_Status"] = df["Marital_Status"].replace({"Alone": "Single", "YOLO": "Single", "Absurd": "Single"})
df["Education"] = df["Education"].replace({"2n Cycle": "Master"})
print(df["Marital_Status"].value_counts(), "\n")
print(df["Education"].value_counts())


# ============================================================
# 5. Поиск аномальных значений
# ============================================================
num_cols = ["Year_Birth", "Income", "Recency", "MntWines", "MntFruits", "MntMeatProducts",
            "MntFishProducts", "MntSweetProducts", "MntGoldProds", "NumDealsPurchases",
            "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth"]
print(df[num_cols].describe().T.round(2))

fig, axes = plt.subplots(4, 4, figsize=(16, 13))
for ax, col in zip(axes.flat, num_cols):
    sns.histplot(df[col].dropna(), bins=30, kde=True, ax=ax, color="#4C72B0")
    ax.set_title(col)
    ax.set_xlabel("")
for ax in axes.flat[len(num_cols):]:
    ax.axis("off")
save("03_hist_before")

fig, axes = plt.subplots(4, 4, figsize=(16, 12))
for ax, col in zip(axes.flat, num_cols):
    sns.boxplot(x=df[col], ax=ax, color="#DD8452")
    ax.set_title(col)
    ax.set_xlabel("")
for ax in axes.flat[len(num_cols):]:
    ax.axis("off")
save("04_boxplot_before")

def iqr_bounds(s, k=1.5):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

rows = []
for col in num_cols:
    s = df[col].dropna()
    low, high = iqr_bounds(s)
    z = np.abs(stats.zscore(s))
    rows.append([col, round(low, 1), round(high, 1), ((s < low) | (s > high)).sum(), (z > 3).sum()])
outliers = pd.DataFrame(rows, columns=["Признак", "Нижняя граница", "Верхняя граница", "Выбросы IQR", "Выбросы |z|>3"])
print(outliers)

print("Самые ранние годы рождения:", sorted(df["Year_Birth"])[:5])
print("Самые большие доходы:", sorted(df["Income"].dropna())[-5:])
fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
sns.scatterplot(data=df, x="Year_Birth", y="Income", ax=axes[0], alpha=0.5)
axes[0].set_title("Год рождения и доход")
sns.scatterplot(x=df["Income"], y=df[num_cols[3:9]].sum(axis=1), ax=axes[1], alpha=0.5)
axes[1].set_title("Доход и сумма покупок")
axes[1].set_ylabel("Сумма покупок")
save("05_scatter_anomalies")


# ============================================================
# 6. Заполнение пропусков и устранение выбросов
# ============================================================
# невозможные значения: год рождения раньше 1920 и доход 666666 заменяем на пропуски
df.loc[df["Year_Birth"] < 1920, "Year_Birth"] = np.nan
df.loc[df["Income"] > 200000, "Income"] = np.nan
print("Пропуски после пометки аномалий:")
print(df[["Year_Birth", "Income"]].isna().sum())

# пропуски в доходе заполняем медианой по уровню образования, год рождения - общей медианой
df["Income"] = df["Income"].fillna(df.groupby("Education")["Income"].transform("median"))
df["Year_Birth"] = df["Year_Birth"].fillna(df["Year_Birth"].median()).astype(int)
print("\nПропусков после заполнения:", df.isna().sum().sum())

# оставшиеся выбросы ограничиваем границами межквартильного размаха (винзоризация)
clip_cols = [c for c in num_cols if c != "Year_Birth"]
for col in clip_cols:
    low, high = iqr_bounds(df[col])
    df[col] = df[col].clip(lower=max(low, 0), upper=high)

rows = []
for col in num_cols:
    low, high = iqr_bounds(df[col])
    rows.append([col, ((df[col] < low) | (df[col] > high)).sum()])
print(pd.DataFrame(rows, columns=["Признак", "Выбросы IQR после обработки"]))

plt.figure(figsize=(12, 5))
sns.heatmap(df.isna(), cbar=False, cmap="viridis", yticklabels=False)
plt.title("Карта пропусков (после обработки)")
save("06_missing_after")

fig, axes = plt.subplots(4, 4, figsize=(16, 12))
for ax, col in zip(axes.flat, num_cols):
    sns.boxplot(x=df[col], ax=ax, color="#55A868")
    ax.set_title(col)
    ax.set_xlabel("")
for ax in axes.flat[len(num_cols):]:
    ax.axis("off")
save("07_boxplot_after")


# ============================================================
# 7. Генерация новых признаков
# ============================================================
mnt_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
buy_cols = ["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]
cmp_cols = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"]
last_date = df["Dt_Customer"].max()

df["Age"] = last_date.year - df["Year_Birth"]                    # возраст клиента
df["Children"] = df["Kidhome"] + df["Teenhome"]                  # количество детей
df["TotalSpent"] = df[mnt_cols].sum(axis=1)                      # общая сумма покупок
df["TotalPurchases"] = df[buy_cols].sum(axis=1)                  # общее количество покупок
df["AvgCheck"] = (df["TotalSpent"] / df["TotalPurchases"].replace(0, np.nan)).fillna(0).round(2)  # средний чек
df["TotalAcceptedCmp"] = df[cmp_cols].sum(axis=1)                # принято рекламных предложений
df["CustomerDays"] = (last_date - df["Dt_Customer"]).dt.days     # дней с момента регистрации

# у клиентов с одной-двумя покупками средний чек получается аномально большим, ограничиваем его по IQR
df["AvgCheck"] = df["AvgCheck"].clip(upper=iqr_bounds(df["AvgCheck"])[1])

new_cols = ["Age", "Children", "TotalSpent", "TotalPurchases", "AvgCheck", "TotalAcceptedCmp", "CustomerDays"]
print(df[new_cols].describe().T.round(2))

fig, axes = plt.subplots(2, 4, figsize=(16, 7))
for ax, col in zip(axes.flat, new_cols):
    sns.histplot(df[col], bins=25, kde=True, ax=ax, color="#8172B3")
    ax.set_title(col)
    ax.set_xlabel("")
sns.boxplot(data=df, x="Children", y="TotalSpent", ax=axes.flat[-1], color="#8172B3")
axes.flat[-1].set_title("TotalSpent по числу детей")
save("08_new_features")

corr_cols = ["Income", "Age", "Children", "Recency", "TotalSpent", "TotalPurchases",
             "AvgCheck", "NumWebVisitsMonth", "NumDealsPurchases", "TotalAcceptedCmp", "CustomerDays", "Response"]
plt.figure(figsize=(11, 9))
sns.heatmap(df[corr_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True)
plt.title("Матрица корреляций")
save("09_corr_heatmap")


# ============================================================
# 8. Кодирование категориальных признаков
# ============================================================
# порядковое кодирование уровня образования
edu_map = {"Basic": 0, "Graduation": 1, "Master": 2, "PhD": 3}
df["Education_Code"] = df["Education"].map(edu_map)

# бинаризация: состоит ли клиент в паре, есть ли дети
df["InCouple"] = df["Marital_Status"].isin(["Married", "Together"]).astype(int)
df["IsParent"] = (df["Children"] > 0).astype(int)

# бинаризация по порогу с помощью Binarizer: доход выше медианы
binarizer = Binarizer(threshold=df["Income"].median())
df["HighIncome"] = binarizer.fit_transform(df[["Income"]]).astype(int).ravel()

print(df[["Education", "Education_Code", "Marital_Status", "InCouple", "Children", "IsParent", "Income", "HighIncome"]].head(8))

# One-Hot Encoding для страны и семейного положения
ohe = OneHotEncoder(sparse_output=False, dtype=int)
ohe_arr = ohe.fit_transform(df[["Country", "Marital_Status"]])
ohe_df = pd.DataFrame(ohe_arr, columns=ohe.get_feature_names_out(), index=df.index)
print("Новые OHE-признаки:")
print(textwrap.fill(", ".join(ohe_df.columns), width=100))

df_enc = pd.concat([df.drop(columns=["Education", "Marital_Status", "Country", "Dt_Customer", "ID"]), ohe_df], axis=1)
print("Размер после кодирования:", df_enc.shape)
print("Нечисловых столбцов:", df_enc.select_dtypes(exclude="number").shape[1])
print(ohe_df.head())


# ============================================================
# 9. Стандартизация и нормализация
# ============================================================
scale_cols = ["Income", "Age", "Recency", "TotalSpent", "TotalPurchases", "AvgCheck",
              "NumWebVisitsMonth", "NumDealsPurchases", "CustomerDays"] + mnt_cols

std_scaler = StandardScaler()
df_std = df_enc.copy()
df_std[scale_cols] = std_scaler.fit_transform(df_enc[scale_cols])

mm_scaler = MinMaxScaler()
df_mm = df_enc.copy()
df_mm[scale_cols] = mm_scaler.fit_transform(df_enc[scale_cols])

check = pd.DataFrame({
    "mean (std)": df_std[scale_cols].mean(),
    "std (std)": df_std[scale_cols].std(ddof=0),
    "min (minmax)": df_mm[scale_cols].min(),
    "max (minmax)": df_mm[scale_cols].max(),
}).round(3)
print(check)

fig, axes = plt.subplots(3, 3, figsize=(15, 10))
for i, col in enumerate(["Income", "TotalSpent", "Age"]):
    sns.histplot(df_enc[col], bins=30, kde=True, ax=axes[i, 0], color="#4C72B0")
    sns.histplot(df_std[col], bins=30, kde=True, ax=axes[i, 1], color="#DD8452")
    sns.histplot(df_mm[col], bins=30, kde=True, ax=axes[i, 2], color="#55A868")
    axes[i, 0].set_title(f"{col}: исходные")
    axes[i, 1].set_title(f"{col}: StandardScaler")
    axes[i, 2].set_title(f"{col}: MinMaxScaler")
    for ax in axes[i]:
        ax.set_xlabel("")
save("10_scaling_hist")

fig, axes = plt.subplots(1, 2, figsize=(16, 5.5))
sns.boxplot(data=df_std[scale_cols], ax=axes[0], color="#DD8452")
axes[0].set_title("После стандартизации (StandardScaler)")
sns.boxplot(data=df_mm[scale_cols], ax=axes[1], color="#55A868")
axes[1].set_title("После нормализации (MinMaxScaler)")
for ax in axes:
    ax.tick_params(axis="x", rotation=90)
save("11_scaling_box")

df_std.to_csv("marketing_data/marketing_prepared_std.csv", index=False)
df_mm.to_csv("marketing_data/marketing_prepared_minmax.csv", index=False)
print("Итоговый размер датасета:", df_std.shape)
