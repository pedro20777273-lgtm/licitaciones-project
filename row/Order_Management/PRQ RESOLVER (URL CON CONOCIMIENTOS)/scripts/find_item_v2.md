```py
#!/usr/bin/env python3
"""
find_item_v2.py — Buscar un item code en los catalogos Hologic
================================================================
VERSION 2.0 — VERIFICADO contra los 3 catalogos oficiales:
  - Breast and Skeletal products catalogue.pdf
  - Surgical products catalogue.pdf
  - Diagnostics product catalogue.pdf

Uso:
    python find_item_v2.py EVIVA_0913-12T
    python find_item_v2.py 302929
    python find_item_v2.py NVD-CD-012
    python find_item_v2.py "ATEC 0909-20"

Devuelve: division, descripcion, presentacion (Box of X)
SIN cargar los PDFs.

Total items en la base de datos interna: 334
  - Breast & Skeletal: 31
  - GYN Surgical:      53
  - Diagnostics:       250
"""

import sys
import json
import re

# ============================================================
# BASE DE DATOS — Breast & Skeletal (31 items)
# ============================================================
BREAST_ITEMS = {
    "ATEC 0909-20": ("Standard 9G x 9cm x 20mm", 5),
    "ATEC 0909-12": ("Petite 9G x 9cm x 12mm", 5),
    "ATEC 0912-20": ("Standard 9G x 12cm x 20mm", 5),
    "ATEC 0912-12": ("Petite 9G x 12cm x 12mm", 5),
    "ATEC 0914-20": ("Standard 9G x 14cm x 20mm", 5),
    "ATEC 1209-20": ("Standard 12G x 9cm x 20mm", 5),
    "ATEC 1212-20": ("Standard 12G x 12cm x 20mm", 5),
    "ATEC 0914-20MR": ("Standard MR 9G x 14cm", 5),
    "ATEC 0914-12MR": ("Petite MR 9G x 14cm", 5),
    "ATEC TF-1": ("Filter for ATEC/Eviva", 5),
    "ATEC RTFA": ("Filter for ATEC", 5),
    "ATEC CANISTER": ("Suction canister with lid", 10),
    "EVIVA_0910-20": ("Standard 9G x 10cm x 20mm", 5),
    "EVIVA_0910-12": ("Petite 9G x 10cm x 12mm", 5),
    "EVIVA_0910-12T": ("Petite Trocar 9G x 10cm x 12mm", 5),
    "EVIVA_0913-20": ("Standard 9G x 13cm x 20mm", 5),
    "EVIVA_0913-12": ("Petite 9G x 13cm x 12mm", 5),
    "EVIVA_0913-12T": ("Petite Trocar 9G x 13cm x 12mm", 5),
    "EVIVA_1213-20": ("Standard 12G x 13cm x 20mm", 5),
    "EVIVA_1210-20": ("Standard 12G x 10cm x 20mm", 5),
    "MP101": ("MammoPad Small 20x24cm", 100),
    "MP201": ("MammoPad Medium 25x29cm", 50),
    "MP301": ("MammoPad Large 29x30cm", 50),
    "TUMARK-E13-S-Q": ("Tumark Standard Q Eviva", 10),
    "TUMARK-E13-P-Q": ("Tumark Petite Q Eviva", 10),
    "TUMARK-BREV-S-Q": ("Tumark Standard Q Brevera", 10),
    "SMARK-ATEC-13-09": ("SecurMark ATEC 9G mini cork", 10),
    "SMARK-EVIVA-13": ("SecurMark Eviva/Brevera mini cork", 10),
    "BREVDISP09": ("Brevera Standard Stereotactic Biopsy Needle", 5),
    "BREVTF01": ("Brevera Spare Tissue Filter single", 5),
    "BREVTF12": ("Brevera Spare Tissue Filter 12 chambers", 5),
}

# ============================================================
# BASE DE DATOS — GYN Surgical (53 items)
# ============================================================
SURGICAL_ITEMS = {
    "RFC2010": ("RF Controller Model 10", 1),
    "NSV5-003": ("NovaSure V5 Sterilised", 3),
    "814003": ("RFC Power Cord 230V Europe", 1),
    "814004": ("RFC Power Cord UK", 1),
    "814009": ("RFC Power Cord Italy", 1),
    "814011": ("RFC Power Cord Switzerland", 1),
    "815012": ("CO2 Cylinders", 5),
    "52124-001": ("Foot switch", 1),
    "60-250-1": ("Omni 0 Standard Kit", 1),
    "60-250-2": ("Omni 0 Light Kit", 1),
    "60-200": ("Omni 0 Base Hysteroscope", 1),
    "60-201": ("Omni 0 3.7mm Diagnostic Sheath", 1),
    "60-202": ("Omni 0 5.5mm Operative Sheath", 1),
    "60-203": ("Omni 0 6.0mm Operative Sheath", 1),
    "40-201": ("Rod Lens Hysteroscope Outflow Channel", 1),
    "50-201XL": ("XL Rod Lens Hysteroscope Outflow Channel", 1),
    "60-250-30-1": ("Omni 30 Standard Kit", 1),
    "60-250-30-2": ("Omni 30 Light Kit", 1),
    "60-200-30": ("Omni 30 Base Hysteroscope", 1),
    "60-201-30": ("Omni 30 3.7mm Diagnostic Sheath", 1),
    "60-202-30": ("Omni 30 5.5mm Operative Sheath", 1),
    "60-203-30": ("Omni 30 6.0mm Operative Sheath", 1),
    "MME-04608": ("NTOC Tray for Omni Hysteroscopic Set", 1),
    "60-903-1": ("Omni Instrument Tray", 1),
    "OLK-100": ("Omni Lok Cervical Seal", 5),
    "60-5FR": ("Omni 5 Fr Seal Cap", 10),
    "40-905": ("Hysteroscope Polishing Paste", 3),
    "40-902": ("Hysteroscope Seal Single-Use", 10),
    "40-911": ("Hysteroscope Outflow Channel Spare Parts Kit", 1),
    "60-911": ("Omni Hysteroscopes Spare Parts Kit", 1),
    "ASY-04996": ("Hysteroscope Light Guide Adapters Set", 1),
    "40-900": ("Storz Light Guide Adapter", 1),
    "40-901": ("Wolf Light Guide Adapter", 1),
    "40-904": ("End Cap", 3),
    "10-550": ("MyoSure Control Unit With Foot Switch", 1),
    "20-403ML": ("MyoSure MANUAL Tissue Removal Device", 3),
    "10-403FC": ("MyoSure REACH Tissue Removal Device", 3),
    "30-403LITE": ("MyoSure LITE Tissue Removal Device", 3),
    "50-503XL": ("MyoSure XL Tissue Removal Device", 3),
    "50-603XL": ("MyoSure FMS-XL Tissue Removal Device", 3),
    "ASY-05106": ("Control Unit Power Cord Europe", 1),
    "ASY-05107": ("Control Unit Power Cord UK", 1),
    "ASY-05101": ("Control Unit Power Cord Switzerland", 1),
    "ASY-05103": ("Control Unit Power Cord Italy", 1),
    "FLT-100": ("Fluent Fluid Management System", 1),
    "FLT-112": ("Fluent Flopak Procedure Kit", 6),
    "FLT-005": ("Fluent Waste Bag", 5),
    "FLT-010": ("Fluent Disposable Tissue Sock", 10),
    "ASY-15688": ("Fluent Power Cord Switzerland 4m", 1),
    "ASY-15690": ("Fluent Power Cord Italy 4m", 1),
    "ASY-15693": ("Fluent Power Cord Europe 4m", 1),
    "ASY-15694": ("Fluent Power Cord UK 4m", 1),
    "ASY-15695": ("Fluent Power Cord Denmark 4m", 1),
}

# ============================================================
# BASE DE DATOS — Diagnostics (250 items)
# ============================================================
DIAGNOSTICS_ITEMS = {
    "70096-003": ("ThinPrep Pap Test Kit Cytobrush+Spatula 500T", 500),
    "70096-004": ("ThinPrep Pap Test Kit Cervex Brush 500T", 500),
    "70096-005": ("ThinPrep Pap Test Kit Cervex Brush Combi 500T", 500),
    "70096-002": ("ThinPrep Pap Test Kit No Device 500T", 500),
    "70662-003": ("ThinPrep Pap Test Kit Cytobrush Imager 500T", 500),
    "70662-004": ("ThinPrep Pap Test Kit Cervex Brush Imager 500T", 500),
    "70662-005": ("ThinPrep Pap Test Kit Cervex Combi Imager 500T", 500),
    "70662-002": ("ThinPrep Pap Imaging Test Kit No Device 500T", 500),
    "70098-002": ("PreservCyt Solution Vial 10x25 vials", 250),
    "70099-001": ("ThinPrep Gynaecological Filters Clear 5x100", 500),
    "70303-001": ("ThinPrep Microscope Slides 5x100", 500),
    "70124-001": ("Cytobrush/Plastic Spatula 20x25", 500),
    "70671-001": ("Cervex Brush Collection Devices 20x25", 500),
    "70825-001": ("ThinPrep Imager Microscope Slides 5x100", 500),
    "380101-030": ("Cervex Brush Combi Collection 20x25", 500),
    "50374-001": ("Wallach Papette Kit", 100),
    "ASY-14762": ("PreservCyt Solution Vial 4x25", 100),
    "70897-002": ("Papanicolaou Stain Set", 1),
    "70780-001": ("ThinPrep Nuclear Stain 4L", 1),
    "70779-001": ("ThinPrep Rinse Solution 4L", 1),
    "70793-001": ("ThinPrep Bluing Solution 4L", 1),
    "70781-002": ("ThinPrep Orange G Solution 4L", 1),
    "70782-002": ("ThinPrep EA Solution 4L", 1),
    "ASY-04876": ("ThinPrep Bluing II Solution 4L", 1),
    "0234000": ("General Cytology Kit 100T", 100),
    "71091-001": ("General Cytology Kit 500T", 500),
    "70766-001": ("Deluxe General Cytology Kit 500T centrifuge tubes", 500),
    "70766-002": ("Deluxe General Cytology Kit 500T collection cups", 500),
    "71265-001": ("UroCyte Cytology Kit 100T", 100),
    "70204-002-KIT": ("General Cytology Kit No CytoLyt 100T", 100),
    "70408-002": ("CytoLyt Solution 4x946ml", 4),
    "70406-002": ("PreservCyt Solution 4x946ml", 4),
    "ASY-14753": ("PreservCyt Solution Vial 4x25", 100),
    "70205-001": ("ThinPrep Filters General Cytology Blue 100", 100),
    "70372-001": ("ThinPrep Slides General Cytology 100", 100),
    "0236080": ("CytoLyt Solution Centrifuge Tubes 80x50ml", 80),
    "0236050": ("CytoLyt Solution Collection Cups 50x120ml", 50),
    "70126-002": ("Immunocytochemistry Microscope Slides 72", 72),
    "70472-001": ("ThinPrep UroCyte Filters Yellow 100", 100),
    "70471-001": ("ThinPrep UroCyte Microscope Slides 100", 100),
    "ASY-15311": ("ThinPrep UroCyte PreservCyt Vial 4x25", 100),
    "70908-001": ("Urocyte Collection Kit 20", 20),
    "70987-001": ("Urocyte Software Upgrade Kit", 1),
    "PRD-04573": ("ThinPrep Genesis Processor", 1),
    "PRD-04720": ("ThinPrep Genesis Accessory Kit", 1),
    "PRD-05064": ("ThinPrep Genesis Aliquot Starter Kit", 1),
    "PRD-04677": ("ThinPrep Genesis Aptima Tube Printer", 1),
    "PRD-04678": ("ThinPrep Genesis Slide Printer", 1),
    "71362-001": ("ThinPrep 5000 Processor", 1),
    "ASY-05528": ("AutoLoader Ready ThinPrep 5000 Processor", 1),
    "ASY-03098": ("ThinPrep 5000 AutoLoader Processor", 1),
    "71917-001": ("ThinPrep 5000 Fixative Bath", 1),
    "51873-001": ("Staining Rack Sakura 20 slides", 1),
    "71919-001": ("Packaged Input Carousel T5000", 1),
    "MTL-00486": ("Silicone Lubricant", 1),
    "71920-001": ("T5000 Absorbent Pad Filter Plug", 1),
    "71921-001": ("T5000 Absorbent Pad Evaporation Cover", 1),
    "MME-00900": ("Carbon Filter 0.3 microns", 1),
    "ASY-14280": ("Genius Digital Imager", 1),
    "ASY-14451": ("Information Management System-XL", 1),
    "ASY-14303": ("Genius Review Station", 1),
    "PRD-05815": ("Genius Digital Imager", 1),
    "CMP-01669": ("Genius Review Station Display 27in", 1),
    "ASY-14304": ("Genius Review Station Computer", 1),
    "ASY-14305": ("Genius Image Management Server Base", 1),
    "PRD-00788": ("ThinPrep Integrated Imager", 1),
    "OEM-01079": ("Microscope Slide Tray Capacity 30", 1),
    "OEM-01080": ("Microscope Slide Adapter Capacity 30", 1),
    "ASY-05576": ("Compass Stainer", 1),
    "OEM-01084": ("Fume Cover", 1),
    "OEM-01078": ("Reagent Containers with Lids", 6),
    "OEM-01100": ("Rack Adapter Leica/Sakura", 10),
    "OEM-01081": ("Active Carbon Filter", 1),
    "LEQ-00101": ("Multi-Mix Racked Vortexor", 1),
    "LEQ-00102": ("Custom Rack for Multi-Mix Vortexor", 1),
    "71300-001": ("Cellient Automated Cell Block System", 1),
    "71305-001": ("Cellient Filter Cassette Kit 50T", 50),
    "05379-001": ("Cellient Cassette", 50),
    "71410-001": ("Cellient Filter Holder", 50),
    "71373-001": ("Cellient Wax Tray", 50),
    "72008-001": ("Pipette Tips Box 150", 150),
    "PRD-03000": ("Aptima HIV-1 Quant Dx Assay Kit 100T", 100),
    "PRD-03506": ("Aptima HCV Quant Dx Assay Kit 100T", 100),
    "PRD-03424": ("Aptima HBV Quant Assay Kit 100T", 100),
    "PRD-03001": ("Aptima HIV-1 Quant Dx Calibrator Kit", 1),
    "PRD-03002": ("Aptima HIV-1 Quant Dx Control Kit", 1),
    "PRD-03507": ("Aptima HCV Quant Dx Calibrator Kit", 1),
    "PRD-03508": ("Aptima HCV Quant Dx Control Kit", 1),
    "PRD-03425": ("Aptima HBV Quant Calibrator Kit", 1),
    "PRD-03426": ("Aptima HBV Quant Control Kit", 1),
    "PRD-06419": ("Aptima SARS-CoV-2 Assay Kit 250T", 250),
    "PRD-06420": ("Aptima SARS-CoV-2 Control Kit", 1),
    "PRD-06554": ("Specimen Lysis Tubes Option 1 - 100", 100),
    "PRD-06744": ("Specimen Lysis Tube Replacement Caps 100", 100),
    "PRD-06660": ("Specimen Lysis Tubes Option 2 - 1200", 1200),
    "PRD-06723": ("Specimen Lysis Tube Replacement Caps 1000", 1000),
    "PRD-06951": ("Direct Load Capture Cap Collection Kit 100", 100),
    "PRD-06815": ("Aptima SARS-CoV-2/Flu Assay Kit 250T", 250),
    "PRD-06816": ("Aptima SARS-CoV-2/Flu Control Kit", 1),
    "PRD-05576": ("Aptima Combo2 Assay Kit 100T", 100),
    "PRD-05571": ("Aptima Combo2 Assay Kit 250T", 250),
    "301110": ("Aptima Combo2 / CT / NG Control Kit", 1),
    "302925": ("Aptima Chlamydia trachomatis Assay Kit 100T", 100),
    "302927": ("Aptima Neisseria gonorrhoeae Assay Kit 100T", 100),
    "302807": ("Aptima Trichomonas vaginalis Control Kit", 1),
    "303209": ("Aptima Trichomonas vaginalis Kit 100T", 100),
    "303163": ("Aptima Trichomonas vaginalis Kit 250T", 250),
    "PRD-03919": ("Aptima Mycoplasma genitalium Kit 100T w/Calibrators", 100),
    "PRD-03374": ("Aptima Mycoplasma genitalium Kit 100T no Calibrators", 100),
    "PRD-03568": ("Aptima HSV 1 & 2 Assay Kit 100T", 100),
    "PRD-05186": ("Aptima BV Assay Kit 100T", 100),
    "PRD-05189": ("Aptima CV/TV Assay Kit 100T", 100),
    "PRD-03393": ("Aptima Mycoplasma genitalium Calibrator Kit", 1),
    "PRD-03569": ("Aptima HSV 1 & 2 Control Kit", 1),
    "PRD-05187": ("Aptima BV Control Kit", 1),
    "PRD-05188": ("Aptima BV Calibrator Kit", 1),
    "PRD-05190": ("Aptima CV/TV Control Kit", 1),
    "PRD-05191": ("Aptima CV/TV Calibrator Kit", 1),
    "302929": ("Aptima HPV Assay Kit 100T", 100),
    "303093": ("Aptima HPV Assay Kit 250T", 250),
    "303236": ("Aptima HPV 16 18/45 Genotype Kit 100T", 100),
    "302554": ("Aptima HPV Calibrator Kit", 1),
    "303235": ("Aptima HPV 16 18/45 Genotype Calibrator Kit", 1),
    "303096": ("Panther Run Kit (5000 tests)", 5000),
    "303014": ("Panther Aptima Assay Fluids Kit (1000 tests)", 1000),
    "303013": ("Aptima Auto Detect Kit (1000 tests)", 1000),
    "104772-02": ("Multi-tube Unit Kit MTU 500T (10x10)", 500),
    "902731": ("Panther Waste Bag Box 10", 10),
    "504405": ("Panther Waste Bin Cover Box 10", 10),
    "PRD-03455": ("Panther Run Kit Real-Time Assays 5000T", 5000),
    "903031": ("Tips 1000ul Conductive Liquid Sensing 10x96", 960),
    "302101": ("Bleach Enhancer 2x3800ml", 2),
    "PRD-06783": ("Aptima Whole Blood Diluent Tubes 100", 100),
    "PRD-06720": ("Hologic Solid Caps 100", 100),
    "503762": ("Aptima Specimen Aliquot Tubes 100", 100),
    "504415": ("Caps for Aptima Specimen Aliquot Tubes 100", 100),
    "CL0041": ("Replacement Caps 250T Kits Amp/Probe", 100),
    "CL0040": ("Replacement Caps 250T Kits TCR/Selection", 100),
    "501604": ("Replacement Caps 100T Kits TCR/TER/Selection", 100),
    "501616": ("Replacement Caps 250T Kits Enzyme", 100),
    "402950": ("Advanced Cleaning Solution 255ml", 1),
    "PRD-03003": ("Aptima Specimen Diluent 4x30ml", 4),
    "PRD-05110": ("Aptima Specimen Transfer Kit Printable 100", 100),
    "301154C": ("Aptima Specimen Transfer Kit 100", 100),
    "302657": ("Aptima Cervical Specimen Collection Kit 50", 50),
    "301041": ("Aptima Unisex Swab Specimen Collection Kit 50", 50),
    "PRD-03546": ("Aptima Multitest Swab Collection Kit 50", 50),
    "301040": ("Aptima Urine Specimen Collection Kit 50", 50),
    "105575": ("Aptima Urine Specimen Transfer Tubes 100", 100),
    "105668": ("Aptima Penetrable Caps 100", 100),
    "103036A": ("Replacement Non-penetrable Caps 3000", 3000),
    "303658": ("Aptima Transfer Solution Kit SurePath", 1),
    "PRD-03478": ("Aptima Specimen Diluent Kit", 1),
    "PRD-07400": ("Panther Fusion SARS-CoV-2/Flu A/B/RSV Cartridge 12x8", 96),
    "PRD-04328": ("Panther Fusion Flu A/B/RSV Cartridge 12x8", 96),
    "PRD-04330": ("Panther Fusion AdV/hMPV/RV Cartridge 12x8", 96),
    "PRD-04329": ("Panther Fusion Paraflu Cartridge 12x8", 96),
    "PRD-04868": ("Panther Fusion Bordetella Cartridge 12x8", 96),
    "PRD-07401": ("Panther Fusion SARS-CoV-2/Flu A/B/RSV Controls", 1),
    "PRD-04336": ("Panther Fusion Flu A/B/RSV Control Kit", 1),
    "PRD-04338": ("Panther Fusion AdV/hMPV/RV Control Kit", 1),
    "PRD-04337": ("Panther Fusion Paraflu Control Kit", 1),
    "PRD-04869": ("Panther Fusion Bordetella Control Kit", 1),
    "PRD-04803": ("Panther Fusion MRSA Cartridge 12x8", 96),
    "PRD-04484": ("Panther Fusion GBS Cartridge 12x8", 96),
    "PRD-04805": ("Panther Fusion MRSA Control Kit", 1),
    "PRD-04485": ("Panther Fusion GBS Control Kit", 1),
    "PRD-04000": ("Panther Fusion Tube Trays 18x56", 1008),
    "PRD-04339": ("Panther Fusion Specimen Lysis Tubes 100", 100),
    "PRD-04331": ("Panther Fusion Extraction Reagent-S 240x4", 960),
    "PRD-04332": ("Panther Fusion Internal Control-S 240x4", 960),
    "PRD-04333": ("Panther Fusion Reconstitution Buffer I 960x2", 1920),
    "PRD-04804": ("Panther Fusion Reconstitution Buffer II 960x2", 1920),
    "PRD-04334": ("Panther Fusion Elution Buffer 1200x2", 2400),
    "PRD-04335": ("Panther Fusion Oil Reagent 960x2", 1920),
    "PRD-04477": ("Panther Fusion Extraction Reagent-X 240x4", 960),
    "PRD-04476": ("Panther Fusion Internal Control-X 240x4", 960),
    "PRD-06232": ("Panther Fusion Extraction Reagent-B 240x4", 960),
    "PRD-06234": ("Panther Fusion Internal Control-B 240x4", 960),
    "PRD-04430": ("Panther Fusion Universal Fluids Kit", 1),
    "PRD-04431": ("Panther Fusion Assay Fluids I-S", 1),
    "ASY-12890": ("Laptop with myAccess Software", 1),
    "PRD-04303": ("Open Access RNA/DNA Enzyme Cartridge 12x8", 96),
    "PRD-04304": ("Aptima Oil Reagent 24.6ml", 1),
    "PRD-04926": ("1M Magnesium Chloride Solution", 1),
    "PRD-04927": ("1M Potassium Chloride Solution", 1),
    "PRD-04935": ("1M Tris pH 8.0", 1),
    "PRD-04306": ("DNA IC Primers 0.53ml", 1),
    "PRD-04307": ("RNA IC Primers 0.53ml", 1),
    "PRD-04308": ("DNA IC Probe 0.53ml", 1),
    "PRD-04309": ("RNA IC Probe 0.53ml", 1),
    "PRD-04311": ("Open Access Primer/Probe Tubes 2.0ml 100", 100),
    "PRD-04312": ("Open Access Primer/Probe Caps 100", 100),
    "PRD-04305": ("Panther Fusion Open Access Pack", 1),
    "PRD-04423": ("Specimen Transport Medium STM 80ml", 1),
    "PRD-04943": ("Urine Transport Medium UTM 80ml", 1),
    "PRD-04944": ("Blood Transport Medium BTM 80ml", 1),
    "PRD-04945": ("Open Access Diluent Additive 1ml", 1),
    "302351": ("Specimen Diluent Kit PCA3 26ml", 1),
    "401457": ("Transport Tube Polypropylene 50", 50),
    "PRD-07157": ("Panther Fusion EBV Quant Cartridge 12x8", 96),
    "PRD-07232": ("Panther Fusion BKV Quant Cartridge 12x8", 96),
    "PRD-07159": ("Panther Fusion EBV Quant Calibrators", 1),
    "PRD-07158": ("Panther Fusion EBV-BKV Quant Controls", 1),
    "PRD-07234": ("Panther Fusion BKV Quant Calibrators", 1),
    "PRD-05074": ("Aptima CMV Quant Assay Kit 100T", 100),
    "PRD-05076": ("Aptima CMV Quant Calibrator Kit", 1),
    "PRD-05075": ("Aptima CMV Quant Control Kit", 1),
    "303095": ("Panther System", 1),
    "PRD-05490": ("Panther Plus", 1),
    "PRD-07161": ("Panther Track Ready Connection", 1),
    "PRD-03417": ("Panther Fluorometer Assembly 677", 1),
    "ASY-07548": ("Panther Fluorometer Installation", 1),
    "PRD-05847": ("Panther Upgrade Continuous Fluid+Waste Module", 1),
    "PRD-05846": ("Panther Upgrade CF+Waste+Drain Module", 1),
    "PRD-05844": ("Panther Upgrade CF+Waste+MTU Expansion", 1),
    "PRD-05845": ("Panther Upgrade CF+Waste+Drain+MTU Exp", 1),
    "PRD-06119": ("Panther Link Connectivity", 1),
    "PRD-04172": ("Panther Fusion System", 1),
    "PRD-04173": ("Panther Fusion Module", 1),
    "903013": ("Sample Rack", 1),
    "902998": ("Sample Rack Tray", 1),
    "903015": ("Sample Shield", 1),
    "902807": ("Reagent Rack 100T Kit", 1),
    "902808": ("Reagent Rack 250T Kit", 1),
    "902841": ("TCR Adaptor 250T Kit", 1),
    "902842": ("TCR Adaptor 100T Kit", 1),
    "ASY-07379": ("Tomcat Instrument", 1),
    "504080": ("Tomcat Waste Kit Box 30", 30),
    "303683": ("Tomcat Reagent Bottle", 1),
    "FAB-10694": ("Input Rack for ThinPrep Vials", 1),
    "FAB-10693": ("Input Rack for SurePath Vials", 1),
    "NVD-INST-B-K": ("Novodiag Instrument Rev B Package", 1),
    "NVD-TSC-K": ("Novodiag Touchscreen Package", 1),
    "NVD-TSCA-K": ("Novodiag Touchscreen Arm Package", 1),
    "NVD-TSCP-K": ("Novodiag Touchscreen Post Package", 1),
    "NVD-STK-K": ("Novodiag Stack Package", 1),
    "03358976001": ("MagNA Lyser Instrument Roche", 1),
    "P002391P24T0-A.0": ("Precellys 24 Touch Bertin", 1),
    "NVD-BGE-012": ("Novodiag Bacterial GE+ Cartridges", 12),
    "NVD-CRB-012": ("Novodiag CarbaR+ Cartridges", 12),
    "NVD-CD-012": ("Novodiag C. difficile Cartridges", 12),
    "NVD-SP-010": ("Novodiag Stool Parasites Cartridges", 10),
    "NVD-CV-012": ("Novodiag COVID-19 Cartridges", 12),
    "NVD-RP4-012": ("Novodiag RESP-4 Cartridges", 12),
    "MD-NAT-50": ("mNAT Medium Tube 50", 50),
    "MD-NATR-50": ("mNAT R Medium Tube 50", 50),
    "MD-NATS-50": ("mNAT S Medium Tube 50", 50),
    "MD-NATV-50": ("mNAT V Medium Tube 50", 50),
    "480CE": ("eSwab Medium Tube and FLOQSwabs 1ml 50", 50),
}

# ============================================================
# DETECCION DE DIVISION POR PATRON
# ============================================================
PATTERNS = [
    (r"^(EVIVA_|ATEC|MP\d|TUMARK|TRIMARK|SMARK|BREV)", "Breast & Skeletal"),
    (r"^(RFC2010|NSV5|60-|40-|50-|10-|20-|30-|FLT-|OLK-|52124|814\d|81501|ASY-0510|ASY-1568|ASY-1569|ASY-04996|MME-04608)", "GYN Surgical"),
    (r"^(70|71|ASY-1[0-4]|PRD-0|NVD-|MD-NAT|480CE|0234|0236|3801|301|302|303|105|104|503|504|902|903|CL00|402|401|MTL-0|CMP-0|CBL-0|FAB-|OEM-|LEQ-|03358|P002391)", "Diagnostics"),
]


def detect_division(item_code):
    """Detecta la division por patron."""
    code = item_code.upper().strip()
    for pattern, division in PATTERNS:
        if re.match(pattern, code, re.IGNORECASE):
            return division
    return "UNKNOWN"


def find_item(item_code):
    """Busca un item_code en los 3 catalogos."""
    code = item_code.strip()

    for source, items in [
        ("catalogo_breast.pdf", BREAST_ITEMS),
        ("catalogo_surgical.pdf", SURGICAL_ITEMS),
        ("catalogo_diagnostics.pdf", DIAGNOSTICS_ITEMS),
    ]:
        if code in items:
            description, box_of = items[code]
            division_map = {
                "catalogo_breast.pdf": "Breast & Skeletal",
                "catalogo_surgical.pdf": "GYN Surgical",
                "catalogo_diagnostics.pdf": "Diagnostics",
            }
            return {
                "found": True,
                "item_code": code,
                "catalogue": source,
                "division": division_map[source],
                "description": description,
                "box_of": box_of,
                "presentation": f"Box of {box_of}" if box_of > 1 else "Unit",
            }

    division = detect_division(code)
    return {
        "found": False,
        "item_code": code,
        "catalogue": None,
        "division": division,
        "description": None,
        "box_of": None,
        "presentation": None,
        "note": (
            f"Item not found in internal DB (334 items). "
            f"Probable division: {division}. "
            f"Check the corresponding PDF catalogue manually."
        ),
    }


def main():
    if len(sys.argv) < 2:
        print(f"find_item_v2.py — Internal DB: 334 items")
        print(f"  - Breast & Skeletal: 31")
        print(f"  - GYN Surgical:      53")
        print(f"  - Diagnostics:       250")
        print()
        print("Usage: python find_item_v2.py <item_code>")
        print("Examples:")
        print("  python find_item_v2.py EVIVA_0913-12T")
        print("  python find_item_v2.py 302929")
        print("  python find_item_v2.py NVD-CD-012")
        sys.exit(1)

    item_code = " ".join(sys.argv[1:])
    result = find_item(item_code)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

```