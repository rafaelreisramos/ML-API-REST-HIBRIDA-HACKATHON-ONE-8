@echo off
:: =============================================
::  VIBECODE OCI CONTROLLER - CONFIGURADO (APP SERVER)
:: =============================================

:: --- [ OCI INSTANCE SETTINGS ] ---
:: ID da Instância App Server
set "INSTANCE_OCID=ocid1.instance.oc1.sa-saopaulo-1.antxeljrmgi33kacidu3oz4hozvgsrezank7gz3uhervxhm5442ujyxlfzia"

:: --- [ SSH CONNECTION ] ---
set "SSH_KEY_PATH=C:\Users\renan\.ssh\id_ed25519"
set "SSH_USER=opc"

:: --- [ FINOPS ] ---
:: VM.Standard3.Flex (Intel)
set "COST_PER_HOUR=0.10"

:: --- [ SYSTEM ] ---
set "OCI_PATH=C:\Users\renan\bin"
set "LOG_FILE=vibecode_oci_control.log"
