import os
import json
import re
import rich

os.system("")

class Parse(object):
    def __init__(self) -> None:
        pass

    def TupleParse(self, data: tuple):
        d = "\033[00m( "
        num = 0

        for item in data:
            num += 1

            if type(item) == str:
                if len(data) - num == 0:
                    d += f"\033[32m'{item}'\033[00m "
                else:
                    d += f"\033[32m'{item}'\033[00m, "

            if type(item) == int:
                if len(data) - num == 0:
                    d += f"\033[93m{item}\033[00m "
                else:
                    d += f"\033[93m{item}\033[00m, "

            if type(item) == bool:
                if len(data) - num == 0:
                    if item == True:
                        d += f"\033[94mtrue\033[00m "
                    else:
                        d += f"\033[91mfalse\033[00m "
                
                else:
                    if item == True:
                        d += f"\033[94mtrue\033[00m, "
                    else:
                        d += f"\033[91mfalse\033[00m, "

            if type(item) == tuple:
                if len(data) - num == 0:
                    d += f"\033[00m{self.TupleParse(item)}\033[00m "
                else:
                    d += f"\033[00m{self.TupleParse(item)}\033[00m "

            if type(item) == dict:
                if len(data) - num == 0:
                    d += f"\033[00m{self.DictParse(item)}\033[00m "
                else:
                    d += f"\033[00m{self.DictParse(item)}\033[00m "

            if type(item) == list:
                if len(data) - num == 0:
                    d += f"\033[00m{self.ListParse(item)}\033[00m "
                else:
                    d += f"\033[00m{self.ListParse(item)}\033[00m "

            if type(item) == set:
                if len(data) - num == 0:
                    d += f"\033[00m{self.SetParse(item)}\033[00m "
                else:
                    d += f"\033[00m{self.SetParse(item)}\033[00m "

        d += "\033[00m)"

        return d

    def SetParse(self, data: set):
        d = "\033[00m{ "
        num = 0

        for item in data:
            num += 1
            
            if type(item) == str:
                if len(data) - num == 0:
                    d += f"\033[32m'{item}'\033[00m "
                else:
                    d += f"\033[32m'{item}'\033[00m, "

            if type(item) == int:
                if len(data) - num == 0:
                    d += f"\033[93m{item}\033[00m "
                else:
                    d += f"\033[93m{item}\033[00m, "

            if type(item) == bool:
                if len(data) - num == 0:
                    if item == True:
                        d += f"\033[94mtrue\033[00m "
                    else:
                        d += f"\033[91mfalse\033[00m "

                else:
                    if item == True:
                        d += f"\033[94mtrue\033[00m, "
                    else:
                        d += f"\033[91mfalse\033[00m, "

        d += " \033[00m}"

        return d

    def ListParse(self, data: list):
        d = "\033[00m[ "
        num = 0

        for item in data:
            num += 1

            if type(item) == str:
                if len(data) - num == 0:
                    d += f"\033[32m'{item}'\033[00m "
                else:
                    d += f"\033[32m'{item}'\033[00m, "
            
            if type(item) == int:
                if len(data) - num == 0:
                    d += f"\033[93m{item}\033[00m "
                else:
                    d += f"\033[93m{item}\033[00m, "

            if type(item) == bool:
                if len(data) - num == 0:
                    if item == True:
                        d += f"\033[94mtrue\033[00m "
                    else:
                        d += f"\033[91mfalse\033[00m "

                else:
                    if item == True:
                        d += f"\033[94mtrue\033[00m, "
                    else:
                        d += f"\033[91mfalse\033[00m, "

            if type(item) == list:
                if len(data) - num == 0:
                    d += f"\033[93m{self.ListParse(item)}\033[00m "
                else:
                    d += f"\033[93m{self.ListParse(item)}\033[00m, "

            if type(item) == dict:
                if len(data) - num == 0:
                    d += f"\033[93m{self.DictParse(item)}\033[00m "
                else:
                    d += f"\033[93m{self.DictParse(item)}\033[00m, "

            if type(item) == tuple:
                if len(data) - num == 0:
                    d += f"\033[00m{self.TupleParse(item)}\033[00m "
                else:
                    d += f"\033[00m{self.TupleParse(item)}\033[00m "

            if type(item) == set:
                if len(data) - num == 0:
                    d += f"\033[00m{self.SetParse(item)}\033[00m "
                else:
                    d += f"\033[00m{self.SetParse(item)}\033[00m "

        d += "\033[00m]"

        return d

    def DictParse(self, data: dict):
        d = "\033[00m{ "
        num = 0

        for key, val in data.items():
            num += 1

            if type(key) == str and type(val) == str:
                if len(data.keys()) - num == 0:
                    d += f"\033[00m{key}: \033[32m'{val}'\033[00m "
                else:
                    d += f"\033[00m{key}: \033[32m'{val}'\033[00m, "

            if type(key) == str and type(val) == int:
                if len(data.keys()) - num == 0:
                    d += f"\033[00m{key}: \033[93m{val}\033[00m "
                else:
                    d += f"\033[00m{key}: \033[93m{val}\033[00m, "

            if type(key) == str and type(val) == bool:
                if len(data.keys()) - num == 0:
                    if str(val) == "True":
                        d += f"\033[00m{key}: \033[94mtrue\033[00m "
                    else:
                        d += f"\033[00m{key}: \033[91mfalse\033[00m "
                else:
                    if str(val) == "True":
                        d += f"\033[00m{key}: \033[94mtrue\033[00m, "
                    else:
                        d += f"\033[00m{key}: \033[91mfalse\033[00m, "

            if type(key) == int and type(val) == str:
                if len(data.keys()) - num == 0:
                    d += f"\033[93m{key}\033[00m: \033[32m'{val}'\033[00m "
                else:
                    d += f"\033[93m{key}\033[00m: \033[32m'{val}'\033[00m, "

            if type(key) == int and type(val) == int:
                if len(data.keys()) - num == 0:
                    d += f"\033[93m{key}\033[00m: \033[93m{val}\033[00m "
                else:
                    d += f"\033[93m{key}\033[00m: \033[93m{val}\033[00m, "

            if type(key) == int and type(val) == bool:
                if len(data.keys()) - num == 0:
                    if str(val) == "True":
                        d += f"\033[93m{key}\033[00m: \033[94mtrue\033[00m "
                    else:
                        d += f"\033[93m{key}\033[00m: \033[91mfalse\033[00m "
                else:
                    if str(val) == "True":
                        d += f"\033[93m{key}\033[00m: \033[94mtrue\033[00m, "
                    else:
                        d += f"\033[93m{key}\033[00m: \033[91mfalse\033[00m, "

            if type(key) == int and type(val) == dict:
                if len(data.keys()) - num == 0:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.DictParse(val)} "
                else:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.DictParse(val)}, "

            if type(key) == int and type(val) == tuple:
                if len(data.keys()) - num == 0:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.TupleParse(val)} "
                else:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.TupleParse(val)}, "

            if type(key) == int and type(val) == set:
                if len(data.keys()) - num == 0:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.SetParse(val)} "
                else:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.SetParse(val)}, "

            if type(key) == int and type(val) == list:
                if len(data.keys()) - num == 0:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.ListParse(val)} "
                else:
                    d += f"\033[93m{key}\033[00m: \033[00m{self.ListParse(val)}, "

            if type(key) == str and type(val) == dict:
                if len(data.keys()) - num == 0:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.DictParse(val)} "
                else:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.DictParse(val)}, "

            if type(key) == str and type(val) == tuple:
                if len(data.keys()) - num == 0:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.TupleParse(val)} "
                else:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.TupleParse(val)}, "

            if type(key) == str and type(val) == set:
                if len(data.keys()) - num == 0:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.SetParse(val)} "
                else:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.SetParse(val)}, "

            if type(key) == str and type(val) == list:
                if len(data.keys()) - num == 0:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.ListParse(val)} "
                else:
                    d += f"\033[00m{key}\033[00m: \033[00m{self.ListParse(val)}, "

        d += "\033[00m}"

        return d

    def ListParseFlex(self, data: list, flex: int = 2):
        dy = str(json.dumps(data, indent=flex))
        
        for item in data:
            if type(item) == int or type(item) == float:
                dy = dy.replace(f"1", f"<YELLOW>1<WHITE>").replace(f"2", f"<YELLOW>2<WHITE>").replace(f"3", f"<YELLOW>3<WHITE>").replace(f"4", f"<YELLOW>4<WHITE>").replace(f"5", f"<YELLOW>5<WHITE>").replace(f"6", f"<YELLOW>6<WHITE>").replace(f"7", f"<YELLOW>7<WHITE>").replace(f"8", f"<YELLOW>8<WHITE>").replace(f"9", f"<YELLOW>9<WHITE>").replace(f"0", f"<YELLOW>0<WHITE>")

            if type(item) == str:
                dy = dy.replace(f"'{item}'", f"<GREEN>'{item}'<WHITE>").replace(f'"{item}"', f"<GREEN>'{item}'<WHITE>")
            
            if type(item) == bool:
                dy = dy.replace("true", "<BLUE>true<WHITE>").replace("false", "<RED>false<WHITE>")

            if type(item) == list:
                dy = dy.replace(item, self.ListParseFlex(item, flex=flex))

        return "\033[00m" + dy.replace("<BLUE>", "\033[94m").replace("<RED>", "\033[91m").replace("<GREEN>", "\033[32m").replace("<YELLOW>", "\033[93m").replace("<WHITE>", "\033[00m")
    
    def JsonParse(self, data: dict, flex: int = 2):
        ready = json.dumps(data, indent=flex)
        ready = re.sub(r'\b(\d+)\b', r'\033[1;33m\1\033[m', ready)
        ready = re.sub(r'"(.*?)"', r"\033[32m'\033[1;32m\1'\033[m", ready)
        for _ in data.keys():
            ready = ready.replace(f"'{str(_)}'", f"\033[00m{str(_)}")
            ready = ready.replace("false", "\033[91mfalse\033[00m")
            ready = ready.replace("true", "\033[94mtrue\033[00m")
        
        ready = ready.replace("'", "\033[32m'").replace(",", "\033[00m,").replace(":", "\033[00m:")
        return ready
    
    def JsonRichParse(self, data: dict):
        rich.print(data)