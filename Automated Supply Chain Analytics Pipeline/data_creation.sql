CREATE TABLE IF NOT EXISTS table_m3 (
    "Product type" VARCHAR,
    "SKU" VARCHAR,
    "Price" FLOAT,
    "Availability" INT,
    "Number of products sold" INT,
    "Revenue generated" FLOAT,
    "Customer demographics" VARCHAR,
    "Stock levels" INT,
    "Lead times" INT,
    "Order quantities" INT,
    "Shipping times" INT,
    "Shipping carriers" VARCHAR,
    "Shipping costs" FLOAT,
    "Supplier name" VARCHAR,
    "Location" VARCHAR,
    "Lead time" INT,
    "Production volumes" INT,
    "Manufacturing lead time" INT,
    "Manufacturing costs" FLOAT,
    "Inspection results" VARCHAR,
    "Defect rates" FLOAT,
    "Transportation modes" VARCHAR,
    "Routes" VARCHAR,
    "Costs" FLOAT
);

COPY table_m3
FROM '/var/lib/postgresql/data/P2M3_clarence_manzo_data_raw.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM table_m3;