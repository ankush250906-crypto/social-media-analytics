@app.get("/debug-sentry")
async def trigger_sentry_error():
    division_by_zero = 1 / 0
    return {"result": division_by_zero}