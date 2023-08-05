package hutao.serverinfo;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.PluginCommand;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.NotNull;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ServerInfoPlugin extends JavaPlugin implements CommandExecutor {

    private Logger logger;

    @Override
    public void onEnable() {
        logger = getLogger();

        PluginCommand infoCommand = getCommand("info");
        if (infoCommand != null) {
            infoCommand.setExecutor(this);
        }
    }

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command cmd, @NotNull String label, String[] args) {
        if (cmd.getName().equalsIgnoreCase("info")) {
            if (sender instanceof Player) {
                Player player = (Player) sender;

                double cpuLoad = getCPULoad();
                double memoryUsage = getMemoryUsage();

                player.sendMessage("服务器CPU占用: " + cpuLoad + "%");
                player.sendMessage("服务器内存占用: " + memoryUsage + " MB");

                return true;
            } else {
                sender.sendMessage("该指令只能由玩家使用！");
                return false;
            }
        }
        return false;
    }

    public double getCPULoad() {
        double cpuLoad = 0.0;
        try {
            Process process = Runtime.getRuntime().exec("wmic cpu get loadpercentage");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            // Skip the first line (column header)
            reader.readLine();
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    cpuLoad = Double.parseDouble(line);
                    break;
                }
            }
            reader.close();
        } catch (IOException e) {
            logger.log(Level.SEVERE, "获取CPU占用率时发生异常：", e);
        } catch (NumberFormatException e) {
            logger.log(Level.SEVERE, "解析CPU占用率时发生异常：", e);
        }
        return cpuLoad;
    }

    public double getMemoryUsage() {
        double memoryUsage = 0.0;
        try {
            Process process = Runtime.getRuntime().exec("wmic OS get FreePhysicalMemory");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            // Skip the first line (column header)
            reader.readLine();
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    memoryUsage = Double.parseDouble(line) / 1024.0; // Convert to MB
                    break;
                }
            }
            reader.close();
        } catch (IOException e) {
            logger.log(Level.SEVERE, "获取内存占用时发生异常：", e);
        } catch (NumberFormatException e) {
            logger.log(Level.SEVERE, "解析内存占用时发生异常：", e);
        }
        return memoryUsage;
    }
}
