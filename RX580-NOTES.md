# EFI adaptada — ERYING THM570 + i9-11900H ES + RX 580

Upstream: `Forte500/ERYING-i9-11900H-ES-Hackintosh`  
Upstream commit: `d35124e47c8dae92dfa01d701fcb21d5eaea4289`

## Hardware alvo
- ERYING THM570 / THM5701xx
- Intel Core i9-11900H ES (Tiger Lake-H)
- 16 GB DDR4-3200
- AMD Radeon RX 580 (Polaris)
- Kingston SSD SATA 480 GB

## Alterações realizadas
- removido `agdpmod=pikera`, desnecessário para a RX 580/Polaris
- removida a injeção cosmética de modelo `RX 6600 XT`
- mantidos `-igfxvesa` e `-wegswitchgpu` para neutralizar a Intel Xe e priorizar a Radeon dedicada
- `UTBMap111.kext` habilitado para BIOS stock THM570111
- `UTBMap10729.kext` desabilitado
- GPU BAR resizing do OpenCore desabilitado quando a chave existe
- SMBIOS mantido como `iMacPro1,1`, com a identidade pública do upstream removida
- patches de CPU/CPUID/ACPI/power management do Forte500 preservados

## BIOS — primeiro boot
- SATA Mode: **AHCI**
- XHCI Hand-off: **Enabled**
- CFG Lock: **Disabled**
- Overclocking Lock: **Disabled**
- VT-d: **Enabled**
- Internal Graphics: **Auto**
- Primary Display: **Auto / PEG se disponível**
- Fast Boot: **Disabled**
- Secure Boot: **Disabled**
- Re-Size BAR: **Disabled inicialmente para a RX 580**

## Obrigatório antes de iServices
Gere valores únicos de `SystemSerialNumber`, `MLB`, `SystemUUID` e `ROM` para `iMacPro1,1` com GenSMBIOS. O `config.plist` contém marcadores deliberados para impedir o uso acidental dos números públicos do upstream.

## Limitação conhecida
Sleep continua sendo uma limitação conhecida da plataforma/BIOS e não foi tratado por este patch.
