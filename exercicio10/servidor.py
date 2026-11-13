# Participantes: [Jean Aquilla] 
import asyncio
import logging
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from comum import argumentos, configurar_log, executar

clientes = {}


async def transmitir(texto, origem):
    destinos = [ws for ws in clientes if ws != origem]
    if destinos:
        # Um cliente que caiu não interrompe os demais envios.
        await asyncio.gather(*(ws.send(texto) for ws in destinos), return_exceptions=True)


async def atender(ws):
    nome = None
    try:
        apelido = await asyncio.wait_for(ws.recv(), timeout=15)
        if not isinstance(apelido, str) or not 1 <= len(apelido.strip()) <= 30:
            await ws.close(1008, "Nome inválido")
            return
        apelido = apelido.strip()
        if apelido in clientes.values():
            await ws.close(1008, "Nome já utilizado")
            return
        nome = apelido
        clientes[ws] = nome
        await ws.send("Conectado. Digite sair para encerrar.")
        await transmitir(f"* {nome} entrou", ws)
        async for texto in ws:
            if not isinstance(texto, str):
                await ws.close(1003, "Use mensagens de texto")
                break
            if texto.strip().lower() == "sair":
                break
            if texto.strip():
                await transmitir(f"{nome}: {texto.strip()}", ws)
    except (ConnectionClosed, TimeoutError):
        pass
    finally:
        if nome:
            clientes.pop(ws, None)
            await transmitir(f"* {nome} saiu", ws)
            logging.info("%s saiu", nome)


async def iniciar(args):
    configurar_log()
    # Sem compressão, o conteúdo dos frames fica mais fácil de estudar.
    async with serve(atender, args.host, args.porta, compression=None, max_size=4096):
        logging.info("WebSocket em ws://%s:%s", args.host, args.porta)
        await asyncio.Future()


if __name__ == "__main__":
    executar(lambda: asyncio.run(iniciar(argumentos("Chat WebSocket", 8765))))
