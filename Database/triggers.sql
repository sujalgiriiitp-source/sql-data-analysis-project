-- ==============================================================
-- Project: Indian E-Commerce SQL Data Analysis
-- File: triggers.sql
-- Description: Database Triggers for automation and auditing.
-- ==============================================================

-- 1. Trigger to log Product Price Changes
-- Create an Audit Table
CREATE TABLE IF NOT EXISTS Product_Price_Audit (
    audit_id SERIAL PRIMARY KEY,
    product_id INT,
    old_price NUMERIC(10, 2),
    new_price NUMERIC(10, 2),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger Function
CREATE OR REPLACE FUNCTION log_price_change()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price <> OLD.price THEN
        INSERT INTO Product_Price_Audit(product_id, old_price, new_price)
        VALUES (OLD.product_id, OLD.price, NEW.price);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger Definition
CREATE TRIGGER price_change_trigger
AFTER UPDATE OF price ON Products
FOR EACH ROW
EXECUTE FUNCTION log_price_change();


-- 2. Trigger to Prevent Negative Stock
-- Trigger Function
CREATE OR REPLACE FUNCTION check_negative_stock()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.stock_quantity < 0 THEN
        RAISE EXCEPTION 'Stock quantity cannot be negative for product %', NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger Definition
CREATE TRIGGER enforce_positive_stock
BEFORE INSERT OR UPDATE OF stock_quantity ON Products
FOR EACH ROW
EXECUTE FUNCTION check_negative_stock();


-- 3. Trigger to Update Order Status if Payment Fails
-- Trigger Function
CREATE OR REPLACE FUNCTION update_order_on_payment_fail()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.payment_status = 'Failed' THEN
        UPDATE Orders
        SET order_status = 'Cancelled'
        WHERE order_id = NEW.order_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger Definition
CREATE TRIGGER handle_failed_payment
AFTER INSERT OR UPDATE OF payment_status ON Payments
FOR EACH ROW
EXECUTE FUNCTION update_order_on_payment_fail();
