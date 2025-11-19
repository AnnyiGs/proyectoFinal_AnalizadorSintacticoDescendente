import re

class Parser3Direcciones:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
        self.errores = []
        self.cuadruplos = []
        self.contador_temp = 0
        self.contador_etiqueta = 0
        self.tabla_simbolos = {}
    
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
        error_msg = f"Error en posicion {self.pos}: {message}"
        self.errores.append(error_msg)
        raise SyntaxError(error_msg)
    
    def nueva_temporal(self):
        temp = f"t{self.contador_temp}"
        self.contador_temp += 1
        self.tabla_simbolos[temp] = {'tipo': 'temporal'}
        return temp
    
    def nueva_etiqueta(self):
        etiqueta = f"L{self.contador_etiqueta}"
        self.contador_etiqueta += 1
        return etiqueta
    
    def agregar_cuadruplo(self, op, arg1, arg2, resultado):
        cuadruplo = (op, arg1, arg2, resultado)
        self.cuadruplos.append(cuadruplo)
    
    def mostrar_codigo_intermedio(self):
        print("\n" + "\033[95mCODIGO DE 3 DIRECCIONES GENERADO\033[0m")
        print("=" * 60)
        if not self.cuadruplos:
            print("No se genero codigo de 3 direcciones")
            return
        for i, cuadruplo in enumerate(self.cuadruplos):
            op, arg1, arg2, resultado = cuadruplo
            arg1_str = f"'{arg1}'" if arg1 is not None else "None"
            arg2_str = f"'{arg2}'" if arg2 is not None else "None"
            resultado_str = f"'{resultado}'" if resultado is not None else "None"
            print(f"{i:3d}: ({op:4}, {arg1_str:8}, {arg2_str:8}, {resultado_str:10})")
    
    def mostrar_tabla_simbolos(self):
        print("-" * 60)
        print("\n\033[95mTABLA DE SIMBOLOS\033[0m")
        print("=" * 60)
        print(f"{'Variable':<12} | {'Tipo':<10}")
        print("-" * 60)
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
                f.write("\n" + "=" * 60 + "\n")
                f.write("TABLA DE SIMBOLOS\n")
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
            print(f"Codigo guardado en: {nombre_archico}")
            return True
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return False

    def programa(self):
        try:
            print("-" * 60)
            print("\n\033[93mIniciando analisis sintactico...\033[0m\n")
            if not self.match('being'):
                self.error("Se esperaba 'being' al inicio del programa")
            self.declaraciones()
            self.ordenes()
            if not self.match('end'):
                self.error("Se esperaba 'end' al final del programa")
            print("\033[36mAnalisis sintactico completado exitosamente\033[0m\n")
            return True, self.errores
        except SyntaxError:
            return False, self.errores
    
    def declaraciones(self):
        if self.current_token and self.current_token[0] in ['entero', 'real']:
            self.declaracion()
            if not self.match(';'):
                self.error("Se esperaba ';' después de declaracion")
            self.declaraciones()
    
    def declaracion(self):
        tipo = self.tipo()
        self.lista_variables(tipo)
    
    def tipo(self):
        if self.match('entero'):
            return 'entero'
        elif self.match('real'):
            return 'real'
        else:
            self.error("Se esperaba 'entero' o 'real'")
    
    def lista_variables(self, tipo):
        id_name = self.identificador()
        self.tabla_simbolos[id_name] = {'tipo': tipo}
        self.lista_variablesR(tipo)
    
    def lista_variablesR(self, tipo):
        if self.match(','):
            id_name = self.identificador()
            self.tabla_simbolos[id_name] = {'tipo': tipo}
            self.lista_variablesR(tipo)
    
    def identificador(self):
        if self.current_token and self.current_token[0] == 'IDENTIFICADOR':
            id_name = self.current_token[1]
            self.match('IDENTIFICADOR')
            return id_name
        else:
            self.error("Se esperaba un identificador")
    
    def ordenes(self):
        self.orden()
        self.ordenesR()

    def ordenesR(self):
        if self.match(';'):
            self.orden()
            self.ordenesR()
    
    def orden(self):
        if self.current_token and self.current_token[0] == 'if':
            self.condicion()
        elif self.current_token and self.current_token[0] == 'while':
            self.bucle_while()
        else:
            self.asignar()
    
    def condicion(self):
        if not self.match('if'):
            self.error("Se esperaba 'if'")
        if not self.match('('):
            self.error("Se esperaba '(' después de if")
        op1, operador_comp, op2 = self.comparacion()
        if not self.match(')'):
            self.error("Se esperaba ')' después de comparacion")
        etiqueta_else = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()
        self.agregar_cuadruplo(f'if{operador_comp}', op1, op2, etiqueta_else)
        self.ordenes()
        self.agregar_cuadruplo('goto', None, None, etiqueta_fin)
        self.agregar_cuadruplo('label', None, None, etiqueta_else)
        self.else_opt()
        self.agregar_cuadruplo('label', None, None, etiqueta_fin)
    
    def else_opt(self):
        if self.match('else'):
            self.ordenes()
    
    def comparacion(self):
        op1 = self.operador()
        cond_op = self.condicion_op()
        op2 = self.operador()
        return op1, cond_op, op2
    
    def condicion_op(self):
        operadores = ['=', '<=', '>=', '<>', '<', '>']
        for op in operadores:
            if self.match(op):
                return op
        self.error("Se esperaba operador de comparacion (=, <=, >=, <>, <, >)")
    
    def operador(self):
        if self.current_token and self.current_token[0] == 'IDENTIFICADOR':
            return self.identificador()
        else:
            return self.numeros()
    
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
    
    def bucle_while(self):
        if not self.match('while'):
            self.error("Se esperaba 'while'")
        if not self.match('('):
            self.error("Se esperaba '(' después de while")
        etiqueta_inicio = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()
        self.agregar_cuadruplo('label', None, None, etiqueta_inicio)
        op1, operador_comp, op2 = self.comparacion()
        if not self.match(')'):
            self.error("Se esperaba ')' después de comparacion")
        self.agregar_cuadruplo(f'if{operador_comp}', op1, op2, etiqueta_fin)
        self.ordenes()
        self.agregar_cuadruplo('goto', None, None, etiqueta_inicio)
        self.agregar_cuadruplo('label', None, None, etiqueta_fin)
    
    def asignar(self):
        id_destino = self.identificador()
        if not self.match(':='):
            self.error("Se esperaba ':=' en asignacion")
        temp_resultado = self.expresion_arit()
        self.agregar_cuadruplo(':=', temp_resultado, None, id_destino)
    
    def expresion_arit(self):
        temp = self.termino()
        return self.expresion_aritR(temp)
    
    def expresion_aritR(self, temp_inicial):
        if self.match('+') or self.match('-'):
            operador = self.tokens[self.pos-1][1]
            temp2 = self.termino()
            nueva_temp = self.nueva_temporal()
            self.agregar_cuadruplo(operador, temp_inicial, temp2, nueva_temp)
            return self.expresion_aritR(nueva_temp)
        return temp_inicial
    
    def termino(self):
        temp = self.factor()
        return self.terminoR(temp)
    
    def terminoR(self, temp_inicial):
        if self.match('*') or self.match('/'):
            operador = self.tokens[self.pos-1][1]
            temp2 = self.factor()
            nueva_temp = self.nueva_temporal()
            self.agregar_cuadruplo(operador, temp_inicial, temp2, nueva_temp)
            return self.terminoR(nueva_temp)
        return temp_inicial
    
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
            self.error("Se esperaba identificador, número o expresion entre paréntesis")

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
        raise ValueError(f"Caracter no reconocido: '{char}'")
    return tokens

def analizar_con_3_direcciones():
    print("\n")
    print("=" * 60)
    print("\033[94m            ANALIZADOR SINTACTICO DESCENDENTE\033[0m")
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
            print("\n\033[36mINGRESA TU PROGRAMA:\033[0m")
            print("(Escribe 'fin' en una linea separada para terminar)")
            lineas = []
            while True:
                linea = input()
                if linea.strip().lower() == 'fin':
                    break
                lineas.append(linea)
            codigo_fuente = "\n".join(lineas)
            if not codigo_fuente.strip():
                print("-" * 60 )
                print("\033[91mNo se ingreso ningún codigo\033[0m")
                continue
            procesar_codigo(codigo_fuente)
        
        elif opcion == '2':
            mostrar_ejemplos()
        
        elif opcion == '3':
            print("CERRANDO PROGRAMA")
            break
        
        else:
            print("Opcion no valida. Por favor selecciona 1, 2 o 3.")

def mostrar_ejemplos():
    print("-" * 60)
    print("EJEMPLOS PREDEFINIDOS:\n")
    print("\033[92m✓ EJEMPLOS CORRECTOS:\033[0m")
    print("  1. Expresiones aritméticas simples")
    print("  2. Condicional if-else")
    print("  3. Bucle while")
    print("  4. Programa completo con todo")
    print("\n" + "»" * 60)
