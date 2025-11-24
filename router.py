from fastapi import APIRouter
from api import *



router = APIRouter(
    tags=['blog'],
    prefix='/blog/api'
)



router.add_api_route('/user/create', create_user_api, methods=['POST'], response_model=UserResponse)
router.add_api_route('/post/create/{user_id}', create_post_api, methods=['POST'], response_model=PostResponse)
router.add_api_route('/user/email/{user_email}', get_user_by_email_api, methods=['GET'], response_model=UserResponse)
router.add_api_route('/user/id/{user_id}', get_user_by_id_api, methods=['GET'], response_model=UserResponse)
router.add_api_route('/post/{post_id}', get_post_api, methods=['GET'], response_model=PostResponse)
router.add_api_route('/posts/all', get_posts_api, methods=['GET'], response_model=list[PostResponse])
router.add_api_route('/post/update/{post_id}', update_post_api, methods=['PATCH'], response_model=PostResponse)
router.add_api_route('/post/delete/{post_id}', delete_post_api, methods=['DELETE'])
router.add_api_route('/user/posts/{user_id}', get_user_post_api, methods=['GET'], response_model=list[PostResponse])