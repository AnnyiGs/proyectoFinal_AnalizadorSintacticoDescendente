import re

class Parser3Direcciones:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        self.errores = []
        
        # Para generación de código de 3 direcciones
        self.cuadruplos = []  # Lista de cuadruplos: (op, arg1, arg2, resultado)
        self.contador_temp = 0
        self.contador_etiqueta = 0
        self.tabla_simbolos = {}  # Para almacenar información de variables
    
    def get_next_token(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def match(self, expected_type):
        if self.current_token and self.current_token[0] == expected_type:
            self.get_next_token()
            return True
        return False
    
    def error(self, message):
        error_msg = f"Error en posición {self.pos}: {message}"
        self.errores.append(error_msg)
        raise SyntaxError(error_msg)
    
    def nueva_temporal(self):
        """Genera un nuevo nombre de variable temporal"""
        temp = f"t{self.contador_temp}"
        self.contador_temp += 1
        # Registrar la temporal en tabla de símbolos
        self.tabla_simbolos[temp] = {'tipo': 'temporal'}
        return temp
    
    def nueva_etiqueta(self):
        """Genera una nueva etiqueta"""
        etiqueta = f"L{self.contador_etiqueta}"
        self.contador_etiqueta += 1
        return etiqueta
    
    def agregar_cuadruplo(self, op, arg1, arg2, resultado):
        """Agrega un cuadruplo al código intermedio"""
        cuadruplo = (op, arg1, arg2, resultado)
        self.cuadruplos.append(cuadruplo)
    
    def mostrar_codigo_intermedio(self):
        """Muestra el código de 3 direcciones generado de forma organizada"""
        print("\n" + "CODIGO DE 3 DIRECCIONES GENERADO")
        print("=" * 60)
        
        if not self.cuadruplos:
            print("No se genero codigo de 3 direcciones")
            return
        
        for i, cuadruplo in enumerate(self.cuadruplos):
            op, arg1, arg2, resultado = cuadruplo
            
            # Formatear para mejor visualización
            arg1_str = f"'{arg1}'" if arg1 is not None else "None"
            arg2_str = f"'{arg2}'" if arg2 is not None else "None"
            resultado_str = f"'{resultado}'" if resultado is not None else "None"
            
            print(f"{i:3d}: ({op:4}, {arg1_str:8}, {arg2_str:8}, {resultado_str:10})")
    
    def mostrar_tabla_simbolos(self):
        """Muestra la tabla de símbolos"""
        print("-" * 60)
        print("\nTABLA DE SIMBOLOS")
        print("=" * 60)
        print(f"{'Variable':<12} | {'Tipo':<10}")
        print("-" * 60)
        
        # Mostrar variables primero, luego temporales
        variables = {k: v for k, v in self.tabla_simbolos.items() if v['tipo'] != 'temporal'}
        temporales = {k: v for k, v in self.tabla_simbolos.items() if v['tipo'] == 'temporal'}
        
        for simbolo, info in variables.items():
            print(f"{simbolo:<12} | {info['tipo']:<10}")
        
        if temporales:
            print("-" * 60)
            print("TEMPORALES:")
            for temp, info in temporales.items():
                print(f"{temp:<12} | {info['tipo']:<10}")
    
    def guardar_codigo_archivo(self, nombre_archivo="codigo_3direcciones.txt"):
        """Guarda el código de 3 direcciones en un archivo"""
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("CODIGO DE 3 DIRECCIONES GENERADO\n")
                f.write("=" * 60 + "\n\n")
                
                for i, cuadruplo in enumerate(self.cuadruplos):
                    op, arg1, arg2, resultado = cuadruplo
                    arg1_str = f"'{arg1}'" if arg1 is not None else "None"
                    arg2_str = f"'{arg2}'" if arg2 is not None else "None"
                    resultado_str = f"'{resultado}'" if resultado is not None else "None"
                    
                    f.write(f"{i:3d}: ({op:4}, {arg1_str:8}, {arg2_str:8}, {resultado_str:10})\n")
                
                # Agregar tabla de símbolos al archivo
                f.write("\n" + "=" * 60 + "\n")
                f.write("TABLA DE SÍMBOLOS\n")
                f.write("=" * 60 + "\n")
                f.write(f"{'Variable':<12} | {'Tipo':<10}\n")
                f.write("-" * 60 + "\n")
                
                variables = {k: v for k, v in self.tabla_simbolos.items() if v['tipo'] != 'temporal'}
                temporales = {k: v for k, v in self.tabla_simbolos.items() if v['tipo'] == 'temporal'}
                
                for simbolo, info in variables.items():
                    f.write(f"{simbolo:<12} | {info['tipo']:<10}\n")
                
                if temporales:
                    f.write("-" * 60 + "\n")
                    f.write("TEMPORALES:\n")
                    for temp, info in temporales.items():
                        f.write(f"{temp:<12} | {info['tipo']:<10}\n")
            
            print(f"Código guardado en: {nombre_archivo}")
            return True
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return False

    # <programa> → being <declaraciones><ordenes> end
    def programa(self):
        try:
            print("-" * 60)
            print("\nIniciando análisis sintáctico...\n")
            
            if not self.match('being'):
                self.error("Se esperaba 'being' al inicio del programa")
            
            self.declaraciones()
            self.ordenes()
            
            if not self.match('end'):
                self.error("Se esperaba 'end' al final del programa")
            
            print("Analisis sintáctico completado exitosamente\n")
            return True, self.errores
            
        except SyntaxError:
            return False, self.errores
    
    # <declaraciones> → <declaracion>;<declaraciones> | ε
    def declaraciones(self):
        if self.current_token and self.current_token[0] in ['entero', 'real']:
            self.declaracion()
            if not self.match(';'):
                self.error("Se esperaba ';' después de declaración")
            self.declaraciones()
    
    # <declaracion> → <tipo><lista_variables>
    def declaracion(self):
        tipo = self.tipo()
        self.lista_variables(tipo)
    
    # <tipo> → entero | real
    def tipo(self):
        if self.match('entero'):
            return 'entero'
        elif self.match('real'):
            return 'real'
        else:
            self.error("Se esperaba 'entero' o 'real'")
    
    # <lista_variables> → <identificador><lista_variablesR>
    def lista_variables(self, tipo):
        id_name = self.identificador()
        # Registrar variable en tabla de símbolos
        self.tabla_simbolos[id_name] = {'tipo': tipo}
        self.lista_variablesR(tipo)
    
    # <lista_variablesR> → ,<identificador><lista_variablesR> | ε
    def lista_variablesR(self, tipo):
        if self.match(','):
            id_name = self.identificador()
            # Registrar variable en tabla de símbolos
            self.tabla_simbolos[id_name] = {'tipo': tipo}
            self.lista_variablesR(tipo)
    
    # <identificador> → <letra><resto_letras>
    def identificador(self):
        if self.current_token and self.current_token[0] == 'IDENTIFICADOR':
            id_name = self.current_token[1]
            self.match('IDENTIFICADOR')
            return id_name
        else:
            self.error("Se esperaba un identificador")
    
    # <ordenes> → <orden><ordenesR>
    def ordenes(self):
        self.orden()
        self.ordenesR()
    
    # <ordenesR> → ;<orden><ordenesR> | ε
    def ordenesR(self):
        if self.match(';'):
            self.orden()
            self.ordenesR()
    
    # <orden> → <condicion> | <bucle_while> | <asignar>
    def orden(self):
        if self.current_token and self.current_token[0] == 'if':
            self.condicion()
        elif self.current_token and self.current_token[0] == 'while':
            self.bucle_while()
        else:
            self.asignar()
    
    # <condicion> → if(<comparacion>)<ordenes><else_opt>end
    def condicion(self):
        if not self.match('if'):
            self.error("Se esperaba 'if'")
        
        if not self.match('('):
            self.error("Se esperaba '(' después de if")
        
        # Generar código para comparación
        op1, operador_comp, op2 = self.comparacion()
        
        if not self.match(')'):
            self.error("Se esperaba ')' después de comparación")
        
        # Generar etiquetas para el flujo de control
        etiqueta_else = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()
        
        # Generar salto condicional (si la condición es falsa, saltar a else)
        self.agregar_cuadruplo(f'if{operador_comp}', op1, op2, etiqueta_else)
        
        # Código para el then
        self.ordenes()
        
        # Salto al final después del then
        self.agregar_cuadruplo('goto', None, None, etiqueta_fin)
        
        # Etiqueta para el else
        self.agregar_cuadruplo('label', None, None, etiqueta_else)
        
        # Código para el else (si existe)
        self.else_opt()
        
        # Etiqueta de fin
        self.agregar_cuadruplo('label', None, None, etiqueta_fin)
    
    # <else_opt> → else <ordenes> | ε
    def else_opt(self):
        if self.match('else'):
            self.ordenes()
    
    # <comparacion> → <operador><condicion_op><operador>
    def comparacion(self):
        op1 = self.operador()
        cond_op = self.condicion_op()
        op2 = self.operador()
        return op1, cond_op, op2
    
    # <condicion_op> → = | <= | >= | <> | < | >
    def condicion_op(self):
        operadores = ['=', '<=', '>=', '<>', '<', '>']
        for op in operadores:
            if self.match(op):
                return op
        self.error("Se esperaba operador de comparación (=, <=, >=, <>, <, >)")
    
    # <operador> → <identificador> | <numeros>
    def operador(self):
        if self.current_token and self.current_token[0] == 'IDENTIFICADOR':
            return self.identificador()
        else:
            return self.numeros()
    
    # <numeros> → <numero_entero> | <numero_real>
    def numeros(self):
        if self.current_token and self.current_token[0] == 'ENTERO':
            valor = self.current_token[1]
            self.match('ENTERO')
            return valor
        elif self.current_token and self.current_token[0] == 'REAL':
            valor = self.current_token[1]
            self.match('REAL')
            return valor
        else:
            self.error("Se esperaba número entero o real")
    
    # <bucle_while> → while(<comparacion>)<ordenes>endwhile
    def bucle_while(self):
        if not self.match('while'):
            self.error("Se esperaba 'while'")
        
        if not self.match('('):
            self.error("Se esperaba '(' después de while")
        
        # Generar etiquetas para el bucle
        etiqueta_inicio = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()
        
        # Etiqueta de inicio del bucle
        self.agregar_cuadruplo('label', None, None, etiqueta_inicio)
        
        # Evaluar condición
        op1, operador_comp, op2 = self.comparacion()
        
        if not self.match(')'):
            self.error("Se esperaba ')' después de comparación")
        
        # Si condición es falsa, salir del bucle
        self.agregar_cuadruplo(f'if{operador_comp}', op1, op2, etiqueta_fin)
        
        # Cuerpo del bucle
        self.ordenes()
        
        # Volver al inicio del bucle
        self.agregar_cuadruplo('goto', None, None, etiqueta_inicio)
        
        # Etiqueta de fin del bucle
        self.agregar_cuadruplo('label', None, None, etiqueta_fin)
    
    # <asignar> → <identificador>:=<expresion_arit>
    def asignar(self):
        id_destino = self.identificador()
        
        if not self.match(':='):
            self.error("Se esperaba ':=' en asignación")
        
        # Evaluar expresión y obtener el resultado
        temp_resultado = self.expresion_arit()
        
        # Asignar el resultado a la variable destino
        self.agregar_cuadruplo(':=', temp_resultado, None, id_destino)
    
    # <expresion_arit> → <término><expresion_aritR>
    def expresion_arit(self):
        temp = self.termino()
        return self.expresion_aritR(temp)
    
    # <expresion_aritR> → (+|-)<termino><expresion_aritR> | ε
    def expresion_aritR(self, temp_inicial):
        if self.match('+') or self.match('-'):
            operador = self.tokens[self.pos-1][1]  # '+' o '-'
            temp2 = self.termino()
            nueva_temp = self.nueva_temporal()
            self.agregar_cuadruplo(operador, temp_inicial, temp2, nueva_temp)
            return self.expresion_aritR(nueva_temp)
        return temp_inicial
    
    # <termino> → <factor><terminoR>
    def termino(self):
        temp = self.factor()
        return self.terminoR(temp)
    
    # <terminoR> → (*|/)<factor><terminoR> | ε
    def terminoR(self, temp_inicial):
        if self.match('*') or self.match('/'):
            operador = self.tokens[self.pos-1][1]  # '*' o '/'
            temp2 = self.factor()
            nueva_temp = self.nueva_temporal()
            self.agregar_cuadruplo(operador, temp_inicial, temp2, nueva_temp)
            return self.terminoR(nueva_temp)
        return temp_inicial
    
    # <factor> → <identificador> | <numeros> | (<expresion_arit>)
    def factor(self):
        if self.current_token and self.current_token[0] == 'IDENTIFICADOR':
            return self.identificador()
        elif self.current_token and self.current_token[0] in ['ENTERO', 'REAL']:
            return self.numeros()
        elif self.match('('):
            temp = self.expresion_arit()
            if not self.match(')'):
                self.error("Se esperaba ')'")
            return temp
        else:
            self.error("Se esperaba identificador, número o expresión entre paréntesis")

# Analizador Léxico
def lexer(code):
    tokens = []
    
    keywords = ['being', 'end', 'entero', 'real', 'if', 'else', 'while', 'endwhile']
    symbols = ['(', ')', ',', ';', ':=', '=', '<=', '>=', '<>', '<', '>', '+', '-', '*', '/']
    
    identifier_pattern = r'[a-zA-Z][a-zA-Z0-9]*'
    integer_pattern = r'\d+'
    real_pattern = r'\d+\.\d+'
    
    i = 0
    while i < len(code):
        char = code[i]
        
        if char.isspace():
            i += 1
            continue
        
        if char.isalpha():
            match = re.match(identifier_pattern, code[i:])
            if match:
                token = match.group()
                if token in keywords:
                    tokens.append((token, token))
                else:
                    tokens.append(('IDENTIFICADOR', token))
                i += len(token)
                continue
        
        if char.isdigit():
            real_match = re.match(real_pattern, code[i:])
            if real_match:
                tokens.append(('REAL', real_match.group()))
                i += len(real_match.group())
                continue
            
            int_match = re.match(integer_pattern, code[i:])
            if int_match:
                tokens.append(('ENTERO', int_match.group()))
                i += len(int_match.group())
                continue
        
        if i + 1 < len(code):
            two_char = code[i:i+2]
            if two_char in [':=', '<=', '>=', '<>']:
                tokens.append((two_char, two_char))
                i += 2
                continue
        
        if char in symbols:
            tokens.append((char, char))
            i += 1
            continue
        
        raise ValueError(f"Carácter no reconocido: '{char}'")
    
    return tokens

# Función principal interactiva
def analizar_con_3_direcciones():
    print("\n")
    print("=" * 60)
    print("            ANALIZADOR SINTACTICO DESCENDENTE")
    print("=" * 60)
    
    while True:
        print("=" * 60)
        print("\nOPCIONES:")
        print("1. Ingresar programa")
        print("2. Ejemplos predefinidos")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opcion (1-3): ").strip()
        
        if opcion == '1':
            print("-" * 60)
            print("\nINGRESA TU PROGRAMA:")
            print("(Escribe 'fin' en una línea separada para terminar)")
            
            lineas = []
            while True:
                linea = input()
                if linea.strip().lower() == 'fin':
                    break
                lineas.append(linea)
            
            codigo_fuente = "\n".join(lineas)
            
            if not codigo_fuente.strip():
                print("No se ingresó ningún código")
                continue
            
            procesar_codigo(codigo_fuente)
        
        elif opcion == '2':
            mostrar_ejemplos()
        
        elif opcion == '3':
            print("CERRANDO PROGRAMA")
            break
        
        else:
            print("Opción no válida. Por favor selecciona 1, 2 o 3.")

def mostrar_ejemplos():
    print("-" * 60)
    print("EJEMPLOS PREDEFINIDOS:")
    print("✓ EJEMPLOS CORRECTOS:")
    print("  1. Expresiones aritméticas simples")
    print("  2. Condicional if-else")
    print("  3. Bucle while")
    print("  4. Programa completo con todo")
    print("\n" + "»" * 60)
    print("\n✗ EJEMPLOS CON ERRORES:")
    print("  5. Falta 'being'")
    print("  6. Falta 'end'")
    print("  7. Falta ';' en declaración")
    print("  8. Falta ':=' en asignación")
    print("  9. Paréntesis sin cerrar")
    print("  10. Identificador inválido")
    
    sub_opcion = input("\nSelecciona ejemplo (1-10): ").strip()
    
    ejemplos = {
        '1': """being
        entero a, b, c, resultado;
        a := 5;
        b := 3;
        c := 2;
        resultado := (a + b) * c
        end""",
                
                '2': """being
        entero x, y;
        x := 15;
        if(x > 10)
            y := 100
        else
            y := 200
        end
        end""",
                
                '3': """being
        entero i, suma;
        i := 0;
        suma := 0;
        while(i < 5)
            suma := suma + i;
            i := i + 1
        endwhile
        end""",
                
                '4': """being
        entero base, altura, area, contador;
        real precio, total;
        base := 10;
        altura := 5;
        area := base * altura;
        contador := 0;
        precio := 25.5;
        if(area > 20)
            total := precio * area
        else
            total := 0.0
        end;
        while(contador < 3)
            total := total + 10;
            contador := contador + 1
        endwhile
        end""",
                
        #ejemplo con errores
        '5': """entero x, y;
        x := 10;
        y := x + 5
        end""",
                
        '6': """being
        entero x, y;
        x := 10;
        y := x + 5""",
                
        '7': """being
        entero x y;
        x := 10;
        y := x + 5
        end""",
                
        '8': """being
        entero x, y;
        x = 10;
        y = x + 5
        end""",
                
        '9': """being
        entero x, y;
        x := 10;
        if(x > 5
            y := 20
        end
        end""",
                
        '10': """being
        entero 123abc, x;
        x := 10
        end"""
            }
    
    if sub_opcion in ejemplos:
        tipo = "✓ CORRECTO" if int(sub_opcion) <= 4 else "✗ CON ERROR"
        print(f"\nEJEMPLO {sub_opcion} ({tipo}):")
        print("=" * 60)
        print(ejemplos[sub_opcion])
        print("=" * 60)
        
        if int(sub_opcion) <= 4:  # Solo para ejemplos correctos
            guardar = input("\n¿Quieres guardar el código de 3 direcciones en archivo? (s/n): ").strip().lower()
            procesar_codigo(ejemplos[sub_opcion], guardar == 's')
        else:  # Para ejemplos con errores
            input("\nPresiona Enter para ver el manejo de errores...")
            procesar_codigo(ejemplos[sub_opcion])
    else:
        print("Opcion no valida")

def procesar_codigo(codigo_fuente, guardar_archivo=False):
    """Procesa el código y muestra los resultados"""
    print("\n" + "=" * 60)
    print("\n" + "ANALIZANDO CODIGO...")
    print("\n")
    print("=" * 60)
    print("Código fuente:")
    print(codigo_fuente)
    print("\n" + "=" * 60)
    
    try:
        # Análisis léxico
        tokens = lexer(codigo_fuente)
        print(f"\nTokens generados: {len(tokens)} tokens")
        print(f"   {tokens}")
        
        # Análisis sintáctico y generación de código de 3 direcciones
        parser = Parser3Direcciones(tokens)
        exito, errores = parser.programa()
        
        if exito:
            print("-" * 60)
            print("PROGRAMA SINTACTICAMENTE CORRECTO")
            print("-" * 60)
            
            # Mostrar código de 3 direcciones generado
            parser.mostrar_codigo_intermedio()
            
            # Mostrar tabla de símbolos
            parser.mostrar_tabla_simbolos()
            
            # Guardar en archivo si se solicita
            if guardar_archivo:
                nombre_archivo = input("\nNombre del archivo (Enter para 'codigo_3direcciones.txt'): ").strip()
                if not nombre_archivo:
                    nombre_archivo = "codigo_3direcciones.txt"
                parser.guardar_codigo_archivo(nombre_archivo)
            
        else:
            print("\nSE ENCONTRARON ERRORES SINTÁCTICOS:")
            for error in errores:
                print(f"   • {error}")
            
    except Exception as e:
        print(f"\nERROR DURANTE EL ANÁLISIS: {e}")

# Ejecutar el programa principal
if __name__ == "__main__":
    try:
        analizar_con_3_direcciones()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
