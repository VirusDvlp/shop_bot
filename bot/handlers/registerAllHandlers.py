from .sellerHandlers.registerSellerHandlers import register_seller_handlers
from .userHandlers.registerUserHandlers import register_user_handlers
from .adminHandlers.registerAdminHandlers import register_admin_handlers

from .defaultHandlers import register_default_handlers


def register_all_handlers(dp):
    register_seller_handlers(dp)
    register_user_handlers(dp)
    register_admin_handlers(dp)
    register_default_handlers(dp)
