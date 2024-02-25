from pydantic import BaseModel
from pydantic.json_schema import SkipJsonSchema


class PreBase(BaseModel):
    class Config:
        from_attributes = True


class Adress(PreBase):
    email_address: str


class GroupName(PreBase):
    name: str | SkipJsonSchema[None] = None


class Group(PreBase):
    group_id: int | SkipJsonSchema[None] = None


class Profile(PreBase):
    zodiac: str


class BaseUser(PreBase):
    id: int
    name: str
    fullname: str

    addresses: Adress | SkipJsonSchema[None] = None
    group: list[Group] | SkipJsonSchema[None] = None
    profile: Profile | SkipJsonSchema[None] = None


class BaseUserPLUS(PreBase):
    id: int
    name: str
    fullname: str

    addresses: Adress | SkipJsonSchema[None] = None
    group: list[GroupName] | SkipJsonSchema[None] = None
    profile: Profile | SkipJsonSchema[None] = None

# class User(PreBase):
#     id: int
#     media_url: str | SkipJsonSchema[None] = None
#     name: str
#     description: str | SkipJsonSchema[None] = None
#     hero: str | SkipJsonSchema[None] = None
#     hero_city: str | SkipJsonSchema[None] = None
#     hero_link: str | SkipJsonSchema[None] = None
#     author: str | SkipJsonSchema[None] = None
#     phone_number: str | SkipJsonSchema[None] = None
#     author_commentary: str | SkipJsonSchema[None] = None
#     publish_date: datetime | SkipJsonSchema[None] = None
#     check_status: bool
#     likes: int
#     liked_by_user: CheckLike
#     priority: int
#     media_type: MediaTypeForMediaSchema
#     user: UserSchema | SkipJsonSchema[None] = None

#     class Config:
#         from_attributes = True
