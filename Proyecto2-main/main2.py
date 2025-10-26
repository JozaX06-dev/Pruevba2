from Empresa import Empresa

def main():
    empresa = Empresa("ACME")

    # Cargar empleados desde CSV (Empresa debe implementar este método)
    empresa.cargar_empleados_csv("empleados.csv")

    # Procesar todos los empleados (ejemplo para periodo por horas)
    resultados = empresa.calcular_neto_empleados(horas_extras=40, tipo_cheque="pago de salario")
    for r in resultados:
        print(r)

    # Procesar un cheque individual por id
    resultado_unico = empresa.procesa_cheque(empleado_id=2, horas_extras=0, tipo_cheque="caja_chica")
    print(resultado_unico)

if __name__ == "__main__":
    main()
