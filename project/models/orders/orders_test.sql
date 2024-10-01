{{
    config(
        tags="unit_test_orders" if var("unit_test", "false") == "true" else "orders"
    )
}}

SELECT 
    "TESTE" AS TESTE
    "bal" as bla