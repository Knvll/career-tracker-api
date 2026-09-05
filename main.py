from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/two-sum")
async def two_sum():
    return {"result": two_sum()}


def two_sum():
    nums = [3, 2, 4]
    target = 6

    seen = {}
    for i, num in enumerate(nums):
        num = target - num
        if num in seen:
            return [seen[num], i]