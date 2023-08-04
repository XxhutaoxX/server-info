import os
import psutil
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'server_info',
    'version': '1.0.0',
    'name': 'Server Info Plugin',
    'description': 'A plugin to display server resource information',
    'author': '胡桃'
}

class ServerInfoPlugin:
    def __init__(self, server: ServerInterface, info_cmd: str):
        self.server = server
        self.info_cmd = info_cmd

        self.server.register_command(
            Literal(self.info_cmd).runs(self.on_info_command)
        )

    def on_info_command(self, src: CommandSource, _):
        if isinstance(src, PlayerCommandSource):
            # 获取服务器资源信息
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent
            network_info = psutil.net_io_counters()
            network_usage = f"Sent: {network_info.bytes_sent} bytes, Received: {network_info.bytes_recv} bytes"

            # 发送信息到聊天栏
            src.get_server().say(
                f"服务器信息:\n"
                f"CPU 使用: {cpu_usage}%\n"
                f"内存 使用: {memory_usage}%\n"
                f"网络 使用: {network_usage}"
            )

def on_server_startup(server: ServerInterface, old_module):
    info_cmd = '!!info'
    server_info_plugin = ServerInfoPlugin(server, info_cmd)

def on_load(server: ServerInterface, prev_module):
    on_server_startup(server, prev_module)
