def format_price(value):
    """Return an integer price with thin grouping: 5000 -> "5 000"."""
    return f'{int(value):,}'.replace(',', ' ')
