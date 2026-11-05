import sys

MAX_VENTA = 4_000_000
MAX_PRODUCTO = 100_000


def fecha_valida(s):
    if len(s) != 10:
        return False

    if s[4] != 45 or s[7] != 45:
        return False

    if not (s[:4].isdigit() and
            s[5:7].isdigit() and
            s[8:10].isdigit()):
        return False

    anio = int(s[:4])
    mes = int(s[5:7])
    dia = int(s[8:10])

    if anio < 1 or mes < 1 or mes > 12:
        return False

    if mes == 2:
        bisiesto = (
            anio % 4 == 0 and
            (anio % 100 != 0 or anio % 400 == 0)
        )
        limite = 29 if bisiesto else 28

    elif mes in (4, 6, 9, 11):
        limite = 30

    else:
        limite = 31

    return 1 <= dia <= limite


def solve():
    read = sys.stdin.buffer.readline

    intervalo = read().split()
    if len(intervalo) != 2:
        return

    fecha_inicio, fecha_fin = intervalo
    n = int(read())

    # Un byte por identificador: memoria compacta para deduplicar.
    usados = bytearray(MAX_VENTA + 1)

    # Acumulación directa por identificador de producto.
    ventas = [0] * (MAX_PRODUCTO + 1)

    for _ in range(n):
        linea = read()
        if not linea:
            continue

        campos = linea.rstrip(b"\r\n").split(b",")
        if len(campos) != 4:
            continue

        fecha, id_venta, id_producto, cantidad = campos

        if not fecha_valida(fecha):
            continue

        try:
            id_venta = int(id_venta)
            id_producto = int(id_producto)
            cantidad = int(cantidad)
        except ValueError:
            continue

        if not (1 <= id_venta <= MAX_VENTA):
            continue
        if not (1 <= id_producto <= MAX_PRODUCTO):
            continue

        # La primera aparición válida reserva el ID, incluso si
        # su fecha queda fuera del intervalo consultado.
        if usados[id_venta]:
            continue
        usados[id_venta] = 1

        # Comparación lexicográfica válida para fechas ISO YYYY-MM-DD.
        if fecha < fecha_inicio or fecha > fecha_fin:
            continue

        ventas[id_producto] += cantidad

    # Mantener únicamente los tres mejores: total descendente,
    # y en empate, identificador de producto ascendente.
    mejor1_id = mejor2_id = mejor3_id = 0
    mejor1_total = mejor2_total = mejor3_total = 0

    for producto in range(1, MAX_PRODUCTO + 1):
        total = ventas[producto]
        if total <= 0:
            continue

        if (total > mejor1_total or
                (total == mejor1_total and
                 (mejor1_id == 0 or producto < mejor1_id))):
            mejor3_id, mejor3_total = mejor2_id, mejor2_total
            mejor2_id, mejor2_total = mejor1_id, mejor1_total
            mejor1_id, mejor1_total = producto, total

        elif (total > mejor2_total or
                (total == mejor2_total and
                 (mejor2_id == 0 or producto < mejor2_id))):
            mejor3_id, mejor3_total = mejor2_id, mejor2_total
            mejor2_id, mejor2_total = producto, total

        elif (total > mejor3_total or
                (total == mejor3_total and
                 (mejor3_id == 0 or producto < mejor3_id))):
            mejor3_id, mejor3_total = producto, total

    if mejor1_id == 0:
        sys.stdout.write("SIN DATOS\n")
        return

    resultado = [f"{mejor1_id} {mejor1_total}"]
    if mejor2_id:
        resultado.append(f"{mejor2_id} {mejor2_total}")
    if mejor3_id:
        resultado.append(f"{mejor3_id} {mejor3_total}")

    sys.stdout.write("\n".join(resultado) + "\n")


if __name__ == "__main__":
    solve()

