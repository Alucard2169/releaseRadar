# from typing import Union
# from fastapi import FastAPI
# import re
# import httpx
# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# # parse github url
# def parse_github_url(url: str) -> Union[dict, None]:
#     pattern = r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)(?:/tree/(?P<branch>[^/]+)(?:/(?P<path>.*))?)?"
#     match = re.match(pattern, url)
#     if match:
#         return match.groupdict()
#     return None

# # fetch github repo content
# async def fetch_github_repo_content(owner: str, repo: str, branch) -> Dict:
#     async with httpx.AsyncClient() as client:
#         base_url = "https://api.github.com"
#         url = f"{base_url}/repos/{owner}/{repo}/contents?ref={branch}"
#         response = await client.get(url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": f"Failed to fetch content: {response.status_code}"}
        

    
# @app.get("/fetch")
# def fetch(url: str):
#     parsed = parse_github_url(url)
#     if not parsed:
#         return {"error": "Invalid GitHub URL"}
#     owner = parsed["owner"]
#     repo = parsed["repo"]
#     branch = parsed.get("branch", "main")
#     path = parsed.get("path", "")
#     content = fetch_github_repo_content(owner, repo,branch)
#     return {"content": content}




from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test/")
def read_test():
    return {"Test": "Test"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}