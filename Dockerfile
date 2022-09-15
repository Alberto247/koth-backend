FROM pypy:3.8-7.3.9-buster
RUN apt install gcc g++
RUN pypy3 -m pip install websockets asyncio numpy
COPY backend.py /
COPY config.py /
COPY game.py /
COPY hex_types.py /
COPY Hex.py /
COPY lloyd.py /
COPY map.py /
COPY player.py /
ENTRYPOINT ["pypy3", "-u", "/backend.py"]