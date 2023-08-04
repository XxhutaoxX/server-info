import os
import psutil
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'server_info',
    'version': '1.1.3',
    'name': '服务器资源信息插件',
    'description': '一个显示服务器资源信息的插件',
    'author': '胡桃'
}

class ServerInfoPlugin:
    def __init__(self, server: ServerInterface, info_cmd: str, server_info_cmd: str):
        self.server = server
        self.info_cmd = info_cmd
        self.server_info_cmd = server_info_cmd

        self.server.register_command(
            Literal(self.info_cmd).runs(self.on_info_command)
        )

        self.server.register_command(
            Literal(self.server_info_cmd).runs(self.on_server_info_command)
        )

    def on_info_command(self, src: CommandSource, _):
        if isinstance(src, PlayerCommandSource):
            # 获取服务器资源信息
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent
            network_info = psutil.net_io_counters()
            network_usage_sent = network_info.bytes_sent / (1024 * 1024)  # 转换为MB
            network_usage_recv = network_info.bytes_recv / (1024 * 1024)  # 转换为MB

            # 向玩家发送服务器资源信息
            src.get_server().tell(
                src.get_player(),
                f"服务器资源信息:\n"
                f"CPU 占用: {cpu_usage}%\n"
                f"内存 占用: {memory_usage}%\n"
                f"网络 发送: {network_usage_sent:.2f} MB, 接收: {network_usage_recv:.2f} MB"
            )

    def on_server_info_command(self, src: CommandSource, _):
        if isinstance(src, PlayerCommandSource):
            # 获取服务器资源信息
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent
            network_info = psutil.net_io_counters()
            network_usage_sent = network_info.bytes_sent / (1024 * 1024)  # 转换为MB
            network_usage_recv = network_info.bytes_recv / (1024 * 1024)  # 转换为MB

            # 向玩家自己发送服务器资源信息
            src.get_server().tell(
                src.get_player(),
                f"服务器资源信息:\n"
                f"CPU 占用: {cpu_usage}%\n"
                f"内存 占用: {memory_usage}%\n"
                f"网络 发送: {network_usage_sent:.2f} MB, 接收: {network_usage_recv:.2f} MB"
            )

# 在服务器启动时加载插件
def on_server_startup(server: ServerInterface):
    info_cmd = '!!info'
    server_info_cmd = '!!服务器信息'
    server_info_plugin = ServerInfoPlugin(server, info_cmd, server_info_cmd)
    
    # 在服务器加载时向控制台发送插件加载消息
    server.logger.info('服务器资源信息插件已加载')

# 在加载插件时调用
def on_load(server: ServerInterface, prev_module):
    on_server_startup(server)
