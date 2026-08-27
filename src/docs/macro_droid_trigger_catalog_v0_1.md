# CDXMS — Catálogo de Estruturas de Gatilhos MacroDroid v0.1

## Escopo

Catálogo estrutural extraído de `All_triggers.macro`, editado em `2026-08-26T23:54:02.369000+00:00`, no contexto do MacroDroid `5.67.x`.

- instâncias analisadas: **144**;
- classes nativas únicas: **118**;
- cobertura: parcial; o arquivo-fonte não contém necessariamente todos os gatilhos da versão.

Este catálogo registra a forma serializada observada. Ele não substitui a documentação do MacroDroid nem autoriza gerar exports sem homologação no aplicativo.

## Regras de uso no CDXMS

1. Preferir gatilho nativo antes de polling, UI Interaction ou loop permanente.
2. Confirmar disponibilidade e permissões na versão/dispositivo alvo.
3. Documentar debounce, duplicação, timeout e retomada após reboot quando aplicáveis.
4. Tratar valores recebidos como entrada não confiável, especialmente Intents, webhooks, notificações e conteúdo de tela.
5. Usar constraints no ponto mais próximo do gatilho sem duplicar validações de domínio.

## Inventário estrutural

| Classe interna | Instâncias | Parâmetros específicos observados |
|---|---:|---|
| `AccessibilityServiceStateTrigger` | 1 | `idList`, `nameList`, `option` |
| `ActivityRecognitionTrigger` | 2 | `lessThan`, `m_confidenceLevel`, `m_selectedIndex` |
| `AirplaneModeTrigger` | 1 | `m_airplaneModeEnabled` |
| `AndroidWearTrigger` | 1 | `iconBgColor`, `m_option` |
| `AppActivityLaunchedTrigger` | 1 | `activityNameToMatch`, `enableRegex`, `ignoreCase`, `launched`, `matchOption` |
| `AppEnabledTrigger` | 1 | `applicationNameList`, `applicationOption`, `option`, `packageNameList` |
| `ApplicationInstalledRemovedTrigger` | 1 | `m_applicationNameList`, `m_applicationOption`, `m_installed`, `m_packageNameList`, `m_updated` |
| `ApplicationLaunchedTrigger` | 2 | `excludeMode`, `isAllApps`, `m_applicationNameList`, `m_launched`, `m_packageNameList`, `usePackageNameOption` |
| `AssistantActivatedTrigger` | 1 | `option` |
| `AutoRotateChangeTrigger` | 1 | `m_option` |
| `AutoSyncChangeTrigger` | 1 | `m_option` |
| `BatteryLevelTrigger` | 2 | `m_batteryLevel`, `m_decreasesTo`, `m_option` |
| `BatterySaverTrigger` | 1 | `m_option` |
| `BatteryTemperatureTrigger` | 3 | `decreasesTo`, `option`, `temperature`, `varDictionaryKeys`, `variableName` |
| `BluetoothBeaconTrigger` | 1 | `option`, `selectedBeacons` |
| `BluetoothTrigger` | 1 | `m_anyDevice`, `m_btState`, `m_deviceName` |
| `BootTrigger` | 1 | — |
| `CalendarTrigger` | 1 | `calendarAccount`, `enableRegex`, `ignoreCase`, `m_advanceTimeSeconds`, `m_availability`, `m_calendarId`, `m_calendarName`, `m_checkInAdvance`, `m_detailText`, `m_eventStart`, `m_ignoreAllDay`, `m_negativeAdvanceCheck`, `m_titleText`, `simpleCalendarName` |
| `CallActiveTrigger` | 1 | `isExclude`, `m_contactList`, `m_groupIdList`, `m_groupNameList`, `m_option`, `m_phoneNumber`, `m_phoneNumberExclude`, `m_secondaryClassType`, `m_signalOn`, `subscriptionId`, `useRegex` |
| `CallEndedTrigger` | 1 | `isExclude`, `m_contactList`, `m_groupIdList`, `m_groupNameList`, `m_option`, `m_phoneNumber`, `m_phoneNumberExclude`, `useRegex` |
| `CallMissedTrigger` | 1 | `isExclude`, `m_contactList`, `m_groupIdList`, `m_groupNameList`, `m_option`, `m_phoneNumberExclude`, `useRegex` |
| `CameraFlashlightTrigger` | 1 | `option` |
| `CameraInUseTrigger` | 1 | `cameraOption`, `option` |
| `CellTowerTrigger` | 1 | `m_cellGroupName`, `m_cellIds`, `m_inRange` |
| `ClipboardChangeTrigger` | 1 | `enableRegex`, `ignoreCase`, `isConfigured`, `m_text` |
| `CustomSceneTrigger` | 1 | `identifier`, `isShown` |
| `DarkThemeTrigger` | 1 | `m_option` |
| `DataOnOffTrigger` | 1 | `m_dataAvailable` |
| `DataUsedTrigger` | 1 | `billingDay`, `calendarScope`, `cooldownMinutes`, `networkType`, `periodKind`, `rollingAmount`, `rollingUnitMinutes`, `thresholdAmount`, `thresholdUnit`, `useVariableThreshold`, `variableThresholdUnit` |
| `DayDreamTrigger` | 1 | `m_dayDreamEnabled` |
| `DayTrigger` | 2 | `m_dayOfMonth`, `m_dayOfWeek`, `m_hour`, `m_minute`, `m_monthOfYear`, `m_option`, `m_useAlarm`, `m_useVariable` |
| `DeviceUnlockedTrigger` | 1 | — |
| `DialNumberTrigger` | 2 | `m_makeCall`, `m_numberToDial` |
| `DockTrigger` | 2 | `m_dockType` |
| `DrawerOpenCloseTrigger` | 2 | `drawerType`, `option` |
| `EmailReceivedTrigger` | 1 | `bodyPattern`, `emailSource`, `enableRegex`, `fromAddressPattern`, `ignoreCase`, `isConfigured`, `lastBody`, `lastFromAddress`, `lastSubject`, `legacyImapPort`, `legacyImapServer`, `legacyUseSSL`, `markAsRead`, `selectedServerId`, `subjectPattern`, `useAlarm` |
| `EmptyTrigger` | 1 | — |
| `ExternalPowerTrigger` | 1 | `m_hasSetNewPowerConnectedOptions`, `m_hasSetUSBOption`, `m_powerConnected`, `m_powerConnectedOptions` |
| `FailedLoginTrigger` | 1 | `m_numFailures`, `m_timeIndex` |
| `FileChangedTrigger` | 1 | `fileFilter`, `folderPath`, `useStaticFolder`, `watchForCreated`, `watchForDeleted`, `watchForModified` |
| `FingerprintGestureTrigger` | 1 | `option` |
| `FlipDeviceTrigger` | 2 | `m_anyStart`, `m_faceDown`, `m_workWithScreenOff` |
| `FloatingButtonTrigger` | 1 | `disableTriggerOnRemove`, `drawOverSystemApps`, `fixedLocation`, `forceLocation`, `iconText`, `iconTextColor`, `iconTintColor`, `iconTintEnabled`, `iconType`, `identifier`, `longPressEnabled`, `m_alpha`, `m_iconBgColor`, `m_imageResourceId`, `m_padding`, `m_showOnLockScreen`, `m_size`, `m_transparentBackground`, `overridenAlpha`, `overridenBgColor`, `overridenSize`, `overridenTransparentBackground`, `preventRemoveByDrag`, `showPositionOnMove`, `usePercentForLocation`, `vibrateOnClick`, `xLocation`, `yLocation` |
| `FloatingTextShownHiddenTrigger` | 1 | `identifier`, `option` |
| `GPSEnabledTrigger` | 1 | `m_gpsModeEnabled` |
| `GeofenceTrigger` | 1 | `m_enterArea`, `m_geofenceId`, `m_geofenceUpdateRateMinutes`, `m_triggerFromUnknown`, `m_updateRateText` |
| `GoogleAssistantTrigger` | 1 | — |
| `HeadphonesTrigger` | 3 | `d`, `m_headphonesConnected`, `m_micOption` |
| `HomeButtonLongPressTrigger` | 1 | `option` |
| `HotspotTrigger` | 1 | `m_hotspotEnabled` |
| `HttpServerTrigger` | 1 | `headerParams`, `identifier`, `ipAddressWhiteList`, `responseCode`, `responseText`, `saveBodyToFile`, `saveBodyToFileDirectory`, `saveBodyToFileFilename`, `sendResponse`, `variableWhiteList`, `variableWhiteListEnabled` |
| `IncomingCallTrigger` | 1 | `isExclude`, `m_groupIdList`, `m_groupNameList`, `m_incomingCallFromList`, `m_option`, `m_phoneNumberExclude`, `useRegex` |
| `IncomingSMSTrigger` | 1 | `enableRegex`, `enableRegexPhoneNumber`, `ignoreCase`, `isExcludeContact`, `m_exactMatch`, `m_excludes`, `m_groupIdList`, `m_groupNameList`, `m_option`, `m_smsContent`, `m_smsFromList`, `m_smsNumberExclude`, `subscriptionId` |
| `IntentReceivedTrigger` | 1 | `action`, `enableRegex`, `extraDictionaryKeys`, `extraParams`, `extraValuePatterns`, `extraVariables`, `extrasDictKeys`, `extrasDictVarName`, `saveExtrasToDict` |
| `IpAddressChangeTrigger` | 1 | — |
| `KeyboardOpenCloseTrigger` | 1 | `option` |
| `LightSensorTrigger` | 1 | `m_lightLevel`, `m_lightLevelFloat`, `m_option` |
| `LocationTrigger` | 1 | `m_dontTriggerFromUnknownEnter`, `m_enterArea`, `m_geofenceId`, `m_latitude`, `m_longitude`, `m_newTriggerFromUnknown`, `m_radius`, `m_triggerFromUnknown` |
| `LogcatTrigger` | 1 | `component`, `ignoreCase`, `textToMatch` |
| `MacroDroidEnabledTrigger` | 1 | — |
| `MacroDroidIconLongPressShortcutTrigger` | 1 | `fgColor`, `iconBgColor`, `iconText`, `iconType`, `imagePackageName`, `imageResourceId`, `imageResourceName`, `shortcutName` |
| `MacroDroidInitialisedTrigger` | 1 | — |
| `MacroEnabledTrigger` | 1 | — |
| `MacroFinishedTrigger` | 1 | `macroId`, `macroName` |
| `MediaButtonPressedTrigger` | 1 | `m_cancelPress`, `m_option`, `m_optionIndex` |
| `MediaButtonV2Trigger` | 1 | `optionsEnabledArray` |
| `MediaTrackChangedTrigger` | 1 | — |
| `ModeEnterExitTrigger` | 2 | `m_anyChange`, `m_mode`, `m_modeEntered` |
| `MusicPlayingTrigger` | 1 | `option` |
| `NFCStateTrigger` | 1 | `option` |
| `NetworkRoamingChangedTrigger` | 1 | `m_roamingEnabled` |
| `NotificationButtonTrigger` | 1 | `REQUEST_CODE_SELECT_BUTTON`, `m_collapseNotification`, `m_id` |
| `NotificationTrigger` | 2 | `enableRegex`, `ignoreCase`, `m_applicationNameList`, `m_exactMatch`, `m_excludeApps`, `m_excludes`, `m_ignoreOngoing`, `m_option`, `m_packageNameList`, `m_soundOption`, `m_supressMultiples`, `m_textContent`, `matchOptionMessage`, `matchOptionTitle`, `separateTitleAndMessage` |
| `OrientationTrigger` | 1 | `option` |
| `OutgoingCallTrigger` | 1 | `isExclude`, `m_groupIdList`, `m_groupNameList`, `m_option`, `m_outgoingCallToList`, `m_phoneNumber`, `m_phoneNumberExclude`, `useRegex` |
| `PhotoTakenTrigger` | 1 | — |
| `PowerButtonLongPressTrigger` | 1 | — |
| `PowerButtonToggleTrigger` | 1 | `m_numToggles` |
| `PriorityModeTrigger` | 2 | `option` |
| `ProximityTrigger` | 3 | `m_near`, `m_selectedOption` |
| `QuickSettingsTileTrigger` | 3 | `m_tileOption`, `m_toggleOption`, `quickTileImageName`, `quickTileIsCollapseOnPress`, `quickTileIsToggle`, `quickTileLabel`, `quickTileSubtitle` |
| `RegularIntervalTrigger` | 1 | `m_ignoreReferenceStartTime`, `m_minutes`, `m_seconds`, `m_startHour`, `m_startMinute`, `m_useAlarm`, `m_useIntervalVariable`, `m_useReferenceTimeVariable` |
| `SMSSentTrigger` | 1 | `enableRegexPhoneNumber`, `ignoreCase`, `isExcludeContact`, `m_contactList`, `m_exactMatch`, `m_excludes`, `m_option`, `m_smsContent`, `m_smsNumberExclude`, `useRegex` |
| `ScreenContentTrigger` | 1 | `activityEnableRegex`, `activityIgnoreCase`, `activityNameToMatch`, `appNameList`, `enableRegex`, `ignoreCase`, `includeOverlays`, `isOffScreen`, `limitToActivity`, `matchOption`, `packageNameList`, `textToMatch` |
| `ScreenOnOffTrigger` | 1 | `m_screenOn` |
| `ScreenshotContentTrigger` | 1 | `activityEnableRegex`, `activityIgnoreCase`, `activityNameToMatch`, `appNameList`, `enableRegex`, `ignoreCase`, `isOffScreen`, `limitToActivity`, `packageNameList`, `textToMatch` |
| `ShakeDeviceTrigger` | 1 | — |
| `ShareFileTrigger` | 1 | `enableRegex`, `filePatternToCheck`, `ignoreCase`, `matchOption`, `safPathName`, `safPathUri`, `saveToNewLocation`, `useAllFilesAccess` |
| `ShareTextTrigger` | 1 | `enableRegex`, `ignoreCase`, `matchOption`, `saveExtrasToDict`, `textToCheck` |
| `ShizukuStoppedTrigger` | 1 | — |
| `ShortcutTrigger` | 1 | — |
| `SignalOnOffTrigger` | 1 | `m_signalOn`, `subscriptionId` |
| `SilentModeTrigger` | 1 | `m_silentEnabled` |
| `SimChangeTrigger` | 1 | `option` |
| `SleepTrigger` | 1 | `option` |
| `SpotifyTrigger` | 1 | `option` |
| `StopwatchTrigger` | 1 | `dontUseAlarm`, `m_seconds`, `m_stopwatchName` |
| `SunriseSunsetTrigger` | 1 | `m_option`, `timeAdjustSeconds`, `useAlarm` |
| `SwipeTrigger` | 2 | `m_cleared`, `m_swipeMotion`, `m_swipeStartArea` |
| `SystemLogTrigger` | 1 | `enableRegex`, `ignoreCase`, `matchOption`, `text` |
| `SystemSettingTrigger` | 1 | `globalEnabled`, `regexEnabled`, `secureEnabled`, `settingPattern`, `systemEnabled` |
| `TimerTrigger` | 2 | `m_daysOfWeek`, `m_hour`, `m_minute`, `m_second`, `m_useAlarm`, `m_useVariable`, `m_variableName` |
| `ToastTrigger` | 1 | `appNameList`, `enableRegex`, `ignoreCase`, `packageNameList`, `textToMatch` |
| `UIClickTrigger` | 1 | `appNameList`, `clickType`, `enableRegex`, `ignoreCase`, `packageNameList`, `textToMatch`, `useContentDescriptionText` |
| `USBTetheringTrigger` | 1 | `option` |
| `UsbDeviceConnectionTrigger` | 1 | `option` |
| `VariableTrigger` | 1 | `anyDictionaryKeyChange`, `checkCase`, `dictionaryKeys`, `dictionaryType`, `enableRegex`, `m_anyValueChange`, `m_booleanValue`, `m_doubleValue`, `m_intCompareVariable`, `m_intGreaterThan`, `m_intLessThan`, `m_intNotEqual`, `m_intValue`, `m_otherValueToCompare`, `m_stringComparisonType`, `m_stringEqual`, `m_stringValue`, `m_variable` |
| `VolumeButtonTrigger` | 1 | `m_dontChangeVolume`, `m_monitorOption`, `m_notConfigured`, `m_option` |
| `VolumeLongPressTrigger` | 1 | `isNew`, `option` |
| `VpnTrigger` | 1 | `option` |
| `WearOSComplicationClickTrigger` | 1 | `complicationType` |
| `WeatherTrigger` | 3 | `m_humidityAbove`, `m_humidityValue`, `m_option`, `m_tempBelow`, `m_tempCelcius`, `m_temperature`, `m_weatherCondition`, `m_windSpeedAbove`, `m_windSpeedValue`, `m_windSpeedValueMph` |
| `WebHook2wayTrigger` | 1 | `headerParams`, `identifier`, `ipAddressWhiteList`, `responseCode`, `responseText`, `saveBodyDictionaryKeys`, `saveBodyVariableName`, `sendResponse` |
| `WebHookTrigger` | 1 | `identifier`, `ipAddressWhiteList`, `queryParamsDictionaryName`, `variableWhiteList`, `variableWhiteListEnabled` |
| `WidgetPressedTrigger` | 1 | `iconTintEnabled`, `m_imageId`, `m_widgetType`, `tintColor` |
| `WifiConnectionTrigger` | 4 | `customAddedSSIDs`, `m_SSIDList`, `m_wifiState` |
| `WifiSSIDTrigger` | 1 | `m_InRange`, `m_SSIDList`, `wifiCellInfoList` |
| `WorkProfileTrigger` | 1 | `workProfileEnabled` |

## Atualização

Regere o catálogo sempre que um novo export de referência for coletado:

```bash
python src/scripts/generate_macrodroid_trigger_catalog.py All_triggers.macro src/docs
```

Toda diferença deve ser revisada como mudança de implementação interna do MacroDroid, não como contrato estável da plataforma.
