#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source.common.config import get_settings
from .database import BaseDatabaseManager, Driver


def init(settings: dict) -> BaseDatabaseManager:
    driver = Driver(settings["driver"])
    if driver is Driver.MONGODB:
        return init_nosql(driver=driver, settings=settings)
    else:
        return init_sql(driver=driver, settings=settings)


def init_sql(driver: Driver, settings: dict):
    from .database_sql import init
    keys = {'database', "host", "port", "user", "password"}
    settings = {k: v for k, v in settings.items() if k in keys}
    return init(driver, settings)


def init_nosql(driver: Driver, settings: dict):
    from .database_mongo import init
    return init(driver, settings=settings)


settings = get_settings("database.")
database_manager: "BaseDatabaseManager" = init(settings=settings)
