# EFI adaptada — ERYING THM570 + i9-11900H ES + RX 580

Upstream: Forte500/ERYING-i9-11900H-ES-Hackintosh  
Upstream commit: `d35124e47c8dae92dfa01d701fcb21d5eaea4289`

## Hardware alvo
- ERYING THM570 / THM5701xx
- Intel Core i9-11900H ES (Tiger Lake-H)
- 16 GB DDR4-3200
- AMD Radeon RX 580 (Polaris)
- Kingston SSD SATA 480 GB

## Alterações em relação à EFI do Forte500
- removido `agdpmod=pikera` (específico/útil para Navi; não necessário na RX 580)
- removida a injeção cosmética de modelo `RX 6600 XT`
- mantidos `-igfxvesa` e `-wegswitchgpu` para neutralizar a Intel Xe e usar a Radeon dedicada
- `UTBMap111.kext` habilitado para BIOS stock THM570111
- `UTBMap10729.kext` desabilitado
- redimensionamento de GPU BAR do OpenCore colocado em modo desabilitado quando presente
- SMBIOS mantido como `iMacPro1,1`, mas números públicos do upstream foram removidos

## BIOS recomendada para o primeiro boot
- SATA Mode: **AHCI**
- XHCI Hand-off: **Enabled**
- CFG Lock: **Disabled**
- Overclocking Lock: **Disabled**
- VT-d: **Enabled**
- Internal Graphics: **Auto**
- Primary Display: **Auto / PEG se disponível e estável**
- Fast Boot: **Disabled**
- Secure Boot: **Disabled**
- Re-Size BAR: **Disabled inicialmente para a RX 580**

## Antes de usar iCloud / iMessage / FaceTime
O arquivo `EFI/OC/config.plist` foi deliberadamente deixado sem uma identidade Apple reutilizada. Gere valores **únicos** de `SystemSerialNumber`, `MLB`, `SystemUUID` e `ROM` para `iMacPro1,1` com GenSMBIOS antes de usar iServices.

## Observação
Sleep continua sendo uma limitação conhecida desta plataforma/BIOS. A EFI foi preparada para boot e uso como desktop; não foi alterado o conjunto de patches de CPU/ACPI do Forte500.
