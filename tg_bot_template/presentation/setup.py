from aiogram import Dispatcher
from .filters.custom_filters import CreatorFilter, NonRegistrationFilter, RegistrationFilter

def setup_filters(dp: Dispatcher) -> None:
    dp.filters_factory.bind(CreatorFilter)
    dp.filters_factory.bind(RegistrationFilter)
    dp.filters_factory.bind(NonRegistrationFilter)