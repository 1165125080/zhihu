# -*- coding: utf-8 -*-
import json

import scrapy
from zhihu.items import UserItem


class ZhihuUserSpider(scrapy.Spider):
    name = 'zhihu_user'
    allowed_domains = ['www.zhihu.com']
    # 用户信息配置
    start_users = ['excited-vczh', 'chenbailing', 'ma-qian-zu', 'kaifulee', 'amuro1230']
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,\
        following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,\
        following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,\
        favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,\
        account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,\
        is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,\
        thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,\
        industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    # 粉丝配置
    # 粉丝与关注，因为数据结构相同，因此只需改动此处
    follows = ['followers', 'followees']
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/{follow}?include={include}&offset=0&limit=20'
    follow_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,\
        is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        for user in self.start_users:
            yield scrapy.Request(self.user_url.format(user=user, include=self.user_query), callback=self.parse_user)
            for follow in self.follows:
                yield scrapy.Request(self.follow_url.format(user=user, follow=follow, include=self.follow_query),
                                     callback=self.parse_follow)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

    def parse_follow(self, response):
        result = json.loads(response.text)

        if 'data' in result.keys():
            for user_info in result.get('data'):
                user = user_info.get('url_token')
                yield scrapy.Request(self.user_url.format(user=user, include=self.user_query), callback=self.parse_user)

        if 'paging' in result.keys() and not result.get('paging').get('is_end'):
            next_url = result.get('paging').get('next')
            yield scrapy.Request(next_url, callback=self.parse_follow)
