# app/utils/utils.py
import ast

def limpar_lista(lista_string):
        """
        Remove colchetes e aspas caso o valor seja algo como ['Fulano'].
        """
        if isinstance(lista_string, str) and lista_string.startswith("[") and lista_string.endswith("]"):
            try:
                parsed = ast.literal_eval(lista_string)
                if isinstance(parsed, list):
                    return ", ".join(parsed)
            except:
                pass
        return lista_string.strip("[]'")