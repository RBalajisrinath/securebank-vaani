# Vaani Custom Tools (Persona -> Tools & Integrations -> Add via cURL)
# Base = your Render URL, e.g. https://securebank-backend-xxx.onrender.com
# Paste each cURL in Vaani dashboard. Keep timeout <3s (backend already fast).
# Give each tool a clear WHEN description so Eva triggers it correctly.

## 1. createApplication — WHEN user says "start application / apply"
curl -X POST "https://YOUR_RENDER_URL_HERE/tools/create-application" -H "Content-Type: application/json" -d '{"product":"{{product_type}}","customer_name":"{{customer_name}}"}'

## 2. getContact — WHEN user asks contact / branch / helpline / off-topic
curl -X POST "https://YOUR_RENDER_URL_HERE/tools/get-contact" -H "Content-Type: application/json" -d '{"reason":"general"}'

## 3. checkManager — WHEN user asks "speak to manager"
curl -X POST "https://YOUR_RENDER_URL_HERE/tools/manager-check" -H "Content-Type: application/json" -d '{}'

## 4. scheduleFeedback — WHEN manager busy + user gives phone number
curl -X POST "https://YOUR_RENDER_URL_HERE/tools/schedule-feedback" -H "Content-Type: application/json" -d '{"customer_name":"{{customer_name}}","phone_number":"{{customer_phone}}","reason":"{{session_purpose}}"}'

## 5. analyzeInvoice — WHEN user gives vendor + total + currency on voice
curl -X POST "https://YOUR_RENDER_URL_HERE/tools/analyze-invoice" -H "Content-Type: application/json" -d '{"description":"Invoice from vendor","total":250.0,"currency":"USD","vendor":"Test Corp"}'

## 6. processPayment — WHEN user says YES to pay invoice
curl -X POST "https://YOUR_RENDER_URL_HERE/tools/process-payment" -H "Content-Type: application/json" -d '{"application_ref":"{{application_ref}}","invoice_total":250.0,"vendor":"Test Corp"}'

## 7. getApplicationStatus — WHEN user asks "check status APP-..."
# Vaani cURL tools are POST-biased; if GET-with-path fails, add this wrapper to backend or call via voice:
# GET https://YOUR_RENDER_URL_HERE/tools/application-status/APP-12345678
curl "https://YOUR_RENDER_URL_HERE/tools/application-status/APP-12345678"

# --- Trigger calls (after telephony + API key) ---
# Outbound phone call:
# curl -X POST https://api.vaanivoice.ai/api/trigger-call/ -H "X-API-Key: vaani_KEY" -H "Content-Type: application/json" -d '{"agent_id":"AGENT_UUID","medium":"telephony","contact_number":"+91XXXXXXXXXX","name":"Test User","metadata":{"customer_name":"Test User"},"dnd_check_skipped":true}'
# Browser voice (WebRTC):
# curl -X POST https://api.vaanivoice.ai/api/trigger-call/ -H "X-API-Key: vaani_KEY" -H "Content-Type: application/json" -d '{"agent_id":"AGENT_UUID","medium":"webrtc"}'
