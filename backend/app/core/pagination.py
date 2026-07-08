from sqlalchemy.orm import Query

def paginate(query: Query, page: int, size: int) -> dict:
    total = query.count()
    data = query.offset((page - 1) * size).limit(size).all()

    return {
        "data": data, 
        "total": total, 
        "page": page, 
        "size": size
    }
