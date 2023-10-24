CREATE DATABASE WEBSITE;
USE Website;
CREATE TABLE Customer (
    CustomerId INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Age INT,
    Gender CHAR(1),
    EmailId VARCHAR(255),
    Contact VARCHAR(255),
    ShippingAddress VARCHAR(255),
    Pincode_Shipping INT,
    City_Shipping VARCHAR(255),
    BillingAddress VARCHAR(255),
Pincode_Billing INT,
City_Billing VARCHAR(255),
CustPass Varchar(255)
);

-- Seller/Retailer Table
CREATE TABLE SellerRetailer (
    SellerId INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Age INT,
    Gender CHAR(1),
    EmailId VARCHAR(255),
    Contact VARCHAR(255),
    PaymentInfo VARCHAR(255),
    BillingAddress VARCHAR(255),
    SellPass VARCHAR(255)
);

-- Product Table
CREATE TABLE Product (
    ProductId INT PRIMARY KEY AUTO_INCREMENT,
    Price INT,
    Category VARCHAR(255),
    Description VARCHAR(255),
    ProductImages VARCHAR(255),
    QuantityAvailable INT,
    EstimatedDeliveryTime VARCHAR(255),
    SellerId INT,
    product_name varchar(25),
    FOREIGN KEY (SellerId) REFERENCES SellerRetailer(SellerId)
);

-- Order Table
CREATE TABLE OrderTable (
    OrderId INT PRIMARY KEY AUTO_INCREMENT,
    Quantity INT,
    ProductId INT,
    CustomerId INT,
    Amount INT,
    FOREIGN KEY (ProductId) REFERENCES Product(ProductId),
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
);

-- Cart Table
CREATE TABLE Cart (
    CustomerId INT,
    ProductId INT,
    product_name varchar(25),
    Quantity INT,
    Amount INT,
    PRIMARY KEY (CustomerId, ProductId),
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
    FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
);

-- Wishlist Table
CREATE TABLE Wishlist (
    CustomerId INT,
    ProductId INT,
    PRIMARY KEY (CustomerId, ProductId),
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
    FOREIGN KEY (ProductId) REFERENCES Product(ProductId)
);