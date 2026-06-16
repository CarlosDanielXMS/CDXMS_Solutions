# Testes Manuais — JCM v1.0.0

## 1. ensure_core
Operation = ensure_core
Esperado: Resultado.success = true; core mínimo criado.

## 2. leitura completa
Operation = read_json
File Path = core/settings.json
Json Path = $
Esperado: Resultado.data.value contém o documento completo.

## 3. leitura por propriedade
Operation = read_json
File Path = core/settings.json
Json Path = settings.language
Esperado: Resultado.data.value = pt-BR.

## 4. filtro com continuidade
Arquivo de teste:
{"config":{"services":[{"id":"x","name":"Teste","enabled":true}]}}
Json Path = config.services[id="x"].name
Esperado: Resultado.data.value = Teste.

## 5. filtro canônico
Json Path = $.config.services[?(@.id=="x")].enabled
Esperado: Resultado.data.value = true.

## 6. recursive descent
Json Path = $..id
Esperado: Resultado.data.match_count >= 1 quando houver ids.

## 7. write_json seguro
Json Path = config.services[id="x"].enabled
Value Json = false
Esperado: altera apenas um item.

## 8. merge_json em objeto
Json Path = config.services[id="x"]
Value Json = {"timeout_seconds":30}
Merge Strategy = deep_merge
Esperado: adiciona timeout_seconds preservando os demais campos.

## 9. escrita ambígua bloqueada
Json Path = config.services[*].enabled
Value Json = false
Esperado: Resultado.success=false; error.code=JSON_PATH_AMBIGUOUS_MATCH.
