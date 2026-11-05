import sys

MAX_ID = 4_000_000
MAX_PRODUCTO = 100_000


def fecha_valida(s):
    if len(s) != 10 or s[4:5] != b"-" or s[7:8] != b"-":
        return False

    try:
        y = int(s[:4])
        m = int(s[5:7])
        d = int(s[8:10])
    except ValueError:
        return False

    if not 1 <= m <= 12:
        return False

    if m == 2:
        bisiesto = y % 4 == 0 and (
            y % 100 != 0 or y % 400 == 0
        )
        limite = 29 if bisiesto else 28
    elif m in (4, 6, 9, 11):
        limite = 30
    else:
        limite = 31

    return 1 <= d <= limite


def solve():
    read = sys.stdin.buffer.readline

    fechas = read().split()
    if len(fechas) != 2:
        return

    d1, d2 = fechas
    n = int(read())

    usados = bytearray(MAX_ID + 1)
    ventas = [0] * (MAX_PRODUCTO + 1)

    for _ in range(n):
        linea = read()
        campos = linea.rstrip(b"\r\n").split(b",")

        if len(campos) != 4:
            continue

        fecha, venta, producto, cantidad = campos

        if not fecha_valida(fecha):
            continue

        try:
            venta = int(venta)
            producto = int(producto)
            cantidad = int(cantidad)
        except ValueError:
            continue

        if not 1 <= venta <= MAX_ID:
            continue

        if not 1 <= producto <= MAX_PRODUCTO:
            continue

        # Primera aparición válida, incluso fuera del intervalo.
        if usados[venta]:
            continue

        usados[venta] = 1

        if fecha < d1 or fecha > d2:
            continue

        ventas[producto] += cantidad

    mejores = []

    for producto in range(1, MAX_PRODUCTO + 1):
        total = ventas[producto]

        if total > 0:
            mejores.append((total, -producto))

    mejores.sort(reverse=True)
    mejores = mejores[:3]

    if not mejores:
        print("SIN DATOS")
        return

    for total, producto in mejores:
        print(-producto, total)


if __name__ == "__main__":
    solve()
