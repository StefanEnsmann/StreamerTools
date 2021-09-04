import argparse

def calc_width(n_bars, bar_width, bar_space):
    return n_bars * bar_width + (n_bars-1) * bar_space

def main():
    parser = argparse.ArgumentParser("Audio bar calculator")
    parser.add_argument("width", type=int, help="Defines the width of the visualizer in pixels")
    parser.add_argument("-n-min", default=20, type=int, help="Defines the minimum amount of bars")
    parser.add_argument("-n-max", default=200, type=int, help="Defines the maximum amount of bars")
    parser.add_argument("-w-min", default=3, type=int, help="Defines the minimum width of bars")
    parser.add_argument("-w-max", default=50, type=int, help="Defines the maximum width of bars")
    parser.add_argument("-s-min", default=0, type=int, help="Defines the minimum space between bars")
    parser.add_argument("-s-max", default=20, type=int, help="Defines the maximum space between bars")
    args = parser.parse_args()
    current_width = None
    values = [["N", "Bar width", "Bar spacing"]]
    for n_bars in range(args.n_min, args.n_max + 1):
        for bar_width in range(args.w_min, args.w_max + 1):
            if calc_width(n_bars, bar_width, 0) > args.width:
                break
            for bar_space in range(args.s_min, args.s_max + 1):
                current_width = calc_width(n_bars, bar_width, bar_space)
                if current_width >= args.width:
                    if current_width == args.width:
                        values.append([n_bars, bar_width, bar_space])
                    break
    print("Found {:} combinations for width {:}".format(len(values)-1, args.width))
    for n, w, s in values:
        print("{:<5} {:<9} {:<11}".format(n, w, s))

if __name__ == "__main__":
    main()