import json


class JSONCommandsMixin:
    """Set commands mixin.

        For commands details see: https://oss.redislabs.com/redisjson/commands/
    """

    encoder = json
    decoder = json

    encode = getattr(encoder, 'dumps')
    decode = getattr(decoder, 'loads')

    def __init__(self, encoder=None, decoder=None):
        if encoder is not None:
            self.encoder = encoder
            self.encode = getattr(self.encoder, 'dumps')
        if decoder is not None:
            self.decoder = decoder
            self.decode = getattr(self.decoder, 'loads')

    async def set(self, key, path, jsonable, nx=False, xx=False):
        """
        Set the JSON value at ``key`` under the ``path`` to ``jsonable``
        ``nx`` if set to True, set ``value`` only if it does not exist
        ``xx`` if set to True, set ``value`` only if it exists
        """
        pieces = [self.encode(jsonable)]
        if nx and xx:
            raise Exception('nx and xx are mutually exclusive: use one, the '
                            'other or neither - but not both')
        elif nx:
            pieces.append('NX')
        elif xx:
            pieces.append('XX')
        return await self.execute(b'JSON.SET', key, path, *pieces)

    async def get(self, key, *paths):
        """
        Get the object stored as a JSON value at ``key``
        ``paths`` is zero or more paths, and defaults to root path
        """
        result = await self.execute('JSON.GET', key, *paths)
        return self.decode(result)

    async def delete(self, key, path='.'):
        """
        Deletes the JSON value stored at ``key`` under ``path``
        """
        return await self.execute(b'JSON.DEL', key, path)

    async def mget(self, *keys, path='.'):
        """
        Gets the objects stored as a JSON values under ``path`` from
        ``keys``
        """
        results = await self.execute('JSON.MGET', *keys, path)
        return [self.decode(obj) for obj in results]

    async def type(self, key, path='.'):
        """
        Gets the type of the JSON value under ``path`` from ``key``
        """
        return await self.execute(b'JSON.TYPE', key, path)

    async def numincrby(self, key, path, number):
        """
        Increments the numeric (integer or floating point) JSON value under
        ``path`` at ``key`` by the provided ``number``
        """
        return await self.execute(b'JSON.NUMINCRBY', key, path, number)

    async def nummultby(self, key, path, number):
        """
        Multiplies the numeric (integer or floating point) JSON value under
        ``path`` at ``key`` with the provided ``number``
        """
        return await self.execute(b'JSON.NUMMULTBY', key, path, number)

    async def strappend(self, key, string, path='.'):
        """
        Appends to the string JSON value under ``path`` at ``key`` the
        provided ``string``
        """
        return await self.execute(b'JSON.STRAPPEND', key, path, self.encode(string))

    async def strlen(self, key, path='.'):
        """
        Returns the length of the string JSON value under ``path`` at
        ``key``
        """
        return await self.execute(b'JSON.STRLEN', key, path)

    async def arrappend(self, key, path, *jsonables):
        """
        Appends the objects ``args`` to the array under the ``path` in
        ``key``
        """
        pieces = []
        for o in jsonables:
            pieces.append(self.encode(o))
        return await self.execute(b'JSON.ARRAPPEND', key, path, *pieces)

    async def arrindex(self, key, path, scalar, start=0, stop=-1):
        """
        Returns the index of ``scalar`` in the JSON array under ``path`` at
        ``key``. The search can be limited using the optional inclusive
        ``start`` and exclusive ``stop`` indices.
        """
        return self.execute(b'JSON.ARRINDEX', key, path, self.encode(scalar), start, stop)

    async def arrinsert(self, key, path, index, *args):
        """
        Inserts the objects ``args`` to the array at index ``index`` under the
        ``path` in ``key``
        """
        pieces = []
        for o in args:
            pieces.append(self.encode(o))
        return self.execute(b'JSON.ARRINSERT', key, path, index, *pieces)

    async def arrlen(self, key, path='.'):
        """
        Returns the length of the array JSON value under ``path`` at
        ``key``
        """
        return self.execute(b'JSON.ARRLEN', key, path)

    async def arrpop(self, key, path='.', index=-1):
        """
        Pops the element at ``index`` in the array JSON value under ``path`` at
        ``key``
        """
        return self.execute(b'JSON.ARRPOP', key, path, index)

    async def arrtrim(self, key, path, start, stop):
        """
        Trim the array JSON value under ``path`` at ``key`` to the
        inclusive range given by ``start`` and ``stop``
        """
        return self.execute(b'JSON.ARRTRIM', key, path, start, stop)

    async def objkeys(self, key, path='.'):
        """
        Returns the key names in the dictionary JSON value under ``path`` at
        ``key``
        """
        return self.execute(b'JSON.OBJKEYS', key, path)

    async def objlen(self, key, path='.'):
        """
        Returns the length of the dictionary JSON value under ``path`` at
        ``key``
        """
        return self.execute(b'JSON.OBJLEN', key, path)