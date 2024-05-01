from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_stock_alert(product_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "stock_alerts", {
            "type": "stock.alert",
            "message": message
        }
    )
