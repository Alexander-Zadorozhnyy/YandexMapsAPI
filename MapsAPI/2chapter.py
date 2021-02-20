from Samples.mapapi_PG import show_map
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('coord_x', type=float)
parser.add_argument('coord_y', type=float)
parser.add_argument('--zoom', type=float, default=1)
res = parser.parse_args()


def main():
    # Показываем карту с фиксированным масштабом.
    ll_spn = f"ll={res.coord_x},{res.coord_y}&spn={res.zoom},{res.zoom}"
    show_map(ll_spn, "map")


if __name__ == "__main__":
    main()