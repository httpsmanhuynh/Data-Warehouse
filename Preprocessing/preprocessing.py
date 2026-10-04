import pandas as pd
import numpy as np
from pathlib import Path


# Thư mục gốc của repository Data-Warehouse
BASE_DIR = Path(__file__).resolve().parent.parent

# Thư mục chứa dataset
DATASET_DIR = BASE_DIR / "Dataset"

# File dữ liệu gốc
INPUT_FILE = DATASET_DIR / "Pakistan Largest Ecommerce Dataset.csv"

# File dữ liệu sau tiền xử lý
OUTPUT_FILE = DATASET_DIR / "ecommerce_cleaned.csv"

# Báo cáo tổng hợp quá trình tiền xử lý
REPORT_FILE = DATASET_DIR / "preprocessing_report.csv"

# Báo cáo giá trị ngoại lệ
OUTLIER_REPORT_FILE = DATASET_DIR / "outlier_report.csv"


def section(title):
    print("\n" + "=" * 75)
    print(title)
    print("=" * 75)


def missing_summary(df):
    result = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_percent": df.isna().mean().values * 100
    })

    return result.sort_values(
        "missing_count",
        ascending=False
    )


# ============================================================
# 1. ĐỌC DỮ LIỆU GỐC
# ============================================================

section("1. ĐỌC DỮ LIỆU GỐC")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Không tìm thấy file dữ liệu:\n{INPUT_FILE}"
    )

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

original_rows = len(df)
original_columns = len(df.columns)

print(f"Số dòng ban đầu : {original_rows:,}")
print(f"Số cột ban đầu  : {original_columns}")


# ============================================================
# 2. CHUẨN HÓA TÊN CỘT
# ============================================================

section("2. CHUẨN HÓA TÊN CỘT")

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)

print("Đã loại bỏ khoảng trắng thừa trong tên cột.")


# ============================================================
# 2.1. LOẠI CÁC CỘT UNNAMED HOÀN TOÀN RỖNG
# ============================================================

section("2.1. LOẠI CÁC CỘT UNNAMED HOÀN TOÀN RỖNG")

unnamed_columns = [
    column
    for column in df.columns
    if column.startswith("Unnamed:")
]

empty_unnamed_columns = [
    column
    for column in unnamed_columns
    if df[column].isna().all()
]

if empty_unnamed_columns:

    df = df.drop(
        columns=empty_unnamed_columns
    )

    print(
        f"Đã loại bỏ "
        f"{len(empty_unnamed_columns)} "
        f"cột Unnamed hoàn toàn rỗng:"
    )

    for column in empty_unnamed_columns:
        print(f"- {column}")

else:

    print(
        "Không phát hiện cột Unnamed "
        "hoàn toàn rỗng."
    )


# ============================================================
# 3. LOẠI BỎ DÒNG HOÀN TOÀN TRỐNG
# ============================================================

section("3. XỬ LÝ DÒNG HOÀN TOÀN TRỐNG")

empty_rows = df.isna().all(axis=1).sum()

print(
    f"Số dòng hoàn toàn trống: "
    f"{empty_rows:,}"
)

df = df.dropna(
    how="all"
).copy()

print(
    f"Số dòng sau khi loại bỏ: "
    f"{len(df):,}"
)


# ============================================================
# 4. CHUẨN HÓA GIÁ TRỊ THIẾU
# ============================================================

section("4. CHUẨN HÓA GIÁ TRỊ THIẾU")

text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for column in text_columns:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )

    df[column] = df[column].replace(
        [
            r"\N",
            "",
            "NULL",
            "null",
            "None",
            "none"
        ],
        np.nan
    )

print(
    "Đã chuẩn hóa NULL, \\N và chuỗi rỗng thành NaN."
)


# ============================================================
# 5. ĐÁNH GIÁ GIÁ TRỊ THIẾU
# ============================================================

section("5. ĐÁNH GIÁ GIÁ TRỊ THIẾU")

missing_before = missing_summary(df)

missing_before = missing_before[
    missing_before["missing_count"] > 0
]

if len(missing_before) > 0:

    print(
        missing_before.to_string(
            index=False
        )
    )

else:

    print(
        "Không phát hiện giá trị thiếu."
    )


# ============================================================
# 6. XỬ LÝ SALES_COMMISSION_CODE
# ============================================================

section("6. XỬ LÝ SALES_COMMISSION_CODE")

sales_commission_removed = False
sales_commission_missing = 0
sales_commission_missing_percent = 0

if "sales_commission_code" in df.columns:

    sales_commission_missing = (
        df["sales_commission_code"]
        .isna()
        .sum()
    )

    sales_commission_missing_percent = (
        df["sales_commission_code"]
        .isna()
        .mean()
        * 100
    )

    print(
        f"Số giá trị thiếu: "
        f"{sales_commission_missing:,}"
    )

    print(
        f"Tỷ lệ thiếu: "
        f"{sales_commission_missing_percent:.2f}%"
    )

    # Tỷ lệ thiếu rất cao nên không giữ lại
    df = df.drop(
        columns=["sales_commission_code"]
    )

    sales_commission_removed = True

    print(
        "Đã loại bỏ sales_commission_code "
        "do tỷ lệ thiếu cao."
    )


# ============================================================
# 7. CHUẨN HÓA DỮ LIỆU CHUỖI
# ============================================================

section("7. CHUẨN HÓA DỮ LIỆU CHUỖI")

string_columns = [
    "status",
    "sku",
    "category_name_1",
    "payment_method",
    "Customer ID",
    "increment_id",
    "BI Status",
    "Customer Since"
]

for column in string_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

print(
    "Đã loại bỏ khoảng trắng thừa "
    "ở các thuộc tính dạng chuỗi."
)


# ============================================================
# 8. CHUẨN HÓA STATUS
# ============================================================

section("8. CHUẨN HÓA STATUS")

status_missing_before = 0

if "status" in df.columns:

    df["status"] = (
        df["status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    status_missing_before = (
        df["status"]
        .isna()
        .sum()
    )

    print(
        "Các trạng thái sau khi chuẩn hóa:"
    )

    print(
        df["status"]
        .value_counts(
            dropna=False
        ).to_string()
    )


# ============================================================
# 8.1. XỬ LÝ STATUS THIẾU
# ============================================================

section("8.1. XỬ LÝ STATUS THIẾU")

if "status" in df.columns:

    df["status"] = (
        df["status"]
        .fillna("unknown")
    )

    print(
        f"Đã thay thế "
        f"{status_missing_before:,} "
        f"giá trị status thiếu bằng 'unknown'."
    )


# ============================================================
# 8.2. XỬ LÝ CATEGORY THIẾU
# ============================================================

section("8.2. XỬ LÝ CATEGORY THIẾU")

category_missing_before = 0

if "category_name_1" in df.columns:

    category_missing_before = (
        df["category_name_1"]
        .isna()
        .sum()
    )

    df["category_name_1"] = (
        df["category_name_1"]
        .fillna("Unknown")
    )

    print(
        f"Đã thay thế "
        f"{category_missing_before:,} "
        f"giá trị category_name_1 thiếu "
        f"bằng 'Unknown'."
    )


# ============================================================
# 9. CHUYỂN ĐỔI KIỂU DỮ LIỆU SỐ
# ============================================================

section("9. CHUYỂN ĐỔI KIỂU DỮ LIỆU SỐ")

numeric_columns = [
    "item_id",
    "price",
    "qty_ordered",
    "grand_total",
    "discount_amount",
    "MV",
    "Year",
    "Month"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        print(
            f"{column}: numeric"
        )


# ============================================================
# 10. CHUYỂN ĐỔI KIỂU DỮ LIỆU THỜI GIAN
# ============================================================

section("10. CHUYỂN ĐỔI KIỂU DỮ LIỆU THỜI GIAN")

date_columns = [
    "created_at",
    "Working Date"
]

for column in date_columns:

    if column in df.columns:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        print(
            f"{column}: datetime"
        )


# ============================================================
# 11. KIỂM TRA DỮ LIỆU TRÙNG LẶP
# ============================================================

section("11. KIỂM TRA DỮ LIỆU TRÙNG LẶP")

duplicate_count = df.duplicated().sum()

print(
    f"Số bản ghi trùng hoàn toàn: "
    f"{duplicate_count:,}"
)

if duplicate_count > 0:

    df = df.drop_duplicates().copy()

    print(
        "Đã loại bỏ duplicate hoàn toàn."
    )

else:

    print(
        "Không phát hiện duplicate hoàn toàn."
    )


# ============================================================
# 12. KIỂM TRA CÁC KHÓA
# ============================================================

section("12. KIỂM TRA CÁC KHÓA")

key_columns = [
    "item_id",
    "increment_id",
    "sku",
    "Customer ID"
]

for column in key_columns:

    if column in df.columns:

        missing_count = (
            df[column]
            .isna()
            .sum()
        )

        duplicate_count_key = (
            df[column]
            .duplicated()
            .sum()
        )

        print(f"\n{column}")

        print(
            f"  Missing   : "
            f"{missing_count:,}"
        )

        print(
            f"  Duplicate : "
            f"{duplicate_count_key:,}"
        )


# ============================================================
# 13. XỬ LÝ MISSING Ở KHÓA BẮT BUỘC
# ============================================================

section("13. XỬ LÝ MISSING Ở KHÓA")

required_keys = [
    "item_id",
    "increment_id",
    "sku",
    "Customer ID"
]

existing_required_keys = [
    column
    for column in required_keys
    if column in df.columns
]

before_key_cleaning = len(df)

if existing_required_keys:

    df = df.dropna(
        subset=existing_required_keys
    ).copy()

removed_key_rows = (
    before_key_cleaning -
    len(df)
)

print(
    f"Dòng bị loại do thiếu khóa: "
    f"{removed_key_rows:,}"
)


# ============================================================
# 14. KIỂM TRA DỮ LIỆU KHÔNG HỢP LỆ
# ============================================================

section("14. KIỂM TRA DỮ LIỆU KHÔNG HỢP LỆ")

invalid_price = 0
invalid_total = 0
invalid_discount = 0

if "price" in df.columns:

    invalid_price = (
        df["price"] <= 0
    ).sum()

    print(
        f"price <= 0: "
        f"{invalid_price:,}"
    )


if "grand_total" in df.columns:

    invalid_total = (
        df["grand_total"] < 0
    ).sum()

    print(
        f"grand_total < 0: "
        f"{invalid_total:,}"
    )


if "discount_amount" in df.columns:

    invalid_discount = (
        df["discount_amount"] < 0
    ).sum()

    print(
        f"discount_amount < 0: "
        f"{invalid_discount:,}"
    )


# ============================================================
# 15. XỬ LÝ DỮ LIỆU KHÔNG HỢP LỆ
# ============================================================

section("15. XỬ LÝ DỮ LIỆU KHÔNG HỢP LỆ")

before_invalid = len(df)

# Tạo một điều kiện lọc chung
valid_mask = pd.Series(
    True,
    index=df.index
)

if "price" in df.columns:
    valid_mask &= df["price"] > 0

if "grand_total" in df.columns:
    valid_mask &= df["grand_total"] >= 0

if "discount_amount" in df.columns:
    valid_mask &= df["discount_amount"] >= 0

# Chỉ lọc DataFrame một lần
df = df.loc[valid_mask]

invalid_removed = (
    before_invalid - len(df)
)

print(
    f"Dòng bị loại do dữ liệu "
    f"không hợp lệ: "
    f"{invalid_removed:,}"
)


# ============================================================
# 16. ĐÁNH GIÁ GIÁ TRỊ NGOẠI LỆ
# ============================================================

section("16. ĐÁNH GIÁ GIÁ TRỊ NGOẠI LỆ")

outlier_columns = [
    "price",
    "qty_ordered",
    "grand_total"
]

outlier_report = []

for column in outlier_columns:

    if column not in df.columns:
        continue

    series = df[column].dropna()

    if len(series) == 0:
        continue

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    outlier_count = (
        (series < lower_bound) |
        (series > upper_bound)
    ).sum()

    outlier_percent = (
        outlier_count /
        len(series) *
        100
    )

    outlier_report.append({
        "column": column,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": outlier_count,
        "outlier_percent": outlier_percent
    })

    print(f"\n{column}")

    print(
        f"Q1: {q1:,.2f}"
    )

    print(
        f"Q3: {q3:,.2f}"
    )

    print(
        f"IQR: {iqr:,.2f}"
    )

    print(
        f"Lower bound: "
        f"{lower_bound:,.2f}"
    )

    print(
        f"Upper bound: "
        f"{upper_bound:,.2f}"
    )

    print(
        f"Outlier: "
        f"{outlier_count:,} "
        f"({outlier_percent:.2f}%)"
    )


# ============================================================
# 17. QUY TẮC XỬ LÝ OUTLIER
# ============================================================

section("17. QUY TẮC XỬ LÝ OUTLIER")

print(
    "Không loại bỏ outlier chỉ dựa trên IQR."
)

print(
    "Các giá trị lớn có thể phản ánh "
    "giao dịch thực tế trong thương mại điện tử."
)

print(
    "Chỉ các giá trị vi phạm logic nghiệp vụ "
    "được xử lý ở bước 15."
)


# ============================================================
# 18. KIỂM TRA TÍNH NHẤT QUÁN CỦA MV
# ============================================================

section("18. KIỂM TRA TÍNH NHẤT QUÁN CỦA MV")

mv_mismatch = 0

if all(
    column in df.columns
    for column in [
        "price",
        "qty_ordered",
        "MV"
    ]
):

    df["MV_calculated"] = (
        df["price"] *
        df["qty_ordered"]
    )

    df["MV_difference"] = (
        df["MV"] -
        df["MV_calculated"]
    )

    mv_mismatch = (
        df["MV_difference"]
        .abs()
        > 0.01
    ).sum()

    print(
        "Số dòng MV không khớp "
        "price × qty_ordered: "
        f"{mv_mismatch:,}"
    )

    print(
        "MV chỉ được sử dụng để kiểm tra "
        "tính nhất quán, không sử dụng "
        "làm chỉ tiêu doanh thu chính."
    )


# ============================================================
# 19. TẠO GIÁ TRỊ GIAO DỊCH CẤP DÒNG
# ============================================================

section("19. TẠO GIÁ TRỊ GIAO DỊCH CẤP DÒNG")

if all(
    column in df.columns
    for column in [
        "price",
        "qty_ordered",
        "discount_amount"
    ]
):

    # Giá trị gộp ở grain item
    df["line_gross_value"] = (
        df["price"] *
        df["qty_ordered"]
    )

    # Giá trị ròng sau chiết khấu
    df["line_net_value"] = (
        df["line_gross_value"]
        - df["discount_amount"]
    )

    print(
        "Đã tạo line_gross_value = "
        "price × qty_ordered"
    )

    print(
        "Đã tạo line_net_value = "
        "line_gross_value - discount_amount"
    )


# ============================================================
# 20. KIỂM TRA GRAIN VÀ GRAND_TOTAL
# ============================================================

section("20. KIỂM TRA GRAIN VÀ GRAND_TOTAL")

inconsistent_orders = 0

if all(
    column in df.columns
    for column in [
        "increment_id",
        "grand_total"
    ]
):

    order_total_variation = (
        df.groupby("increment_id")[
            "grand_total"
        ]
        .nunique()
    )

    inconsistent_orders = (
        order_total_variation > 1
    ).sum()

    print(
        "Số đơn hàng có nhiều "
        "grand_total khác nhau:"
    )

    print(
        f"{inconsistent_orders:,}"
    )

    print("\nQuy tắc xử lý:")

    print(
        "- Giữ grand_total để tham chiếu."
    )

    print(
        "- Không SUM grand_total trực tiếp "
        "ở grain item."
    )

    print(
        "- Doanh thu cấp dòng sử dụng "
        "line_net_value."
    )


# ============================================================
# 21. CHUẨN HÓA THUỘC TÍNH THỜI GIAN
# ============================================================

section("21. CHUẨN HÓA THUỘC TÍNH THỜI GIAN")

if "created_at" in df.columns:

    df["Year"] = (
        df["created_at"]
        .dt.year
    )

    df["Month"] = (
        df["created_at"]
        .dt.month
    )

    print(
        "Year và Month được tính lại "
        "từ created_at."
    )


# ============================================================
# 22. LOẠI CÁC CỘT THỜI GIAN DƯ THỪA
# ============================================================

section("22. LOẠI CÁC CỘT THỜI GIAN DƯ THỪA")

redundant_date_columns = [
    "Working Date",
    "M-Y",
    "FY"
]

existing_redundant_columns = [
    column
    for column in redundant_date_columns
    if column in df.columns
]

if existing_redundant_columns:

    df = df.drop(
        columns=existing_redundant_columns
    )

    for column in existing_redundant_columns:

        print(
            f"Đã loại: {column}"
        )


# ============================================================
# 23. LOẠI BỎ CÁC CỘT KHÔNG SỬ DỤNG
# ============================================================

section("23. LOẠI BỎ CÁC CỘT KHÔNG SỬ DỤNG")

columns_to_remove = [
    "MV",
    "MV_calculated",
    "MV_difference"
]

existing_columns_to_remove = [
    column
    for column in columns_to_remove
    if column in df.columns
]

if existing_columns_to_remove:

    df = df.drop(
        columns=existing_columns_to_remove
    )

    print(
        "Đã loại bỏ các cột:"
    )

    for column in existing_columns_to_remove:

        print(
            f"- {column}"
        )


# ============================================================
# 24. KIỂM TRA CUỐI CÙNG
# ============================================================

section("24. KIỂM TRA DỮ LIỆU SAU TIỀN XỬ LÝ")

final_rows = len(df)
final_columns = len(df.columns)

print(
    f"Số dòng cuối cùng: "
    f"{final_rows:,}"
)

print(
    f"Số cột cuối cùng: "
    f"{final_columns}"
)

print(
    f"Duplicate còn lại: "
    f"{df.duplicated().sum():,}"
)

print("\nGiá trị thiếu còn lại:")

missing_after = missing_summary(df)

remaining_missing = missing_after[
    missing_after["missing_count"] > 0
]

if len(remaining_missing) > 0:

    print(
        remaining_missing.to_string(
            index=False
        )
    )

else:

    print(
        "Không còn giá trị thiếu."
    )


# ============================================================
# 25. KIỂM TRA CÁC CỘT QUAN TRỌNG
# ============================================================

section("25. KIỂM TRA CÁC CỘT QUAN TRỌNG")

important_columns = [
    "item_id",
    "increment_id",
    "Customer ID",
    "sku",
    "created_at",
    "price",
    "qty_ordered",
    "discount_amount",
    "grand_total",
    "line_gross_value",
    "line_net_value",
    "status",
    "category_name_1"
]

print("Các cột quan trọng:")

for column in important_columns:

    if column in df.columns:

        print(
            f"[OK] {column}"
        )

    else:

        print(
            f"[THIẾU] {column}"
        )


# ============================================================
# 26. LƯU DỮ LIỆU ĐÃ TIỀN XỬ LÝ
# ============================================================

section("26. LƯU DỮ LIỆU ĐÃ TIỀN XỬ LÝ")

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Đã lưu dữ liệu sạch tại:\n"
    f"{OUTPUT_FILE}"
)


# ============================================================
# 27. TẠO BÁO CÁO TIỀN XỬ LÝ
# ============================================================

section("27. TẠO BÁO CÁO TIỀN XỬ LÝ")

report = pd.DataFrame({
    "metric": [
        "original_rows",
        "original_columns",
        "empty_rows",
        "rows_after_empty_removal",
        "empty_unnamed_columns_removed",
        "duplicate_rows",
        "sales_commission_missing",
        "sales_commission_missing_percent",
        "rows_removed_missing_keys",
        "invalid_price_rows",
        "invalid_grand_total_rows",
        "invalid_discount_rows",
        "MV_mismatch_rows",
        "inconsistent_grand_total_orders",
        "category_missing_replaced",
        "status_missing_replaced",
        "final_rows",
        "final_columns"
    ],

    "value": [
        original_rows,
        original_columns,
        empty_rows,
        original_rows - empty_rows,
        len(empty_unnamed_columns),
        duplicate_count,
        sales_commission_missing,
        sales_commission_missing_percent,
        removed_key_rows,
        invalid_price,
        invalid_total,
        invalid_discount,
        mv_mismatch,
        inconsistent_orders,
        category_missing_before,
        status_missing_before,
        final_rows,
        final_columns
    ]
})

report.to_csv(
    REPORT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Đã lưu báo cáo tại:\n"
    f"{REPORT_FILE}"
)


# ============================================================
# 28. LƯU BÁO CÁO OUTLIER
# ============================================================

section("28. LƯU BÁO CÁO OUTLIER")

if len(outlier_report) > 0:

    outlier_report_df = pd.DataFrame(
        outlier_report
    )

    outlier_report_df.to_csv(
        OUTLIER_REPORT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Đã lưu báo cáo outlier tại:\n"
        f"{OUTLIER_REPORT_FILE}"
    )

else:

    print(
        "Không có dữ liệu để tạo báo cáo outlier."
    )


# ============================================================
# 29. HOÀN TẤT
# ============================================================

section("HOÀN TẤT")

print(
    "Đã hoàn thành quy trình tiền xử lý dữ liệu."
)

print(
    "Dataset sạch đã được chuẩn hóa "
    "theo grain giao dịch ở cấp item."
)

print(
    "Các giá trị outlier hợp lệ được giữ lại "
    "để tránh làm mất thông tin giao dịch."
)

print(
    "Doanh thu cấp dòng được tính bằng "
    "line_net_value thay vì sử dụng MV "
    "hoặc cộng trực tiếp grand_total."
)

print("\nCác file đầu ra:")

print(
    f"1. {OUTPUT_FILE}"
)

print(
    f"2. {REPORT_FILE}"
)

print(
    f"3. {OUTLIER_REPORT_FILE}"
)