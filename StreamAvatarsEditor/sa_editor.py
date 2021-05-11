import argparse
import json
import os
import shutil

StreamAvatarsFile = "streamavatars_json.txt"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--status", action="store_true", help="Displays a count of all enabled and disabled avatars")
    parser.add_argument("-l", "--list", action="store_true", help="Displays a list of all avatars with their activation status")
    parser.add_argument("-w", "--wipe-spawned", action="store_true", help="Wipes all manually spawned test avatars from the database. Looking for 'spawned*'")
    parser.add_argument("-ea", "--enable-all", action="store_true", help="Enables all avatars, unless specified via --disable")
    parser.add_argument("-da", "--disable-all", action="store_true", help="Disables all avatars, unless specified via --enable")
    parser.add_argument("-e", "--enable", action="append", help="Enables the given avatar, if it is present. Overrides --disable-all", metavar="AVATAR")
    parser.add_argument("-d", "--disable", action="append", help="Disables the given avatar, if it is present. Overrides --enable-all", metavar="AVATAR")
    return parser.parse_args()

def print_list(li, step=10):
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
    return "isEnabled" in data["avatarData"][a] and data["avatarData"][a]["isEnabled"]

def main():
    args = parse_args()
    if not args.list and not args.status and not args.enable and not args.disable and not args.enable_all and not args.disable_all and not args.wipe_spawned:
        print("No command is given!")
    elif args.disable_all and args.enable_all:
        print("Can not both disable and enable all avatars!")
    elif not os.path.isfile(StreamAvatarsFile):
        print("Can not find file: " + StreamAvatarsFile)
    else:
        shutil.copyfile(StreamAvatarsFile, StreamAvatarsFile + ".bak")
        data = None
        with open(StreamAvatarsFile, "r") as fp:
            data = json.load(fp)
        avatars = sorted(list(data["avatarData"].keys()))
        if args.list or args.status:
            status_list = []
            enabled = 0
            disabled = 0
            for i in range(len(avatars)):
                a = avatars[i]
                if enabled_state(a, data):
                    enabled += 1
                    status_list.append("(*)" + a)
                else:
                    disabled += 1
                    status_list.append("( )" + a)
            print("Enabled: " + str(enabled) + ", disabled: " + str(disabled))
            if args.list:
                print_list(status_list)
        if args.enable or args.disable or args.enable_all or args.disable_all or args.wipe_spawned:
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
            print("Writing file...")
            with open(StreamAvatarsFile, "w") as fp:
                json.dump(data, fp, separators=(",", ":"))

if __name__ == "__main__":
    main()