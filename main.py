import os
import sys
from collections import defaultdict

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

# Load environment variables from .env file
load_dotenv()


def get_racks_for_current_orders(*order_ids):
    try:
        db_info = {
            'dbname': os.getenv('POSTGRES_DB_NAME'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
        }
        # Connect to the PostgreSQL database
        with psycopg2.connect(**db_info) as conn:
            # Create a cursor object
            with conn.cursor() as cur:
                query = sql.SQL('''
                    SELECT ico.item_id, i.item_name, ico.quantity, 
                        ico.customer_order_id, ir.is_main, r.rack_letter, r.id
                    FROM ItemCustomerOrder ico
                    JOIN ItemRack ir ON ico.item_id = ir.item_id
                    JOIN Item i ON ico.item_id = i.id
                    JOIN Rack r ON ir.rack_id = r.id
                    WHERE ico.customer_order_id IN %s
                    GROUP BY r.rack_letter, r.id, ico.item_id, i.item_name, ico.quantity, ico.customer_order_id, ir.is_main
                    ORDER BY r.rack_letter, ico.item_id;
                    ''')
                # Execute the query with the provided order IDs
                cur.execute(query, (order_ids,))

                main_racks = defaultdict(list)
                additional_racks = defaultdict(list)
                for rack in cur.fetchall():
                    item_id, item_name, quantity, customer_order_id, is_main, rack_letter, rack_id = rack
                    if is_main:
                        main_racks[(rack_id, rack_letter)].append((item_name, item_id, customer_order_id, quantity))
                    else:
                        additional_racks[item_name].append(rack_letter)

                print(f'=+=+=+=\nСтраница сборки заказов {",".join(map(str, order_ids))}\n')
                for key, value in main_racks.items():
                    rack_id, rack_letter = key
                    print(f'===Стеллаж {rack_letter}')
                    for sub_value in value:
                        item_name, item_id, customer_order_id, quantity = sub_value
                        print(
                            f'{item_name} (id={item_id})\n'
                            f'заказ {customer_order_id}, {quantity} шт'
                        )
                        if item_name in additional_racks:
                            print(f'доп стеллаж: {",".join(additional_racks[item_name])}')
                        print('')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    args = sys.argv[1]
    order_ids = [int(order_id) for order_id in args.split(',')]
    get_racks_for_current_orders(*order_ids)
