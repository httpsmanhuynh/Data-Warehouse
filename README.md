# Pakistan E-commerce Data Warehouse & AI

## 1. Giới thiệu

Đề tài xây dựng Data Warehouse và hệ thống phân tích dữ liệu thương mại điện tử dựa trên **Pakistan Largest Ecommerce Dataset**.

Hệ thống tập trung vào hai hướng chính:

- Phân tích hành vi và đặc điểm khách hàng
- Dự báo khả năng mua lại của khách hàng dựa trên lịch sử giao dịch

Quy trình được triển khai theo hướng từ dữ liệu nguồn đến Data Warehouse, mô hình AI, Dashboard và GenBI nhằm hỗ trợ phân tích và ra quyết định kinh doanh.

## 2. Mục tiêu

- Xây dựng quy trình tiền xử lý và tích hợp dữ liệu thương mại điện tử
- Đánh giá và cải thiện chất lượng dữ liệu
- Thiết kế Data Warehouse phục vụ phân tích
- Phân tích hành vi mua sắm của khách hàng
- Xây dựng đặc trưng khách hàng từ lịch sử giao dịch
- Xây dựng mô hình dự báo khả năng mua lại
- Xây dựng Dashboard trực quan hóa kết quả
- Ứng dụng GenBI để hỗ trợ truy vấn và khai thác dữ liệu
- Đưa ra các khuyến nghị hỗ trợ quyết định kinh doanh

## 3. Dataset

Nguồn dữ liệu sử dụng:

**Pakistan Largest Ecommerce Dataset**

Dữ liệu chứa các thông tin liên quan đến:

- Đơn hàng
- Khách hàng
- Sản phẩm
- Danh mục sản phẩm
- Giá và số lượng
- Giảm giá
- Phương thức thanh toán
- Trạng thái đơn hàng
- Thời gian giao dịch

Dữ liệu gốc được lưu trong thư mục:

```text
data/raw/
```

## 4. Kiến trúc hệ thống

```text
Pakistan Ecommerce Dataset
            │
            ▼
    Data Preprocessing
            │
            ▼
         Bronze
            │
            ▼
          Silver
            │
            ▼
     Data Warehouse
            │
       ┌────┴────┐
       ▼         ▼
 Customer      Sales
 Analysis     Analysis
       │
       ▼
 Feature Engineering
       │
       ▼
 Repurchase Prediction
       │
   ┌───┴────┐
   ▼        ▼
Dashboard  GenBI
   │        │
   └───┬────┘
       ▼
Decision Support
```

## 5. Cấu trúc Repository

```text
Pakistan-Ecommerce-DW-AI/
│
├── README.md
│
├── dataset/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── preprocessing/
│   ├── data_cleaning.py
│   ├── data_quality.py
│   └── feature_engineering.py
│
├── data_warehouse/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── dimensions/
│   └── facts/
│
├── eda/
│   ├── eda_sales.ipynb
│   ├── eda_customer.ipynb
│   └── visualizations/
│
├── ai/
│   ├── customer_behavior/
│   │   ├── rfm_analysis.py
│   │   └── customer_segmentation.py
│   │
│   └── repurchase_prediction/
│       ├── create_target.py
│       ├── feature_engineering.py
│       ├── train_model.py
│       └── evaluate_model.py
│
├── dashboard/
│   ├── sales_dashboard/
│   ├── customer_dashboard/
│   └── repurchase_dashboard/
│
├── genbi/
│   ├── queries.sql
│   └── prompts.md
│
├── docs/
│   ├── architecture/
│   ├── data_dictionary/
│   ├── erd/
│   └── report/
│
└── requirements.txt
```

## 6. Data Warehouse

Data Warehouse được tổ chức theo mô hình phân tích với các bảng fact và dimension.

### Fact

`fact_sales`

Các chỉ số chính:

- Quantity
- Price
- Grand Total
- Discount Amount

### Dimension

- `dim_customer`
- `dim_product`
- `dim_category`
- `dim_payment`
- `dim_date`

Mô hình được thiết kế nhằm hỗ trợ phân tích doanh thu, sản phẩm, khách hàng, phương thức thanh toán và xu hướng theo thời gian.

## 7. Phân tích hành vi khách hàng

Hành vi khách hàng được phân tích dựa trên lịch sử giao dịch.

Các đặc trưng có thể sử dụng:

- Recency
- Frequency
- Monetary
- Total Orders
- Total Quantity
- Average Order Value
- Total Discount
- Category Diversity

Các đặc trưng này được sử dụng để mô tả và phân tích sự khác biệt giữa các nhóm khách hàng.

## 8. Dự báo khả năng mua lại

Mục tiêu của mô hình là dự báo liệu khách hàng có phát sinh giao dịch trở lại trong một khoảng thời gian xác định hay không.

Quy trình:

```text
Transaction History
        ↓
Customer Features
        ↓
Define Repurchase Target
        ↓
Train / Test Split
        ↓
Machine Learning Model
        ↓
Model Evaluation
        ↓
Repurchase Prediction
```

Kết quả dự báo được sử dụng kết hợp với dữ liệu khách hàng và dữ liệu kinh doanh để hỗ trợ phân tích.

## 9. Dashboard

Dashboard tập trung vào các nhóm chỉ số:

### Sales

- Total Revenue
- Total Orders
- Total Quantity
- Average Order Value
- Revenue Trend

### Product

- Top Products
- Revenue by Category
- Quantity by Category

### Customer

- Customer Count
- Customer Behavior
- Customer Segments
- Customer Revenue

### Repurchase

- Repurchase Rate
- Customers with High Repurchase Probability
- Customer Prediction Distribution

## 10. GenBI

GenBI được sử dụng để hỗ trợ khai thác dữ liệu bằng ngôn ngữ tự nhiên.

Một số câu hỏi phân tích:

```text
Doanh thu theo từng tháng là bao nhiêu?

Danh mục sản phẩm nào có doanh thu cao nhất?

Top 10 sản phẩm có doanh thu cao nhất?

Khách hàng nào có giá trị mua hàng cao?

Nhóm khách hàng nào có tần suất mua hàng
```
