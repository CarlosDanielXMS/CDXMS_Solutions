import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
path = root / 'src/capabilities/juif_ui_builder/macrodroid/[CDXMS]_JUIF_UI_Builder.ablock'
string_path = root / 'src/capabilities/string_utils/macrodroid/[CDXMS]_String_Utils.ablock'
output = path

doc = json.loads(path.read_text(encoding='utf-8'))
string_doc = json.loads(string_path.read_text(encoding='utf-8'))
macro = doc['macro']
string_guid = string_doc['macro']['m_GUID']
vars_by_name = {v['m_name']: v for v in macro['localVariables']}


def variable(name, var_type, description, value=''):
    return {
        'description': description,
        'dictionary': {'entries': [], 'isArray': False, 'variableType': 4, 'type': 'Dictionary'},
        'isActionBlockWorkingVar': True,
        'isLocalVar': True,
        'isSecure': False,
        'm_booleanValue': False,
        'm_decimalValue': 0.0,
        'm_intValue': 0,
        'm_name': name,
        'm_stringValue': value,
        'm_type': var_type,
        'supportsInput': False,
        'supportsOutput': False,
    }

macro['localVariables'] = [
    vars_by_name['Config Json'],
    vars_by_name['UI Schema Json'],
    vars_by_name['Escape Json'],
    vars_by_name['Resultado'],
    variable('Tmp_ConfigEscapeResult', 4, 'Resultado da String Utils ao escapar Config Json para consumo seguro pelo JavaScript.'),
    variable('Tmp_SchemaEscapeResult', 4, 'Resultado da String Utils ao escapar UI Schema Json para consumo seguro pelo JavaScript.'),
    variable('Tmp_CoreResultJson', 2, 'Resultado intermediário serializado pelo motor principal do Builder.'),
    variable('Tmp_CoreResult', 4, 'Resultado intermediário parseado para acesso seguro aos dados gerados.'),
    variable('Tmp_CoreResultJsonEscape', 4, 'Resultado da String Utils ao escapar o Resultado intermediário para a etapa de finalização.'),
    variable('Tmp_UiEscapeResult', 4, 'Resultado da String Utils com o JUIF UI Json escapado uma vez.'),
    variable('Tmp_UiDoubleEscapeResult', 4, 'Resultado da String Utils com o JUIF UI Json escapado duas vezes para uso seguro no JavaScript final.'),
    variable('Tmp_ResultJson', 2, 'Resultado universal final serializado antes da publicação em Resultado.', '{}'),
]

original_actions = macro['m_actionList']
group = original_actions[0]
core = original_actions[1]
end_group = original_actions[-2]
exit_action = original_actions[-1]

script = core['scriptText']
start = script.find('function mdBlock')
end = script.find('function nowIso')
if start >= 0 and end > start:
    script = script[:start] + script[end:]
start = script.find('function escapeForMacroDroid')
end = script.find('function slug', start)
if start >= 0 and end > start:
    script = script[:start] + script[end:]
script = script.replace('function buildUi(config, schema, shouldEscape)', 'function buildUi(config, schema)')
script = script.replace('juif_ui_json_escaped: shouldEscape ? escapeForMacroDroid(juifUiJson) : juifUiJson,', 'juif_ui_json_escaped: juifUiJson,')
tail = script.find('var __cdxms_result = "";')
if tail < 0:
    raise RuntimeError('Tail do JavaScript principal não localizado')
script = script[:tail] + '''var __cdxms_result = "";
try {
  var configJson = "{lv=Tmp_ConfigEscapeResult[data][value]}";
  var schemaJson = "{lv=Tmp_SchemaEscapeResult[data][value]}";

  var config = parseJson(configJson, "Config Json");
  var schema = parseJson(schemaJson, "UI Schema Json");
  var built = buildUi(config, schema);

  __cdxms_result = buildResult(true, "success", "JUIF UI gerada com sucesso.", built, null);
} catch (e) {
  var err = e && e.code ? e : buildError("PROCESSING_FAILED", String(e && e.message ? e.message : e), {}, false);
  __cdxms_result = buildResult(false, "error", err.message || "Falha ao gerar JUIF UI.", {}, err);
}
__cdxms_result;
'''


def string_call(suffix, text, target, label, comment):
    return {
        'actionBlockId': string_guid,
        'actionBlockName': '[CDXMS] String Utils',
        'continueActionsWithoutWaiting': False,
        'inputDictionaryMap': {},
        'inputVarsMap': {'Operation': 'escape_json_string', 'Text': text},
        'outputDictionaryMap': {'Resultado': {'keys': []}},
        'outputVarsMap': {'Resultado': target},
        'actionLabel': label,
        'disableLogging': False,
        'm_SIGUID': -7051298459320190000 - suffix,
        'm_classType': 'ActionBlockAction',
        'm_comment': comment,
        'm_constraintList': [],
        'm_isDisabled': False,
        'm_isOrCondition': False,
    }

core.update({
    'scriptText': script,
    'stringVariableName': 'Tmp_CoreResultJson',
    'm_comment': 'Consome entradas previamente escapadas pela String Utils, valida e constrói o Resultado intermediário.',
    'actionLabel': 'Construir contrato JUIF',
})
core.pop('stringResultVariableName', None)

parse_core = {
    'dictionaryKeys': {'keys': []},
    'dictionaryVarName': 'Tmp_CoreResult',
    'stringVarName': 'Tmp_CoreResultJson',
    'actionLabel': 'Parsear Resultado intermediário',
    'disableLogging': False,
    'm_SIGUID': -1232511650262984930,
    'm_classType': 'JsonParseAction',
    'm_comment': 'Disponibiliza os dados do Resultado intermediário para as etapas de escape.',
    'm_constraintList': [],
    'm_isDisabled': False,
    'm_isOrCondition': False,
}

final_script = '''// Finaliza o Resultado usando somente valores preparados pela String Utils.
function normalizeBool(value, fallback) {
  if (value === true || value === false) return value;
  var normalized = String(value == null ? "" : value).trim().toLowerCase();
  if (["true", "1", "sim", "s", "verdadeiro"].indexOf(normalized) >= 0) return true;
  if (["false", "0", "não", "nao", "n", "falso"].indexOf(normalized) >= 0) return false;
  return fallback === true;
}

function failure(message, reason) {
  return JSON.stringify({
    schema_version: 1,
    namespace: "CDXMS",
    success: false,
    status: "error",
    artifact_type: "capability",
    artifact_id: "juif_ui_builder",
    operation: "build_ui",
    message: message,
    data: {},
    error: {
      code: "PROCESSING_FAILED",
      message: message,
      details: { reason: reason || "" },
      recoverable: false
    },
    meta: {
      source: "[CDXMS] JUIF UI Builder",
      version: "1.0.0",
      component_catalog_version: "1.0.0",
      timestamp: new Date().toISOString()
    }
  });
}

var __cdxms_result = "";
try {
  var serializedResult = "{lv=Tmp_CoreResultJsonEscape[data][value]}";
  var result = JSON.parse(serializedResult);

  if (result && result.success === true && result.data) {
    var rawUiJson = "{lv=Tmp_UiEscapeResult[data][value]}";
    var escapedUiJson = "{lv=Tmp_UiDoubleEscapeResult[data][value]}";
    var shouldEscape = normalizeBool("{lv=Escape Json}", true);
    result.data.juif_ui_json_escaped = shouldEscape ? escapedUiJson : rawUiJson;
  }

  __cdxms_result = JSON.stringify(result);
} catch (e) {
  var reason = String(e && e.message ? e.message : e);
  __cdxms_result = failure("Falha ao finalizar o Resultado do JUIF UI Builder.", reason);
}
__cdxms_result;
'''

final_action = {
    'blockNextAction': True,
    'javascriptEngine': 'JetPack JavascriptEngine',
    'scriptText': final_script,
    'stringVariableName': 'Tmp_ResultJson',
    'actionLabel': 'Finalizar Resultado',
    'disableLogging': False,
    'm_SIGUID': -6124819654017382553,
    'm_classType': 'JavaScriptAction',
    'm_comment': 'Reconstrói o Resultado final e aplica o valor escapado produzido pela String Utils.',
    'm_constraintList': [],
    'm_isDisabled': False,
    'm_isOrCondition': False,
}

parse_final = {
    'dictionaryKeys': {'keys': []},
    'dictionaryVarName': 'Resultado',
    'stringVarName': 'Tmp_ResultJson',
    'actionLabel': 'Publicar Resultado',
    'disableLogging': False,
    'm_SIGUID': -1232511650262984931,
    'm_classType': 'JsonParseAction',
    'm_comment': 'Converte o Resultado textual final na saída pública única.',
    'm_constraintList': [],
    'm_isDisabled': False,
    'm_isOrCondition': False,
}

group.update({
    'm_comment': 'Escapa fronteiras textuais via String Utils, constrói o contrato JUIF e publica a saída universal.',
})
end_group.update({'m_comment': 'Fecha o fluxo do Builder.', 'actionLabel': 'Fim — Build JUIF UI Contract'})

macro['m_actionList'] = [
    group,
    string_call(11, '{lv=Config Json}', 'Tmp_ConfigEscapeResult', 'Escapar Config Json', 'Prepara Config Json para entrada segura no JavaScript.'),
    string_call(12, '{lv=UI Schema Json}', 'Tmp_SchemaEscapeResult', 'Escapar UI Schema Json', 'Prepara UI Schema Json para entrada segura no JavaScript.'),
    core,
    parse_core,
    string_call(13, '{lv=Tmp_CoreResultJson}', 'Tmp_CoreResultJsonEscape', 'Escapar Resultado intermediário', 'Prepara o Resultado intermediário para a etapa JavaScript final.'),
    string_call(14, '{lv=Tmp_CoreResult[data][juif_ui_json]}', 'Tmp_UiEscapeResult', 'Escapar JUIF UI Json', 'Produz o valor público juif_ui_json_escaped.'),
    string_call(15, '{lv=Tmp_UiEscapeResult[data][value]}', 'Tmp_UiDoubleEscapeResult', 'Escapar JUIF UI Json para literal', 'Protege o valor já escapado para entrada no JavaScript final.'),
    final_action,
    parse_final,
    end_group,
    exit_action,
]
macro['lastEditedTimestamp'] = 1782230400000
macro['m_description'] = 'CDXMS JUIF UI Builder v1.0.0. Constrói o contrato JUIF e delega o escape de fronteiras textuais à capability [CDXMS] String Utils.'

output.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
