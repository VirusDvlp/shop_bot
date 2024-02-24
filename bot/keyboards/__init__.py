from .sellerKb.mainSellerKb import main_seller_kb, get_shift_kb
from .sellerKb.goodDataChangeKb import good_data_change_kb, get_choose_good_kb
from .sellerKb.orderKb import get_accept_order_req_kb, get_ordering_kb

from .userKb.mainUserKb import main_user_kb
from .userKb.catalogKb import get_add_to_basket_kb, get_select_good_number
from .userKb.basketKb import get_basket_kb
from .userKb.orderKb import ask_getting_type_kb, get_buy_order_kb, choose_pay_type_kb, orders_type_kb

from .adminKb.mainAdminKb import main_admin_kb

from .historyOfOrdersKb import get_list_of_orders_kb
from .chooseCategoryKb import get_choose_cat_kb