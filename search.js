(function(){
var glossaryData = [
  {term:"ALN (Assistance Listing Number)", definition:"A five-digit number identifying a specific Federal funding program on SAM.gov. The HUD Housing Policy Research Grant ALN is 14.536."},
  {term:"Allocable Costs", definition:"Costs that can be fairly assigned to a federal award based on the benefit the award receives. Must be tracked and documented."},
  {term:"Allowable Costs", definition:"Costs permitted to be charged to a Federal award — must be necessary, reasonable, consistent, and adequately documented per 2 CFR Part 200."},
  {term:"AOR (Authorized Organization Representative)", definition:"Individual authorized to legally bind the applicant and submit applications through Grants.gov."},
  {term:"Award", definition:"Financial assistance provided by the Federal Government to carry out a public purpose — includes grants and cooperative agreements."},
  {term:"Budget Period", definition:"The specific time span during which approved project costs may be incurred and charged to the award."},
  {term:"Closeout", definition:"The process by which HUD formally completes an award after all work is finished and reporting requirements are met (2 CFR § 200.344)."},
  {term:"Code of Conduct", definition:"A written policy preventing, identifying, and addressing conflicts of interest when spending Federal award funds (2 CFR § 200.318(c))."},
  {term:"Cooperative Agreement", definition:"A Federal assistance award where HUD expects substantial involvement in carrying out the funded activity — distinct from a grant."},
  {term:"Cost Sharing / Matching", definition:"The portion of total project costs not paid with Federal funds. Not required for NOFO PDR-2600-DC-029M."},
  {term:"De minimis Indirect Cost Rate", definition:"A 15% indirect cost rate on Modified Total Direct Costs (MTDC), available to entities without a negotiated rate (2 CFR § 200.414(f))."},
  {term:"Direct Costs", definition:"Costs clearly and directly linked to a specific award activity — salaries, data purchases, computing, travel, subrecipient costs."},
  {term:"Disallowed Costs", definition:"Costs determined by HUD to be unallowable under regulations, statutes, or award terms. Must be repaid if identified."},
  {term:"E-Biz POC", definition:"E-Business Point of Contact — the individual managing Federal system registrations and authorizing AORs in SAM.gov."},
  {term:"Effective Date", definition:"The date an award officially begins. Costs may only be charged on or after this date."},
  {term:"Eligibility Requirements", definition:"Mandatory conditions an applicant must meet to be considered for funding. Failure in any criterion means no review."},
  {term:"F&A Costs (Indirect Costs)", definition:"Facilities and Administrative costs that support multiple activities. Also called indirect costs."},
  {term:"FAIN (Federal Award Identification Number)", definition:"A unique number assigned by HUD to identify a specific federal award for tracking, reporting, and audit purposes."},
  {term:"FFR (Federal Financial Report)", definition:"SF-425 form used to report financial information for a federal award — submitted quarterly."},
  {term:"GTR (Government Technical Representative)", definition:"The HUD official responsible for technical oversight — approves work plans, reviews deliverables, provides guidance."},
  {term:"Grants Officer", definition:"The HUD official authorized to execute, amend, and administer federal awards — handles financial and administrative authority."},
  {term:"Intangible Property", definition:"Non-physical property of value — copyrights, patents, data, software, licenses created under a federal award."},
  {term:"Intellectual Property", definition:"Creative works and innovations including research methods, data, software, and publications. HUD retains a Government Purpose License."},
  {term:"Key Personnel", definition:"Individuals named in the application critical to carrying out the project. Changes require HUD prior approval."},
  {term:"LOCCS (Line of Credit Control System)", definition:"HUD's system for requesting and receiving grant funds on a reimbursement basis."},
  {term:"MTDC (Modified Total Direct Costs)", definition:"Cost base for calculating indirect costs — includes salaries, fringe, materials, services, travel, and first $25K of each subaward."},
  {term:"MWP (Management and Work Plan)", definition:"Detailed plan showing tasks, timelines, milestones, staffing, and deliverables. Subject to HUD approval."},
  {term:"NOFO (Notice of Funding Opportunity)", definition:"Formal announcement describing available federal funding, eligibility, application instructions, and deadlines."},
  {term:"NOI (Notice of Intent)", definition:"PD&R's mechanism for receiving unsolicited research proposals on a noncompetitive basis."},
  {term:"OTA (Office of Technical Assistance)", definition:"Division within HUD PD&R that manages the lifecycle of research and technical assistance awards."},
  {term:"OZ (Opportunity Zone)", definition:"Designated low-income census tracts offering tax incentives for investment through Qualified Opportunity Funds."},
  {term:"PD&R (Office of Policy Development and Research)", definition:"HUD's research office responsible for building evidence on housing and community development policy."},
  {term:"Period of Performance", definition:"The total time span of the award during which work may be performed and costs incurred."},
  {term:"Prior Approval", definition:"HUD's written authorization required before certain actions — budget revisions, scope changes, or unusual costs."},
  {term:"Recipient", definition:"The organization that receives a federal award directly from HUD and bears primary responsibility for compliance."},
  {term:"Section 3", definition:"HUD Act of 1968 requirement that employment and contracting opportunities from HUD-funded projects go to low-income persons."},
  {term:"Subrecipient", definition:"An entity that carries out part of the award's scope under a subaward from the recipient — distinct from a contractor."},
  {term:"SF-424", definition:"Standard form used as the face page for federal grant applications."},
  {term:"SF-LLL", definition:"Disclosure of Lobbying Activities form required with federal grant applications."},
  {term:"Technical Assistance", definition:"Support services to help recipients comply with grant requirements and achieve program outcomes."},
  {term:"UEI (Unique Entity Identifier)", definition:"A 12-character alphanumeric ID assigned by SAM.gov — required for all federal grant applicants."},
  {term:"Uniform Guidance (2 CFR Part 200)", definition:"The set of federal regulations governing grant administration, cost principles, and audit requirements."}
];

var style = document.createElement('style');
style.textContent = [
  '#site-search {',
  '  width: 100%;',
  '  padding: .75rem 1rem;',
  '  font-size: 1rem;',
  '  font-family: var(--font-main, "Source Sans Pro", sans-serif);',
  '  border: 2px solid var(--hud-gray-light, #dfe1e2);',
  '  border-radius: var(--radius, 6px);',
  '  outline: none;',
  '  transition: border-color .2s;',
  '  box-sizing: border-box;',
  '}',
  '#site-search:focus {',
  '  border-color: var(--cf-teal, #0d6b6b);',
  '  box-shadow: 0 0 0 3px var(--cf-teal-pale, #e0f5f5);',
  '}',
  '#search-results {',
  '  margin-top: .5rem;',
  '  max-height: 500px;',
  '  overflow-y: auto;',
  '  border: 1px solid var(--hud-gray-light, #dfe1e2);',
  '  border-radius: var(--radius, 6px);',
  '  background: var(--hud-white, #fff);',
  '  box-shadow: 0 4px 12px rgba(0,0,0,.1);',
  '  display: none;',
  '}',
  '#search-results.active {',
  '  display: block;',
  '}',
  '.search-result-item {',
  '  padding: .75rem 1rem;',
  '  border-bottom: 1px solid var(--hud-gray-light, #dfe1e2);',
  '  cursor: pointer;',
  '  transition: background .15s;',
  '}',
  '.search-result-item:last-child {',
  '  border-bottom: none;',
  '}',
  '.search-result-item:hover,',
  '.search-result-item.highlighted {',
  '  background: var(--cf-teal-pale, #e0f5f5);',
  '}',
  '.search-result-term {',
  '  font-weight: 700;',
  '  color: var(--hud-blue, #003a70);',
  '  font-size: .95rem;',
  '}',
  '.search-result-term mark {',
  '  background: var(--hud-gold, #f0ab00);',
  '  color: var(--hud-blue, #003a70);',
  '  padding: .1rem .2rem;',
  '  border-radius: 2px;',
  '}',
  '.search-result-def {',
  '  font-size: .85rem;',
  '  color: var(--hud-gray, #565c65);',
  '  margin-top: .2rem;',
  '  line-height: 1.4;',
  '}',
  '.search-result-def mark {',
  '  background: var(--cf-teal-pale, #e0f5f5);',
  '  color: var(--cf-teal, #0d6b6b);',
  '  padding: .1rem .2rem;',
  '  border-radius: 2px;',
  '}',
  '#search-results .search-empty {',
  '  padding: 1.5rem;',
  '  text-align: center;',
  '  color: var(--hud-gray, #565c65);',
  '  font-style: italic;',
  '}'
].join('\n');
document.head.appendChild(style);

function initSearch() {
  var input = document.getElementById('site-search');
  var results = document.getElementById('search-results');
  if (!input || !results) return;

  input.addEventListener('input', function(){
    var q = input.value.trim().toLowerCase();
    if (!q) {
      results.classList.remove('active');
      results.innerHTML = '';
      return;
    }

    var matches = glossaryData.filter(function(item){
      return item.term.toLowerCase().indexOf(q) !== -1 ||
             item.definition.toLowerCase().indexOf(q) !== -1;
    });

    if (!matches.length) {
      results.innerHTML = '<div class="search-empty">No matching terms found</div>';
      results.classList.add('active');
      return;
    }

    var html = '';
    for (var i = 0; i < matches.length; i++) {
      var item = matches[i];
      var termHighlighted = highlightText(item.term, q);
      var defHighlighted = highlightText(item.definition, q);
      html += '<div class="search-result-item">' +
        '<div class="search-result-term">' + termHighlighted + '</div>' +
        '<div class="search-result-def">' + defHighlighted + '</div>' +
        '</div>';
    }
    results.innerHTML = html;
    results.classList.add('active');
  });

  document.addEventListener('click', function(e){
    if (input && results && !input.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove('active');
    }
  });
}

function highlightText(text, query) {
  if (!query) return escapeHtml(text);
  var idx = text.toLowerCase().indexOf(query);
  if (idx === -1) return escapeHtml(text);
  var before = escapeHtml(text.slice(0, idx));
  var match = escapeHtml(text.slice(idx, idx + query.length));
  var after = highlightText(text.slice(idx + query.length), query);
  return before + '<mark>' + match + '</mark>' + after;
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

initSearch();
})();
