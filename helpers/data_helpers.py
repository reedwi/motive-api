def parse_items(items, item_type):
    if items:
        try:
            all_items = [item[item_type] for item in items]
        except:
            all_items = []
    else:
        all_items = []
    return all_items

