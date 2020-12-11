# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 12:05 上午
# @File    : async_mysql_utils.py
import asyncio
import logging
import aiomysql
from typing import List
from aiomysql import create_pool, Pool

__all__ = ('AsyncMysql',)


class AsyncMysql(object):
    """
    Handles mysql db connections
    """

    def __init__(self):
        self.connection_pool = None
        self._conn = None

    async def create_pool(self, loop: asyncio.AbstractEventLoop, **kwargs) -> None:
        """

        :param loop:
        :param kwargs:
        :return:
        """

        self.connection_pool = await create_pool(loop=loop, **locals())

    def get_pool(self):
        return self.connection_pool

    def set_conn(self, _conn):
        self._conn = _conn

    async def execute(self, query: str, params: List = None):
        if not params:
            params = []

        logging.debug("'%s' with params '%s'", query, str(params))
        if self._conn:
            async with self._conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, *params)
                return await cur.fetchall()

        async with self.connection_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, *params)
                return await cur.fetchall()

    async def close(self):
        if self.connection_pool:
            self.connection_pool.close()
            self.connection_pool = None
