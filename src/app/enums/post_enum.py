from enum import Enum
class PostSortEnum(str, Enum):
    LATEST ="LATEST" #최신순
    OLDEST = "OLDEST" # 오래된순
    VIEWS = "VIEWS" # 조회순
    
class PostSearchEnum(str, Enum):
    TITLE = "TITLE" #젬ㄱ
    CONTENT = "CONTENT"
    WRITER = "WRITER"
    TITLE_CONTENT = "TITLE_CONTENT"

    