import pandas as pd

menu = pd.read_csv('kfc_data.csv')

def handle_order(order_text):
    items = []
    for item in menu['deal']:
        if item.lower() in order_text.lower():
            items.append(item)

    response = f"You have ordered {', '.join(items)}. "

    total_cost = calculate_total(items)
    response += f"Your total is Rupees. {total_cost}. "

    return items


def calculate_total(items):
    total = 0
    for item in items:
        try:
            item_price = menu.loc[menu['deal'] == item, 'price (in rs.)'].values[0]
            total += float(item_price)  
        except IndexError:
            print(f"Item '{item}' not found in the menu.")
        except ValueError:
            print(f"Invalid price value for item '{item}'.")
    return total

