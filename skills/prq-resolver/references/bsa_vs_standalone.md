<!-- Slide 1 -->
# Context
In EMEA, pricing agreements in Oracle can be created using two methods:
BSA (Blanket Sales Agreement)
Standalone Price Modifiers
Choosing the wrong agreement type at the start can lead to several issues:
⚠️Incorrect pricing triggers(PTWP - PT WRONG PRICINGprice queries)
⚠️Order processing delaysand additional price‑related queries
⚠️Extra work for the Pricing Team(agreement termination + recreation)
⚠️ Customer impact due to order holds and manual corrections
Before submitting any setup request to the Pricing Team:
✅Always review the flowchart on the next slideto ensure you select the correct agreement type.

<!-- Slide 2 -->
# Use this flowchart to determine whether your request should follow a BSA setup or a Standalone Price Modifier setup.
<!-- image: Picture 2 (slide 2) -->

<!-- Slide 3 -->
# Use a BSA when:
There isone unique Bill-Tocustomer (Ship-To accounts may vary but must belinkedin Oracle/H1)
Contract pricing isnot restricted to specific Bill-To / Ship-To combinations
It concerns abuying group, where:
multiple customers share the same pricing
each customer pays their own invoices
each customer has its own volume commitment
→ therefore each requires its own BSA
A BSA provides the following capabilities:
✅ Commitment tracking (via the Fulfillment section)
✅ Grace period triggering
✅ Auto-renew functionality
✅ Attachment storage (PRF, pricing documents, internal notes)

<!-- Slide 4 -->
# Use a Standalone Price Modifier when:
Pricing applies tomultiple and specific Bill-To / Ship-To combinations
The account structure is too complex to manage under a single customer‑level BSA
Standalone modifiers doNOT support:
❌ Commitment tracking
❌ Grace period triggering
❌ Auto-renewal
❌ Attachment storage (PRF, pricing documents, comments)