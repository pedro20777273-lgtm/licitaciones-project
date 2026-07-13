## Instructions NEW pending reason

| Open attachment tool on the header of the order |
| --- |
| Click to add a new attachment line and select the catalog. DO NOT TYPE ANY TEXT IN THE NEW LINE ! |
| Choose category PENDING REASON  and ALWAYS USE CAPS |
| Choose who you identified as the root cause (example SALES) and ALWAYS USE CAPS to fill this into Title |
| Click Find |
| You can now select the applicable pending reason code from the list |
| Click Attach |
| Your pending reason code is now attached to the order and can NOT be amended |

## Instructions AMEND reason

| To update your reason code, simply delete the original and click save |
| --- |
| Click to add a new attachment line and select the catalog. DO NOT TYPE ANY TEXT IN THE NEW LINE  + repeat the process for NEW pending reason |

## Pending reason code list

| Title (who is the root cause) | Short Code | Description | Used by | Use | Owner |
| --- | --- | --- | --- | --- | --- |
| CUSTOMER SERVICE | CSC | CSC - CS CHECK | CS | CS needs to verify/check | CS |
| CSE | CSE - CS ERROR | CS + CC&T | CS made an error, preventing possibility to book | CS |  |
| CSM | CSM - CS MISS | CS + CC&T | CS missed to book the order same day | CS |  |
| CSN | CSN - CS NEW HIRE | CS | CS new hire entered an order that still requires checking by more senior CS | CS |  |
| CUSTOMERS | CSL | CSL - CUST  SH. SH. LIFE | CS | Customer requires a specific Shelf Life, CS is waiting for their approval | CS |
| CWDC | CWDC - CUST CHANGE/DELAY /CANCELLATION | CS | Waiting: Customer requested delay in shipment, check-up required to cancel or ship order or requested a change and check is required before booking | CS |  |
| CWLC | CWLC - CUST WAIT LC | CS | Waiting: Customer needs to provide LC document | CS |  |
| CWLO | CWLO - CUST CONFIRM LOGI | CS | Waiting: Customer needs to confirm logistic details | CS |  |
| CWNP | CWNP - CUSTOMER NO PRICE | CS + CC&T | Customer ordering without any pricing for any item on their PO | CS + CC&T |  |
| CWPA | CWPA - CUSTOMER WRONG ADDRESS | CS | Missing address or wrong address - for some customers, we know that the billing address is X, but customers keep putting Y | CS |  |
| CWPI | CWPI - CUSTOMER WRONG ITEM CODE | CS + CC&T | Customer Using superseded/non existing item codes | CS + CC&T |  |
| CWPP | CWPP - CUSTOMER WRONG PRICE | CS + CC&T | Prices on PO not matching Oracle | CS + CC&T |  |
| CWPU | CWPU - CUSTOMER WRONG UNIT | CS + CC&T | Customer ordering in units (i.e. brushes, one box is 500 units) instead of boxes as per contract | CS |  |
| CWPV | CWPV - CUSTOMER WRONG VAT | CS + CC&T | Prices on PO with VAT included - Oracle is looking for the price as per contract, so without VAT | CS |  |
| CWSP | CWSP - CUSTOMER SPARE SERVICE OPS | CC&T | PO parts are spare parts and were not loaded on the BSA | CC&T |  |
| PTNP | PTNP - PT NEW PRICING | CC&T | Pricing was not set up yet e.g. pre-load not possible/no signed contract received by customer | CC&T |  |
| CWPF | CWPF - CUSTOMER WRONG FORM | CS + CC&T | DACH Specific ! Customer is still using the old order form template. | CC&T |  |
| CWPT | CWPO - CUSTOMER WRONG TEMPLATE | CS | Customer is sending a PO template that can't be read (too light, too dark, handwriting not clear,...) | CS |  |
| CWNC | CWNC - CUSTOMER WRONG NOT COMPLIANT | CC&T | Customer had previous orders(s) on CWPP and was contacted to amend, but failed to do so for the next order. | CC&T |  |
| CWBP | CWBP - CUSTOMER WRONG BANDED PRICING | CC&T | UK only ! Customer is on banded pricing (1-2-3) | CC&T |  |
| CWNPO | CWNPO - CUSTOMER WRONG NO PO | CS | Installation Customer did not present a Purchase order | CS |  |
| CUSTOMS | CTA | CTA - APPROVAL TO SHIP | CS | Awaiting approval to ship related to customs clearance | CS |
| CTI | CTI - CUSTOMS ITTQ | CS | Awaiting approval from Legal/Regulatory or Compliance for IITQ | CS |  |
| EDI | EDE | EDE - EDI ERROR | CS | GHX (GFAX) pushed the order through incorrectly | CS |
| EDL | EDL - EDI LATE | CS | PO arrived / pushed through into the system after 16h | CS |  |
| EDM | EDM - EDI WRONG MAPPING | CS + CC&T | EDI wrong due to incorrect mapping by CS or CC&T | CS + CC&T |  |
| EDS | EDS - EDI SPLIT | CS + CC&T | The PO got split in 2. One part went through ticketing and the other one through EDI touchless. | CS + CC&T |  |
| FINANCE | FCC | FCC - FINANCE CREDIT CHECK | CS | Customer order is automatically put on hold in Oracle (Payment). | CS |
| MANUAL OVERRIDE | MONP | MONP - NO PRICE LIST | CS | No price list available, causing incorrect pricing | CS |
| MOPL | MOPL - FOC PRICE LIST | CS | CS Manual override for item that is FOC, but is showing a price due to CDQ Price List adjustment remove all FOC | CS |  |
| MOPM | MOPM - FOC PROMO MODIFIER | CS | CS Manual override for item that is FOC, but is showing a price due to promo modifier | CS |  |
| MOU | MOU - URGENT NO PRICE | CS | CS Manual override because the price was incorrect in the system, but needed urgent shipment, so could not wait for the resolution | CS |  |
| PRICE QUERY | PRQ | PRQ - PRICE QUERY | CS | Price between Oracle and Customer PO does not match. Next step is for Sales Support to identify root cause and adjust Reason Code  on the order. See tab reason codes for sales support. | CC&T |
| PRICING TEAM | PTBA | PTBA - PT BSA AUTOMATIC | CC&T | A BSA is applicable, but not triggered or multiple BSA's are possible, but none are correct or triggered | CC&T |
| PTPI | PTPI - PT PRICE INCREASE SET UP | CC&T | Price increase not set up | CC&T |  |
| PTWP | PTWP - PT WRONG PRICING | CC&T | Pricing was set up incorrectly or with delay or FOC list price issue without manual override | CC&T |  |
| REGULATORY AND COMPLIANCE | REC | REC - RA EXPORT COMPLIANCE HOLD | CS | Items blocked by export compliance hold in Oracle. | CS |
| RETURNS | RCE | RCE - CUST ERROR - UOM | CS | Customer is ordering the EA quantity and not the ordereable quantity (ex. 3 X NS2013 instead of 1 | CS |
| RIN | RIN - INVESTIGATION NEEDED | CS | This return was created by another department and needs actioning/investigation | CS |  |
| SALES | SAC | SAC - SALES APPS CONFIG | CS | Sales Application needs to confirm the configuration split of KITS (Africa only) | CS |
| SBC | SBC - SALES BOOK CONFIRMATION | CS | Order is in entered, we need confirmation from sales to book | CS |  |
| SCPR | SCPR - SALES CPR | CS | CPR orders in entered status and to be approved by Sales to book | CS |  |
| SEC | SEC - SALES EXPIRED CONTRACT | CC&T | Sales haven’t provided a signed contract. Note: this does not become SNC after a certain period. | CC&T |  |
| SMI | SMI - SALES MISSING ITEM | CC&T | Priced item / FOC item is missing from the contract / sales provided additional/alternative item codes to customer outside of contract | CC&T |  |
| SNC | SNC - SALES NO CONTRACT | CC&T | No contract at all, item has never been quoted. | CC&T |  |
| SPI | SPI - SALES PRICE INCREASE | CC&T | Price increase project causing price discrepancies in Oracle | CC&T |  |
| SBR | SBR - SALES BUSINESS RULES | CC&T | Contract set-up not compliant with system ->automated pricing not possible or manual adjustment/tracking required to book the order | CC&T |  |
| CREDIT NOTES | CNAL | CNAL - ALBARAN | CS | On Credit order type | CS |
|  | CNCO | CNCO - COVID | CS | On Credit order type | CS |
|  | CND | CND - CS ERROR - DUPLICATE ORDER | CS | On Credit order type | CS |
|  | CNE | CNE - CS ERROR - BILL TO | CS | On Credit order type | CS |
|  | CNEP | CNEP - CS ERROR - WRONG PRICING | CS | On Credit order type | CS |
|  | CNFB | CNFB - FINANCE CREDIT BOOK HOLD | CS | On Credit order type | CS |
|  | CNFO | CNFO - FOC | CS | On Credit order type | CS |
|  | CNFR | CNFR - FREIGHT/HANDLING COST | CS | On Credit order type | CS |
|  | CNM | CNM - MISSING DELIVERY | CS | On Credit order type | CS |
|  | CNPI | CNPI - PRICE INCREASE | CS | On Credit order type | CS |
|  | CNQ | CNQ - CS ERROR - QUANTITY | CS | On Credit order type | CS |
|  | CNPT | CNPT - PRICING TEAM ERROR | CS | On Credit order type | CS |
|  | CNAS | CNAS - CS ERROR - ACCOUNT SETUP | CS | On Credit order type | CS |
|  | CNEX | CNEX - EXPIRY DATE | CS | On Credit order type | CS |
| CUSTOMER DATA | DNA | DNA - DT NEW / AMEND ADDRESS | CS | A new shipping/billing address needs to be set up in Oracle or Existing address is incorrect and needs to be adjusted | CS |
| DNR | DNR - DT NEW RELATIONSHIP / ACCOUNT | CS | A relationship between 2 accounts might require extra information needed by CDQ (Sales contact) | CS |  |
| DWA | DWA - DT WRONG ACCOUNT | CC&T | CS chose wrong bill/sold-to account(misleading account/PO /understanding from stakeholders (= sales, CS, CC&T, Pricing/Data team, customer)-> price query. | CS |  |
| DFR | DFR - DATA WRONG FREIGHT | CC&T | Freight has charged/not charged or with the wrong amount as per customer terms | CC&T |  |
| STOCK | SAL | SAL - STOCK ALLOCATION | CS | Item is not available and stays in ready to release status. | CS |
| SAP | SAP - STOCK APPROVAL | CS | Item is either in short-shelf life or needs to be approved by Upper Management. | CS |  |
| SBA | SBA - STOCK ALTERNATIVE ITEM | CS | Item is not in stock, and CS is waiting for the customer to send adjusted PO for alternative item | CS |  |
| SBO | SBO - STOCK BACKORDER | CS | Master Lot item is on backorder, CS already checked and is waiting for stock | CS |  |
| CC&T | SSM | SSM - SALES SUPPORT MISS | CC&T | Sales Support Missed to add certain items on thee BSA form / missed to send the full BSA form | CC&T |
| THIRD PARTY | TPI | TPI - INTEGRATION | CS | ! Only use this reason code for orders that are entered and can't be booked, related to an integration project | CS |
| TPM | TPM - MASTER DATA | CS | Master Data (item etc..) not set up yet/correctly | CS |  |
| TPS | TPS - SYSTEM ERROR | CS + CC&T | ! Only use for Oracle related issue, that needs IT. E.g. BSA doesn't trigger because request date in future, but ship date within contract time. | CS + CC&T |  |
| TPSA | TPSA - SITE ASSESSMENT | CS | Installation Site asssessment is missing or incorrect | CS |  |
| Grand Total |  |  |  |  |  |

## RAW list

| Title | Short Code | Description | Category | Use | Used by | Owner |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CREDIT NOTES | CNAL | CNAL - ALBARAN | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNAS | CNAS - CS ERROR - ACCOUNT SETUP | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNCO | CNCO - COVID | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CND | CND - CS ERROR - DUPLICATE ORDER | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNE | CNE - CS ERROR - BILL TO | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNEP | CNEP - CS ERROR - WRONG PRICING | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNEX | CNEX - EXPIRY DATE | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNFB | CNFB - FINANCE CREDIT BOOK HOLD | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNFO | CNFO - FOC | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNFR | CNFR - FREIGHT/HANDLING COST | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNM | CNM - MISSING DELIVERY | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNPI | CNPI - PRICE INCREASE | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNPT | CNPT - PRICING TEAM ERROR | PENDING REASON | On Credit order type | CS | CS |  |
| CREDIT NOTES | CNQ | CNQ - CS ERROR - QUANTITY | PENDING REASON | On Credit order type | CS | CS |  |
| CUSTOMER SERVICE | CSC | CSC - CS CHECK | PENDING REASON | CS needs to verify/check | CS | CS |  |
| CUSTOMER SERVICE | CSE | CSE - CS ERROR | PENDING REASON | CS made an error, preventing possibility to book | CS + CC&T | CS |  |
| CUSTOMERS | CSL | CSL - CUST  SH. SH. LIFE | PENDING REASON | Customer requires a specific Shelf Life, CS is waiting for their approval | CS | CS |  |
| CUSTOMER SERVICE | CSM | CSM - CS MISS | PENDING REASON | CS missed to book the order same day | CS + CC&T | CS |  |
| CUSTOMER SERVICE | CSN | CSN - CS NEW HIRE | PENDING REASON | CS new hire entered an order that still requires checking by more senior CS | CS | CS |  |
| CUSTOMS | CTA | CTA - APPROVAL TO SHIP | PENDING REASON | Awaiting approval to ship related to customs clearance | CS | CS |  |
| CUSTOMS | CTI | CTI - CUSTOMS ITTQ | PENDING REASON | Awaiting approval from Legal/Regulatory or Compliance for IITQ | CS | CS |  |
| CUSTOMERS | CWBP | CWBP - CUSTOMER WRONG BANDED PRICING | PENDING REASON | UK only ! Customer is on banded pricing (1-2-3) | CC&T | CC&T |  |
| CUSTOMERS | CWDC | CWDC - CUST CHANGE/DELAY /CANCELLATION | PENDING REASON | Waiting: Customer requested delay in shipment, check-up required to cancel or ship order or requested a change and check is required before booking | CS | CS |  |
| CUSTOMERS | CWLC | CWLC - CUST WAIT LC | PENDING REASON | Waiting: Customer needs to provide LC document | CS | CS |  |
| CUSTOMERS | CWLO | CWLO - CUST CONFIRM LOGI | PENDING REASON | Waiting: Customer needs to confirm logistic details | CS | CS |  |
| CUSTOMERS | CWNC | CWNC - CUSTOMER WRONG NOT COMPLIANT | PENDING REASON | Customer had previous orders(s) on CWPP and was contacted to amend, but failed to do so for the next order. | CC&T | CC&T |  |
| CUSTOMERS | CWNP | CWNP - CUSTOMER NO PRICE | PENDING REASON | Customer ordering without pricing | CS + CC&T | CS + CC&T |  |
| CUSTOMERS | CWNPO | CWNPO - CUSTOMER WRONG NO PO | PENDING REASON | Installation Customer did not present a Purchase order | CS | CS |  |
| CUSTOMERS | CWPA | CWPA - CUSTOMER WRONG ADDRESS | PENDING REASON | Missing address or wrong address - for some customers, we know that the billing address is X, but customers keep putting Y | CS | CS |  |
| CUSTOMERS | CWPF | CWPF - CUSTOMER WRONG FORM | PENDING REASON | DACH Specific ! Customer is still using the old order form template. | CS + CC&T | CC&T |  |
| CUSTOMERS | CWPI | CWPI - CUSTOMER WRONG ITEM CODE | PENDING REASON | Customer Using superseded/non existing item codes | CS + CC&T | CS + CC&T |  |
| CUSTOMERS | CWPP | CWPP - CUSTOMER WRONG PRICE | PENDING REASON | Prices on PO not matching Oracle | CS + CC&T | CS + CC&T |  |
| CUSTOMERS | CWPT | CWPO - CUSTOMER WRONG TEMPLATE | PENDING REASON | Customer is sending a PO template that can't be read (too light, too dark, handwriting not clear,...) | CS | CS |  |
| CUSTOMERS | CWPU | CWPU - CUSTOMER WRONG UNIT | PENDING REASON | Customer ordering in units (i.e. brushes, one box is 500 units) instead of boxes as per contract | CS + CC&T | CS |  |
| CUSTOMERS | CWPV | CWPV - CUSTOMER WRONG VAT | PENDING REASON | Prices on PO with VAT included - Oracle is looking for the price as per contract, so without VAT | CS + CC&T | CS |  |
| CUSTOMERS | CWSP | CWSP - CUSTOMER SPARE SERVICE OPS | PENDING REASON | PO parts are spare parts and were not loaded on the BSA | CC&T | CC&T |  |
| CUSTOMER DATA | DNA | DNA - DT NEW / AMEND ADDRESS | PENDING REASON | A new shipping/billing address needs to be set up in Oracle or Existing address is incorrect and needs to be adjusted | CS | CS |  |
| CUSTOMER DATA | DNR | DNR - DT NEW RELATIONSHIP / ACCOUNT | PENDING REASON | A relationship between 2 accounts might require extra information needed by CDQ (Sales contact) | CS | CS |  |
| CUSTOMER DATA | DWA | DWA - DT WRONG ACCOUNT | PENDING REASON | CS chose wrong bill/sold-to account(misleading account/PO /understanding from stakeholders (= sales, CS, CC&T, Pricing/Data team, customer)-> price query. | CC&T | CS |  |
| EDI | EDE | EDE - EDI ERROR | PENDING REASON | GHX (GFAX) pushed the order through incorrectly | CS | CS |  |
| EDI | EDL | EDL - EDI LATE | PENDING REASON | PO arrived / pushed through into the system after 16h | CS | CS |  |
| EDI | EDM | EDM - EDI WRONG MAPPING |  | EDI wrong due to incorrect mapping by CS or CC&T | CS + CC&T | CS + CC&T |  |
| EDI | EDS | EDS - EDI SPLIT | The PO got split in 2. One part went through ticketing and the other one through EDI touchless. | The PO got split in 2. One part went through ticketing and the other one through EDI touchless. | CS + CC&T | CS + CC&T |  |
| FINANCE | FCC | FCC - FINANCE CREDIT CHECK | PENDING REASON | Customer order is automatically put on hold in Oracle (Payment). | CS | CS |  |
| MANUAL OVERRIDE | MONP | MONP - NO PRICE LIST | PENDING REASON | No price list available, causing incorrect pricing | CS | CS |  |
| MANUAL OVERRIDE | MOPL | MOPL - FOC PRICE LIST | PENDING REASON | CS Manual override for item that is FOC, but is showing a price due to CDQ Price List adjustment remove all FOC | CS | CS |  |
| MANUAL OVERRIDE | MOPM | MOPM - FOC PROMO MODIFIER | PENDING REASON | CS Manual override for item that is FOC, but is showing a price due to promo modifier | CS | CS |  |
| MANUAL OVERRIDE | MOU | MOU - URGENT NO PRICE | PENDING REASON | CS Manual override because the price was incorrect in the system, but needed urgent shipment, so could not wait for the resolution | CS | CS |  |
| PRICE QUERY | PRQ | PRQ - PRICE QUERY | PENDING REASON | Price between Oracle and Customer PO does not match. Next step is for Sales Support to identify root cause and adjust Reason Code  on the order. See tab reason codes for sales support. | CS | CC&T |  |
| PRICING TEAM | PTBA | PTBA - PT BSA AUTOMATIC | PENDING REASON | A BSA is applicable, but not triggered or multiple BSA's are possible, but none are correct or triggered | CC&T | CC&T |  |
| CUSTOMERS | PTNP | PTNP - PT NEW PRICING | PENDING REASON | Pricing was not set up yet e.g. pre-load not possible/no signed contract received by customer | CC&T | CC&T |  |
| PRICING TEAM | PTPI | PTPI - PT PRICE INCREASE SET UP | PENDING REASON | Price increase not set up | CC&T | CC&T |  |
| PRICING TEAM | PTWP | PTWP - PT WRONG PRICING | PENDING REASON | Pricing was set up incorrectly or with delay or FOC list price issue without manual override | CC&T | CC&T |  |
| RETURNS | RCE | RCE - CUST ERROR - UOM | PENDING REASON | Customer is ordering the EA quantity and not the ordereable quantity (ex. 3 X NS2013 instead of 1 | CS | CS |  |
| REGULATORY AND COMPLIANCE | REC | REC - RA EXPORT COMPLIANCE HOLD | PENDING REASON | Items blocked by export compliance hold in Oracle. | CS | CS |  |
| RETURNS | RIN | RIN - INVESTIGATION NEEDED | PENDING REASON | This return was created by another department and needs actioning/investigation | CS | CS |  |
| SALES | SAC | SAC - SALES APPS CONFIG | PENDING REASON | Sales Application needs to confirm the configuration split of KITS (Africa only) | CS | CS |  |
| STOCK | SAL | SAL - STOCK ALLOCATION | PENDING REASON | Item is not available and stays in ready to release status. | CS | CS |  |
| STOCK | SAP | SAP - STOCK APPROVAL | PENDING REASON | Item is either in short-shelf life or needs to be approved by Upper Management. | CS | CS |  |
| STOCK | SBA | SBA - STOCK ALTERNATIVE ITEM | PENDING REASON | Item is not in stock, and CS is waiting for the customer to send adjusted PO for alternative item | CS | CS |  |
| SALES | SBC | SBC - SALES BOOK CONFIRMATION | PENDING REASON | Order is in entered, we need confirmation from sales to book | CS | CS |  |
| STOCK | SBO | SBO - STOCK BACKORDER | PENDING REASON | Master Lot item is on backorder, CS already checked and is waiting for stock | CS | CS |  |
| SALES | SBR | SBR - SALES BUSINESS RULES | PENDING REASON | Contract set-up not compliant with system ->automated pricing not possible or manual adjustment/tracking required to book the order | CC&T | CC&T |  |
| SALES | SCPR | SCPR - SALES CPR | PENDING REASON | CPR orders in entered status and to be approved by Sales to book | CS | CS |  |
| SALES | SEC | SEC - SALES EXPIRED CONTRACT | PENDING REASON | Sales haven’t provided a signed contract. Note: this doesnotbecome SNC after a certain period. | CC&T | CC&T |  |
| SALES | SMI | SMI - SALES MISSING ITEM | PENDING REASON | Priced item / FOC item is missing from the contract / sales provided additional/alternative item codes to customer outside of contract | CC&T | CC&T |  |
| SALES | SNC | SNC - SALES NO CONTRACT | PENDING REASON | No contract at all, item has never been quoted. | CC&T | CC&T |  |
| SALES | SPI | SPI - SALES PRICE INCREASE | PENDING REASON | Price increase project causing price discrepancies in Oracle | CC&T | CC&T |  |
| CC&T | SSM | SSM - SALES SUPPORT MISS | PENDING REASON | Sales Support Missed to add certain items on thee BSA form / missed to send the full BSA form | CC&T | CC&T |  |
| THIRD PARTY | TPI | TPI - INTEGRATION | PENDING REASON | ! Only use this reason code for orders that are entered and can't be booked, related to an integration project | CS | CS |  |
| THIRD PARTY | TPM | TPM - MASTER DATA | PENDING REASON | Master Data (item etc..) not set up yet/correctly | CS | CS |  |
| THIRD PARTY | TPS | TPS - SYSTEM ERROR | PENDING REASON | ! Only use for Oracle related issue, that needs IT. E.g. BSA doesn't trigger because request date in future, but ship date within contract time. | CS + CC&T | CS + CC&T |  |
| THIRD PARTY | TPSA | TPSA - SITE ASSESSMENT | PENDING REASON | Installation Site asssessment is missing or incorrect | CS | CS |  |
| CUSTOMER DATA | DFR | DFR - DATA WRONG FREIGHT | PENDING REASON | Freight has charged/not charged or with the wrong amount as per customer terms | CC&T | CC&T |  |

## Verification Oracle set-up

| Code | ShortCode | LookupCodeMeaning | Description | LookupCodeDescription | Tag | Effective Date: From | Effective Date: To | Enabled | Title | Title | Use | Use | Owner | Owner | Usedby | UsedBy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CNAL | CNAL | CNAL | CNAL-ALBARAN | CNAL-ALBARAN | 45942 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNAS | CNAS | CNAS | CNAS-CSERROR-ACCOUNTSETUP | CNAS-CSERROR-ACCOUNTSETUP | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNCO | CNCO | CNCO | CNCO-COVID | CNCO-COVID | 45942 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CND | CND | CND | CND-CSERROR-DUPLICATEORDER | CND-CSERROR-DUPLICATEORDER | 45944 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNE | CNE | CNE | CNE-CSERROR-BILLTO | CNE-CSERROR-BILLTO | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNEP | CNEP | CNEP | CNEP-CSERROR-WRONGPRICING | CNEP-CSERROR-WRONGPRICING | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNEX | CNEX | CNEX | CNEX-EXPIRYDATE | CNEX-EXPIRYDATE | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNFB | CNFB | CNFB | CNFB-FINANCECREDITBOOKHOLD | CNFB-FINANCECREDITBOOKHOLD | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNFO | CNFO | CNFO | CNFO-FOC | CNFO-FOC | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNFR | CNFR | CNFR | CNFR-FREIGHT/HANDLINGCOST | CNFR-FREIGHT/HANDLINGCOST | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNM | CNM | CNM | CNM-MISSINGDELIVERY | CNM-MISSINGDELIVERY | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNPI | CNPI | CNPI | CNPI-PRICEINCREASE | CNPI-PRICEINCREASE | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNPT | CNPT | CNPT | CNPT-PRICINGTEAMERROR | CNPT-PRICINGTEAMERROR | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CNQ | CNQ | CNQ | CNQ-CSERROR-QUANTITY | CNQ-CSERROR-QUANTITY | 45951 | * | CREDITNOTES | CREDITNOTES | On Credit order type | On Credit order type | CS | CS | CS | CS |  |  |
| CSC | CSC | CSC | CSC-CSCHECK | CSC-CSCHECK | 45942 | * | CUSTOMERSERVICE | CUSTOMERSERVICE | CS needs to verify/check | CS needs to verify/check | CS | CS | CS | CS |  |  |
| CSE | CSE | CSE | CSE-CSERROR | CSE-CSERROR | 45951 | * | CUSTOMERSERVICE | CUSTOMERSERVICE | CS made an error, preventing possibility to book | CS made an error, preventing possibility to book | CS | CS | CS+CC&T | CS+CC&T |  |  |
| CSL | CSL | CSL | CSL-CUST SH.SH.LIFE | CSL-CUST SH.SH.LIFE | 45951 | * | CUSTOMERS | CUSTOMERS | Customer requires a specific Shelf Life, CS is waiting for their approval | Customer requires a specific Shelf Life, CS is waiting for their approval | CS | CS | CS | CS |  |  |
| CSM | CSM | CSM | CSM-CSMISS | CSM-CSMISS | 45951 | * | CUSTOMERSERVICE | CUSTOMERSERVICE | CS missed to book the order same day | CS missed to book the order same day | CS | CS | CS+CC&T | CS+CC&T |  |  |
| CSN | CSN | CSN | CSN-CSNEWHIRE | CSN-CSNEWHIRE | 45951 | * | CUSTOMERSERVICE | CUSTOMERSERVICE | CS new hire entered an order that still requires checking by more senior CS | CS new hire entered an order that still requires checking by more senior CS | CS | CS | CS | CS |  |  |
| CTA | CTA | CTA | CTA-APPROVALTOSHIP | CTA-APPROVALTOSHIP | 45951 | * | CUSTOMS | CUSTOMS | Awaiting approval to ship related to customs clearance | Awaiting approval to ship related to customs clearance | CS | CS | CS | CS |  |  |
| CTI | CTI | CTI | CTI-CUSTOMSITTQ | CTI-CUSTOMSITTQ | 45942 | * | CUSTOMS | CUSTOMS | Awaiting approval from Legal/Regulatory or Compliance for IITQ | Awaiting approval from Legal/Regulatory or Compliance for IITQ | CS | CS | CS | CS |  |  |
| CWBP | CWBP | CWBP | CWBP-CUSTOMERWRONGBANDEDPRICING | CWBP-CUSTOMERWRONGBANDEDPRICING | 45951 | * | CUSTOMERS | CUSTOMERS | UK only ! Customer is on banded pricing (1-2-3) | UK only ! Customer is on banded pricing (1-2-3) | CC&T | CC&T | CC&T | CC&T |  |  |
| CWDC | CWDC | CWDC | CWDC-CUST CHANGE/DELAY/CANCELLATION | CWDC-CUST CHANGE/DELAY/CANCELLATION | 45951 | * | CUSTOMERS | CUSTOMERS | Waiting: Customer requested delay in shipment, check-up required to cancel or ship order or requested a change and check is required before booking | Waiting: Customer requested delay in shipment, check-up required to cancel or ship order or requested a change and check is required before booking | CS | CS | CS | CS |  |  |
| CWLC | CWLC | CWLC | CWLC-CUSTWAITLC | CWLC-CUSTWAITLC | 45951 | * | CUSTOMERS | CUSTOMERS | Waiting: Customer needs to provide LC document | Waiting: Customer needs to provide LC document | CS | CS | CS | CS |  |  |
| CWLO | CWLO | CWLO | CWLO-CUSTCONFIRMLOGI | CWLO-CUSTCONFIRMLOGI | 45951 | * | CUSTOMERS | CUSTOMERS | Waiting: Customer needs to confirm logistic details | Waiting: Customer needs to confirm logistic details | CS | CS | CS | CS |  |  |
| CWNC | CWNC | CWNC | CWNC-CUSTOMERWRONGNOTCOMPLIANT | CWNC-CUSTOMERWRONGNOTCOMPLIANT | 45951 | * | CUSTOMERS | CUSTOMERS | Customer had previous orders(s) on CWPP and was contacted to amend, but failed to do so for the next order. | Customer had previous orders(s) on CWPP and was contacted to amend, but failed to do so for the next order\ | CC&T | CC&T | CC&T | CC&T |  |  |
| CWNP | CWNP | CWNP | CWNP-CUSTOMERNOPRICE | CWNP-CUSTOMERNOPRICE | 45951 | * | CUSTOMERS | CUSTOMERS | Customer ordering without pricing | Customer ordering without pricing | CS+CC&T | CS+CC&T | CS+CC&T | CS+CC&T |  |  |
| CWNPO | CWNPO | CWNPO | CWNPO-CUSTOMERWRONGNOPO | CWNPO-CUSTOMERWRONGNOPO | 45951 | * | CUSTOMERS | CUSTOMERS | Installation Customer did not present a Purchase order | Installation Customer did not present a Purchase order | CS | CS | CS | CS |  |  |
| CWPA | CWPA | CWPA | CWPA-CUSTOMERWRONGADDRESS | CWPA-CUSTOMERWRONGADDRESS | 45951 | * | CUSTOMERS | CUSTOMERS | Missing address or wrong address - for some customers, we know that the billing address is X, but customers keep putting Y | Missing address or wrong address - for some customers, we know that the billing address is X, but customers keep putting Y | CS | CS | CS | CS |  |  |
| CWPF | CWPF | CWPF | CWPF-CUSTOMERWRONGFORM | CWPF-CUSTOMERWRONGFORM | 45951 | * | CUSTOMERS | CUSTOMERS | DACH Specific ! Customer is still using the old order form template. | DACH Specific ! Customer is still using the old order form template\ | CC&T | CC&T | CS+CC&T | CS+CC&T |  |  |
| CWPI | CWPI | CWPI | CWPI-CUSTOMERWRONGITEMCODE | CWPI-CUSTOMERWRONGITEMCODE | 45942 | * | CUSTOMERS | CUSTOMERS | Customer Using superseded/non existing item codes | Customer Using superseded/non existing item codes | CS+CC&T | CS+CC&T | CS+CC&T | CS+CC&T |  |  |
| CWPP | CWPP | CWPP | CWPP-CUSTOMERWRONGPRICE | CWPP-CUSTOMERWRONGPRICE | 45951 | * | CUSTOMERS | CUSTOMERS | Prices on PO not matching Oracle | Prices on PO not matching Oracle | CS+CC&T | CS+CC&T | CS+CC&T | CS+CC&T |  |  |
| CWPT | CWPT | CWPT | CWPO-CUSTOMERWRONGTEMPLATE | CWPO-CUSTOMERWRONGTEMPLATE | 45951 | * | CUSTOMERS | CUSTOMERS | Customer is sending a PO template that can't be read (too light, too dark, handwriting not clear,...) | Customer is sending a PO template that can't be read (too light, too dark, handwriting not clear,\ | CS | CS | CS | CS |  |  |
| CWPU | CWPU | CWPU | CWPU-CUSTOMERWRONGUNIT | CWPU-CUSTOMERWRONGUNIT | 45951 | * | CUSTOMERS | CUSTOMERS | Customer ordering in units (i.e. brushes, one box is 500 units) instead of boxes as per contract | Customer ordering in units (i\ brushes, one box is 500 units) instead of boxes as per contract | CS | CS | CS+CC&T | CS+CC&T |  |  |
| CWPV | CWPV | CWPV | CWPV-CUSTOMERWRONGVAT | CWPV-CUSTOMERWRONGVAT | 45951 | * | CUSTOMERS | CUSTOMERS | Prices on PO with VAT included - Oracle is looking for the price as per contract, so without VAT | Prices on PO with VAT included - Oracle is looking for the price as per contract, so without VAT | CS | CS | CS+CC&T | CS+CC&T |  |  |
| CWSP | CWSP | CWSP | CWSP-CUSTOMERSPARESERVICEOPS | CWSP-CUSTOMERSPARESERVICEOPS | 45951 | * | CUSTOMERS | CUSTOMERS | PO parts are spare parts and were not loaded on the BSA | PO parts are spare parts and were not loaded on the BSA | CC&T | CC&T | CC&T | CC&T |  |  |
| DNA | DNA | DNA | DNA-DTNEW/AMENDADDRESS | DNA-DTNEW/AMENDADDRESS | 45942 | * | CUSTOMERDATA | CUSTOMERDATA | A new shipping/billing address needs to be set up in Oracle or Existing address is incorrect and needs to be adjusted | A new shipping/billing address needs to be set up in Oracle or Existing address is incorrect and needs to be adjusted | CS | CS | CS | CS |  |  |
| DNR | DNR | DNR | DNR-DTNEWRELATIONSHIP/ACCOUNT | DNR-DTNEWRELATIONSHIP/ACCOUNT | 45951 | * | CUSTOMERDATA | CUSTOMERDATA | A relationship between 2 accounts might require extra information needed by CDQ (Sales contact) | A relationship between 2 accounts might require extra information needed by CDQ (Sales contact) | CS | CS | CS | CS |  |  |
| DWA | DWA | DWA | DWA-DTWRONGACCOUNT | DWA-DTWRONGACCOUNT | 45951 | * | CUSTOMERDATA | CUSTOMERDATA | CS chose wrong bill/sold-to account(misleading account/PO /understanding from stakeholders (= sales, CS, CC&T, Pricing/Data team, customer)-> price query. | CS chose wrong bill/sold-to account(misleading account/PO /understanding from stakeholders | CS | CS | CC&T | CC&T |  |  |
| EDE | EDE | EDI | EDE-EDIERROR | EDE-EDIERROR | 45951 | * | EDI | EDI | GHX (GFAX) pushed the order through incorrectly | GHX (GFAX) pushed the order through incorrectly | CS | CS | CS | CS |  |  |
| EDL | EDL | EDL | EDL-EDILATE | EDL-EDILATE | 45942 | * | EDI | EDI | PO arrived / pushed through into the system after 16h | PO arrived / pushed through into the system after 16h | CS | CS | CS | CS |  |  |
| EDM | EDM | EDM | EDM-EDIWRONGMAPPING | EDM-EDIWRONGMAPPING | 45952 | * | EDI | EDI | EDI wrong due to incorrect mapping by CS or CC&T | EDI wrong due to incorrect mapping by CS or CC&T | CS+CC&T | CS+CC&T | CS+CC&T | CS+CC&T |  |  |
| EDS | EDS | EDS | EDS-EDISPLIT | EDS-EDISPLIT | 45952 | * | EDI | EDI | The PO got split in 2. One part went through ticketing and the other one through EDI touchless. | The PO got split in 2\ One part went through ticketing and the other one through EDI touchless\ | CS+CC&T | CS+CC&T | CS+CC&T | CS+CC&T |  |  |
| PRQ | PRQ | PRQ | PRQ-PRICEQUERY | PRQ-PRICEQUERY | 45951 | * | PRICEQUERY | PRICEQUERY | Price between Oracle and Customer PO does not match. Next step is for Sales Support to identify root cause and adjust Reason Code  on the order. See tab reason codes for sales support. | Customer is ordering the EA quantity and not the ordereable quantity (ex\ 3 X NS2013 instead of 1 | CC&T | CC&T | CS | CS |  |  |
| PTBA | PTBA | PTBA | PTBA-PTBSAAUTOMATIC | PTBA-PTBSAAUTOMATIC | 45951 | * | PRICINGTEAM | PRICINGTEAM | A BSA is applicable, but not triggered or multiple BSA's are possible, but none are correct or triggered | Items blocked by export compliance hold in Oracle\ | CC&T | CC&T | CC&T | CC&T |  |  |
| PTNP | PTNP | PTNP | PTNP-PTNEWPRICING | PTNP-PTNEWPRICING | 45951 | * | CUSTOMERS | PRICINGTEAM | Pricing was not set up yet e.g. pre-load not possible/no signed contract received by customer | This return was created by another department and needs actioning/investigation | CC&T | CC&T | CC&T | CC&T |  |  |
| PTPI | PTPI | PTPI | PTPI-PTPRICEINCREASESETUP | PTPI-PTPRICEINCREASESETUP | 45951 | * | PRICINGTEAM | PRICINGTEAM | Price increase not set up | Sales Application needs to confirm the configuration split of KITS (Africa only) | CC&T | CC&T | CC&T | CC&T |  |  |
| PTWP | PTWP | PTWP | PTWP-PTWRONGPRICING | PTWP-PTWRONGPRICING | 45952 | * | PRICINGTEAM | PRICINGTEAM | Pricing was set up incorrectly or with delay or FOC list price issue without manual override | Item is not available and stays in ready to release status\ | CC&T | CC&T | CC&T | CC&T |  |  |
| RCE | RCE | RCE | RCE-CUSTERROR-UOM | RCE-CUSTERROR-UOM | 45952 | * | RETURNS | RETURNS | Customer is ordering the EA quantity and not the ordereable quantity (ex. 3 X NS2013 instead of 1 | Item is either in short-shelf life or needs to be approved by Upper Management\ | CS | CS | CS | CS |  |  |
| REC | REC | REC | REC-RA EXPORTCOMPLIANCEHOLD | REC-RA EXPORTCOMPLIANCEHOLD | 45952 | * | REGULATORYANDCOMPLIANCE | REGULATORYANDCOMPLIANCE | Items blocked by export compliance hold in Oracle. | Item is not in stock, and CS is waiting for the customer to send adjusted PO for alternative item | CS | CS | CS | CS |  |  |
| RIN | RIN | RIN | RIN-INVESTIGATIONNEEDED | RIN-INVESTIGATIONNEEDED | 45951 | * | RETURNS | RETURNS | This return was created by another department and needs actioning/investigation | Order is in entered, we need confirmation from sales to book | CS | CS | CS | CS |  |  |
| SAC | SAC | SAC | SAC-SALESAPPSCONFIG | SAC-SALESAPPSCONFIG | 45952 | * | SALES | SALES | Sales Application needs to confirm the configuration split of KITS (Africa only) | Master Lot item is on backorder, CS already checked and is waiting for stock | CS | CS | CS | CS |  |  |
| SAL | SAL | SAL | SAL-STOCK ALLOCATION | SAL-STOCK ALLOCATION | 45952 | * | STOCK | STOCK | Item is not available and stays in ready to release status. | Contract set-up not compliant with system ->automated pricing not possible or manual adjustment/tracking required to book the order | CS | CS | CS | CS |  |  |
| SAP | SAP | SAP | SAP-STOCKAPPROVAL | SAP-STOCKAPPROVAL | 45952 | * | STOCK | STOCK | Item is either in short-shelf life or needs to be approved by Upper Management. | CPR orders in entered status and to be approved by Sales to book | CS | CS | CS | CS |  |  |
| SBA | SBA | SBA | SBA-STOCKALTERNATIVEITEM | SBA-STOCKALTERNATIVEITEM | 45952 | * | STOCK | STOCK | Item is not in stock, and CS is waiting for the customer to send adjusted PO for alternative item | Sales haven’t provided a signed contract\ Note: this does not become SNC after a certain period\ | CS | CS | CS | CS |  |  |
| SBC | SBC | SBC | SBC-SALESBOOKCONFIRMATION | SBC-SALESBOOKCONFIRMATION | 45952 | * | SALES | SALES | Order is in entered, we need confirmation from sales to book | Priced item / FOC item is missing from the contract / sales provided additional/alternative item codes to customer outside of contract | CS | CS | CS | CS |  |  |
| SBO | SBO | SBO | SBO-STOCKBACKORDER | SBO-STOCKBACKORDER | 45952 | * | STOCK | STOCK | Master Lot item is on backorder, CS already checked and is waiting for stock | No contract at all, item has never been quoted\ | CS | CS | CS | CS |  |  |
| SBR | SBR | SBR | SBR-SALESBUSINESSRULES | SBR-SALESBUSINESSRULES | 45952 | * | SALES | SALES | Contract set-up not compliant with system ->automated pricing not possible or manual adjustment/tracking required to book the order | Price increase project causing price discrepancies in Oracle | CC&T | CC&T | CC&T | CC&T |  |  |
| SCPR | SCPR | SCPR | SCPR-SALESCPR | SCPR-SALESCPR | 45952 | * | SALES | SALES | CPR orders in entered status and to be approved by Sales to book | Sales Support Missed to add certain items on thee BSA form / missed to send the full BSA form | CS | CS | CS | CS |  |  |
| SEC | SEC | SEC | SEC-SALESEXPIREDCONTRACT | SEC-SALESEXPIREDCONTRACT | 45952 | * | SALES | SALES | Sales haven’t provided a signed contract. Note: this doesnotbecome SNC after a certain period. | ! Only use this reason code for orders that are entered and can't be booked, related to an integration project | CC&T | CC&T | CC&T | CC&T |  |  |
| SMI | SMI | SMI | SMI-SALESMISSINGITEM | SMI-SALESMISSINGITEM | 45952 | * | SALES | SALES | Priced item / FOC item is missing from the contract / sales provided additional/alternative item codes to customer outside of contract | Master Data (item etc\) not set up yet/correctly | CC&T | CC&T | CC&T | CC&T |  |  |
| SNC | SNC | SNC | SNC-SALESNOCONTRACT | SNC-SALESNOCONTRACT | 45952 | * | SALES | SALES | No contract at all, item has never been quoted. | ! Only use for Oracle related issue, that needs IT\ BSA doesn't trigger because request date in future, but ship date within contract time\ | CC&T | CC&T | CC&T | CC&T |  |  |
| SPI | SPI | SPI | SPI-SALESPRICEINCREASE | SPI-SALESPRICEINCREASE | 45952 | * | SALES | SALES | Price increase project causing price discrepancies in Oracle | Installation Site asssessment is missing or incorrect | CC&T | CC&T | CC&T | CC&T |  |  |
| SSM | SSM | SSM | SSM-SALESSUPPORTMISS | SSM-SALESSUPPORTMISS | CC&T | CC&T | Sales Support Missed to add certain items on thee BSA form / missed to send the full BSA form | CC&T | CC&T | CC&T | CC&T |  |  |  |  |  |
| TPI | TPI | TPI | TPI-INTEGRATION | TPI-INTEGRATION | THIRDPARTY | THIRDPARTY | ! Only use this reason code for orders that are entered and can't be booked, related to an integration project | CS | CS | CS | CS |  |  |  |  |  |
| TPM | TPM | TPM | TPM-MASTERDATA | TPM-MASTERDATA | THIRDPARTY | THIRDPARTY | Master Data (item etc..) not set up yet/correctly | CS | CS | CS | CS |  |  |  |  |  |
| TPS | TPS | TPS | TPS-SYSTEMERROR | TPS-SYSTEMERROR | THIRDPARTY | THIRDPARTY | ! Only use for Oracle related issue, that needs IT. E.g. BSA doesn't trigger because request date in future, but ship date within contract time. | CS+CC&T | CS+CC&T | CS+CC&T | CS+CC&T |  |  |  |  |  |
| TPSA | TPSA | TPSA | TPSA-SITEASSESSMENT | TPSA-SITEASSESSMENT | THIRDPARTY | THIRDPARTY | Installation Site asssessment is missing or incorrect | CS | CS | CS | CS |  |  |  |  |  |