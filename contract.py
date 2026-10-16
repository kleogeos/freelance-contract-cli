#!/usr/bin/env python3
"""Generate a plain-language freelance services agreement (HTML) from a JSON file. Zero dependencies."""
import argparse
import html
import json
import sys

DISCLAIMER = (
    "This is a general-purpose template, not legal advice. It covers the basics "
    "(scope, payment, IP, termination) for straightforward freelance work. For "
    "complex, high-value, or cross-border engagements, have a licensed attorney "
    "in your jurisdiction review or draft the agreement instead."
)


def esc(s):
    return html.escape(str(s))


def render(data):
    freelancer = data["freelancer"]
    client = data["client"]
    scope = data.get("scope", [])
    payment_amount = data.get("payment_amount")
    payment_terms = data.get("payment_terms", "")
    start_date = data.get("start_date", "")
    end_date = data.get("end_date", "")
    ip_clause = data.get("ip_ownership", "client")
    termination_days = data.get("termination_notice_days", 14)
    governing_law = data.get("governing_law", "")

    scope_items = "\n".join(f"<li>{esc(s)}</li>" for s in scope) or "<li>(scope to be filled in)</li>"

    if ip_clause == "client":
        ip_text = (
            "Upon full payment, all work product created specifically for this "
            "engagement transfers to the Client. Pre-existing tools, libraries, "
            "and generic know-how of the Freelancer remain the Freelancer's property."
        )
    elif ip_clause == "freelancer":
        ip_text = (
            "The Freelancer retains ownership of the work product. The Client "
            "receives a non-exclusive, perpetual license to use it for its intended purpose."
        )
    else:
        ip_text = esc(ip_clause)

    payment_line = f"{payment_amount}" if payment_amount is not None else "(amount to be filled in)"

    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Services Agreement — {esc(freelancer)} & {esc(client)}</title>
<style>
body{{font-family:-apple-system,Arial,sans-serif;max-width:680px;margin:40px auto;color:#1a1a1a;line-height:1.5}}
h1{{font-size:22px}}
h2{{font-size:16px;margin-top:28px;color:#333}}
.meta{{color:#666;font-size:14px}}
.disclaimer{{background:#fff8e6;border:1px solid #f0d58c;border-radius:6px;padding:12px 16px;font-size:13px;color:#664d03;margin-top:24px}}
.sig{{margin-top:40px;display:flex;gap:40px}}
.sig div{{flex:1;border-top:1px solid #999;padding-top:6px;font-size:13px;color:#666}}
@media print{{body{{margin:0}} .disclaimer{{background:none}}}}
</style></head><body>
<h1>Services Agreement</h1>
<p class="meta">Between <b>{esc(freelancer)}</b> ("Freelancer") and <b>{esc(client)}</b> ("Client")<br>
{"Start: " + esc(start_date) if start_date else ""}{" &middot; End: " + esc(end_date) if end_date else ""}</p>

<h2>1. Scope of work</h2>
<ul>{scope_items}</ul>

<h2>2. Payment</h2>
<p>Total fee: {esc(payment_line)}.<br>{esc(payment_terms) if payment_terms else "Payment terms to be agreed in writing before work begins."}</p>

<h2>3. Intellectual property</h2>
<p>{ip_text}</p>

<h2>4. Termination</h2>
<p>Either party may terminate this agreement with {esc(termination_days)} days' written notice. The Freelancer will be paid for all work completed up to the termination date.</p>

<h2>5. Confidentiality</h2>
<p>Each party agrees to keep the other's confidential business information private, both during and after this engagement.</p>

{"<h2>6. Governing law</h2><p>This agreement is governed by the laws of " + esc(governing_law) + ".</p>" if governing_law else ""}

<div class="sig">
<div>{esc(freelancer)}<br>Date: ____________</div>
<div>{esc(client)}<br>Date: ____________</div>
</div>

<p class="disclaimer">{esc(DISCLAIMER)}</p>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="JSON contract file (see example.json)")
    ap.add_argument("-o", "--output", help="output HTML file (default: stdout)")
    args = ap.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    for required in ("freelancer", "client"):
        if required not in data:
            print(f"error: missing required field '{required}'", file=sys.stderr)
            sys.exit(1)

    out = render(data)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
