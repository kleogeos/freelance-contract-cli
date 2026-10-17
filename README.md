# freelance-contract-cli

![Test CLI](https://github.com/kleogeos/freelance-contract-cli/actions/workflows/test.yml/badge.svg)

Generate a plain-language, print-ready freelance services agreement (HTML) from a JSON file. No dependencies, no sign-up, no SaaS account.

```bash
python3 contract.py example.json -o contract.html
```

Produces a one-page agreement: scope of work, payment terms, IP ownership, termination notice, confidentiality, and a signature block — ready to open in a browser, review together, and print to PDF or sign.

### Install (optional)

```bash
pip install git+https://github.com/kleogeos/freelance-contract-cli
freelance-contract example.json -o contract.html
```

### JSON format

```json
{
  "freelancer": "Your name",
  "client": "Client name",
  "start_date": "2026-11-01",
  "end_date": "2026-12-15",
  "scope": ["Task one", "Task two"],
  "payment_amount": "$3,200 total, 50% deposit, 50% on delivery",
  "payment_terms": "Invoiced on delivery. Net 14.",
  "ip_ownership": "client",
  "termination_notice_days": 14,
  "governing_law": "the State of California"
}
```

Only `freelancer` and `client` are required; everything else is optional and has a sensible default or placeholder.

`ip_ownership` accepts `"client"` (default — work product transfers to the client on full payment), `"freelancer"` (client gets a non-exclusive license instead), or any custom string to use as the clause verbatim.

### Is this legal advice?

No. This is a general-purpose template covering the basics of straightforward freelance work. For complex, high-value, or cross-border engagements, have a licensed attorney in your jurisdiction review or draft the agreement instead. The generated document says so too, right above the signature block. For a plain-language breakdown of which clauses actually matter and why, see [How to Write a Freelance Contract](https://kleogeos.github.io/freelancer-tools/how-to-write-a-freelance-contract.html?src=cli-contract-howto).

### Where this fits

Send a [proposal](https://github.com/kleogeos/freelance-proposal-cli) → get it signed with this → track the work with [freelance-time-cli](https://github.com/kleogeos/freelance-time-cli) → turn the hours into an invoice with [freelance-timesheet-to-invoice-cli](https://github.com/kleogeos/freelance-timesheet-to-invoice-cli) and [freelance-invoice-cli](https://github.com/kleogeos/freelance-invoice-cli). Before signing anything, you can also run the terms through [contract-checklist-cli](https://github.com/kleogeos/contract-checklist-cli) to catch common missing clauses.

Want a more complete set of clauses (confidentiality carve-outs, IP assignment variants, non-compete) plus a matching proposal and invoice template already laid out? See the [Freelancer Starter Kit](https://kleogeos.github.io/freelancer-tools/kit.html?src=cli-contract).

## Tests

```bash
python3 test_contract.py
```
