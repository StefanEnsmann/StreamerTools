#!/usr/bin/env python
"""A batch editor for StreamAvatars written in Python."""

import argparse
import json
import os
import shutil

__author__     = "Stefan Ensmann"
__copyright__  = "Copyright 2021, Stefan Ensmann"
__credits__    = ["Stefan Ensmann"]

__license__    = "AGPL-3.0"
__version__    = "1.0.0"
__maintainer__ = "Stefan Ensmann"
__email__      = "stefan@ensmann.de"
__status__     = "Production"

def parse_args():
    """Parses the console arguments and returns the ArgumentParser result."""
    StreamAvatarsFile = os.path.join(os.path.dirname(os.getenv("APPDATA")), "LocalLow", "ClonzeWork", "Streaming Avatars", "data", "streamavatars_json.txt")
    desc = "A batch editor for StreamAvatars written in Python."
    parser = argparse.ArgumentParser(prog="StreamAvatars Editor", description=desc)
    parser.add_argument("-s", "--status", action="store_true", help="Displays a count of all enabled and disabled avatars")
    parser.add_argument("-l", "--list", action="store_true", help="Displays a list of all avatars with their activation status")
    parser.add_argument("-w", "--wipe-spawned", action="store_true", help="Wipes all manually spawned test avatars from the database. Looking for 'spawned*'")
    parser.add_argument("-ea", "--enable-all", action="store_true", help="Enables all avatars, unless specified via --disable")
    parser.add_argument("-da", "--disable-all", action="store_true", help="Disables all avatars, unless specified via --enable")
    parser.add_argument("-e", "--enable", action="append", help="Enables the given avatar, if it is present. Overrides --disable-all", metavar="AVATAR")
    parser.add_argument("-d", "--disable", action="append", help="Disables the given avatar, if it is present. Overrides --enable-all", metavar="AVATAR")
    parser.add_argument("-c", "--columns", default=10, type=validColumnCount, help="Set the amount of columns to use for list printing. Default: 10")
    parser.add_argument("-f", "--file", default=StreamAvatarsFile, help="Set the path to streamavatars_json.txt. Default: %%APPDATA%%/LocalLow/ClonzeWork/Streaming Avatars/data/streamavatars_json.txt", metavar="PATH")
    return parser.parse_args()

def validColumnCount(s):
    """Checks the passed column parameter for a positive interger."""
    if not s.isdigit():
        raise ValueError(s + " is not a valid positive integer!")
    else:
        v = int(s)
        if v <= 0:
            raise ValueError(s + " is not a valid positive integer!")
        else:
            return v

def print_list(li, step):
    """Prints a given list in equally sized columns."""
    l = len(li)
    max_width = 0
    for a in li:
        max_width = max(max_width, len(a))
    template = "{:" + str(max_width + 1) + "}"
    lower = -1
    upper = 0
    while upper < l:
        lower = upper
        upper = min(upper + step, l)
        s = (upper - lower) * template
        print(s.format(*li[lower:upper]))

def enable_avatar(a, args, default):
    """Returns if the given avatar should be enabled or not."""
    if args.enable is not None and a in args.enable and args.disable is not None and a in args.disable:
        return None
    elif args.enable is not None and a in args.enable:
        return True
    elif args.disable is not None and a in args.disable:
        return False
    elif args.enable_all:
        return True
    elif args.disable_all:
        return False
    else:
        return default

def enabled_state(a, data):
    """Returns the current 'isEnabled' value of the given avatar."""
    return "isEnabled" in data["avatarData"][a] and data["avatarData"][a]["isEnabled"]

def main():
    """Main logic loop."""
    args = parse_args()
    if not args.list and not args.status and not args.enable and not args.disable and not args.enable_all and not args.disable_all and not args.wipe_spawned:
        print("No command is given!")
    elif args.disable_all and args.enable_all:
        print("Can not both disable and enable all avatars!")
    elif not os.path.isfile(args.file):
        print("Can not find file: " + args.file)
    else:
        # Create backup and load settings file
        shutil.copyfile(args.file, args.file + ".bak")
        data = None
        with open(args.file, "r") as fp:
            data = json.load(fp)
        
        # Sort avatars alphabetically and optionally print them
        avatars = sorted(list(data["avatarData"].keys()))
        if args.list or args.status:
            enabled_list = []
            disabled_list = []
            for i in range(len(avatars)):
                a = avatars[i]
                if enabled_state(a, data):
                    enabled_list.append("(*)" + a)
                else:
                    disabled_list.append("( )" + a)
            print("Enabled: " + str(len(enabled_list)) + ", disabled: " + str(len(disabled_list)))
            if args.list:
                print_list(enabled_list + disabled_list, args.columns)
        
        if args.enable or args.disable or args.enable_all or args.disable_all or args.wipe_spawned:
            # Update avatar activation
            if args.enable or args.disable or args.enable_all or args.disable_all:
                print("Updating avatar activation...")
                hasEnabledAvatar = False
                for a in avatars:
                    enable_state = enable_avatar(a, args, enabled_state(a, data))
                    if enable_state is None:
                        print("Avatar " + a + " is set for both enabling and disabling, aborting!")
                        return
                    if enable_state:
                        data["avatarData"][a]["isEnabled"] = True
                    elif "isEnabled" in data["avatarData"][a]:
                        del data["avatarData"][a]["isEnabled"]
                    hasEnabledAvatar = hasEnabledAvatar or enable_state
                if not hasEnabledAvatar:
                    print("No avatars left enabled, aborting!")
                    return
            
            # Remove users matching the format 'spawned*'
            if args.wipe_spawned:
                print("Wiping 'spawned*' users from database...")
                users = sorted(list(data["userData"].keys()))
                removed_users = []
                for u in users:
                    if u.startswith("spawned") and len(u) > 7 and u[7:].isdigit():
                        del data["userData"][u]
                        removed_users.append(u)
                if len(data["userData"].keys()) == 0:
                    print("No users left after wipe, aborting!")
                    return
                else:
                    print("Removed users from database:")
                    print_list(removed_users)
            
            # Write new file
            print("Writing file...")
            with open(args.file, "w") as fp:
                json.dump(data, fp, separators=(",", ":"))

if __name__ == "__main__":
    main()