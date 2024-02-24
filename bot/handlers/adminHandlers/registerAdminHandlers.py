from .mainAdminHandlers import register_main_admin_handlers


def register_admin_handlers(dp) -> None:
    register_main_admin_handlers(dp)
