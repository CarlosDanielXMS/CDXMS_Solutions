# CDXMS — Catálogo de Estruturas de Ações MacroDroid v0.1
Arquivo analisado: `All_Actions.ablock`. Este documento registra as estruturas observadas diretamente no export MacroDroid enviado para servir como referência de engenharia do ecossistema CDXMS.
> Observação: este catálogo é baseado no export fornecido. Ele não substitui a homologação no MacroDroid real, mas passa a ser a fonte prática local para conhecer nomes de classes, campos e formatos internos das ações.

O snapshot foi editado em `2026-06-16` e representa aproximadamente o contexto do MacroDroid `5.64.x`. Ele é parcial: a linha `5.67.x` já possui ações posteriores, como Sensor Read, Read Sound Level e Mute Microphone. Ausência neste catálogo não significa indisponibilidade na versão alvo.
## Resumo executivo
- Total de ações no export: **189**.
- Classes de ação únicas observadas: **171**.
- Estrutura top-level do export: `globalVariables`, `macro`, `macroExportVersion`.
- O export é um Action Block: `macro.isActionBlock = true`.

## Ações mais importantes para o CDXMS agora
### `FileOperationV21Action`
- Ocorrências no All_Actions: 5.
- Índice de amostra: 39.
- Campos de configuração observados: `listFilesDictionaryKeys, listFilesOutputType, listFilesSortAscending, listFilesSortBy, listFilesVariableName, m_fileExtensions, m_fileOption, m_filePattern, m_folderName, m_fromName, m_fromUriString, m_option, m_toName, m_toUriString, waitToComplete`.
```json
{
  "listFilesOutputType": 0,
  "listFilesSortAscending": true,
  "listFilesSortBy": 0,
  "m_fileExtensions": [],
  "m_fileOption": 0,
  "m_filePattern": "*",
  "m_fromName": "CDXMS_Solutions",
  "m_fromUriString": "content://com.android.externalstorage.documents/tree/primary%3ADocuments%2FCDXMS_Solutions",
  "m_option": 0,
  "m_toName": "CDXMS_Solutions",
  "m_toUriString": "content://com.android.externalstorage.documents/tree/primary%3ADocuments%2FCDXMS_Solutions",
  "waitToComplete": true
}
```
### `FileOperationAllFilesAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 45.
- Campos de configuração observados: `fileExtensions, fileOption, filePattern, fromPath, listFilesOutputType, listFilesSortAscending, listFilesSortBy, option, toPath, waitToComplete`.
```json
{
  "fileExtensions": [],
  "fileOption": 0,
  "filePattern": "*",
  "fromPath": "teste",
  "listFilesOutputType": 0,
  "listFilesSortAscending": true,
  "listFilesSortBy": 0,
  "option": 0,
  "toPath": "teste",
  "waitToComplete": true
}
```
### `ReadFileAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 44.
- Campos de configuração observados: `allFilesAccessPath, dictionaryKeys, staticFilename, useAllFilesAccess, variableName`.
```json
{
  "allFilesAccessPath": "teste",
  "dictionaryKeys": {
    "keys": [
      "teste"
    ]
  },
  "staticFilename": false,
  "useAllFilesAccess": true,
  "variableName": "teste1"
}
```
### `WriteToFileAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 38.
- Campos de configuração observados: `allFilesPath, m_append, m_filename, m_logText, m_prepend, overwrite, useAllFilesAccess`.
```json
{
  "allFilesPath": "teste",
  "m_append": true,
  "m_filename": "teste",
  "m_logText": "teste",
  "m_prepend": false,
  "overwrite": false,
  "useAllFilesAccess": true
}
```
### `TextManipulationAction`
- Ocorrências no All_Actions: 2.
- Índice de amostra: 179.
- Campos de configuração observados: `m_option, m_text, m_textManipulation, varDictionaryKeys, variableName`.
```json
{
  "m_option": 1,
  "m_text": "teste",
  "m_textManipulation": {
    "type": "ReplaceAllManipulation",
    "params": [
      "teste",
      "tste",
      "true"
    ]
  },
  "variableName": "teste2"
}
```
### `JsonParseAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 109.
- Campos de configuração observados: `dictionaryKeys, dictionaryVarName, stringVarName`.
```json
{
  "dictionaryKeys": {
    "keys": []
  },
  "dictionaryVarName": "teste1",
  "stringVarName": "teste2"
}
```
### `JsonOutputAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 110.
- Campos de configuração observados: `dictionaryKeys, dictionaryVarName, stringVarName`.
```json
{
  "dictionaryKeys": {
    "keys": []
  },
  "dictionaryVarName": "teste1",
  "stringVarName": "teste2"
}
```
### `ArrayManipulationAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 181.
- Campos de configuração observados: `endIndex, inputArrayKeys, inputArrayVarName, numericalExpressionFilterText, option, outputArrayKeys, outputArrayVarName, startIndex, stringFilterIgnoreCase, stringFilterOption, stringFilterRegex, stringFilterText`.
```json
{
  "endIndex": 0,
  "inputArrayKeys": {
    "keys": []
  },
  "inputArrayVarName": "0 entradas",
  "numericalExpressionFilterText": "",
  "option": 3,
  "outputArrayKeys": {
    "keys": []
  },
  "outputArrayVarName": "0 entradas",
  "startIndex": 0,
  "stringFilterIgnoreCase": true,
  "stringFilterOption": 0,
  "stringFilterRegex": false,
  "stringFilterText": "teste"
}
```
### `IterateDictionaryAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 56.
- Campos de configuração observados: `childrenCollapsed, dictionaryKeys, dontLogIfConditionIsFalse, isArray, m_fixedOptionCount, m_option, timedDurationValue, timedTimeUnit, variableName`.
```json
{
  "dictionaryKeys": {
    "keys": []
  },
  "isArray": false,
  "variableName": "teste1",
  "m_fixedOptionCount": 1,
  "m_option": 0,
  "timedDurationValue": 1,
  "timedTimeUnit": 0,
  "childrenCollapsed": false,
  "dontLogIfConditionIsFalse": false
}
```
### `ClearDictionaryArrayEntryAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 177.
- Campos de configuração observados: `clearOption, dictionaryKeys, isAllEntries, variableName`.
```json
{
  "clearOption": 0,
  "dictionaryKeys": [],
  "isAllEntries": false,
  "variableName": "0 entradas"
}
```
### `SetVariableAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 175.
- Campos de configuração observados: `dictionaryKeys, dictionaryOrArrayType, existingManualKeyType, m_booleanInvert, m_darkMode, m_doubleRandomMax, m_doubleRandomMin, m_falseLabel, m_intExpression, m_intRandom, m_intRandomMax, m_intRandomMin, m_intValueDecrement, m_intValueIncrement, m_newBooleanValue, m_newDoubleValue, m_newIntValue, m_trueLabel, m_userPrompt, m_userPromptEmptyAtStart, m_userPromptPassword, m_userPromptPasswordToggle, m_userPromptShowCancel, m_userPromptStopAfterCancel, m_variable`.
```json
{
  "dictionaryKeys": [],
  "dictionaryOrArrayType": -1,
  "existingManualKeyType": 0,
  "m_booleanInvert": false,
  "m_darkMode": -1,
  "m_doubleRandomMax": 0.0,
  "m_doubleRandomMin": 0.0,
  "m_falseLabel": "Falso",
  "m_intExpression": false,
  "m_intRandom": false,
  "m_intRandomMax": 0,
  "m_intRandomMin": 0,
  "m_intValueDecrement": false,
  "m_intValueIncrement": false,
  "m_newBooleanValue": false,
  "m_newDoubleValue": 0.0,
  "m_newIntValue": 0,
  "m_trueLabel": "Verdadeiro",
  "m_userPrompt": false,
  "m_userPromptEmptyAtStart": false,
  "m_userPromptPassword": false,
  "m_userPromptPasswordToggle": false,
  "m_userPromptShowCancel": true,
  "m_userPromptStopAfterCancel": true,
  "m_variable": {
    "dictionary": {
      "entries": [],
      "isArray": false,
      "variableType": 4,
      "type": "Dictionary"
    },
    "isActionBlockWorkingVar": false,
    "isLocalVar": true,
    "isSecure": false,
    "m_booleanValue": false,
    "m_decimalValue": 0.0,
    "m_intValue": 0,
    "m_name": "teste",
    "m_stringValue": "",
    "m_type": 0,
    "supportsInput": false,
    "supportsOutput": true
  }
}
```
### `ClearVariablesAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 178.
- Campos de configuração observados: `variableNames`.
```json
{
  "variableNames": [
    "teste1",
    "teste2"
  ]
}
```
### `DeleteVariableAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 176.
- Campos de configuração observados: `variableName`.
```json
{
  "variableName": "0 entradas"
}
```
### `HttpRequestAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 111.
- Campos de configuração observados: `requestConfig`.
```json
{
  "requestConfig": {
    "allFilesAccessPath": "",
    "allowAnyCertificate": false,
    "basicAuthEnabled": false,
    "basicAuthPassword": "",
    "basicAuthUsername": "",
    "blockNextAction": false,
    "clientCertEnabled": false,
    "clientCertKeyStoreDisplayName": "",
    "clientCertKeyStoreUri": "",
    "clientCertPassword": "",
    "contentBodyDynamicFileName": "",
    "contentBodyFileDisplayName": "",
    "contentBodyFileUri": "",
    "contentBodyFolderDisplayName": "",
    "contentBodyFolderUri": "",
    "contentBodySource": 0,
    "contentBodyText": "",
    "contentType": "",
    "followRedirects": true,
    "headerParams": [
      {
        "paramName": "teste",
        "paramValue": "teste"
      }
    ],
    "localFileUri": "",
    "prettifyJson": false,
    "proxyEnabled": false,
    "proxyHost": "",
    "proxyPort": 8080,
    "proxyType": 0,
    "queryParams": [
      {
        "paramName": "teste",
        "paramValue": "teste"
      }
    ],
    "requestTimeOutSeconds": 30,
    "requestType": 0,
    "returnCodeDictionaryKeys": {
      "keys": [
        "teste"
      ]
    },
    "returnCodeVariableName": "teste1",
    "returnHeadersDictionaryKeys": {
      "keys": []
    },
    "returnHeadersVariableName": "teste1",
    "saveResponseAllFilesAccessPath": "",
    "saveResponseFileName": "",
    "saveResponseFolderPathDisplayName": "",
    "saveResponseFolderPathUri": "",
    "saveResponseType": 0,
    "saveResponseUseAllFilesAccess": false,
    "saveReturnCodeToVariable": true,
    "saveReturnHeadersToVariable": true,
    "urlToOpen": "teste",
    "useAllFilesAccess": false,
    "useLocalFileUri": false,
    "useStaticContentBodyFile": true
  }
}
```
### `ConnectivityCheckAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 67.
- Campos de configuração observados: `blockActions, site, timeout, variable`.
```json
{
  "blockActions": true,
  "site": "www.google.com",
  "timeout": 3000,
  "variable": {
    "dictionary": {
      "entries": [],
      "isArray": false,
      "variableType": 4,
      "type": "Dictionary"
    },
    "isActionBlockWorkingVar": false,
    "isLocalVar": true,
    "isSecure": false,
    "m_booleanValue": false,
    "m_decimalValue": 0.0,
    "m_intValue": 0,
    "m_name": "teste",
    "m_stringValue": "",
    "m_type": 0,
    "supportsInput": false,
    "supportsOutput": true
  }
}
```
### `LogAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 150.
- Campos de configuração observados: `logLevel, logMacro, m_logText`.
```json
{
  "logLevel": "STANDARD",
  "logMacro": true,
  "m_logText": "teste"
}
```
### `ExportLogAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 147.
- Campos de configuração observados: `displayPath, fileName, filePath, needsFileReconfiguration, pathUri, showMilliseconds, useHtmlFormat, userLog`.
```json
{
  "displayPath": "Documents/CDXMS_Solutions",
  "fileName": "teste",
  "filePath": "Documents/CDXMS_Solutions",
  "needsFileReconfiguration": false,
  "pathUri": "content://com.android.externalstorage.documents/tree/primary%3ADocuments%2FCDXMS_Solutions",
  "showMilliseconds": false,
  "useHtmlFormat": false,
  "userLog": true
}
```
### `ClearLogAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 148.
- Campos de configuração observados: `m_userLog, systemLogMode`.
```json
{
  "m_userLog": true,
  "systemLogMode": 0
}
```
### `ActionBlockAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 119.
- Campos de configuração observados: `actionBlockId, actionBlockName, continueActionsWithoutWaiting, inputDictionaryMap, inputVarsMap, outputDictionaryMap, outputVarsMap`.
```json
{
  "actionBlockId": -8974663416693308765,
  "actionBlockName": "[CDXMS] Bootstrap",
  "continueActionsWithoutWaiting": false,
  "inputDictionaryMap": {},
  "inputVarsMap": {},
  "outputDictionaryMap": {},
  "outputVarsMap": {}
}
```
### `JavaScriptAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 30.
- Campos de configuração observados: `blockNextAction, javascriptEngine, scriptText`.
```json
{
  "blockNextAction": true,
  "javascriptEngine": "JetPack JavascriptEngine",
  "scriptText": ""
}
```
### `ShellScriptAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 35.
- Campos de configuração observados: `blockNextAction, m_nonRoot, m_script, timeoutSeconds, useHelper, useShizuku`.
```json
{
  "blockNextAction": false,
  "m_nonRoot": true,
  "m_script": "teste",
  "timeoutSeconds": 600,
  "useHelper": false,
  "useShizuku": false
}
```
### `UIInteractionAction`
- Ocorrências no All_Actions: 2.
- Índice de amostra: 12.
- Campos de configuração observados: `action, uiInteractionConfiguration`.
```json
{
  "action": 0,
  "uiInteractionConfiguration": {
    "blocking": true,
    "checkOverlays": false,
    "clickOption": 0,
    "contentDescription": "",
    "longClick": false,
    "returnVariable": {
      "variableName": "teste",
      "keys": {
        "keys": []
      }
    },
    "textMatchOption": 0,
    "useRegex": false,
    "xyPercentages": false,
    "type": "Click"
  }
}
```
### `ReadScreenContentsAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 157.
- Campos de configuração observados: `dictionaryKeys, forceScreenRefresh, includeOverlays, includeScreenLocation, includeWithoutText, isLocalVar, variableName`.
```json
{
  "dictionaryKeys": {
    "keys": []
  },
  "forceScreenRefresh": true,
  "includeOverlays": true,
  "includeScreenLocation": true,
  "includeWithoutText": true,
  "isLocalVar": true,
  "variableName": "teste1"
}
```
### `ReadScreenshotContentsAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 156.
- Campos de configuração observados: `charsetOption, dictionaryKeys, includeScreenLocation, isLocalVar, variableName`.
```json
{
  "charsetOption": 0,
  "dictionaryKeys": {
    "keys": []
  },
  "includeScreenLocation": true,
  "isLocalVar": false,
  "variableName": "0 entradas"
}
```
### `OCRAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 162.
- Campos de configuração observados: `charsetOption, dictionaryKeys, fileDisplayName, flashOption, isLocalVar, option, useFrontCamera, variableName`.
```json
{
  "charsetOption": 0,
  "dictionaryKeys": {
    "keys": []
  },
  "fileDisplayName": "",
  "flashOption": 0,
  "isLocalVar": false,
  "option": 0,
  "useFrontCamera": false,
  "variableName": "0 entradas"
}
```
### `CheckTextOnScreenAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 165.
- Campos de configuração observados: `booleanVariableName, enableRegex, forceScreenRefresh, ignoreCase, ignoreHiddenText, includeOverlays, locationDictionaryKeys, locationVariableName, matchOption, textToCheck, viewIdStringVariableName`.
```json
{
  "booleanVariableName": "teste",
  "enableRegex": false,
  "forceScreenRefresh": true,
  "ignoreCase": true,
  "ignoreHiddenText": true,
  "includeOverlays": true,
  "locationDictionaryKeys": {
    "keys": []
  },
  "locationVariableName": "teste1",
  "matchOption": 0,
  "textToCheck": "teste",
  "viewIdStringVariableName": "teste2"
}
```
### `CheckTextInScreenshotAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 164.
- Campos de configuração observados: `booleanVariableName, charsetOption, enableRegex, ignoreCase, locationDictionaryKeys, locationVariableName, matchOption, textToCheck`.
```json
{
  "booleanVariableName": "teste",
  "charsetOption": 0,
  "enableRegex": false,
  "ignoreCase": true,
  "locationDictionaryKeys": {
    "keys": []
  },
  "locationVariableName": "teste1",
  "matchOption": 0,
  "textToCheck": "teste"
}
```
### `GetTextByViewIdAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 161.
- Campos de configuração observados: `booleanVariableName, enableRegex, forceScreenRefresh, ignoreCase, includeOverlays, stringVariableName, viewId`.
```json
{
  "booleanVariableName": "teste",
  "enableRegex": false,
  "forceScreenRefresh": false,
  "ignoreCase": true,
  "includeOverlays": false,
  "stringVariableName": "teste2",
  "viewId": "teste"
}
```
### `CustomSceneAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 103.
- Campos de configuração observados: `sceneDescription`.
```json
{
  "sceneDescription": {
    "itemList": {
      "items": [
        {
          "type": "SceneButton",
          "sceneButtonConfig": {
            "buttonColor": -1,
            "closeSceneOnPress": true,
            "htmlFormatting": false,
            "padding": "8",
            "text": "Botão",
            "textAlignment": "Center",
            "textColor": -13421773,
            "textSize": "20"
          },
          "guid": -6392093540271712664,
          "iconRes": 2131231211,
          "lastRefreshValue": 0
        }
      ]
    },
    "sceneConfig": {
      "backgroundColor": -13421773,
      "backgroundImageDisplayMode": "CENTER_CROP",
      "blockNextActions": true,
      "closeOnBackgroundTouch": false,
      "contentPadding": 8,
      "dismissOnBackPress": true,
      "dismissOnHomeTaskSwitch": false,
      "displayOption": {
        "type": "FullScreen",
        "nameRes": 2132021886
      },
      "foregroundColor": -1118482,
      "name": "Scene1",
      "roundedCornerAmount": 0,
      "showOnLockScreen": false,
      "updateValuesOnSceneClose": false
    }
  }
}
```
### `SelectionDialogAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 90.
- Campos de configuração observados: `bgColor, buttonStyle, continueMacroOnBackPress, customEntries, defaultButtonIndex, defaultKey, defaultTimeOutSecs, dictionaryKeys, dictionaryVarName, hasDefault, message, option, preventBackButtonClose, saveIndexVariable, saveKeyVariable, saveValueVariable, showDictionaryKeys, textColor`.
```json
{
  "bgColor": -13619152,
  "buttonStyle": 0,
  "continueMacroOnBackPress": true,
  "customEntries": [],
  "defaultButtonIndex": 0,
  "defaultKey": "",
  "defaultTimeOutSecs": 30,
  "dictionaryKeys": {
    "keys": []
  },
  "dictionaryVarName": "teste1",
  "hasDefault": false,
  "message": "teste",
  "option": 1,
  "preventBackButtonClose": false,
  "saveIndexVariable": {
    "variableName": "teste1",
    "keys": {
      "keys": [
        "teste"
      ]
    }
  },
  "saveKeyVariable": {
    "variableName": "teste2",
    "keys": {
      "keys": []
    }
  },
  "saveValueVariable": {
    "variableName": "teste2",
    "keys": {
      "keys": []
    }
  },
  "showDictionaryKeys": false,
  "textColor": -1118482
}
```
### `OptionDialogAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 89.
- Campos de configuração observados: `actionBlockData, blockNextAction, continueOnBackPress, m_actionMacroGuids, m_buttonNames, m_defaultButton, m_defaultTimeOutSecs, m_message, m_title, preventBackButtonClosing`.
```json
{
  "actionBlockData": [
    {
      "actionBlockGuid": -8974663416693308765,
      "actionBlockName": "[CDXMS] Bootstrap",
      "inputDictionaryMap": {},
      "inputVarsMap": {
        "Requested Artifact Type": "teste",
        "Requested Artifact Id": "teste",
        "Operation": "twste",
        "Config Json": "tws"
      },
      "outputDictionaryMap": {},
      "outputVarsMap": {}
    },
    null,
    null
  ],
  "blockNextAction": true,
  "continueOnBackPress": false,
  "m_actionMacroGuids": [
    -8974663416693308765,
    0,
    0
  ],
  "m_buttonNames": [
    "tssre",
    "",
    ""
  ],
  "m_defaultButton": 1,
  "m_defaultTimeOutSecs": 30,
  "m_message": "Escolher uma opção entre valores abaixo.",
  "m_title": "Selecione uma opção",
  "preventBackButtonClosing": false
}
```
### `MessageDialogAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 135.
- Campos de configuração observados: `autoExpand, blockNextAction, dimBackground, disableHtml, displayOverStatusBar, hasSetColors, iconText, iconType, liveNotification, m_backgroundColor, m_iconBgColor, m_imageResourceId, m_macroGUIDToRun, m_notificationChannelType, m_notificationSubject, m_notificationText, m_overwriteExisting, m_priority, m_ringtoneIndex, m_ringtoneName, m_runMacroWhenPressed, m_secondaryClassType, m_textColor, maintainSpaces, notificationActionButtons, notificationChannelName, notificationIdString, notificatonId, preventAndroid16Grouping, preventBackButtonClosing, preventRemovalByBin, showAsOverlayOption, yPosition`.
```json
{
  "hasSetColors": true,
  "m_secondaryClassType": "MessageDialogAction",
  "autoExpand": true,
  "blockNextAction": false,
  "dimBackground": true,
  "disableHtml": false,
  "displayOverStatusBar": false,
  "iconText": "",
  "iconType": 0,
  "liveNotification": false,
  "m_backgroundColor": -13421773,
  "m_iconBgColor": -769226,
  "m_imageResourceId": 0,
  "m_macroGUIDToRun": 0,
  "m_notificationChannelType": 0,
  "m_notificationSubject": "teste",
  "m_notificationText": "teste",
  "m_overwriteExisting": false,
  "m_priority": 0,
  "m_ringtoneIndex": 0,
  "m_ringtoneName": "Padrão",
  "m_runMacroWhenPressed": false,
  "m_textColor": -1118482,
  "maintainSpaces": false,
  "notificationActionButtons": [],
  "notificationChannelName": "Ação de notificação",
  "notificationIdString": "0",
  "notificatonId": 0,
  "preventAndroid16Grouping": false,
  "preventBackButtonClosing": false,
  "preventRemovalByBin": false,
  "showAsOverlayOption": 1,
  "yPosition": 0.5
}
```
### `OverlayDialogAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 87.
- Campos de configuração observados: `autoExpand, blockNextAction, dimBackground, disableHtml, displayOverStatusBar, iconText, iconType, liveNotification, m_backgroundColor, m_iconBgColor, m_imageResourceId, m_macroGUIDToRun, m_notificationChannelType, m_notificationSubject, m_notificationText, m_overwriteExisting, m_priority, m_ringtoneIndex, m_ringtoneName, m_runMacroWhenPressed, m_secondaryClassType, m_textColor, maintainSpaces, notificationActionButtons, notificationChannelName, notificationIdString, notificatonId, preventAndroid16Grouping, preventBackButtonClosing, preventRemovalByBin, showAsOverlayOption, yPosition`.
```json
{
  "m_secondaryClassType": "OverlayDialogAction",
  "autoExpand": true,
  "blockNextAction": false,
  "dimBackground": true,
  "disableHtml": false,
  "displayOverStatusBar": true,
  "iconText": "",
  "iconType": 0,
  "liveNotification": false,
  "m_backgroundColor": -587202560,
  "m_iconBgColor": -769226,
  "m_imageResourceId": 0,
  "m_macroGUIDToRun": 0,
  "m_notificationChannelType": 0,
  "m_notificationSubject": "teste",
  "m_notificationText": "teste",
  "m_overwriteExisting": false,
  "m_priority": 0,
  "m_ringtoneIndex": 0,
  "m_ringtoneName": "Padrão",
  "m_runMacroWhenPressed": false,
  "m_textColor": -1,
  "maintainSpaces": false,
  "notificationActionButtons": [
    {
      "clearOnPress": true,
      "label": "teste",
      "macroGuid": 0
    }
  ],
  "notificationChannelName": "Ação de notificação",
  "notificationIdString": "0",
  "notificatonId": 0,
  "preventAndroid16Grouping": false,
  "preventBackButtonClosing": false,
  "preventRemovalByBin": true,
  "showAsOverlayOption": 1,
  "yPosition": 0.5
}
```
### `ToastAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 140.
- Campos de configuração observados: `cancelPrevious, m_backgroundColor, m_displayIcon, m_duration, m_horizontalPosition, m_imageName, m_imagePackageName, m_imageResourceName, m_messageText, m_position, m_textColor, m_tintIcon, maintainSpaces, useTextOnly`.
```json
{
  "cancelPrevious": true,
  "m_backgroundColor": -14606047,
  "m_displayIcon": true,
  "m_duration": 0,
  "m_horizontalPosition": 0,
  "m_imageName": "launcher_no_border",
  "m_imagePackageName": "com.arlosoft.macrodroid",
  "m_imageResourceName": "launcher_no_border",
  "m_messageText": "teste",
  "m_position": 0,
  "m_textColor": -1,
  "m_tintIcon": false,
  "maintainSpaces": true,
  "useTextOnly": false
}
```
### `PauseAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 117.
- Campos de configuração observados: `m_delayInMilliSeconds, m_delayInSeconds, m_useAlarm, unitForVariables`.
```json
{
  "m_delayInMilliSeconds": 0,
  "m_delayInSeconds": 1,
  "m_useAlarm": true,
  "unitForVariables": 0
}
```
### `LoopAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 59.
- Campos de configuração observados: `childrenCollapsed, dontLogIfConditionIsFalse, m_fixedOptionCount, m_option, timedDurationValue, timedTimeUnit`.
```json
{
  "m_fixedOptionCount": 1,
  "m_option": 2,
  "timedDurationValue": 1,
  "timedTimeUnit": 0,
  "childrenCollapsed": false,
  "dontLogIfConditionIsFalse": false
}
```
### `IfConditionAction`
- Ocorrências no All_Actions: 1.
- Índice de amostra: 51.
- Campos de configuração observados: `childrenCollapsed, dontLogIfConditionIsFalse`.
```json
{
  "childrenCollapsed": false,
  "dontLogIfConditionIsFalse": true
}
```
### `ExitActionBlockAction`
- Ocorrências no All_Actions: 2.
- Índice de amostra: 124.
- Campos de configuração observados: `outputOption`.
```json
{
  "outputOption": 0
}
```

## Catálogo completo por classe de ação
| Classe | Ocorrências | Campos específicos observados | Índice de amostra |
|---|---:|---|---:|
| `ActionBlockAction` | 1 | actionBlockId, actionBlockName, continueActionsWithoutWaiting, inputDictionaryMap, inputVarsMap, outputDictionaryMap, outputVarsMap | 119 |
| `ActionGroupAction` | 1 | actionGroupName, childrenCollapsed, dontLogIfConditionIsFalse | 99 |
| `ActionGroupEndAction` | 1 | — | 100 |
| `AddCalendarEntryAction` | 1 | enableNotification, m_allDayEvent, m_availability, m_calendarId, m_detail, m_durationValue, m_fixedDay, m_fixedDays, m_fixedHour, m_fixedHourText, m_fixedMinute, m_fixedMinuteText, m_fixedMonth, m_fixedMonths, m_fixedTime, m_fixedYear, m_relativeDays, m_relativeHours, m_relativeMinutes, m_timeUnitForVariable, m_title, m_useFixedDate, m_useVariableTimeInFuture, notificationMinutesBefore | 146 |
| `AndroidShortcutsAction` | 5 | m_option | 20 |
| `AndroidWearAction` | 3 | m_actionEnabledStates, m_actionIcons, m_actionMacroGuids, m_actionNames, m_brightness, m_notificationSubject, m_notificationText, m_option, m_vibratePattern, m_wifiOption | 63 |
| `AnimationOverlayAction` | 1 | animName, animationType, drawOverSystemApps, height, hideOnClick, hideOnLongClick, ignoreCache, isClearAnimation, longClickMacroGuidToRun, longClickMacroNameToRun, macroGuidToRun, macroNameToRun, opacity, optionValue, selectedAnimation, selectedAnimationId, showOption, useAllFilesAccessGif, width, xPosition, yPosition | 144 |
| `AnswerCallAction` | 1 | m_selectedIndex | 167 |
| `ArrayManipulationAction` | 1 | endIndex, inputArrayKeys, inputArrayVarName, numericalExpressionFilterText, option, outputArrayKeys, outputArrayVarName, startIndex, stringFilterIgnoreCase, stringFilterOption, stringFilterRegex, stringFilterText | 181 |
| `AuthenticateUserAction` | 1 | dictionaryKeys, option, preventPasswordPin, subtitle, title, variableName | 1 |
| `BlockTouchesAction` | 1 | bgColor, height, option, showBlockedArea, useAccessibilityService, width, xPosition, yPosition | 151 |
| `BreakFromLoopAction` | 1 | — | 58 |
| `BubbleNotificationAction` | 1 | autoExpand, blockNextAction, dimBackground, disableHtml, displayOverStatusBar, iconText, iconType, liveNotification, m_backgroundColor, m_iconBgColor, m_imageResourceId, m_macroGUIDToRun, m_notificationChannelType, m_notificationSubject, m_notificationText, m_overwriteExisting, m_priority, m_ringtoneIndex, m_ringtoneName, m_runMacroWhenPressed, m_secondaryClassType, m_textColor, maintainSpaces, notificationActionButtons, notificationChannelName, notificationIdString, notificatonId, preventAndroid16Grouping, preventBackButtonClosing, preventRemovalByBin, showAsOverlayOption, yPosition | 137 |
| `CameraFlashLightAction` | 1 | brightnessPercent, m_launchForeground, m_state, supportsBrightness | 14 |
| `CameraNotificationCircleAction` | 1 | alpha, circleHeightDp, circleWidthDp, colors, drawOverSystemApps, featherEffect, horizontalPositionPercent, option, thicknessDp, timeoutSeconds, verticalPositionPercent | 133 |
| `CancelActiveMacroAction` | 1 | getByName, m_GUID, m_macroName | 120 |
| `CaptureNextClickXYAction` | 2 | dictionaryKeys, passThroughClick, variableName | 2 |
| `CarModeAction` | 1 | m_option | 79 |
| `CheckPixelColorAction` | 1 | booleanResultVarName, dictionaryOutVarKeys, dictionaryOutVarName, usePercentForLocation, xLocation, yLocation | 163 |
| `CheckTextInScreenshotAction` | 1 | booleanVariableName, charsetOption, enableRegex, ignoreCase, locationDictionaryKeys, locationVariableName, matchOption, textToCheck | 164 |
| `CheckTextOnScreenAction` | 1 | booleanVariableName, enableRegex, forceScreenRefresh, ignoreCase, ignoreHiddenText, includeOverlays, locationDictionaryKeys, locationVariableName, matchOption, textToCheck, viewIdStringVariableName | 165 |
| `ClearCallLogAction` | 1 | m_nonContact, m_specificContact, m_type, usePhoneNumber, useRegex | 171 |
| `ClearDialogAction` | 1 | — | 101 |
| `ClearDictionaryArrayEntryAction` | 1 | clearOption, dictionaryKeys, isAllEntries, variableName | 177 |
| `ClearLogAction` | 1 | m_userLog, systemLogMode | 148 |
| `ClearNotificationsAction` | 1 | enableRegex, ignoreCase, m_ageInSeconds, m_applicationNameList, m_clearPersistent, m_excludes, m_matchOption, m_matchText, m_option, m_packageNameList, matchOptionMessage, matchOptionTitle, separateTitleAndMessage | 141 |
| `ClearVariablesAction` | 1 | variableNames | 178 |
| `ClipboardAction` | 1 | m_clipboardText | 17 |
| `ConfigureWidgetButtonAction` | 1 | iconTintEnabled, m_faded, m_iconText, m_imagePackageName, m_imageResourceName, m_macroId, m_triggerGUID, m_widgetLabel, tintColor | 102 |
| `ConfirmNextAction` | 1 | cancelAfterTimeout, m_message, m_title, negativeText, positiveText, timeoutSeconds | 53 |
| `ConnectivityCheckAction` | 1 | blockActions, site, timeout, variable | 67 |
| `ContactViaAppAction` | 1 | appName, appPackage, contact, id, mimeType | 168 |
| `ContinueLoopAction` | 1 | — | 54 |
| `ControlMediaAction` | 1 | m_option, m_sendMediaPlayerCommands, m_simulateMediaButton, optionInt | 129 |
| `CreateChartAction` | 1 | backgroundColor, blockNextActions, chartHeight, chartTitle, chartType, chartWidth, customBarColors, displayMode, foregroundColor, lineMode, linePointColor, maxYAxisValue, minYAxisValue, startXAxisAtZero, startYAxisAtZero, useCustomBarColors, useFixedYAxisRange, variableName, xAxisLabel, xAxisLabelRotation, yAxisLabel | 37 |
| `CustomSceneAction` | 1 | sceneDescription | 103 |
| `DeleteMacroAction` | 1 | m_GUID, m_macroName, matchOption | 122 |
| `DeleteVariableAction` | 1 | variableName | 176 |
| `DimScreenAction` | 1 | m_dimScreenOn, m_percent, overlayStatusBar | 154 |
| `DisableCategoryAction` | 1 | categoriesList, enableMacrosOption, m_enable, m_state | 84 |
| `DisableMacroAction` | 1 | getByName, m_GUID, m_enable, m_macroName, m_state, m_userPromptTitle | 118 |
| `DisableMacroDroidAction` | 1 | state | 97 |
| `DisableTriggerAction` | 1 | enableOption, macroGuid, macroName, triggerGuid, triggerName | 85 |
| `EdgeLightingAction` | 1 | alpha, borderWidthDps, color1, color2, colors, cornerRadius, drawOverSystemApps, featherEffect, option, timeoutSeconds | 139 |
| `EmptyAction` | 1 | — | 86 |
| `EncryptDecryptTextAction` | 1 | option, outputVariableName, password, sourceText, successVariableName | 174 |
| `EndIfAction` | 2 | — | 52 |
| `EndLoopAction` | 2 | — | 57 |
| `ExitActionBlockAction` | 2 | outputOption | 124 |
| `ExpandCollapseStatusBarAction` | 2 | m_option | 9 |
| `ExportLogAction` | 1 | displayPath, fileName, filePath, needsFileReconfiguration, pathUri, showMilliseconds, useHtmlFormat, userLog | 147 |
| `ExportMacrosAction` | 1 | allFilesPath, encryptOutput, encryptionPassword, m_fileName, needsFileReconfiguration, option, useAllFilesAccess | 98 |
| `FileOperationAllFilesAction` | 1 | fileExtensions, fileOption, filePattern, fromPath, listFilesOutputType, listFilesSortAscending, listFilesSortBy, option, toPath, waitToComplete | 45 |
| `FileOperationV21Action` | 5 | listFilesDictionaryKeys, listFilesOutputType, listFilesSortAscending, listFilesSortBy, listFilesVariableName, m_fileExtensions, m_fileOption, m_filePattern, m_folderName, m_fromName, m_fromUriString, m_option, m_toName, m_toUriString, waitToComplete | 39 |
| `FloatingButtonConfigureAction` | 1 | alpha, drawOverSystemApps, enableOption, fixedLocation, iconBgColor, iconText, iconTextColor, iconTintColor, iconTintEnabled, iconType, identifier, imageResourceId, isInitialised, macroGuid, macroName, padding, preventRemoveByDrag, size, transparentBackground, triggerGuid, updateLocation, usePercentForLocation, xLocation, yLocation | 91 |
| `FloatingTextAction` | 1 | alignment, alpha, autoHideAfterDelay, autoHideSeconds, bgColor, corners, drawOverSystemApps, enableShadow, forceFullScreen, hideOnClick, hideOnLongClick, htmlFormattingEnabled, identifier, isInitialised, longClickMacroGuidToRun, longClickMacroNameToRun, macroGuidToRun, macroNameToRun, moveOption, option, padding, preventRemoveByDrag, shadowColor, showOverStatusBar, singleLineScrollingEnabled, textColor, textSize, textToDisplay, updateLocation, updateVariableOnMove, variableWidth, vibrateOnClick, widthPercentage, xPosition, yPosition | 106 |
| `FontScaleAction` | 1 | scalePercent | 77 |
| `ForceLocationUpdateAction` | 1 | blockNextAction, dictionaryVarDictionaryKeys, dictionaryVariableName, timeoutSeconds | 116 |
| `ForceMacroRunAction` | 1 | getByName, isCategoryLocked, m_GUID, m_category, m_ignoreConstraints, m_macroName, m_useOffStatus, m_userPromptTitle, m_waitToComplete | 123 |
| `ForceScreenRotationAction` | 1 | m_option | 155 |
| `GenerateQRCodeAction` | 1 | displayMode, fullScreenMode, qrText, themeMode | 49 |
| `GetCalendarEventsAction` | 1 | calendarId, calendarName, durationUnit, durationValue, outputDictionaryVarName, startOffsetUnit, startOffsetValue | 149 |
| `GetContactsAction` | 1 | dictionaryKeys, dictionaryVarName, makeVariableSecure | 172 |
| `GetDataUsedAction` | 1 | billingDay, calendarScope, networkType, periodKind, rollingAmount, rollingUnitMinutes, unit, varDictionaryKeys, variableName | 71 |
| `GetInstalledAppsAction` | 1 | dictionaryKeys, dictionaryVarName, extendedDetail, includeNonLaunchable | 34 |
| `GetLightLevelAction` | 1 | varDictionaryKeys, variableName | 15 |
| `GetTextByViewIdAction` | 1 | booleanVariableName, enableRegex, forceScreenRefresh, ignoreCase, includeOverlays, stringVariableName, viewId | 161 |
| `GotoAction` | 1 | targetLabel | 55 |
| `HideSceneAction` | 1 | enableRegex, ignoreCase, matchOption, sceneNameToMatch | 104 |
| `HttpRequestAction` | 1 | requestConfig | 111 |
| `HttpServerResponseAction` | 2 | headerParams, htmlText, option, responseCode, text | 112 |
| `IfConditionAction` | 1 | childrenCollapsed, dontLogIfConditionIsFalse | 51 |
| `IfConfirmedThenAction` | 1 | cancelAfterTimeout, childrenCollapsed, dontLogIfConditionIsFalse, negativeText, positiveText, quitOnBackPressed, text, timeoutSeconds, title | 61 |
| `InputKeyEventAction` | 1 | keyCode, keyPressOption, modifierMask | 8 |
| `IterateDictionaryAction` | 1 | childrenCollapsed, dictionaryKeys, dontLogIfConditionIsFalse, isArray, m_fixedOptionCount, m_option, timedDurationValue, timedTimeUnit, variableName | 56 |
| `JavaAction` | 1 | blockNextAction, runInBackgroundThread, scriptText | 29 |
| `JavaScriptAction` | 1 | blockNextAction, javascriptEngine, scriptText | 30 |
| `JsonOutputAction` | 1 | dictionaryKeys, dictionaryVarName, stringVarName | 110 |
| `JsonParseAction` | 1 | dictionaryKeys, dictionaryVarName, stringVarName | 109 |
| `KeepAwakeAction` | 1 | m_enabled, m_permanent, m_screenOption, m_secondsToStayAwakeFor | 160 |
| `KillBackgroundAppAction` | 1 | m_applicationNameList, m_packageNameList, option | 31 |
| `LaunchActivityAction` | 1 | m_applicationName, m_excludeFromRecents, m_packageToLaunch, m_startNew, option | 27 |
| `LaunchAppActivityAction` | 1 | activityName, activityToLaunch, applicationName, forceNew, packageToLaunch | 33 |
| `LaunchHomeScreenAction` | 1 | — | 0 |
| `LaunchShortcutAction` | 1 | m_appName, m_intentEncoded, m_name | 32 |
| `LogAction` | 1 | logLevel, logMacro, m_logText | 150 |
| `LoopAction` | 1 | childrenCollapsed, dontLogIfConditionIsFalse, m_fixedOptionCount, m_option, timedDurationValue, timedTimeUnit | 59 |
| `MacroDroidDrawerAction` | 1 | drawerType, m_option, swipeAreaColour, swipeAreaHeight, swipeAreaOpacity, swipeAreaOption, swipeAreaVerticalOffset, swipeAreaVisibleWidth, swipeAreaWidth | 88 |
| `MacroDroidNotificationTextAction` | 1 | body, showCustom, title | 94 |
| `MacroDroidSettingAction` | 1 | m_activityRecognitionUpdateRate, m_audioStreamSecondaryOption, m_booleanSecondayOption, m_cellTowerUpdateRate, m_lightSensorBgOption, m_notificationPriorityOption, m_option, m_wifiScanRate | 92 |
| `MakeCallAction` | 1 | m_contact, slotId | 170 |
| `MessageDialogAction` | 1 | autoExpand, blockNextAction, dimBackground, disableHtml, displayOverStatusBar, hasSetColors, iconText, iconType, liveNotification, m_backgroundColor, m_iconBgColor, m_imageResourceId, m_macroGUIDToRun, m_notificationChannelType, m_notificationSubject, m_notificationText, m_overwriteExisting, m_priority, m_ringtoneIndex, m_ringtoneName, m_runMacroWhenPressed, m_secondaryClassType, m_textColor, maintainSpaces, notificationActionButtons, notificationChannelName, notificationIdString, notificatonId, preventAndroid16Grouping, preventBackButtonClosing, preventRemovalByBin, showAsOverlayOption, yPosition | 135 |
| `NotificationAction` | 1 | actionBlockData, autoExpand, blockNextAction, dimBackground, disableHtml, displayOverStatusBar, group, iconText, iconType, liveNotification, m_backgroundColor, m_iconBgColor, m_imageResourceId, m_macroGUIDToRun, m_notificationChannelType, m_notificationSubject, m_notificationText, m_overwriteExisting, m_priority, m_ringtoneIndex, m_ringtoneName, m_runMacroWhenPressed, m_textColor, macroNameToRun, maintainSpaces, notificationActionButtons, notificationChannelName, notificationIdString, notificatonId, preventAndroid16Grouping, preventBackButtonClosing, preventRemovalByBin, shortCriticalText, showAsOverlayOption, yPosition | 136 |
| `NotificationInteractionAction` | 1 | actionsOption, applicationName, enableRegex, excludesApps, ignoreCase, matchOption, matchOptionMessage, matchOptionTitle, matchText, messageContent, packageName, separateTitleAndMessage, titleContent, useNotificationTrigger | 138 |
| `NotificationReplyAction` | 1 | applicationName, enableRegex, ignoreCase, matchOption, matchText, packageName, replyText, useNotificationTrigger | 142 |
| `OCRAction` | 1 | charsetOption, dictionaryKeys, fileDisplayName, flashOption, isLocalVar, option, useFrontCamera, variableName | 162 |
| `OpenCallLogAction` | 1 | — | 166 |
| `OpenFileAction` | 1 | allFilesAccessPath, m_appName, m_className, m_packageName, useAllFilesAccess, useStaticFilename, useUri | 36 |
| `OpenLastPhotoAction` | 1 | appName, packageName | 46 |
| `OpenMacroDroidLogAction` | 1 | m_logType | 145 |
| `OpenWebPageAction` | 1 | allowAnyCertificate, blockNextAction, m_disableUrlEncode, m_httpGet, m_urlToOpen, m_variableSuccessResponse, m_variableToSaveResponse | 28 |
| `OptionDialogAction` | 1 | actionBlockData, blockNextAction, continueOnBackPress, m_actionMacroGuids, m_buttonNames, m_defaultButton, m_defaultTimeOutSecs, m_message, m_title, preventBackButtonClosing | 89 |
| `OverlayDialogAction` | 1 | autoExpand, blockNextAction, dimBackground, disableHtml, displayOverStatusBar, iconText, iconType, liveNotification, m_backgroundColor, m_iconBgColor, m_imageResourceId, m_macroGUIDToRun, m_notificationChannelType, m_notificationSubject, m_notificationText, m_overwriteExisting, m_priority, m_ringtoneIndex, m_ringtoneName, m_runMacroWhenPressed, m_secondaryClassType, m_textColor, maintainSpaces, notificationActionButtons, notificationChannelName, notificationIdString, notificatonId, preventAndroid16Grouping, preventBackButtonClosing, preventRemovalByBin, showAsOverlayOption, yPosition | 87 |
| `PauseAction` | 1 | m_delayInMilliSeconds, m_delayInSeconds, m_useAlarm, unitForVariables | 117 |
| `PinUnlockAction` | 1 | digitClickDelay, pinNumber, swipeUpDelay | 5 |
| `PlaySoundAction` | 1 | audioStream, m_selectedIndex, specifyAudioStream, staticFilename, useAllFilesAccess, waitToFinish | 132 |
| `PressBackAction` | 1 | — | 18 |
| `ReadFileAction` | 1 | allFilesAccessPath, dictionaryKeys, staticFilename, useAllFilesAccess, variableName | 44 |
| `ReadQRCodeAction` | 1 | fileDisplayName, flashOption, isLocalVar, option, useAllFilesAccess, useFrontCamera, variableName | 158 |
| `ReadScreenContentsAction` | 1 | dictionaryKeys, forceScreenRefresh, includeOverlays, includeScreenLocation, includeWithoutText, isLocalVar, variableName | 157 |
| `ReadScreenshotContentsAction` | 1 | charsetOption, dictionaryKeys, includeScreenLocation, isLocalVar, variableName | 156 |
| `RecordMicrophoneAction` | 1 | allFilesPath, audioBitRate, audioSamplingRate, m_recordTimeString, m_recordingFormat, m_secondsToRecordFor, source, useAllFilesAccess | 131 |
| `RecordVideoAction` | 1 | allFilesPath, blockNextAction, duration, option, recordUntilStopped, rotationOverride, selectedCamera, selectedQuality, timeUnit, useAllFilesAccess | 130 |
| `RejectCallAction` | 1 | — | 173 |
| `RestoreNotificationsAction` | 1 | m_applicationNameList, m_excludes, m_option, m_packageNameList | 143 |
| `SamsungRoutinesAction` | 1 | actionMode, endPreviousBeforeStart, routineName, routineUuid | 25 |
| `SayTimeAction` | 1 | m_12Hour | 83 |
| `ScreenOnAction` | 1 | m_pieLockScreen, m_screenOff, m_screenOffNoLock, m_screenOnAlternative | 159 |
| `SelectionDialogAction` | 1 | bgColor, buttonStyle, continueMacroOnBackPress, customEntries, defaultButtonIndex, defaultKey, defaultTimeOutSecs, dictionaryKeys, dictionaryVarName, hasDefault, message, option, preventBackButtonClose, saveIndexVariable, saveKeyVariable, saveValueVariable, showDictionaryKeys, textColor | 90 |
| `SendEmailAction` | 1 | blockNextAction, m_attachLog, m_attachUserLog, m_body, m_emailAddress, m_fromEmailAddress, m_subject, sendOption, useHtml, useHtmlForLogs, userLogChannelsList, variable | 127 |
| `SendIntentAction` | 1 | EXTRA_TYPE_AUTO, EXTRA_TYPE_BOOLEAN, EXTRA_TYPE_DOUBLE, EXTRA_TYPE_FLOAT, EXTRA_TYPE_INT, EXTRA_TYPE_LONG, EXTRA_TYPE_STRING, EXTRA_TYPE_STRING_ARRAY, m_action, m_category, m_className, m_data, m_extra1Name, m_extra1Type, m_extra1Value, m_extra2Name, m_extra2Type, m_extra2Value, m_extra3Name, m_extra3Type, m_extra3Value, m_extra4Name, m_extra4Type, m_extra4Value, m_extra5Name, m_extra5Type, m_extra5Value, m_extra6Name, m_extra6Type, m_extra6Value, m_flags, m_mimeType, m_packageName, m_target, useCustomCategory | 7 |
| `SendSMSAction` | 1 | m_addToMessageLog, m_contact, m_messageContent, m_number, m_prePopulate, m_simId | 126 |
| `SetAirplaneModeAction` | 1 | configComplete, m_keepBluetoothOn, m_keepWifiOn, m_state, mechanismOption | 66 |
| `SetAlarmClockAction` | 1 | m_dayOption, m_daysOfWeek, m_delayInHours, m_delayInMinutes, m_hour, m_label, m_minute, m_oneOff, m_option, m_relative | 82 |
| `SetAutoRotateAction` | 1 | m_state | 78 |
| `SetAutoSyncAction` | 1 | m_selectAccounts, m_state | 70 |
| `SetBrightnessAction` | 1 | autoBrightnessOn, forceValue, forceValueEnabled, m_brightness, m_brightnessPercent, m_forcePieMode, migrated, setAutoBrightness, setBrightnessValue | 152 |
| `SetHotspotAction` | 1 | a16PlusMechanism, state, turnWifiOn, useLegacyMechanism | 69 |
| `SetKeyboardAction` | 1 | — | 80 |
| `SetKeyguardAction` | 1 | m_keyguardOn | 74 |
| `SetLocationUpdateRateAction` | 1 | m_updateRate, m_updateRateSeconds | 115 |
| `SetMacroDroidIconAction` | 1 | iconText, iconType, imagePackageName, m_imageResourceName | 95 |
| `SetModeAction` | 1 | blockNextAction, m_mode | 93 |
| `SetNotificationBarIconAction` | 1 | buttonId, buttonNumber, imageId | 96 |
| `SetNotificationSoundAction` | 1 | m_ringtoneUri | 134 |
| `SetPriorityMode` | 1 | m_option | 185 |
| `SetQuickSettingsStateAction` | 1 | iconRes, iconResName, label, m_tileOption, m_toggleOption, setImage, setLabel, setSubtitle, setToggleState, subtitle | 73 |
| `SetRingtoneAction` | 1 | m_ringtoneUri | 169 |
| `SetScreenTimeoutAction` | 1 | m_customValueDelay, m_timeUnit, m_timeoutDelay, m_timeoutDelayString, m_valueType | 153 |
| `SetVariableAction` | 1 | dictionaryKeys, dictionaryOrArrayType, existingManualKeyType, m_booleanInvert, m_darkMode, m_doubleRandomMax, m_doubleRandomMin, m_falseLabel, m_intExpression, m_intRandom, m_intRandomMax, m_intRandomMin, m_intValueDecrement, m_intValueIncrement, m_newBooleanValue, m_newDoubleValue, m_newIntValue, m_trueLabel, m_userPrompt, m_userPromptEmptyAtStart, m_userPromptPassword, m_userPromptPasswordToggle, m_userPromptShowCancel, m_userPromptStopAfterCancel, m_variable | 175 |
| `SetVibrateAction` | 1 | m_option, m_optionInt | 188 |
| `SetVolumeAction` | 1 | m_forceVibrateOff, m_streamIndexArray, m_streamVolumeArray, m_variables, m_volume, setInForeground, varDictionaryKeys | 182 |
| `SetWallpaperAction` | 1 | localFileUri, m_option, m_screenOption, optimiseImage, useDynamicFileName, useUri | 76 |
| `ShareLocationAction` | 1 | m_email, m_oldVariableFormat, m_outputChannel, m_simId, m_variable, useSmtpEmail | 114 |
| `ShareTextAction` | 1 | m_appName, m_className, m_packageName, textToShare | 4 |
| `ShellScriptAction` | 1 | blockNextAction, m_nonRoot, m_script, timeoutSeconds, useHelper, useShizuku | 35 |
| `ShowVolumePopupAction` | 1 | audioStream | 186 |
| `SilentModeVibrateOffAction` | 1 | mechanism, option | 187 |
| `SpeakTextAction` | 1 | m_audioStream, m_pitch, m_queue, m_readNumbersIndividually, m_skipEmojis, m_specifyAudioStream, m_speed, m_textToSay, m_waitToFinish | 11 |
| `SpeakerPhoneAction` | 1 | m_state | 183 |
| `StopWatchAction` | 1 | m_option, m_stopwatchName | 81 |
| `SummariseMacrosAction` | 1 | dictionaryKeys, includeVariables, isLocalVar, option, variableName, variablesOption | 105 |
| `SystemSettingAction` | 1 | settingString, tableOption, useHelper, valueString, valueType | 75 |
| `TakePictureAction` | 1 | actionLabel, applyAutoFocus, m_comment, m_flashOption, m_showIcon, m_useFrontCamera, pathName, pathUri, useAllFilesAccess | 50 |
| `TakeScreenshotAction` | 1 | emailSubject, m_mechanismOption, m_option, saveToJpeg, screenshotFormat, uiOption, useSmtpEmail | 47 |
| `TerminateRunningAction` | 1 | — | 121 |
| `TextManipulationAction` | 2 | m_option, m_text, m_textManipulation, varDictionaryKeys, variableName | 179 |
| `ToastAction` | 1 | cancelPrevious, m_backgroundColor, m_displayIcon, m_duration, m_horizontalPosition, m_imageName, m_imagePackageName, m_imageResourceName, m_messageText, m_position, m_textColor, m_tintIcon, maintainSpaces, useTextOnly | 140 |
| `TranslateTextAction` | 1 | dictionaryKeys, option, outputLanguageCode, sourceLanguageCode, text, variableName | 107 |
| `UDPCommandAction` | 1 | m_destination, m_message, m_port | 108 |
| `UIInteractionAction` | 2 | action, uiInteractionConfiguration | 12 |
| `UpdateClipboardAction` | 1 | — | 19 |
| `UploadPhotoAction` | 1 | emailBody, emailFrom, emailSubject, m_email, m_option, useHtml, useSmtpEmail | 48 |
| `VibrateAction` | 1 | m_vibratePattern, waitToFinish | 26 |
| `VoiceInputAction` | 1 | dictionaryKeys, variableName | 6 |
| `VoiceSearchAction` | 1 | — | 16 |
| `VolumeIncrementDecrementAction` | 1 | m_volumeUp | 184 |
| `WearOsComplicationAction` | 1 | complicationType, imagePackageName, imageResourceId, imageResourceName, maxValue, minValue, setIcon, textContent, value | 68 |
| `WhatsAppAction` | 1 | exitAppAfter, isBusiness, messageText, number, prepopulateOnly, sendButtonPressDelayMs | 128 |
| `WifiSSIDScanAction` | 1 | dictionaryKeys, groupBy, isLocalVar, variableName | 72 |
| `WriteToFileAction` | 1 | allFilesPath, m_append, m_filename, m_logText, m_prepend, overwrite, useAllFilesAccess | 38 |
