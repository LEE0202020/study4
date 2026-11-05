from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgresql import get_postgresql_db
from fastapi import Depends
from sqlalchemy import insert, select, update, delete, func, exists, desc, asc, or_
from sqlalchemy.orm import joinedload

from app.models.post_model import Post
from app.schemas.member_model import
from app.schemas.post_schema import PostCreateDTO
from app.enums.post_enum import PostSortEnum, PostSearchEnum

class PostRepository:

    # 생성자 주입
    def __init__(self, db: AsyncSession):
        self.db = db

    # 게시글 작성
    # save, create
    async def create_post(self, member_id: int, post: PostCreateDTO) -> int:

        query = (
            insert(Post)
            .values(
                **post.model_dump(),
                member_id=member_id
            )
            .returning(
                Post.id
            )
        )

        result = await self.db.execute(query)
        await self.db.commit()
        new_post_id = result.scalar_one()
        return new_post_id

    # 게시글 1개 조회(시작)
    async def find_post_by_id(self, post_id: int):
        query = (
            select(Post)
                .options(joinedload(Post.member))
                .where(Post.id == post_id)
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    # 게시글 전체 조회(페이지네이션 + 정렬)
    # 최신순, 오래된순, 조회순
    # "latest", "oldest", "views"
    async def find_post_by_paging(
        self,
        offset: int,
        limit: int,
        sort_by: PostSortEnum = PostSortEnum.LATEST.value
    ):
        query = (
            select(Post).options(joinedload(Post.member))
        )

        if sort_by == PostSortEnum.OLDEST:
            query = query.order_by(asc(Post.id))
        elif sort_by == PostSortEnum.VIEWS:
            query = query.order_by(desc(Post.post_read_count), desc(Post.id))
        elif sort_by == PostSortEnum.LATEST:
            query = query.order_by(desc(Post.id))

        # 정렬된 상태에서 offset, limit
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    # 게시글 전체 개수 조회
    async def count_posts(self) -> int:
        query = (
            select(func.count())
                .select_from(Post)
        )

        result = await self.db.execute(query)
        return result.scalar_one()
    


     # 게시글 검색(제목, 내용, 작성자, 제목+내용)
    def search_posts(
        self,
        offset: int,
        limit: int,
        sort_by: PostSortEnum = PostSortEnum.LATEST.value,
        search_keyword:PostSearchEnum = PostSearchEnum.TITLE.value, # 구분점 
        keyword: str | None = None # 사용자 검색어 "ABC"
    ):

        # 검색  + 페이지네이션 베이스 쿼리
        query = (
            select(Post).options(joinedload(Post.member))
        )

        # 검색  + 페이지네이션 게시글 분리 
        count_query = (
            select(Post).options(joinedload(Post.member))
        )

        if keyword and search_keyword:
            keyword = f"%{search_keyword}%"

            if search_keyword == PostSearchEnum.TITLE:
                condition = Post.post_title.like(keyword)
            elif search_keyword == PostSearchEnum.CONTENT:
                condition = Post.post_content.like(keyword)
            elif search_keyword == PostSearchEnum.WRITER:
                pass 
            elif search_keyword == PostSearchEnum.TITLE_CONTENT:
                condition = or_(
                    Post.post_title.like(keyword),
                    Post.post_content.like(keyword)
                )

            query = query.where(condition)


        if sort_by == PostSortEnum.OLDEST:
            query = query.order_by(asc(Post.id))
        elif sort_by == PostSortEnum.VIEWS:
            query = query.order_by(desc(Post.post_read_count), desc(Post.id))
        elif sort_by == PostSortEnum.LATEST:
            query = query.order_by(desc(Post.id))

        # 정렬된 상태에서 offset, limit
        query = query.offset(offset).limit(limit)







    # 게시글 수정
    # 게시글 삭제





# 주입 팩토리 메서드
def get_post_repository(db: AsyncSession = Depends(get_postgresql_db)):
    return PostRepository(db)