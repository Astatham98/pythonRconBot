from commands.base_command  import BaseCommand
from utils                  import get_emoji
import valve.rcon
import settings


# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class Rcon(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Will do rcon commands"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["command", "extension"]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        
        command = params[0]
        value = params[1]
        
        if command.lower() == "ip":
            self.set_ip(value)
        elif command.lower() == "password":
            self.set_password(value)
        elif command.lower() == "exec":
            await self.exec(value, message.channel)
        elif command.lower() == "changelevel":
            await self.changelevel(value, message.channel)
        
    def set_ip(self, ip):
        settings.server_ip  = ip
    
    def set_password(self, password):
        settings.server_password = password
    
    async def exec(self, config, channel):
        address = (settings.server_ip.split(":")[0], int(settings.server_ip.split(":")[1]))
        password = settings.server_password
        command = "exec " + config
        
        try:
            out = valve.rcon.execute(address, password, command)
            if "not present; not executing" in out:
                await channel.send("Invalid config")
            else:
                await channel.send(f"Config changed to {config}")
        except valve.rcon.RCONAuthenticationError as e:
            await channel.send(f"ERROR {e}")
        except ConnectionRefusedError as e:
            await channel.send(f"ERROR {e}. Check the server IP and rcon password are correct")
            
    async def changelevel(self, map, channel):
        maps = {"process": "cp_process_f9a", 
            "sunshine": "cp_sunshine",
            "snakewater": "cp_snakewater_final1",
            "metalworks": "cp_metalworks_f3",
            "gullywash": "cp_gullywash_f7",
            "reckoner": "cp_reckoner_rc6",
            "clearcut": "koth_clearcut_b15d", 
            "granary": "cp_granary_pro_rc8",
            "prolands": "cp_prolands_rc2ta", 
            "bball": "ctf_ballin_skyfall",
            "ultiduo": "ultiduo_baloo_v2",
            "subbase": "cp_subbase_a22"}
        
        address = (settings.server_ip.split(":")[0], int(settings.server_ip.split(":")[1]))
        password = settings.server_password
        
        
        if "_" not in map:
            selected_map = maps.get(map.lower(), None)
            if selected_map is None:
                await channel.send("Input a valid map")
                return
        else:
            selected_map = map
        
        command = "changelevel " + selected_map
        
        print(address, password, command)
        try:
            out = valve.rcon.execute(address, password, command)
            if "not present; not executing" in out:
                await channel.send("Invalid map")
        except valve.rcon.RCONCommunicationError as e:
            await channel.send(f"Map changed to {selected_map}")
        except valve.rcon.RCONAuthenticationError as e:
            await channel.send(f"ERROR {e}")
        except ConnectionRefusedError as e:
            await channel.send(f"ERROR {e}. Check the server IP and rcon password are correct")

