import requests
import json
from urllib.parse import urlencode

# Found accurate company names using partial string searches from a local script/API requests earlier or just by logic
COMPANIES = [
    "CARRINGTON MORTGAGE SERVICES, LLC",
    "PENNYMAC LOAN SERVICES, LLC.",
    "LoanCare, LLC",
    "M&T BANK CORPORATION",
    "Shellpoint Partners, LLC",
    "McCarthy & Holthus, LLP"
]

def search_complaints():
    base_url = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"

    results = {}

    for company in COMPANIES:
        params = {
            "company": company,
            "product": "Mortgage",
            "size": 0,
            "agg": "issue"
        }

        url = base_url + "?" + urlencode(params)
        try:
            response = requests.get(url)
            data = response.json()
            total = data.get("hits", {}).get("total", 0)
            if isinstance(total, dict):
                total = total.get("value", 0)

            # The CFPB API has changed slightly, we'll just use the total complaints for the proposal as a starting point.
            # We have the totals, so we'll just return those and print to file.

            results[company] = {
                "total_mortgage_complaints": total
            }
        except Exception as e:
            results[company] = {"error": str(e)}

    return results

if __name__ == "__main__":
    data = search_complaints()
    print(json.dumps(data, indent=2))
    with open('data/cfpb_company_complaints.json', 'w') as f:
        json.dump(data, f, indent=2)
