from .mainSellerHandlers import register_main_seller_handlers
from .editGoodDataHandlers import register_edit_good_data_handlers
from .editShiftHandlers import register_edit_shift_handlers
from .addGoodHandlers import register_add_good_handlers
from .addCategoryHandlers import register_add_category
from .orderHandlers import register_order_handlers
from .historyOfOrdersHandlers import register_history_of_users_handlers
from .mailingHandlers import register_mailing_handlers


def register_seller_handlers(dp):
    register_main_seller_handlers(dp)
    register_edit_good_data_handlers(dp)
    register_edit_shift_handlers(dp)
    register_add_category(dp)
    register_add_good_handlers(dp)
    register_order_handlers(dp)
    register_history_of_users_handlers(dp)
    register_mailing_handlers(dp)
