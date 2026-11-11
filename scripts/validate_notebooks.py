#!/usr/bin/env python3
"""Validate notebook JSON, Python syntax and the translation of function names."""
import ast
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
LEGACY_FUNCTION_NAMES = {
    'ler_colunas_excel_rapidamente', 'dividir_ano', 'registrar_falha',
    'construir_modelo', 'treinar_e_prever', 'calcular_metricas', 'procurar_ficheiro',
    'iterar_linhas_xlsx', 'verificar_cabecalho_xlsx', 'ajustar_prever',
    'obter_treino_por_politica', 'extrair_indicadores_poi', 'mapa_clusters',
    'selecionar', 'normalizar_id', 'medidas', 'treinar_modelo', 'dividir',
}


def main():
    files = sorted((ROOT / 'notebooks').glob('*.ipynb'))
    if not files:
        raise SystemExit('No notebooks found.')
    issues = []
    for path in files:
        try:
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            compiled = 0
            for ci, cell in enumerate(nb.cells):
                if cell.cell_type != 'code':
                    continue
                tree = ast.parse(cell.source, filename=f'{path.name}:cell{ci}')
                compiled += 1
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in LEGACY_FUNCTION_NAMES:
                        issues.append(f'{path.name}:cell{ci}: untranslated function {node.name}')
                if cell.get('outputs'):
                    issues.append(f'{path.name}:cell{ci}: cached output should not be committed')
            print(f'PASS {path.name} ({compiled} code cells)')
        except Exception as exc:
            issues.append(f'{path.name}: {exc}')
    if issues:
        print('\n'.join(issues))
        raise SystemExit(1)
    print(f'Validated {len(files)} notebooks. No experiments were executed.')


if __name__ == '__main__':
    main()
