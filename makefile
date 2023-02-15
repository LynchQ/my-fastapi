dev_run:
	DEBUG=True uvicorn app.main:app --host '0.0.0.0' --port 9001 --http httptools --loop uvloop --log-level debug --no-server-header --reload --proxy-headers --forwarded-allow-ips='*'

