# import traceback
# from functools import wraps

# from .adapters.db.repository import Repository 

# def error_handler(action: str):
#     def func_wrapper(f):
#         @wraps(f)
#         async def wrapper(*args, **kwargs):
#             try:
#                 return await f(*args, **kwargs)
#             except Exception as e:
#                 await Repository.save_error(action, type(e).__name__, traceback.format_exc())

#         return wrapper
#     return func_wrapper