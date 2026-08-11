#!/usr/bin/env python3
import os
import plistlib
from pathlib import Path

TARGET = Path("EFI/OC/config.plist")

with TARGET.open("rb") as f:
    cfg = plistlib.load(f)

# Preserve Forte500's i9-11900H ES / THM570 CPU, ACPI and power-management
# configuration. Adapt only GPU, stock-BIOS mapping and public SMBIOS data.

# RX 580 Polaris: no agdpmod=pikera. Keep Tiger Lake Xe neutralized and
# prefer the external AMD GPU.
add = cfg.setdefault("NVRAM", {}).setdefault("Add", {})
apple = add.setdefault("7C436110-AB2A-4BBB-A880-FE41995C9F82", {})
args = apple.get("boot-args", "")
tokens = [t for t in args.split() if t not in {"agdpmod=pikera", "-wegnoegpu"}]
for required in ("-igfxvesa", "-wegswitchgpu"):
    if required not in tokens:
        tokens.append(required)
apple["boot-args"] = " ".join(tokens)

# Remove RX 6600 XT cosmetic model injection and let WhateverGreen/macOS
# identify the RX 580 naturally.
dev_add = cfg.setdefault("DeviceProperties", {}).setdefault("Add", {})
for pci_path, props in list(dev_add.items()):
    if not isinstance(props, dict):
        continue
    model = props.get("model")
    if isinstance(model, bytes):
        model_text = model.decode("utf-8", errors="ignore")
    elif isinstance(model, str):
        model_text = model
    else:
        model_text = ""
    if "6600" in model_text.lower():
        props.pop("model", None)
    if not props:
        dev_add.pop(pci_path, None)

# Polaris RX 580: do not request GPU BAR resizing from OpenCore.
booter_quirks = cfg.setdefault("Booter", {}).setdefault("Quirks", {})
if "ResizeAppleGpuBars" in booter_quirks:
    booter_quirks["ResizeAppleGpuBars"] = -1
uefi_quirks = cfg.setdefault("UEFI", {}).setdefault("Quirks", {})
if "ResizeGpuBars" in uefi_quirks:
    uefi_quirks["ResizeGpuBars"] = -1

# Stock THM570111 USB map.
for entry in cfg.setdefault("Kernel", {}).setdefault("Add", []):
    if not isinstance(entry, dict):
        continue
    bundle = entry.get("BundlePath", "")
    if bundle == "UTBMap111.kext":
        entry["Enabled"] = True
    elif bundle == "UTBMap10729.kext":
        entry["Enabled"] = False

# Keep the upstream-tested SMBIOS model, but remove the public/shared
# identity. Unique values must be generated before iServices are used.
generic = cfg.setdefault("PlatformInfo", {}).setdefault("Generic", {})
generic["SystemProductName"] = "iMacPro1,1"
generic["SystemSerialNumber"] = "GENERATE_WITH_GENSMBIOS"
generic["MLB"] = "GENERATE_WITH_GENSMBIOS"
generic["SystemUUID"] = "00000000-0000-0000-0000-000000000000"
generic["ROM"] = bytes.fromhex("000000000000")

with TARGET.open("wb") as f:
    plistlib.dump(cfg, f, fmt=plistlib.FMT_XML, sort_keys=False)

# Validate the important invariants immediately.
with TARGET.open("rb") as f:
    check = plistlib.load(f)
check_args = check["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]["boot-args"].split()
assert "agdpmod=pikera" not in check_args
assert "-igfxvesa" in check_args
assert "-wegswitchgpu" in check_args
assert check["PlatformInfo"]["Generic"]["SystemProductName"] == "iMacPro1,1"
maps = {x.get("BundlePath"): x.get("Enabled") for x in check["Kernel"]["Add"] if isinstance(x, dict)}
assert maps.get("UTBMap111.kext") is True
assert maps.get("UTBMap10729.kext") is False

upstream = os.environ.get("UPSTREAM_COMMIT", "unknown")
Path("RX580-NOTES.md").write_text(f"""# EFI adaptada — ERYING THM570 + i9-11900H ES + RX 580

Upstream: `Forte500/ERYING-i9-11900H-ES-Hackintosh`  
Upstream commit: `{upstream}`

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
""", encoding="utf-8")

print("RX580 adaptation validated successfully")
print("boot-args:", apple["boot-args"])
