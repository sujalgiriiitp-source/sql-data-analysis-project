-- ==============================================================
-- Project: Indian E-Commerce SQL Data Analysis
-- File: procedures.sql
-- Description: Stored Procedures to encapsulate business logic.
-- ==============================================================

-- 1. Procedure to Process a New Order
-- Description: Inserts an order and its items, then automatically 
-- deduces the stock from the Products table.
CREATE OR REPLACE PROCEDURE place_new_order(
    p_customer_id INT,
    p_product_id INT,
    p_quantity INT,
    p_payment_mode VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id INT;
    v_unit_price NUMERIC(10, 2);
    v_total_amount NUMERIC(12, 2);
    v_current_stock INT;
BEGIN
    -- 1. Check stock availability
    SELECT stock_quantity, price INTO v_current_stock, v_unit_price
    FROM Products
    WHERE product_id = p_product_id;

    IF v_current_stock < p_quantity THEN
        RAISE EXCEPTION 'Insufficient stock for product %', p_product_id;
    END IF;

    -- 2. Calculate Total Amount
    v_total_amount := v_unit_price * p_quantity;

    -- 3. Create the Order
    INSERT INTO Orders (customer_id, order_date, total_amount, order_status, delivery_city, delivery_state)
    SELECT p_customer_id, CURRENT_TIMESTAMP, v_total_amount, 'Pending', city, state
    FROM Customers WHERE customer_id = p_customer_id
    RETURNING order_id INTO v_order_id;

    -- 4. Add Order Item
    INSERT INTO Order_Items (order_id, product_id, quantity, unit_price)
    VALUES (v_order_id, p_product_id, p_quantity, v_unit_price);

    -- 5. Deduct Stock
    UPDATE Products
    SET stock_quantity = stock_quantity - p_quantity
    WHERE product_id = p_product_id;

    -- 6. Add Payment Record
    INSERT INTO Payments (order_id, payment_date, payment_mode, payment_status, amount)
    VALUES (v_order_id, CURRENT_TIMESTAMP, p_payment_mode, 'Success', v_total_amount);
    
    -- 7. Update Order Status to Processing since payment is successful
    UPDATE Orders
    SET order_status = 'Processing'
    WHERE order_id = v_order_id;

    COMMIT;
    RAISE NOTICE 'Order % placed successfully.', v_order_id;
END;
$$;

-- 2. Procedure to Calculate Customer Lifetime Value (LTV) and update a summary table (if existed)
-- For demonstration, it outputs notice.
CREATE OR REPLACE PROCEDURE calculate_customer_ltv(p_customer_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_ltv NUMERIC(12, 2);
BEGIN
    SELECT COALESCE(SUM(total_amount), 0) INTO v_ltv
    FROM Orders
    WHERE customer_id = p_customer_id AND order_status = 'Delivered';

    RAISE NOTICE 'Lifetime Value for Customer ID % is ₹%', p_customer_id, v_ltv;
END;
$$;
