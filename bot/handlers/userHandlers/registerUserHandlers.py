from .mainUserHandlers import register_main_user_handlers
from .showCatalogHandlers import register_show_catalog_kb
from .basketHandlers import register_basket_handlers
from .orderHandlers import register_order_req_handlers
from .historyOfOrdersHandlers import register_history_of_users_handlers


def register_user_handlers(dp) -> None:
    register_main_user_handlers(dp)
    register_show_catalog_kb(dp)
    register_basket_handlers(dp)
    register_order_req_handlers(dp)
    register_history_of_users_handlers(dp)
