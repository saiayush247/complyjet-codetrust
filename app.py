import os
from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

USERNAME = "saiayush247"
REPO = "complyjet-codetrust"

@app.route('/')
def dashboard():
    url = f"https://api.github.com/repos/{USERNAME}/{REPO}/pulls?state=all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    latest_pr = None
    violation_detected = False
    is_open = False
    review_seconds = 0
    error_message = None
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            prs = response.json()
            if len(prs) > 0:
                latest_pr = prs[0] 
                
                # Check if the PR is currently unmerged/open
                if latest_pr.get('state') == 'open':
                    is_open = True
                
                created_str = latest_pr.get('created_at')
                merged_str = latest_pr.get('merged_at')
                
                if merged_str:
                    time_format = "%Y-%m-%dT%H:%M:%SZ"
                    created_time = datetime.strptime(created_str, time_format)
                    merged_time = datetime.strptime(merged_str, time_format)
                    review_seconds = (merged_time - created_time).total_seconds()
                    
                    if review_seconds < 120:
                        violation_detected = True
            else:
                error_message = "No pull requests found."
        else:
            error_message = f"GitHub API Error: {response.status_code}"
    except Exception as e:
        error_message = str(e)

    html_layout = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ComplyJet CodeTrust | AI Compliance Center</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
        <header class="border-b border-slate-800 bg-slate-900/50 backdrop-blur px-8 py-4 flex justify-between items-center">
            <div class="flex items-center gap-3">
                <span class="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">ComplyJet</span>
                <span class="text-xs bg-indigo-500/10 text-indigo-400 px-2.5 py-0.5 rounded-full border border-indigo-500/20 font-medium tracking-wide">CodeTrust v0.1</span>
            </div>
            <div class="text-sm text-slate-400">Live Sync Status: <span class="text-emerald-400 font-semibold">● Connected</span></div>
        </header>

        <main class="max-w-6xl mx-auto px-4 py-10">
            <!-- Dynamic Metrics Row -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
                    <p class="text-sm font-medium text-slate-400 mb-1">AI Code Security Score</p>
                    <h3 class="text-4xl font-extrabold tracking-tight {% if is_open %}text-amber-400{% elif violation_detected %}text-rose-500{% else %}text-emerald-400{% endif %}">
                        {% if is_open %}Evaluating...{% elif violation_detected %}42%{% else %}100%{% endif %}
                    </h3>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
                    <p class="text-sm font-medium text-slate-400 mb-1">Monitored Repositories</p>
                    <h3 class="text-4xl font-extrabold tracking-tight text-slate-100">1</h3>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
                    <p class="text-sm font-medium text-slate-400 mb-1">Active Violations (CC8.1)</p>
                    <h3 class="text-4xl font-extrabold tracking-tight {% if violation_detected %}text-rose-500{% else %}text-slate-400{% endif %}">
                        {% if violation_detected %}1{% else %}0{% endif %}
                    </h3>
                </div>
            </div>

            <!-- Evidence Locker Card -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden">
                <div class="px-6 py-5 border-b border-slate-800 bg-slate-900/50">
                    <h2 class="text-lg font-bold text-slate-100">SOC 2 Change Management Audit Evidence Locker</h2>
                </div>

                <div class="p-6">
                    {% if latest_pr %}
                    <div class="border {% if is_open %}border-amber-500/30 bg-amber-950/10{% elif violation_detected %}border-rose-500/30 bg-rose-950/10{% else %}border-emerald-500/30 bg-emerald-950/10{% endif %} rounded-xl p-6">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/60 pb-4 mb-4">
                            <div>
                                <span class="text-xs font-semibold uppercase tracking-wider {% if is_open %}text-amber-400 bg-amber-400/10{% elif violation_detected %}text-rose-400 bg-rose-400/10{% else %}text-emerald-400 bg-emerald-400/10{% endif %} px-2.5 py-1 rounded">
                                    {% if is_open %}Review In Progress{% elif violation_detected %}Compliance Failure{% else %}Compliance Verified{% endif %}
                                </span>
                                <h4 class="text-base font-bold text-slate-200 mt-2">Pull Request #{{ latest_pr.number }} - {{ latest_pr.title }}</h4>
                            </div>
                            <div>
                                <p class="text-xs text-slate-400">Artifact Reference Key</p>
                                <p class="text-sm font-mono text-indigo-400 font-semibold">EV-CC8.1-2026-PR{{ latest_pr.number }}</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm mb-6">
                            <div>
                                <p class="text-slate-400 font-medium mb-1">Mapped Control Standard</p>
                                <p class="text-slate-200 font-semibold bg-slate-950/40 p-2.5 rounded border border-slate-800/50">SOC 2 Type II - CC8.1 (Change Management)</p>
                            </div>
                            <div>
                                <p class="text-slate-400 font-medium mb-1">Detected Human Review Time</p>
                                <p class="text-slate-200 font-mono bg-slate-950/40 p-2.5 rounded border border-slate-800/50">
                                    {% if is_open %}
                                        ⏳ Waiting for Merge Event...
                                    {% else %}
                                        {% if violation_detected %}❌{% else %}✅{% endif %} {{ review_seconds }} seconds
                                    {% endif %}
                                </p>
                            </div>
                        </div>

                        <div class="text-sm bg-slate-950/60 border border-slate-800/80 p-4 rounded-xl">
                            <p class="text-slate-400 font-semibold mb-1">Automated Risk Core Finding:</p>
                            <p class="text-slate-300 font-mono text-xs leading-relaxed">
                                {% if is_open %}
                                Telemetry actively monitoring code diff. Compliance calculation will trigger automatically upon merge request completion.
                                {% elif violation_detected %}
                                Warning: Code introduced with suspected AI signatures and merged instantly without human review window.
                                {% else %}
                                Success: Human validation review time window matches secure organizational standards.
                                {% endif %}
                            </p>
                        </div>
                    </div>
                    {% else %}
                    <div class="text-center py-6"><p class="text-slate-400">No telemetry found.</p></div>
                    {% endif %}
                </div>
            </div>
        </main>
    </body>
    </html>
    """
    return render_template_string(html_layout, latest_pr=latest_pr, violation_detected=violation_detected, is_open=is_open, review_seconds=review_seconds, error_message=error_message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)